# Loan
Superuser: jung
Password: 12345

TUTORIAL
Ref: https://blog.logrocket.com/using-react-django-create-app-tutorial/
Ref: https://www.youtube.com/watch?v=dJihgq_4gNg&list=PLM30lSIwxWOivNtja1_ztft1S_vrMyA0z&index=3&ab_channel=SATSifaction

## Structure
-backend_root   (Project Name)
--backend       (Project Name)


## BACKGROUND
* Create an django REST Api for frontend to utilize.
Backend = Django

*React requires node.js to be installed
*Django requires python to be installed

## Concept of Operations
1. Web Scraper
   - Collects public information from Zillow website.
   - Collects photos of buildings from MLS
2. Cost-Benefit Analyzer
   - Determines the best real estate deal for either long or short term business plans.
   - collects photos of the residences and 
   - Uses ML/AI to understand the scope of the repair and maintenance costs.
   - Calculates expected maintenance and repair costs 
   - Calculates costs of a 30 Year VA Loan
   - DIY Option - Sources materials near location
   - City Data - Crime

3. Execution 
   - Automatically contacts nearby contractors and sets up appointments via robot and/or email.
   - Provides property management tools.
   - Tax preparation.

### STEPS

#### BACKEND
1. Create and Clone GitHub Repo 
2. Install Python your system
3. Create virtual environment within repo. 
"py -m venv .venv"
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
8. Create an app using "django-admin startapp MyAPI"


#### FRONTEND
CREATE FRONT END via REACT
1. "npx create-react-app frontend_root" in project folder

GIT VERSION CONTROL
git add .
git commit -m "message"
git push