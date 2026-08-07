import json
import os

class ConfigParser:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = self.load_config()

    def load_config(self):
        try:
            with open(self.config_file, 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            print(f"Config file '{self.config_file}' not found.")
            return {}
        except json.JSONDecodeError:
            print(f"Invalid JSON in config file '{self.config_file}'.")
            return {}

    def get_config(self, key, default=None):
        return self.config.get(key, default)

    def set_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def save_config(self):
        with open(self.config_file, 'w') as file:
            json.dump(self.config, file, indent=4)

    def update_config(self, key, value):
        self.config[key] = value
        self.save_config()

    def delete_config(self, key):
        if key in self.config:
            del self.config[key]
            self.save_config()

def main():
    config_file = 'config.json'
    parser = ConfigParser(config_file)

    while True:
        print("\nConfig Parser Menu:")
        print("1. Get Config Value")
        print("2. Set Config Value")
        print("3. Update Config Value")
        print("4. Delete Config Value")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == '1':
            key = input("Enter config key: ")
            print(f"Config value: {parser.get_config(key)}")
        elif choice == '2':
            key = input("Enter config key: ")
            value = input("Enter config value: ")
            parser.set_config(key, value)
        elif choice == '3':
            key = input("Enter config key: ")
            value = input("Enter new config value: ")
            parser.update_config(key, value)
        elif choice == '4':
            key = input("Enter config key: ")
            parser.delete_config(key)
        elif choice == '5':
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()