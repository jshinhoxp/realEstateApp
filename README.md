# realEstate
Coded in Windows
LF was replaced by CRLF*

TUTORIAL
Ref: https://blog.logrocket.com/using-react-django-create-app-tutorial/

BACKGROUND
* Create an django REST Api for frontend to utilize.
Backend = Django 
Frontend = React

*React requires node.js to be installed
*Django requires python to be installed

STEPS
1. Create and Clone GitHub Repo 
2. Install Python your system
3. Create virtual environment within repo. 
"python3 -m venv .venv"
4. Within venv, install django via pip 
"pip install django"
& pip install djangorestframework = a powerful and flexible toolkit for building Web APIs
& pip install django-cors-headers = an app for handling the server headers required for CORS

5. Create "django-admin startproject backend" in project folder
6. Rename mysite root folder to "backend_root"
7. Migrate and then run server using:
"py manage.py migrate"
"py manage.py runserver"
within mysite_root

CREATE FRONT END via REACT
1. "npx create-react-app frontend_root" in project folder

GIT VERSION CONTROL
git add .
git commit -m "message"
git push