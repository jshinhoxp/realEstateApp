# Overview
## Purpose
Utilizes L1 & L2 regression model to predict future housing prices based on historical Zillow dataset.
## Background
Source data based on 2014 historical Zillow dataset (21613 entries) under "home_data.csv" file.
## Packages
django, django-rest-frameworks, sklearn, plotly, folium, geopy, etc. \n
See requirements.txt for more info


## How the Model Works
Utilizing sklearn library, L1 & L2 regression model are trained based on 5 basic housing features of the home_data.csv dataset: ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors']. The models seek to minimize the residual sum of squares to find the line of best fit. The resulting models are stored by zipcode under 'backend_root/projectApp/ml_models'. \n
More complex modeling can be created by utilizing additional features (e.g year built, grade, etc.) and utilizing higher polynomial fittings. 

## User Interface 
User is prompted with a Django form, requesting an address the user would like to estimate within the Seattle metropolitan region. After submission, a 'POST' request is sent to index(request) within views.py to save and process the input, calculating its geographic locations (i.e lat / long) using geopy and calculating its home estimate using the L1 & L2 regression models. After updating the most recent entries, a marker is placed within the interactive map, containing its address and new home price estimate. 

See requirements.txt for pip packages
## Concept of Operations
## Code Structure
-.venv<br>
- backend_root<br>
-- backend<br>
-- node_modules\n
-- projectApp\n
-- templates\n
-- manage.py\n
-- package-lock.json\n
- public\n
- README.md\n

## Initial Steps to Recreate App 
- Install Python your system
- Create virtual environment within repo: "py -m venv .venv"
- Activate .venv by running activate.bat under /.venv/Scripts
- Within .venv, install django via pip: "pip install django"
- Create "django-admin startproject backend" in project folder
- (Optional) Rename mysite root folder to "backend_root"
- Migrate and then run server using: "py manage.py migrate" "py manage.py runserver"
within backend_root
- Create and name an app using "django-admin startapp projectApp"
- Connected to Amazon AWS Elastic Beanstalk to facilitate data storage and retrieval.
### GIT VERSION CONTROL
git add .
git commit -m "message"
git push