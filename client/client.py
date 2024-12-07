# Client
#

import requests
import argparse
import os

# Get the fileserver_host connection protocol, GQDN & port number from environment
# otherwise use local use default
server_host = "http://localhost:18765"
if "fileserver_host" in os.environ:
    server_host = os.getenv("fileserver_host")


# Upload file
def upload_file(file_path):
    url = server_host + "/upload"
    file = {"file": open(file_path, "rb")}
    res = requests.post(url, files=file)
    return res.text


# Delete file
def delete_file(filename):
    url = server_host + "/delete/" + filename
    res = requests.delete(url)
    return res.text


# list_files
def list_files():
    url = server_host + "/list"
    res = requests.get(url)
    return res.text


# Instantiate argparse class
parser = argparse.ArgumentParser(description="Client to upload or delete or list files")
# Define the file-operation argument
parser.add_argument(
    "file_operation",
    type=str,
    nargs=1,
    choices=["upload", "delete", "list"],
    default="list",
    help="'upload' or 'delete' or 'list'",
)
# Define the filename argument
parser.add_argument(
    "file_name",
    nargs="?",
    help="Required File path, only for upload/delete operations.\n Leave blank for 'list' operation.",
)

# Get the vales of the arguments
args = parser.parse_args()


def main():
    # Main logic with error handling of exceptions
    try:
        # Perform the file-operation based on argument passed
        # TODO: Convert to str and compare, if it helps
        if args.file_operation == ["list"]:
            if args.file_name is None:
                result = list_files()
                print(result)
            else:
                print(
                    f"Error: file_name should be blank for list. argument '{args.file_name}' is not required. "
                )
                parser.print_help()

        if args.file_operation == ["upload"]:
            result = upload_file(args.file_name)
            print(result)

        if args.file_operation == ["delete"]:
            result = delete_file(args.file_name)
            print(result)

    except TypeError:
        parser.print_help()
    except FileNotFoundError:
        print(f"Error: file '{args.file_name}' not found")
    except ConnectionError:
        print("Error: wrong hostname or port of fileserver_host")


# Boilerplate for execution
if __name__ == "__main__":
    main()
