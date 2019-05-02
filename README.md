# Coding-Container
  - A container based service to provide pre built containers consisting various technology stacks over a CLI and an online code editor. This would be helpful Good in projects working with teammates, independent of the system.
  - Technologies Used: Web Technology (client and server scripting), Docker, Django REST framework, CodeMirror.

> Note- This project only works on Linux environment.
## Prerequisites

1. [JAVA 9 or later]

2. [Docker](https://github.com/pranshujain22/Hadoop/blob/master/Docker/Installation.md)
Download and install Docker on local linux machine.

3. Install [Django](https://www.djangoproject.com/).
```
$ pip install Django
```

3. Install [OpenPort](https://openport.io/download).


## Procedure

Clone git repo in local file system.

There are some changes required to perform in some source code:
  - CodingContainer/user/views.py
  - LDAPSearch.java

Replace the value of **base_url** to **'http://localhost:8000/'** in the above .py file..

Now the code is ready to run!

Run the project 
