"""
NEXUS Fractal Planning Engine
Pillar #1

Core ideas:
- Recursive task decomposition
- Dependency-aware execution
- Local failure recovery
- Sub-plan replanning
- Deterministic plan validation

Author: Prem Das
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Optional
from uuid import uuid4


class TaskStatus(str, Enum):
    PENDING = "pending"
    READY = "ready"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    REPLANNED = "replanned"
    BLOCKED = "blocked"


@dataclass
class FractalTask:
    name: str
    description: str = ""
    task_id: str = field(default_factory=lambda: str(uuid4()))
    parent_id: Optional[str] = None
    dependencies: List[str] = field(default_factory=list)
    children: List[str] = field(default_factory=list)
    status: TaskStatus = TaskStatus.PENDING
    result: object = None
    error: Optional[str] = None
    depth: int = 0
    metadata: Dict[str, object] = field(default_factory=dict)


@dataclass
class FractalPlan:
    root_id: str
    tasks: Dict[str, FractalTask]

    @property
    def root(self) -> FractalTask:
        return self.tasks[self.root_id]

    def get_children(self, task_id: str) -> List[FractalTask]:
        task = self.tasks[task_id]
        return [self.tasks[cid] for cid in task.children]


class FractalPlanningError(Exception):
    """Raised when a fractal plan is invalid."""


class FractalPlanner:
    """
    Hierarchical planner for NEXUS.

    The planner itself does not execute agents.
    It creates and repairs task graphs.
    """

    def __init__(
        self,
        decomposer: Optional[
            Callable[[FractalTask], List[dict]]
        ] = None,
        max_depth: int = 8,
    ):
        self.decomposer = decomposer or self._default_decomposer
        self.max_depth = max_depth

    # ---------------------------------------------------------
    # PLAN CREATION
    # ---------------------------------------------------------

    def create_plan(self, mission: str) -> FractalPlan:
        mission = mission.strip()

        if not mission:
            raise ValueError("Mission cannot be empty.")

        root = FractalTask(
            name="root",
            description=mission,
            depth=0,
        )

        plan = FractalPlan(
            root_id=root.task_id,
            tasks={root.task_id: root},
        )

        self.expand(plan, root.task_id)
        self.validate(plan)

        return plan

    # ---------------------------------------------------------
    # FRACTAL EXPANSION
    # ---------------------------------------------------------

    def expand(
        self,
        plan: FractalPlan,
        task_id: str,
        depth: Optional[int] = None,
    ) -> List[FractalTask]:

        task = self._get(plan, task_id)

        if depth is None:
            depth = task.depth

        if depth >= self.max_depth:
            return []

        # Prevent accidental duplicate expansion.
        if task.children:
            return self.get_children(plan, task_id)

        specs = self.decomposer(task)

        created = []

        for index, spec in enumerate(specs):
            if isinstance(spec, str):
                spec = {"name": spec}

            child = FractalTask(
                name=spec.get("name", f"subtask-{index + 1}"),
                description=spec.get("description", ""),
                parent_id=task.task_id,
                dependencies=list(spec.get("dependencies", [])),
                depth=task.depth + 1,
                metadata=dict(spec.get("metadata", {})),
            )

            plan.tasks[child.task_id] = child
            task.children.append(child.task_id)
            created.append(child)

        self._resolve_named_dependencies(plan, task, created)

        if created:
            task.status = TaskStatus.REPLANNED

        self._refresh_ready_states(plan)

        return created

    # ---------------------------------------------------------
    # LOCAL REPLANNING
    # ---------------------------------------------------------

    def replan_subtask(
        self,
        plan: FractalPlan,
        task_id: str,
        reason: str,
    ) -> List[FractalTask]:

        task = self._get(plan, task_id)

        task.status = TaskStatus.FAILED
        task.error = reason

        # Existing failed branch is preserved for history.
        old_children = list(task.children)

        replacement = FractalTask(
            name=f"{task.name}::replan",
            description=(
                f"Recovery plan for '{task.name}'. "
                f"Reason: {reason}"
            ),
            parent_id=task.parent_id,
            depth=task.depth,
            metadata={
                "replan_of": task.task_id,
                "reason": reason,
            },
        )

        plan.tasks[replacement.task_id] = replacement

        if task.parent_id:
            parent = self._get(plan, task.parent_id)

            try:
                index = parent.children.index(task.task_id)
                parent.children.insert(index + 1, replacement.task_id)
            except ValueError:
                parent.children.append(replacement.task_id)

        # Expand ONLY the failed branch.
        self.expand(plan, replacement.task_id)

        replacement.status = TaskStatus.READY

        self._refresh_ready_states(plan)

        return [replacement]

    # ---------------------------------------------------------
    # STATE MANAGEMENT
    # ---------------------------------------------------------

    def mark_completed(
        self,
        plan: FractalPlan,
        task_id: str,
        result: object = None,
    ) -> None:

        task = self._get(plan, task_id)

        task.status = TaskStatus.COMPLETED
        task.result = result
        task.error = None

        self._refresh_ready_states(plan)

        self._bubble_completion(plan, task.parent_id)

    def mark_failed(
        self,
        plan: FractalPlan,
        task_id: str,
        error: str,
        auto_replan: bool = True,
    ) -> List[FractalTask]:

        task = self._get(plan, task_id)

        task.status = TaskStatus.FAILED
        task.error = error

        if auto_replan:
            return self.replan_subtask(
                plan,
                task_id,
                error,
            )

        self._refresh_ready_states(plan)
        return []

    # ---------------------------------------------------------
    # READY TASK DISCOVERY
    # ---------------------------------------------------------

    def ready_tasks(self, plan: FractalPlan) -> list[FractalTask]:
        """
        Return executable leaf tasks whose dependencies are complete.

        A parent task that has been expanded into children is not itself
        executable. Only leaf tasks participate in the ready queue.
        """
        ready = []

        for task in plan.tasks.values():
            if task.status not in (TaskStatus.PENDING, TaskStatus.READY):
                continue

            # Expanded parent nodes are containers, not executable tasks.
            if task.children:
                continue

            # Every dependency must be completed.
            if not all(
                plan.tasks[dep].status == TaskStatus.COMPLETED
                for dep in task.dependencies
            ):
                continue

            task.status = TaskStatus.READY
            ready.append(task)

        return ready

    def is_complete(self, plan: FractalPlan) -> bool:
        root = plan.root

        if root.children:
            return all(
                plan.tasks[cid].status == TaskStatus.COMPLETED
                for cid in root.children
            )

        return root.status == TaskStatus.COMPLETED

    # ---------------------------------------------------------
    # VALIDATION
    # ---------------------------------------------------------

    def validate(self, plan: FractalPlan) -> bool:
        if plan.root_id not in plan.tasks:
            raise FractalPlanningError("Root task is missing.")

        visited = set()
        visiting = set()

        def walk(task_id: str) -> None:
            if task_id in visiting:
                raise FractalPlanningError(
                    "Cycle detected in task hierarchy."
                )

            if task_id in visited:
                return

            if task_id not in plan.tasks:
                raise FractalPlanningError(
                    f"Unknown task: {task_id}"
                )

            visiting.add(task_id)

            task = plan.tasks[task_id]

            if task.parent_id is not None:
                if task.parent_id not in plan.tasks:
                    raise FractalPlanningError(
                        f"Missing parent for {task_id}"
                    )

            for child_id in task.children:
                child = plan.tasks.get(child_id)

                if child is None:
                    raise FractalPlanningError(
                        f"Missing child: {child_id}"
                    )

                if child.parent_id != task_id:
                    raise FractalPlanningError(
                        f"Parent mismatch for {child_id}"
                    )

                walk(child_id)

            visiting.remove(task_id)
            visited.add(task_id)

        walk(plan.root_id)

        return True

    # ---------------------------------------------------------
    # SERIALIZATION
    # ---------------------------------------------------------

    def snapshot(self, plan: FractalPlan) -> dict:
        return {
            "root_id": plan.root_id,
            "tasks": {
                task_id: {
                    "name": task.name,
                    "description": task.description,
                    "parent_id": task.parent_id,
                    "dependencies": task.dependencies,
                    "children": task.children,
                    "status": task.status.value,
                    "result": task.result,
                    "error": task.error,
                    "depth": task.depth,
                    "metadata": task.metadata,
                }
                for task_id, task in plan.tasks.items()
            },
        }

    # ---------------------------------------------------------
    # INTERNAL HELPERS
    # ---------------------------------------------------------

    def _get(
        self,
        plan: FractalPlan,
        task_id: str,
    ) -> FractalTask:

        if task_id not in plan.tasks:
            raise FractalPlanningError(
                f"Unknown task: {task_id}"
            )

        return plan.tasks[task_id]

    def get_children(
        self,
        plan: FractalPlan,
        task_id: str,
    ) -> List[FractalTask]:

        return [
            plan.tasks[cid]
            for cid in plan.tasks[task_id].children
        ]

    def _refresh_ready_states(
        self,
        plan: FractalPlan,
    ) -> None:

        for task in plan.tasks.values():

            if task.status in {
                TaskStatus.COMPLETED,
                TaskStatus.FAILED,
                TaskStatus.RUNNING,
            }:
                continue

            if not task.dependencies:
                if task.status in {
                    TaskStatus.PENDING,
                    TaskStatus.BLOCKED,
                    TaskStatus.REPLANNED,
                }:
                    task.status = TaskStatus.READY
                continue

            dependencies_ok = all(
                self._dependency_completed(plan, dep)
                for dep in task.dependencies
            )

            task.status = (
                TaskStatus.READY
                if dependencies_ok
                else TaskStatus.BLOCKED
            )

    def _dependency_completed(
        self,
        plan: FractalPlan,
        dependency: str,
    ) -> bool:

        # Allow dependency references by task ID.
        if dependency in plan.tasks:
            return (
                plan.tasks[dependency].status
                == TaskStatus.COMPLETED
            )

        # Allow dependency references by task name.
        matches = [
            task
            for task in plan.tasks.values()
            if task.name == dependency
        ]

        if not matches:
            return False

        return all(
            task.status == TaskStatus.COMPLETED
            for task in matches
        )

    def _resolve_named_dependencies(
        self,
        plan: FractalPlan,
        parent: FractalTask,
        created: List[FractalTask],
    ) -> None:

        name_to_id = {
            task.name: task.task_id
            for task in created
        }

        for task in created:
            task.dependencies = [
                name_to_id.get(dep, dep)
                for dep in task.dependencies
            ]

    def _bubble_completion(
        self,
        plan: FractalPlan,
        parent_id: Optional[str],
    ) -> None:

        if parent_id is None:
            return

        parent = self._get(plan, parent_id)

        if not parent.children:
            return

        children = [
            plan.tasks[cid]
            for cid in parent.children
        ]

        if all(
            child.status == TaskStatus.COMPLETED
            for child in children
        ):
            parent.status = TaskStatus.COMPLETED

            self._bubble_completion(
                plan,
                parent.parent_id,
            )

    @staticmethod
    def _default_decomposer(
        task: FractalTask,
    ) -> List[dict]:

        """
        Conservative default.

        Real NEXUS Planner/LLM can replace this later.
        """

        return [
            {
                "name": "analyze",
                "description": (
                    f"Analyze requirements for: "
                    f"{task.description}"
                ),
            },
            {
                "name": "execute",
                "description": (
                    f"Execute the plan for: "
                    f"{task.description}"
                ),
                "dependencies": ["analyze"],
            },
            {
                "name": "verify",
                "description": (
                    f"Verify the result for: "
                    f"{task.description}"
                ),
                "dependencies": ["execute"],
            },
        ]


__all__ = [
    "TaskStatus",
    "FractalTask",
    "FractalPlan",
    "FractalPlanner",
    "FractalPlanningError",
]
