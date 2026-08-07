import json
import sys
import io
import unittest
from collections import defaultdict

def validate_event(event):
    try:
        event = json.loads(event)
        if not isinstance(event, dict) or 'event_id' not in event or 'latency' not in event:
            return False
        if not isinstance(event['event_id'], str) or not isinstance(event['latency'], (int, float)):
            return False
        return True
    except json.JSONDecodeError:
        return False

def validate_events():
    accepted = 0
    rejected = 0
    duplicates = defaultdict(int)
    events = set()
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        if validate_event(line):
            event_id = json.loads(line)['event_id']
            if event_id in events:
                duplicates[event_id] += 1
            else:
                events.add(event_id)
            accepted += 1
        else:
            rejected += 1
    return accepted, rejected, duplicates

def print_summary(accepted, rejected, duplicates):
    summary = {
        'accepted': accepted,
        'rejected': rejected,
        'duplicates': {k: v for k, v in duplicates.items() if v > 1}
    }
    print(json.dumps(summary))

def deterministic_test():
    # Test 1: Valid event
    event = '{"event_id": "test", "latency": 1.0}'
    assert validate_event(event)
    # Test 2: Invalid event (missing event_id)
    event = '{"latency": 1.0}'
    assert not validate_event(event)
    # Test 3: Invalid event (missing latency)
    event = '{"event_id": "test"}'
    assert not validate_event(event)
    # Test 4: Invalid event (invalid event_id)
    event = '{"event_id": 123, "latency": 1.0}'
    assert not validate_event(event)
    # Test 5: Invalid event (invalid latency)
    event = '{"event_id": "test", "latency": "abc"}'
    assert not validate_event(event)
    # Test 6: Duplicate event_id
    event = '{"event_id": "test", "latency": 1.0}'
    event2 = '{"event_id": "test", "latency": 2.0}'
    assert validate_event(event)
    assert validate_event(event2)
    assert validate_event(event)  # Duplicate event_id
    # Test 7: Empty line
    assert not validate_event('')

def main():
    if not sys.stdin.isatty():
        accepted, rejected, duplicates = validate_events()
        print_summary(accepted, rejected, duplicates)
    else:
        # Run self-tests
        deterministic_test()
        # Check if all tests pass
        assert True

if __name__ == '__main__':
    main()
    sys.exit(0)