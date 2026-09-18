from core.planning.fractal_planner import (
    FractalPlanner,
    TaskStatus,
)


def test_plan_creation():
    planner = FractalPlanner()

    plan = planner.create_plan(
        "Build a NEXUS feature"
    )

    assert plan.root.description == "Build a NEXUS feature"
    assert len(plan.root.children) == 3
    assert planner.validate(plan)


def test_dependency_order():
    planner = FractalPlanner()

    plan = planner.create_plan("Test mission")

    ready = planner.ready_tasks(plan)

    names = {task.name for task in ready}

    assert "analyze" in names
    assert "execute" not in names
    assert "verify" not in names


def test_completion_unlocks_next_task():
    planner = FractalPlanner()

    plan = planner.create_plan("Test mission")

    analyze = next(
        task
        for task in plan.tasks.values()
        if task.name == "analyze"
    )

    planner.mark_completed(
        plan,
        analyze.task_id,
        result="analysis complete",
    )

    ready = planner.ready_tasks(plan)
    names = {task.name for task in ready}

    assert "execute" in names
    assert "verify" not in names


def test_local_replan():
    planner = FractalPlanner()

    plan = planner.create_plan("Test mission")

    execute = next(
        task
        for task in plan.tasks.values()
        if task.name == "execute"
    )

    replacements = planner.mark_failed(
        plan,
        execute.task_id,
        "execution failed",
        auto_replan=True,
    )

    assert replacements
    assert execute.status == TaskStatus.FAILED

    replacement = replacements[0]

    assert replacement.metadata["replan_of"] == execute.task_id
    assert replacement.metadata["reason"] == "execution failed"


def test_snapshot():
    planner = FractalPlanner()

    plan = planner.create_plan("Snapshot mission")

    snapshot = planner.snapshot(plan)

    assert snapshot["root_id"] == plan.root_id
    assert len(snapshot["tasks"]) == len(plan.tasks)


def test_custom_decomposer():
    def decomposer(task):
        return [
            {"name": "research"},
            {
                "name": "build",
                "dependencies": ["research"],
            },
        ]

    planner = FractalPlanner(
        decomposer=decomposer
    )

    plan = planner.create_plan("Custom mission")

    names = {
        task.name
        for task in planner.ready_tasks(plan)
    }

    assert names == {"research"}
