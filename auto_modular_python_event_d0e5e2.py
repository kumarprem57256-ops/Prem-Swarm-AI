import json
import sys
import time
import unittest

class EventProcessor:
    def __init__(self):
        self.events = []

    def process_event(self, event):
        try:
            event_data = json.loads(event)
            self.events.append(event_data)
        except json.JSONDecodeError:
            print(f"Invalid JSON: {event}")

    def get_events(self):
        return self.events


class EventReader:
    def __init__(self, input_stream):
        self.input_stream = input_stream

    def read_events(self):
        for line in self.input_stream:
            yield line.strip()


class EventProcessorTest(unittest.TestCase):
    def test_process_event(self):
        processor = EventProcessor()
        processor.process_event('{"key": "value"}')
        self.assertEqual(len(processor.get_events()), 1)

    def test_invalid_json(self):
        processor = EventProcessor()
        processor.process_event('Invalid JSON')
        self.assertEqual(len(processor.get_events()), 0)


class EventReaderTest(unittest.TestCase):
    def test_read_events(self):
        input_stream = EventReader(sys.stdin)
        if not sys.stdin.isatty():
            input_stream.input_stream = iter(['{"key": "value"}', '{"key2": "value2"}'])
        events = list(input_stream.read_events())
        self.assertEqual(len(events), 2)


def process_events(input_stream):
    processor = EventProcessor()
    reader = EventReader(input_stream)
    for event in reader.read_events():
        processor.process_event(event)
    return processor.get_events()


def main():
    try:
        events = process_events(sys.stdin)
        print(json.dumps(events, indent=4))
        unittest.main(argv=[sys.argv[0]])
        sys.exit(0)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()