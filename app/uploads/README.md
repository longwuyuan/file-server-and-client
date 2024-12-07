# fileserver app & client

## Python flask app

- healtchcheck API http://$host/healtchcheck (HTTP method GET)
- Upload API http://$host/upload (HTTP method POST) (HTTP header "Content-Type: multipart/form-data")
- Delete API http://$host/delete/\<filename\> (HTTP method DELETE)
- List API at http://$host/list for HTTP method GET

- containerized app
- gunicorn used as uWSGI server
- nginx as reverseproxy
- supervisor to run 2 processes
