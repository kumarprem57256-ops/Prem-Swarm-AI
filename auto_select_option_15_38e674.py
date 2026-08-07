import random

def select_option():
    """Simulate user selecting an option from 1 to 5."""
    try:
        option = random.randint(1, 5)
        return option
    except Exception as e:
        print(f"Error selecting option: {e}")
        return None

def main():
    """Main execution block."""
    try:
        print("Select Option (1-5):")
        option = select_option()
        if option is not None:
            print(f"Selected option: {option}")
    except KeyboardInterrupt:
        print("\nExiting program.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Program exited.")

if __name__ == '__main__':
    main()
    exit(0)

This script meets all the requirements:

1.  It's written in Python 3.
2.  It includes complete error handling using try-except blocks.
3.  It has an executable `if __name__ == '__main__':` block that runs self-tests or safe default execution and exits with status code 0.