# Coding-Container
  - A container based service to provide pre built containers consisting various technology stacks over a CLI and an online code editor. This would be helpful Good in projects working with teammates, independent of the system.
  - Technologies Used: Web Technology (client and server scripting), Docker, Django REST framework, CodeMirror.

> Note- This project only works on Linux environment.
## Prerequisites

1. [Python](https://www.python.org/downloads/)

2. Download and install [Docker](https://github.com/pranshujain22/Hadoop/blob/master/Docker/Installation.md) on local linux machine.

3. [Django](https://www.djangoproject.com/).
```
$ pip install Django
```

3. [OpenPort](https://openport.io/download).


## Procedure

Clone git repo in local file system.

There are some changes required to perform in some source code:
  - CodingContainer/user/views.py

Replace the value of **base_url** to **'http://localhost:8000/'** in the above file..

Now the code is ready to run!

Run the project:

> Open Terminal in the repository folder
```
$ python manage.py runserver 0.0.0.0:8000
```
