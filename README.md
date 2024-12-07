# File Storage Server

## Introduction

A containerized file-store-server.

## Server

- Gunicorn is used as the uWSGI server.

- Nginx is used as a reverseproxy inside container.

- Supervisor is used to spawn both processes (Nginx & Gunicorn) in the container.

- APIs provided
  - healthcheck  
  - Upload file
  - Delete file
  - List files

- Implemented in  python.

- Python libraries used ;
  - flask
  - werkzeug
  - humanize
  - os
  - time

### Server Build

- Ensure that docker is working on host doing the build.

- Change to the root directory where the Dockerfile is located.

        % ls -l  
        total 20  
        drwxr-xr-x 6 me me 4096 Nov 10 15:17 app  
        drwxr-xr-x 3 me me 4096 Nov 10 18:53 client  
        -rw-r--r-- 1 me me 1538 Nov 10 14:53 Dockerfile  
        -rw-r--r-- 1 me me 4498 Nov 10 19:29 README.md  

- Build docker image

        docker build -t file-storage-server .

### Server Test

- Check if the build works.

- Create a container.

        docker run --rm --name localfileserver -d -p 18765:80 file-storage-server

- Check if there is a listening socket.

        % netstat -lntp 2>/dev/null | grep 18765
        tcp        0      0 0.0.0.0:18765     0.0.0.0:*     LISTEN      -

- Send requests to the app, in the container, that you just created, using curl.

- Example request for the healthcheck api.

        curl <http://localhost:18765/healthcheck>

- Example requests for the upload API.

        echo uploadtest1 > myfile1.txt
        echo uploadtest2 > myfile2.txt
        echo uploadtest3 > myfile3.txt

        curl localhost:18765/upload -X POST \
        -H "Content-Type: multipart/form-data" \
        --form file="@myfile1.txt"

        curl localhost:18765/upload -X POST \
        -H "Content-Type: multipart/form-data" \
        --form file="@myfile2.txt"

        curl localhost:18765/upload -X POST \
        -H "Content-Type: multipart/form-data" \
        --form file="@myfile3.txt"

- Example requests for the delete API.

        curl localhost:18765/delete/myfile2.txt -X DELETE

- Example request for the list API.

        curl localhost:18765/list 

### Server Deploy

- Now that the image is tested locally, deploy it to your environment as needed
- If required, then mount a volume at the path /app/uploads for persistence.

## Client

- The client is also implemented in Python.

- The client is just a python file named`"client.py"`.

- The file `client.py` is in the `client` subdirectory.

        % ls -l     
        total 20  
        drwxr-xr-x 6 me me 4096 Nov 10 15:17 app  
        drwxr-xr-x 3 me me 4096 Nov 10 18:53 client  
        -rw-r--r-- 1 me me 1538 Nov 10 14:53 Dockerfile  
        -rw-r--r-- 1 me me 4812 Nov 10 19:32 README.md  
        % cd client  
        % ls -l  
        total 12  
        -rw-r--r-- 1 me me 2501 Nov 10 18:53 client.py  
        -rw-r--r-- 1 me me   88 Nov 10 13:07 requirements.txt  

### Client Build / Install

- Python libraries used;
  - argparse
  - requests
  - os

- The `argparse` and `os` libraries are already included in python standard libs.

- Only the `requests` library needs to be installed.

- On debian12, install the `python3-requests` package.

        sudo apt install -y python3-requests

- On other operating-systems, install as per respective package-manager.

- On python virtual environments, install with pip.

        pip install requests

### Client Run

- The default connection to the fileserver is at  <https://localhost:18765> .

- Different user deployments require different host:port config.

- For eg. the `-p` switch, of the `docker run` command may decide the `host:port`.

- Also Kubernetes deployments  may decide the `host:port`.

- Each user will most likely need a custom `host:port`.

#### Client Run - Configuration

- A custom `host:port` can be configured, using a env var called __*"fileserver_host"*__.

- Example#1 of configuring custom host:port below.

        fileserver_host="http://custom-host-name:12345" python client.py list

- Example#2 of configuring custom host:port below.

        export fileserver_host="<http://custom-host-name:12345>"
        python client.py list

#### Client Run - Usage

        (venv.fileserver.client) [~/Documents/file-store-server/client] 
        % python client.py -h   
        usage: client.py [-h] {upload,delete,list} [file_name]

        Client to upload or delete or list files

        positional arguments:
          {upload,delete,list}  'upload' or 'delete' or 'list'
          file_name             Required File path, only for upload/delete operations.
                                Leave blank for 'list' operation.

        options:
          -h, --help            show this help message and exit
