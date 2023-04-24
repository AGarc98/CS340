from jupyter_plotly_dash import JupyterDash

import dash
import dash_leaflet as dl
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import dash_table
from dash.dependencies import Input, Output


import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient



from myAnimalShelterlib import AnimalShelter



###########################
# Data Manipulation / Model
###########################

username = "aacuser"
password = "password1234"
shelter = AnimalShelter(username, password)

breed_options = [{'label': db, 'value': db} for db in shelter.get_dog_breeds()]


# class read method must support return of cursor object and accept projection json input
df = pd.DataFrame.from_records(shelter.read_all_dogs({}))





#########################
# Dashboard Layout / View
#########################
app = JupyterDash('Project Two')

app.layout = html.Div([
    html.Div([
        html.Img(src='./Logo.png', style={'width': '100%'})
    ], style={'position': 'absolute', 'top': 0, 'left': 0}),
    html.Div(id='hidden-div', style={'display':'none'}),
    html.H4('Alex Garcia SNHU CS-340 MongoDB Project 2'),
    html.Div([
        dcc.Dropdown(
            id='my-dropdown',
            options=[
                {'label': 'Water Rescue', 'value': 'Water Rescue'},
                {'label': 'Mountain or Wilderness Rescue', 'value': 'Mountain or Wilderness Rescue'},
                {'label': 'Disaster or Individual Tracking', 'value': 'Disaster or Individual Tracking'},
                {'label': 'Reset', 'value': 'Reset'}
            ],
            value='Reset'
        )
    ]),
   
    html.Center(html.B(html.H1('SNHU CS-340 Dashboard'))),
    html.Hr(),
    dash_table.DataTable(
        id='datatable-id',
        columns=[
            {"name": i, "id": i, "deletable": False, "selectable": True} for i in df.columns
        ],
        data=df.to_dict('records'),
        
        # Sorting
        sort_action='native',
        # Filtering
        filter_action='native',
        # Row selection
        row_selectable='multi',
        # Styling
        style_table={'overflowX': 'auto'},
        style_cell={
            'textAlign': 'left',
            'minWidth': '100px', 'width': '100px', 'maxWidth': '100px',
            'whiteSpace': 'normal'
        },
        style_header={
            'backgroundColor': 'white',
            'fontWeight': 'bold'
        }
    ),
    html.Br(),
    html.Hr(),
    html.Div(
        className='row',
        children=[
            html.Div(
                id='map-id',
                className='col s12 m6'
            )
        ]
    )
])

#############################################
# Interaction Between Components / Controller
#############################################
@app.callback(
    Output('datatable-id', 'data'),
    Input('my-dropdown', 'value')
)
def update_table(value):
    
    if value == 'Water Rescue':
        filtered_df = df[(df['breed'].isin(['Labrador Retriever Mix', 'Chesapeake Bay Retriever', 'Newfoundland'])) & 
                         (df['sex_upon_outcome'] == 'Intact Female') &
                         (df['age_upon_outcome_in_weeks'].between(26, 156))]
    elif value == 'Mountain or Wilderness Rescue':
        filtered_df = df[(df['breed'].isin(['German Shepherd', 'Alaskan Malamute', 'Old English Sheepdog', 'Siberian Husky', 'Rottweiler'])) &
                         (df['sex_upon_outcome'] == 'Intact Male') &
                         (df['age_upon_outcome_in_weeks'].between(26, 156))]
    elif value == 'Disaster or Individual Tracking':
        filtered_df = df[(df['breed'].isin(['Doberman Pinscher', 'German Shepherd', 'Golden Retriever', 'Bloodhound', 'Rottweiler'])) &
                         (df['sex_upon_outcome'] == 'Intact Male') &
                         (df['age_upon_outcome_in_weeks'].between(20,300))]
    else:
        filtered_df = df
    return filtered_df.to_dict('records')

@app.callback(
    Output('map-id', "children"),
    [Input('datatable-id', "derived_viewport_data"),
     Input('datatable-id', "selected_rows")])
def update_map(viewData, selected_rows):
    dff = pd.DataFrame.from_dict(viewData)
    selected_data = dff.loc[selected_rows, ['Name', 'location_lat', 'location_long']]
    markers = [dl.Marker(position=[row['location_lat'], row['location_long']], children=[
                    dl.Tooltip(row['Name']),
                    dl.Popup([
                        html.H1("Animal Name"),
                        html.P(dff.iloc[1,9])
                    ])
                ]) for index, row in selected_data.iterrows()]
    return [
        dl.Map(style={'width': '1000px', 'height': '500px'}, center=[30.75,-97.48], zoom=10, children=[
            dl.TileLayer(id="base-layer-id"),
            *markers
        ])
    ]

app