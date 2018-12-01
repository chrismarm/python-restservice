# Python rest service using Flask

The purpose of this project is showing some features of Python language.

- A simple application made with `Flask` that exposes a RESTful service to get/add diving locations by GET/POST methods.
- Although MongoDB would be a better option for data store, diving locations are stored in a JSON file, just to show some basic operations involving files, like loading/dumping json data from/to files.
- Python class to model diving locations instead of processing unstructured data items.
- Some Python basics like dict and list processing, exceptions, method calls, imports, if statements...
- Unit tests are provided.
- The app is containerized in a Docker image built from a Python3 image and stored in DockerHub:
```sh 
$ docker build -t chrismarm/python-restservice . 
$ docker push chrismarm/python-restservice
```