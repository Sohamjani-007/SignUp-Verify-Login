# User - Login - Portal
## Description

This project contains codeBase for all user signup, email - verfication and login - redirecting to main page.


# Following the instructions to Generate database diagram(ERD) with Django Extensions Automatically.
![imagefile_name.png](docs/img/imagefile_name.png)

(https://www.linkedin.com/pulse/generate-database-diagramerd-django-extensions-automatically-srujan-s/
) AND (https://www.wplogout.com/export-database-diagrams-erd-from-django/)


***
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
***

# Django and Python Version for project.
***
    Django - 5.0.6
    Python - 3.11.5
    Django Rest Framework = 3.15.1



***
## *NOTE  --> .env is with the owner. 😅* 
***

## Installing python3.11.5 using pyenv

* The simplest and easiest way to install python3.11.5 along side your existing python version is using `pyenv`.

* Follow the instructions to install `pyenv`.
    [https://github.com/pyenv/pyenv#getting-pyenv](https://github.com/pyenv/pyenv#getting-pyenv)

* Fetch latest publications of python from remote into local
```shell
pyenv update
```
or

Run the command printed on the terminal.
When run the below command.
```shell
pyenv install 3.11.5
```

* Fetch the latest updates. Sample

```shell
cd /Users/deesh/.pyenv/plugins/python-build/../.. && git pull && cd -
```

***

## How to Install Poetry for this Repo.
* Deactivate your current environment if you have any.

1) To check Python.
```shell
which python
```
2) To check the current python existing and other functionality.
```shell
ls -lrtha
```
3) If python 3.11 is not present. Do the below point.
```shell
python -m pip install poetry
```
4) Installing Poetry.
```shell
python 3.11 -m poetry
```
5) Close the shell --> Add new Interpreter --> Local --> Poetry Environment Existing --> 3.11.5

6) Close the terminal and Start again.

Baam !! Its done.

## LTS support for Django.

![img.png](docs/img/django_lts.png)

***

## LTS support for Python

![img.png](docs/img/python_lts.png)

***

# Setup Poetry install before starting the development.

## Getting started

1. Install poetry in any of the following ways.

    ```
   pip install poetry
    ```

2. Run the following command in the root of the project to install the dependecies.

    ```
   poetry install
   ```
   * will install all the dependencies including the dev deps.

3. to configure the environment the poetry created.

    ```
   poetry show -v
   ```
   * Will show the complete path and the packages installed.

4. To activate the terminal
    ```
   poetry shell
   ```

5. To Run the project manually we can run the following command.

   ```
   poetry run python manage.py runserver 8666
   ```

6. Generate `requirements.txt` file from the `pyproject.toml` file.
    * Non-Dev dependency Alone.
      ```shell
        poetry export --without-hashes --without=dev --format=requirements.txt > requirements.txt
      ```
    * All dependecies to use in local.
      ```shell
        poetry export --without-hashes --format=requirements.txt > requirements.txt
       ```

## Flow of Sign-up, Verification and from Login to About Dashboard.
### Here User Sign's Up
![img.png](docs/img/signup.png)

### Here Verifies Email and Activate the Account.
![img.png](docs/img/email_verify.png)

### Here Logs In.
![img.png](docs/img/login.png)

### Here After LogIn User is redirected to About Page.
![img.png](docs/img/about.png)


## Note on Throttling
###### The friend request sending functionality is rate-limited to 3 requests per minute.
###### If you exceed this limit, you will receive a 429 Too Many Requests response.

###  Testing in Local on Postman (CURL COMMAND GIVEN BELOW TO DIRECTLY COPY PASTE IN POSTMAN):::


### For Auth Token is generated for every users.
##### Though if you want to do it.

#### DO RUN THIS SCRIPT IN SHELL :::
```sh
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()
for user in User.objects.all():
    Token.objects.get_or_create(user=user)
```
#### OR
```sh
curl --location 'http://localhost:8666/accounts/token-auth/' \
--header 'Content-Type: application/json' \
--data '{
    "username": "TechyonAdmin",
    "password": "techyonadmin"
}'
```

### Endpoints
#### 1. Sign Up

Endpoint: `/api/signup/`

Method: `POST`

This endpoint allows new users to sign up by providing their first name, last name, email, password, and mobile number.

```sh
curl -X POST http://localhost:8666/api/signup/ \
-H "Content-Type: application/json" \
-d '{
    "first_name": "John",
    "last_name": "Doe",
    "email": "johndoe@example.com",
    "password": "password123",
    "mobile": "1234567890"
}'
```


#### 2. Login

Endpoint: ` /api/login/`

Method: `POST`

This endpoint allows users to log in by providing their email and password.

```sh
curl -X POST http://localhost:8666/api/login/ \
-H "Content-Type: application/json" \
-d '{
    "email": "johndoe@example.com",
    "password": "password123"
}'
'
```

#### 3. Email Activation

Endpoint: `/api/activate/<uidb64>/<token>/`

Method: `GET`

This endpoint is used to activate the user's account after they receive the activation email. \
Replace <uidb64> and <token> with the actual values from the activation link.

```sh
curl -X GET http://localhost:8666/api/activate/<uidb64>/<token>/

```

Example :
```
curl -X GET http://localhost:8000/api/activate/Nw/token1234567890/
```


#### 4. About Page

Endpoint: `/api/about/`

Method: `GET`

This endpoint is only accessible to authenticated users.
Use the token received from the login response to access this endpoint.


```sh
curl -X GET http://localhost:8666/api/about/ \
-H "Authorization: Token your_auth_token"

```
Replace your_auth_token with the actual token received after login.

#### 5. Search Users
Endpoint: `/api/search/?q=<keyword>`

Method: `GET`

Description: Search for users by email or name (paginated to 10).

Request:

```sh
curl -X GET http://localhost:8666/api/search/?q=am \
-H "Authorization: Token ecf6569e4f0eac014392df4385b502c20da9ddf7"
```

#### 6. Send Friend Request
Endpoint: `/api/friend-request/send/<user_id>/`

Method: `POST`

Description: Send a friend request to another user.

Request:

```sh
curl --location --request POST 'http://localhost:8666/accounts/friend-request/send/2/' \
--header 'Authorization: Token ecf6569e4f0eac014392df4385b502c20da9ddf7'
```

#### 7. Accept/Reject Friend Request
Endpoint: `/api/friend-request/respond/<request_id>/<action>/`

Method: `POST`

Description: Accept or reject a friend request.

Request:
```sh
# To accept a friend request
curl -X POST http://localhost:8666/api/friend-request/respond/1/accept/ \
-H "Authorization: Token ecf6569e4f0eac014392df4385b502c20da9ddf7"

# To reject a friend request
curl -X POST http://localhost:8666/api/friend-request/respond/1/reject/ \
-H "Authorization: Token ecf6569e4f0eac014392df4385b502c20da9ddf7"
```

#### 8. List Friends
Endpoint: `/api/friends/`

Method: `GET`

Description: Get a list of friends.

Request:
```sh
curl --location 'http://localhost:8666/accounts/friends/' \
--header 'Authorization: Token ecf6569e4f0eac014392df4385b502c20da9ddf7'
```

#### 9. List Pending Friend Requests
Endpoint: `friend-requests/pending/`

Method: `GET`

Description: Get a list of pending friend requests.

Request:
```sh
curl --location 'http://localhost:8666/accounts/friend-requests/pending/' \
--header 'Authorization: Token 9329e67d37381b153327ee67b5c0cd17fbb4c8d8'
```



# Setting up Postgres in local

1. Install Postgres in your system.
   - [x] [Postgres Installation for all Systems](https://www.timescale.com/blog/how-to-install-psql-on-mac-ubuntu-debian-windows/)


2.  Facing > django.db.utils.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  password authentication failed for user "postgres"?. Follow below lines :

    * Step 1: Check the status of the Postgres cluster.
    ```
    pg_lsclusters
    ```

    * Step 2: Restart the Postgres cluster
    ```
    sudo pg_ctlcluster 15 main start
    ```
    . Make sure to replace 15 with your version of Postgres.

    * Step 3: Check again and connect.
      ```
      pg_lsclusters
      ```
      ```
      sudo -i -u postgres
      ```
      ```
      psql
      ```

3. Facing > django.db.utils.OperationalError: connection to server at "localhost" (127.0.0.1), port 5432 failed: FATAL:  database "otolmsdbloc" does not exist. Facing this error?. Follow below steps:
      ```
      sudo -i u postgres
      ```
      ```
      CREATE DATABASE otolmsdbloc;
      ```
      ```
      ALTER USER postgres WITH PASSWORD 'postgres';
      ```


***
# Dev Responses
- [x] [Django LTS versions](https://www.djangoproject.com/download/)
- [x] [Python LTS versions](https://www.python.org/downloads/)


[//]: # (## Test and Deploy)

***


# Setting up pre-commit hooks

* pre-commit hooks run when we are trying to commit change into the remote repo.
* This will be make sure the steps mentioned in the file `pre-commit-config.yaml` are run if any of the steps fails it will not allow us to commit the changes.
* install pre-commit hooks.
   * mac os

      ```commandline
      brew install pre-commit
      ```
   * linux(any)

     ```commandline
     snap install pre-commit --classic
     ```
   * windows/Any environment

     ```commandline
     python3 -m pip install pre-commit
     ```

* Configuring pre-commit hooks.

1. To configure the pre-commits hooks run the following command.

  * if you install via python3 method.

    ```commandline
    python3 -m pre_commit install
    ```

  * if you installed via apt or brew run the following command to install.

     ```commandline
     pre-commit install
     ```

  * For manually running the commit hooks without even staging the files.

      ```commandline
      pre-commit run --all-files
      ```

    ## or

  * python -m flag.

    ```commandline
    python3 -m pre_commit run --all-files
    ```

## Environment Variables

To run this project, you will need to add the following environment variables to your `.env` file: (Sent on email)

`SECRET_KEY` - Your Django secret key (Check email)

`EMAIL_HOST_USER` - Email host user (Check email)

`EMAIL_HOST_PASSWORD` - Email host password (Check email)

# Dev Note:

![img.png](docs/img/devloper.gif)

# Reason For addition of Packages.

* ipython
  * Easy to handle shell commands rather than IDLE command interface.
  * ref:: https://pypi.org/project/ipython/


* graphviz
* django-extensions
* pyparsing
* pydot
   * This is make a ER Diagram for the model mappings.

* Use of django-environ
    * A Python package like django-environ can help manage environment variables in Django.
