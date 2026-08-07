import json
import sys
import statistics
import time
import threading
from collections import defaultdict
from typing import Dict, List, Any

# Define a simple JSON schema validator
class SchemaValidator:
    def __init__(self, schema: Dict):
        self.schema = schema

    def validate(self, event: Dict) -> bool:
        for key, value in self.schema.items():
            if key not in event or event[key] != value:
                return False
        return True

# Define a simple event processor
class EventProcessor:
    def __init__(self, schema: Dict):
        self.schema_validator = SchemaValidator(schema)
        self.duplicate_ids = set()
        self.group_metrics = defaultdict(lambda: {'min': float('inf'), 'max': float('-inf'), 'sum': 0, 'count': 0})
        self.lock = threading.Lock()

    def process_event(self, event: Dict) -> None:
        if not self.schema_validator.validate(event):
            print(f"Invalid event: {json.dumps(event)}")
            return

        event_id = event['id']
        if event_id in self.duplicate_ids:
            print(f"Duplicate event ID: {event_id}")
            return

        self.duplicate_ids.add(event_id)

        group = event['group']
        with self.lock:
            self.group_metrics[group]['min'] = min(self.group_metrics[group]['min'], event['value'])
            self.group_metrics[group]['max'] = max(self.group_metrics[group]['max'], event['value'])
            self.group_metrics[group]['sum'] += event['value']
            self.group_metrics[group]['count'] += 1

    def get_group_metrics(self, group: str) -> Dict:
        with self.lock:
            metrics = self.group_metrics[group]
            metrics['average'] = metrics['sum'] / metrics['count']
            metrics['percentile_75'] = statistics.quantiles([x for x in self.group_metrics[group]['values'] if x is not None], n=3)[2]
            metrics['std_dev'] = statistics.stdev([x for x in self.group_metrics[group]['values'] if x is not None])
            return metrics

# Define a simple diagnostic printer
class DiagnosticPrinter:
    def print_diagnostic(self, metrics: Dict) -> None:
        print(json.dumps(metrics, indent=4))

# Define a simple benchmark
class Benchmark:
    def __init__(self):
        self.start_time = time.time()

    def elapsed_time(self) -> float:
        return time.time() - self.start_time

# Define a simple test runner
class TestRunner:
    def run_tests(self) -> None:
        # Test 1: Validate a valid event
        event = {'id': '1', 'group': 'A', 'value': 10}
        processor = EventProcessor({'id': 'str', 'group': 'str', 'value': 'int'})
        processor.process_event(event)
        assert processor.schema_validator.validate(event)

        # Test 2: Validate an invalid event
        event = {'id': '1', 'group': 'A', 'value': 'abc'}
        processor = EventProcessor({'id': 'str', 'group': 'str', 'value': 'int'})
        processor.process_event(event)
        assert not processor.schema_validator.validate(event)

        # Test 3: Process a duplicate event ID
        event = {'id': '1', 'group': 'A', 'value': 10}
        processor = EventProcessor({'id': 'str', 'group': 'str', 'value': 'int'})
        processor.process_event(event)
        processor.process_event(event)
        assert '1' in processor.duplicate_ids

        # Test 4: Get group metrics
        event = {'id': '1', 'group': 'A', 'value': 10}
        processor = EventProcessor({'id': 'str', 'group': 'str', 'value': 'int'})
        processor.process_event(event)
        metrics = processor.get_group_metrics('A')
        assert metrics['min'] == 10
        assert metrics['max'] == 10
        assert metrics['average'] == 10
        assert metrics['percentile_75'] == 10
        assert metrics['std_dev'] == 0

# Define the main function
def main() -> None:
    # Read events from stdin
    events = []
    for line in sys.stdin:
        if not sys.stdin.isatty():
            line = line.strip()
        if line:
            events.append(json.loads(line))

    # Process events
    processor = EventProcessor({'id': 'str', 'group': 'str', 'value': 'int'})
    for event in events:
        processor.process_event(event)

    # Get group metrics
    metrics = {}
    for group, group_metrics in processor.group_metrics.items():
        metrics[group] = processor.get_group_metrics(group)

    # Print diagnostic summary
    printer = DiagnosticPrinter()
    printer.print_diagnostic(metrics)

    # Run benchmark
    benchmark = Benchmark()
    print(f"Elapsed time: {benchmark.elapsed_time()} seconds")

    # Run tests
    test_runner = TestRunner()
    test_runner.run_tests()

    # Exit with code 0
    sys.exit(0)

# Run main function
if __name__ == '__main__':
    main()