# %%
# Conventionally people rename the pandas import to pd for brevity
import pandas as pd

# %%
# Load in the data and preview it
sales = pd.read_csv('home_data.csv') 
# Order by zipcode
sales = sales.sort_values('zipcode')
# Create a list of the unique zipcodes (numpy.ndarray)
unique_zipcodes = sales['zipcode'].unique()
# Create list of dataframes by zipcode
list_of_df = []

for zipcode in unique_zipcodes:
   # Create df for each zipcode
   df = sales[sales['zipcode'] == zipcode]
   # Append to the list_of_df
   list_of_df.append(df)

# %%
from sklearn.model_selection import train_test_split
list_of_df_train = []
list_of_df_test = []
# Split each dataframe into train (80%) and test data (20%) 
for df in list_of_df:
   train_data, test_data = train_test_split(df, test_size=0.2)
   list_of_df_train.append(train_data)
   list_of_df_test.append(test_data)

print(f"# of zipcodes:", len(unique_zipcodes))
print(f"# of (train) dataframes:", len(list_of_df_train))
print(f"# of (test) dataframes:", len(list_of_df_test))

# %%
from sklearn import linear_model
from sklearn.metrics import mean_squared_error 

# List features to use for model to predict 
basic_features = ['bedrooms', 'bathrooms', 'sqft_living', 'sqft_lot', 'floors']

list_of_models = []
list_of_rmse_basic_train = []
# Basic Model
for df in list_of_df_train:
   y = df.price # actual price column of training set
   X = df[basic_features] # rest of dataframe data
   # Create and train the model
   basic_model = linear_model.LinearRegression().fit(X, y)
   # Store the model into list of models
   list_of_models.append(basic_model)
   # Predict prices using the model
   y = df.price # actual price column of training set
   X = df[basic_features]
   y_pred = basic_model.predict(X)
   train_rmse_basic = mean_squared_error(y, y_pred, squared=False) #False = rmse
   list_of_rmse_basic_train.append(train_rmse_basic)

print(f"# of ML models: ", len(list_of_models))
print(f"# of Root Mean Squared Error: ", len(list_of_rmse_basic_train))

# %%
# Comparing with Test Data
list_of_rmse_basic_test = []

i = 0
while i < len(list_of_models):
   df = list_of_df_test[i]
   y = df.price
   X = df[basic_features]
   y_pred = list_of_models[i].predict(X)
   test_rmse_basic = mean_squared_error(y, y_pred, squared=False) #False = rmse
   list_of_rmse_basic_test.append(test_rmse_basic)
   i += 1

df = pd.DataFrame({
   'unique_zipcodes': unique_zipcodes,
   'list_of_rmse_basic_train': list_of_rmse_basic_train,
   'list_of_rmse_basic_test': list_of_rmse_basic_test
   })


# %%
from joblib import dump, load

path = "projectApp/ml_models/"

# Create and dump models into designated folder
i = 0
while (i < len(list_of_models)):
   model = list_of_models[i]
   zipcode = unique_zipcodes[i]
   dump(model, path + str(zipcode))
   i += 1


# %%
#Use plotly to display awesome charts
import plotly.express as px

# Shows the geographic data
fig = px.scatter(sales, x="long",y="lat", 
                 color='zipcode', title='King County Housing Dataset 2014',
                 size='price')

# %%
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.graph_objs as go

zipcode_list = sales['zipcode'].unique()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the app layout
app.layout = html.Div([
    dcc.Dropdown(
        id='data-dropdown',
        options=[
           {'label': zipcode, 'value': zipcode} for zipcode in unique_zipcodes],
           value=zipcode  # Initial dropdown value
    ),
    dcc.Graph(id='line-chart')
])

# Define a callback to update the line chart based on dropdown selection
@app.callback(
    Output('line-chart', 'figure'),
    [Input('data-dropdown', 'value')]
)

def update_line_chart(selected_data):
    xaxis = "sqft_living"
    yaxis = "price"
    
    df = sales[sales['zipcode']==int(selected_data)]

    trace = go.Scatter(
        x=df['sqft_living'],
        y=df['price'],
        mode='markers',
        name=selected_data)       

    return {
        'data': [trace],
        'layout': go.Layout(
            title=f'{xaxis} vs {yaxis} <br> zipcode {selected_data}',
            xaxis={'title': xaxis},
            yaxis={'title': yaxis}
        )
    }

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)



