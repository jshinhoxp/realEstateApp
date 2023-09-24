# Overview
## Purpose
Utilizes L1 & L2 regression model to predict future housing prices based on historical Zillow dataset.
## Background
Source data based on 2014 historical Zillow dataset (21613 entries) under "home_data.csv" file.
## Packages
django, django-rest-frameworks, sklearn, plotly, folium, geopy, etc. <br>
See requirements.txt for more info


## How the Model Works
Utilizing sklearn library, L1 & L2 regression model are trained based on 5 basic housing features of the home_data.csv dataset: ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors']. The models seek to minimize the residual sum of squares to find the line of best fit. The resulting models are stored by zipcode under 'backend_root/projectApp/ml_models'. <br>
More complex modeling can be created by utilizing additional features (e.g year built, grade, etc.) and utilizing higher polynomial fittings. 

## User Interface 
User is prompted with a Django form, requesting an address the user would like to estimate within the Seattle metropolitan region. After submission, a 'POST' request is sent to index(request) within views.py to save and process the input, calculating its geographic locations (i.e lat / long) using geopy and calculating its home estimate using the L1 & L2 regression models. After updating the most recent entries, a marker is placed within the interactive map, containing its address and new home price estimate. 

See requirements.txt for pip packages
## Code Structure
-.venv<br>
-backend_root<br>
--backend<br>
--node_modules<br>
--projectApp<br>
--templates<br>
--manage.py<br>
--package-lock.json<br>
-public<br>
-README.md<br>

## Initial Steps to Recreate App 
- Install Python your system <br>
- Create virtual environment within repo: "py -m venv .venv" <br>
- Activate .venv by running activate.bat under /.venv/Scripts <br>
- Within .venv, install django via pip: "pip install django" <br>
- Create "django-admin startproject backend" in project folder <br>
- (Optional) Rename mysite root folder to "backend_root" <br>
- Migrate and then run server using: "py manage.py migrate" "py manage.py runserver" 
within backend_root<br>
- Create and name an app using "django-admin startapp projectApp"<br>
- Connected to Amazon AWS Elastic Beanstalk to facilitate data storage and retrieval.<br>