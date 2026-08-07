import requests
import json
import argparse

def get_http_headers(url):
    try:
        response = requests.head(url)
        return response.headers
    except requests.exceptions.RequestException as e:
        print(f"Error occurred: {e}")
        return None

def check_header(header, value):
    if header in value:
        return True
    else:
        return False

def main():
    parser = argparse.ArgumentParser(description='HTTP Header Checker')
    parser.add_argument('-u', '--url', help='URL to check', required=True)
    parser.add_argument('-h', '--header', help='Header to check', required=True)
    parser.add_argument('-v', '--value', help='Value to check', required=True)
    args = parser.parse_args()

    headers = get_http_headers(args.url)
    if headers:
        if check_header(args.header, headers):
            print(f"Header '{args.header}' found with value '{headers[args.header]}'")
        else:
            print(f"Header '{args.header}' not found")
    else:
        print("Failed to retrieve headers")

if __name__ == "__main__":
    main()