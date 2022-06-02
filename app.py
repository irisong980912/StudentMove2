# from os import truncate
import dash
import dash_bootstrap_components as dbc
from dash_bootstrap_components._components.DropdownMenu import DropdownMenu
from dash_bootstrap_components._components.DropdownMenuItem import DropdownMenuItem
from dash_bootstrap_components._components.NavLink import NavLink
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output, State
# from dash_html_components.Div import Div
import pandas as pd
import plotly.express as px
import math
import numpy as np
import time
import json


plotly_figure = dict(data=[dict(x=[1, 2, 3], y=[2, 4, 8])])
# make the mode 
modebar_config = {'showTips': True,'displayModeBar': True, 'displaylogo': False}


# Load data
df = pd.read_csv('data/combinednew.csv', index_col=0, parse_dates=True,low_memory=False)
filteredDf = df


# ========================== helper function to get the variables ==========================
# propogate the variables to the dropdown list
def get_variables():
    proper = ["Gender", "Age", "Institution", "Monthly Transportation Cost ($)",
              "Main Transportation Mode", "Commute Distance (km)", "Location of Residence"]
    dict_list = []
    for i in proper:
        dict_list.append({'label': i, 'value': i})

    return dict_list

def get_variables_corr():
    proper = ["Gender", "Age", "Institution", "Monthly Transportation Cost ($)",
              "Main Transportation Mode", "Commute Distance (km)"]
    dict_list = []
    for i in proper:
        dict_list.append({'label': i, 'value': i})

    return dict_list

def get_age():
    dict_list = []
    for i in df['Age'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_mode():
    dict_list = []
    for i in df['psmainmodefalltypical'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_commutsatis():
    dict_list = []
    for i in df['ps18HadThe____TravelExperience'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_travelcost():
    dict_list = []
    for i in df['Monthly Transportation Cost ($)'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_livingsit():
    dict_list = []
    for i in df['hhlivingsituation'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_householdmem():
    prop = ["2 or fewer", "3-5", "5+"]
    dict_list = []
    for i in prop:
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_housetype():
    dict_list = []
    for i in df['hhbuildingtype'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_autoav():
    dict_list = []
    for i in df['psautoavailability'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_studentwellbeing():
    dict_list = []
    for i in df['ps21FeelHappy'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_studentacademic():
    dict_list = []
    for i in df['ps25HappyWithAcademicPerformance'].unique():
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_gender():
    dict_list = []
    for i in df['Gender'].unique():
        print(i)
        if(str(i) != 'nan'):
            dict_list.append({'label': i, 'value': i})

    return dict_list


def get_enrollments():
    dict_list = []
    for i in df['psuniversityaffiliation'].unique():
        if(str(i) != 'nan'):

            dict_list.append({'label': str(i)+' uni', 'value': i})

    for i in df['pscollegeaffiliation'].unique():
        if(str(i) != 'nan'):

            dict_list.append({'label': str(i)+' col', 'value': i})

    return dict_list


def get_options_inst():
    dict_list = []
    for i in df['Institution'].unique():
        print(i)
        dict_list.append({'label': i, 'value': i})

    return dict_list


def get_options_workHours():
    dict_list = []
    for i in df['Working Hours'].unique():
        dict_list.append({'label': i, 'value': i})

    return dict_list


# Remote Bootstrap Theme and resposive meta tags
# try running the app with any theme from https://bootswatch.com/
# app = dash.Dash (external_stylesheets=dbc.themes.MORPH)
# app = dash.Dash (external_stylesheets=dbc.themes.CYBORG)

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED],
                meta_tags=[{'name': 'viewport',
                            'content': 'width=device-width, initial-scale=1.0'}]
                )
server = app.server

# Bootstrap Layout
# ========================== HTML Page Container  ==========================
app.layout = html.Div([

    # html.Link(rel='stylesheet', href='/style.css'),

    #  --- navigation bar (dashboard options) ---
    dbc.NavbarSimple(
        children=[
            # dbc.NavItem(dbc.NavLink(
            #     "About", href="http://www.studentmoveto.ca/about/")),
            dbc.DropdownMenu(
                children=[

                    dbc.DropdownMenuItem(
                        "Visualize Variables", href="#visualize", external_link=True),
                    dbc.DropdownMenuItem(
                        "Relate Variables", href="#relate", external_link=True),
                    dbc.DropdownMenuItem(divider=True),

                    dbc.DropdownMenuItem(
                        "Filter Variables", href="#filter", external_link=True),
                ],
                nav=True,
                in_navbar=True,
                label="Dashboard Options",
            ),
        ],

        brand="Data Visualization",
        brand_href="app.py",
        color="#f58220",
        dark=True,
        className="",
        sticky="top",
    ),

    # --- Main Page Banner ---
    dbc.Jumbotron([


        html.Img(src=app.get_asset_url(
            'SMTO-logo.png'), className="mb-5"),

        # Below the line text-area
        html.Hr(className="my-2"),
        html.P(
            "Capturing Transportation Experiences of Post-Secondary Students Across the GTHA",
            className="text-light"
        ),


        html.P(dbc.Button("Learn more", href="http://www.studentmoveto.ca/about/", style={"background-color": "#f58220"},
               className="lead btn btn-secondary")),

    ],
        style={"height": "100%", "background-color": "#43525a", "overflow": "scroll"},
        className="p-5",

    ),


    # --- Number Facts Row #1 ---
    dbc.Row(
        [

            dbc.Col(dbc.Card(
                    [


                        dbc.CardHeader(
                            "No. of Student Respondents", className="bg-dark text-light"),
                        dbc.CardBody(
                            [
                                dbc.Col(dcc.Loading(children=[html.H1(
                                                    str(df.size), className="card-text text-center display-5", id="first_output_2"), ], type="default")),

                                html.P("",
                                       className="card-title text-center"),

                            ],


                        ),

                    ],
                    style={"width": "18rem", "padding": "1rem",
                           "margin-top": "2rem"},
                    )),

            dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader(
                            "% of Total Respondents", className="bg-dark text-light"),
                        dbc.CardBody(
                            [
                                dbc.Col(dcc.Loading(children=[html.H1(
                                                    str(df.size), className="card-text text-center display-5", id="first_output_6"), ], type="default")),

                                html.P("",
                                       className="card-title text-center"),
                            ]
                        ),

                    ],
                    style={"width": "18rem", "padding": "1rem",
                           "margin-top": "2rem"},
                    )),

            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader("Average Commute Distance",
                                   className="bg-dark text-light"),
                    dbc.CardBody(
                        [
                            dbc.Col(dcc.Loading(children=[html.H1(
                                str(df.size), className="card-text text-center display-5", id="first_output_4"), ], type="default")),
                            html.P("",
                                   className="card-title text-center"),
                        ]
                    ),

                ],
                style={"width": "18rem", "padding": "1rem",
                       "margin-top": "2rem"},
            )),

        ],
        className="p-5",
    ),

    # --- Number Facts Row #2 ---
    dbc.Row(
        [
            dbc.Col(dbc.Card(
                    [
                        dbc.CardHeader(
                            "Average Monthly Transportation Cost", className="bg-dark text-light"),
                        dbc.CardBody(
                            [
                                dbc.Col(dcc.Loading(children=[html.H1(
                                                    str(df.size), className="card-text text-center display-5", id="first_output_1"), ], type="default")),

                                html.P("",
                                       className="card-title text-center"),
                            ]
                        ),

                    ],
                    style={"width": "18rem", "padding": "1rem",
                           "margin-top": "2rem"},
                    )),

            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader("Commute Satisfaction",
                                   className="bg-dark text-light"),
                    dbc.CardBody(
                        [
                            dbc.Col(dcc.Loading(children=[html.H1(
                                str(df.size), className="card-text text-center display-5", id="first_output_7"), ], type="default")),
                            html.P("",
                                   className="card-title text-center"),
                        ]
                    ),

                ],
                style={"width": "18rem", "padding": "1rem",
                       "margin-top": "2rem"},
            )),

            dbc.Col(dbc.Card(
                [
                    dbc.CardHeader("Main Transportation Mode",
                                   className="bg-dark text-light"),
                    dbc.CardBody(
                        [
                            dbc.Col(dcc.Loading(children=[html.H1(
                                str(df.size), className="card-text text-center display-5", id="first_output_5"), ], type="default")),
                            html.P("",
                                   className="card-title text-center"),
                        ]
                    ),

                ],
                style={"width": "18rem", "padding": "1rem",
                       "margin-top": "2rem"},
            )),
        ],
        className="p-5",
    ),

    dbc.Row(
        [
            dbc.Col(html.Div([

                # html.H5("Acknowledgment"), 
                html.P("We gratefully acknowledge the contributions made by the following institutions: \nCentennial College, Durham College, McMaster University, Mohawk College, OCAD University, Ontario Tech University, Sheridan College, Toronto Metropolitan University (Ryerson), University of Toronto, York University.")], style={"width": "80%"}), width=12),


        ],
        className="Bottom-space",
        # style={"background-color": "#43525a"},
    ),

    # ========================== SECTION 1 VISUALilize a Variable ==========================

    # Title 
    dbc.Row(
        dbc.Col(html.H1("Visualize Variables", id="visualize",
                        className='text-center text-light p-5 mb-4'), width=12),
        style={"background-color": "#43525a"},
    ),


    # Dropdown
    dbc.Row(
        [
            dbc.Col(html.Div(
                    children=[html.Div(
                        className='div-for-dropdown',
                        children=[
                            dcc.Dropdown(
                                id='demo-dropdown21',
                                options=get_variables(),
                                value='Location of Residence',
                                placeholder='Variables to Visualize',
                                style={'width': '300px', 'height': 'auto',
                                       'display': 'inline-block'}
                            ),

                        ],
                        style={'color': 'black'}), ]
                    ), width=4), 
        ],

        className="p-5",
    ),


    # plot 1
    dbc.Row(
        [
            dbc.Col(dcc.Loading(id="loading-icon1",
                                children=[html.Div(
                                    dcc.Graph(id='plot1', figure=plotly_figure, config=modebar_config))
                                    ], type="default")),
        ],
    ),

    # SECTION 2 Relating Variables


    dbc.Row(
        dbc.Col(html.H1("Relate Variables", id="relate",
                        className='text-center text-light p-5 mb-4'), width=12),
        style={"background-color": "#43525a"},
    ),



    dbc.Row(
        [
            dbc.Col(dcc.Dropdown(
                    id='drop-doublevarvis1',
                    options=get_variables_corr(),
                    placeholder='Variable Vis 1',
                    value='Gender',
                    style={
                        'width': '300px', 'height': 'auto', 'display': 'inline-block'}
                    ),),
            dbc.Col(dcc.Dropdown(
                    id='drop-doublevarvis2',
                    options=get_variables_corr(),
                    placeholder='Variable Vis 2',
                    value='Main Transportation Mode',
                    style={
                        'width': '300px', 'height': 'auto', 'display': 'inline-block'}
                    ),), dbc.Col()
        ],
        className="p-5",
    ),

    
  

    dbc.Row(
        [
            dbc.Col(dcc.Loading(id="loading-icon",
                                children=[html.Div(dcc.Graph(id='plot2', figure=plotly_figure, config=modebar_config))], type="default")),
        ],
        className="p-5",
    ),



    # SECTION 3 - FILTER Multiple VARIABLES

    dbc.Row(
        dbc.Col(html.H1("Filter Variables", id="filter",
                        className='text-center text-light p-5 mb-4'), width=12),
        style={"background-color": "#43525a"},
    ),


    dbc.Row(
        dbc.Col(
            html.H2("Main Filter", className='mb-4'), width=12),
            style={"padding-top": "4rem", "padding-left": "3rem"},
    ),

    dbc.Row(
        dbc.Col(
            html.P("Please select relevant institution"), width=12),
            style={"padding-left": "3rem"},
    ),

    dbc.Row(
        [
            dbc.Col(dcc.Dropdown(
                id='inst-dropdown',
                options=get_options_inst(),
                placeholder='All Institutions',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}
            ), width=4),


        ],
        className="Title"
    ),

    # ------------------
    dbc.Row(
        dbc.Col(
            html.H2("Subfilters", className='mb-4'), width=12),
            style={"padding-top": "3rem", "padding-left": "3em"},
    ),

    #-- demographics
    dbc.Row(
        dbc.Col(
            html.H4("Demographics", className=''), width=12),
            style={ "padding-left": "3rem"},
    ),


    dbc.Row(
    [
        # age
        dbc.Col(dcc.Dropdown(
            id='age-dropdown',
            options=get_age(),
            placeholder='Age',
            style={
                'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # gender
        dbc.Col(dcc.Dropdown(
                id='gender-dropdown',
                options=get_gender(),
                placeholder='Gender',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # enrollment
        dbc.Col(dcc.Dropdown(
                id='enrollments-dropdown',
                options=get_enrollments(),
                placeholder='Enrollment Type',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),


    ],
        className="Title",
        style={"padding-top": "1rem"},
    ),

    #-- Transportation
    dbc.Row(
        dbc.Col(
            html.H4("Transportation", className=' '), width=12),
            style={ "padding-left": "3rem", "padding-top": "2rem"},
    ),


    dbc.Row(
    [
        # primary mode
        dbc.Col(dcc.Dropdown(
            id='mode-dropdown',
            options=get_mode(),
            placeholder='Primary Mode',
            style={
                'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # commute satisfaction
        dbc.Col(dcc.Dropdown(
                id='commsatis-dropdown',
                options=get_commutsatis(),
                placeholder='Commute Satisfaction',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # monthly travel cost ($)
        dbc.Col(dcc.Dropdown(
                id='travcost-dropdown',
                options=get_travelcost(),
                placeholder='Monthly Travel Cost ($)',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),


    ],
        className="Title",
        style={"padding-top": "1rem"},
    ),

    #-- Housing
    dbc.Row(
        dbc.Col(
            html.H4("Housing", className=' '), width=12),
            style={ "padding-left": "3rem", "padding-top": "2rem"},
    ),


    dbc.Row(
    [
        # Members in household
        dbc.Col(dcc.Dropdown(
            id='householdmem-dropdown',
            options=get_householdmem(),
            placeholder='Members In Household',
            style={
                'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # AUtomotive Availability
        dbc.Col(dcc.Dropdown(
                id='autoav-dropdown',
                options=get_autoav(),
                placeholder='Automotive Availability',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # House Type
        dbc.Col(dcc.Dropdown(
                id='housetype-dropdown',
                options=get_housetype(),
                placeholder='House Type',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),


    ],
        className="Title",
        style={"padding-top": "1rem"},
    ),


    #-- Wellbeing
    dbc.Row(
        dbc.Col(
            html.H4("Wellbeing", className=' '), width=12),
            style={ "padding-left": "3rem", "padding-top": "2rem"},
    ),


    dbc.Row(
    [
        # Living Situation
        dbc.Col(dcc.Dropdown(
            id='livingsit-dropdown',
            options=get_livingsit(),
            placeholder='Living Situation',
            style={
                'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # Academic Success
        dbc.Col(dcc.Dropdown(
                id='academic-dropdown',
                options=get_studentacademic(),
                placeholder='Student Is Happy With Their Academic Performance',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

        # Overall Happiness
        dbc.Col(dcc.Dropdown(
                id='wellbeing-dropdown',
                options=get_studentwellbeing(),
                placeholder='Overall Student Happiness',
                style={
                    'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),


    ],
        className="Title",
        style={"padding-top": "1rem"},
    ),




    # dbc.Row([
        # dbc.Col([dbc.Col(dcc.Dropdown(
        #     id='age-dropdown',
        #     options=get_age(),
        #     placeholder='Age',
        #     style={
        #         'width': '100%', 'height': 'auto', 'display': 'inline-block'}

        # ),),
        #     dbc.Col(dcc.Dropdown(
        #         id='gender-dropdown',
        #         options=get_gender(),
        #         placeholder='Gender',
        #         style={
        #             'width': '100%', 'height': 'auto', 'display': 'inline-block'}

        #     ),),
        #     dbc.Col(dcc.Dropdown(
        #         id='enrollments-dropdown',
        #         options=get_enrollments(),
        #         placeholder='Enrollment Type',
        #         style={
        #             'width': '100%', 'height': 'auto', 'display': 'inline-block'}

        #     )), ]),
            # dbc.Col([dbc.Col(dcc.Dropdown(
            #         id='mode-dropdown',
            #         options=get_mode(),
            #         placeholder='Primary Mode',
            #         style={
            #                     'width': '100%', 'height': 'auto', 'display': 'inline-block'}

            #         )),
            #     dbc.Col(dcc.Dropdown(
            #             id='commsatis-dropdown',
            #             options=get_commutsatis(),
            #             placeholder='Commute Satisfaction',
            #             style={
            #                 'width': '100%', 'height': 'auto', 'display': 'inline-block'}

            #             )),
            #     dbc.Col(dcc.Dropdown(
            #             id='travcost-dropdown',
            #             options=get_travelcost(),
            #             placeholder='Monthly Travel Cost ($)',
            #             style={
            #                 'width': '100%', 'height': 'auto', 'display': 'inline-block'}

            #             )),
            # ]),
            # dbc.Col([dbc.Col(dcc.Dropdown(
            #         id='householdmem-dropdown',
            #         options=get_householdmem(),
            #         placeholder='Members In Household',
            #         style={
            #                     'width': '100%', 'height': 'auto', 'display': 'inline-block'}

            #         )),
            #     dbc.Col(dcc.Dropdown(
            #             id='autoav-dropdown',
            #             options=get_autoav(),
            #             placeholder='Automotive Availability',
            #             style={
            #                 'width': '100%', 'height': 'auto', 'display': 'inline-block'}

            #             )),
            #     dbc.Col(dcc.Dropdown(
            #             id='housetype-dropdown',
            #             options=get_housetype(),
            #             placeholder='House Type',
            #             style={
            #                 'width': '100%', 'height': 'auto', 'display': 'inline-block'}

            #             )), ]),
    #         dbc.Col([dbc.Col(dcc.Dropdown(
    #                 id='livingsit-dropdown',
    #                 options=get_livingsit(),
    #                 placeholder='Living Situation',
    #                 style={
    #                     'width': '100%', 'height': 'auto', 'display': 'inline-block'}

    #                 )),
    #             dbc.Col(dcc.Dropdown(
    #                     id='academic-dropdown',
    #                     options=get_studentacademic(),
    #                     placeholder='Student Is Happy With Their Academic Performance',
    #                     style={
    #                         'width': '100%', 'height': 'auto', 'display': 'inline-block'}

    #                     )),
    #             dbc.Col(dcc.Dropdown(
    #                     id='wellbeing-dropdown',
    #                     options=get_studentwellbeing(),
    #                     placeholder='Overall Student Happiness',
    #                     style={
    #                         'width': '100%', 'height': 'auto', 'display': 'inline-block'}

    #                     )), ])
    #     ]
    # ),

        # dbc.Row(
    #     [dbc.Col(
    #         html.Div(
    #             [
    #                 dbc.Button(
    #                     "Main Filter",
    #                     id="auto-toast-toggle-1",
    #                     className="mr-4 btn btn-dark btn-lg",
    #                     n_clicks=0,
    #                 ),

    #                 dbc.Toast(

    #                     [html.P("Select Relevant Institution",
    #                             className="mb-0")],

    #                     id="auto-toast-1",
    #                     header="Academic Institutions",
    #                     icon="#f58220",
    #                     duration=4000,
    #                 ),

    #             ],
    #             className="p-5",
    #         )),


    #      ]),

    # dbc.Row(
    #     [dbc.Col(
    #         html.Div(
    #             [
    #                 dbc.Button(
    #                     "Subfilters",
    #                     id="auto-toast-toggle-2",
    #                     style={"background-color": "#f58220"},
    #                     className="mr-4 btn-lg text-light",

    #                     n_clicks=0,
    #                 ),

    #                 dbc.Toast(

    #                     [html.P("Demographics, Transportation, Housing, Wellbeing",
    #                             className="mb-0")],

    #                     id="auto-toast-2",
    #                     header="Main Categories",
    #                     icon="#f58220",
    #                     duration=4000,
    #                 ),

    #             ],
    #             className="p-5",
    #         )),


    #      ]),

    # dbc.Row(
    #     [

    #         dbc.Col(html.Img(src=app.get_asset_url(
    #             'SSHRC-logo.png'), style={'width': '100%', 'height': 'auto', 'display': 'inline-block'}), width=4),

    #         dbc.Col(html.Div(
    #             [

    #                 html.H2("Partnership Program"),
    #                 # html.P("Development of this data dashboard was made possible through a collaborative SSHRC funded project.")]), width=4),
    #                 html.P("StudentMoveTO research program is supported by a Partnership Development Grant from Social Sciences and Humanities Research Council of Canada (SSHRC).")]), width=4),

            

    #         ],
    #             className="text-light p-5",
    #             style={"background-color": "#43525a", "margin-top": "100px"},
    #         ),


    dbc.Row(dbc.Col(
        html.Div(html.Img(src=app.get_asset_url(
        'SSHRC-logo.png'),width="100%"), style={"width": "20%"}), width=12,className="Center-container Title"),
        className="text-light",
        style={"background-color": "#43525a", "padding-top": "3rem", "margin-top": "6rem"},
    ),



    dbc.Row(
        dbc.Col(html.Div(html.P("StudentMoveTO research program is supported by a Partnership Development Grant from Social Sciences and Humanities Research Council of Canada (SSHRC).",
                        className='text-center text-light'), style={"width": "60%"}), width=12, className="Center-container Bottom-space ", 
                        style={"background-color": "#43525a", "margin-bottom": "3rem"}
                        )
    ),


    dbc.Row(
        [
            dbc.Col(html.Div(html.H2("Project Coordinators"),), width=4),

        ],
        className="Title",
        # style={"background-color": "#43525a"},
    ),

  
    dbc.Row(
        [

            dbc.Col(html.Div(
                [
                    html.H5("Professor Jeremy Bowes"),
                    html.P("Faculty of Design, Visual Analytics Lab at OCAD University.")]), width=4),

            dbc.Col(html.Div(
            [

                html.H5("Raktim Mitra, PhD"),
                html.P("School of Urban and Regional Planning, Director of Transportation and Land Use Planning Research Lab at Toronto Metropolitan Univerity")]), width=4),


        ],
        className="Bottom-space",
        # style={"background-color": "#43525a"},
    ),
    

    dbc.Row(
        [
            dbc.Col(html.Div(html.H2("Research Assistants"),), width=4),

        ],
        className="Title",
        # style={"background-color": "#43525a"},
    ),


    dbc.Row(
        [
            dbc.Col(html.Div([

                html.H5("Bo Louie Siu"), # OCAD
                html.P("Research Assistant and designer of the front-end layout using Bootstrap at OCAD University")]), width=4),

            dbc.Col(html.Div([


                html.H5("Ryan Barquero"), # Ryerson 
                html.P("Research assistant and lead of Geospatial mapping using ArcGIS at Toronto Metropolitan University")]), width=4),

            dbc.Col(html.Div([

            html.H5("Iman Kewalramani & Xiaoqi Gao"), # UofT
            html.P("Research assistant and python programmer of the back-end framework using Dash Plotly at the University of Toronto")]), width=4),


        ],
        className="Bottom-space",
        # style={"background-color": "#43525a"},
    ),

    dbc.Row(
        [

                dbc.Col(
                    html.Div(html.Img(src=app.get_asset_url(
                    'Ryerson-logo.png'),width="100%"), style={"width": "60%"}), width=3,className="Center-container p-5"),

                dbc.Col(html.Div(html.Img(src=app.get_asset_url(
                    'ocadu-logo.png'), width="100%"), style={"width": "60%"}), width=3, className="Center-container p-5"),

                dbc.Col(html.Div(html.Img(src=app.get_asset_url(
                    'UOFT-logo.png'), width="100%"), style={"width": "60%"}), width=3, className="Center-container p-5"),

                dbc.Col(html.Div(html.Img(src=app.get_asset_url(
                    'YORK-logo.png'), width="100%"), style={"width": "60%"}), width=3, className="Center-container p-5"),

            

        ],
        className="text-light p-5",
    ),


    # end -- closing app
])


@ app.callback(
    Output("auto-toast-1", "is_open"),
    [Input("auto-toast-toggle-1", "n_clicks")],
)
def open_toast(n):
    return True


@ app.callback(
    Output("auto-toast-2", "is_open"),
    [Input("auto-toast-toggle-2", "n_clicks")],
)
def open_toast(n):
    return True


@ app.callback(
    Output('first_output_1', 'children'),
    Output('first_output_2', 'children'),
    Output('first_output_4', 'children'),
    Output('first_output_5', 'children'),
    Output('first_output_6', 'children'),
    Output('first_output_7', 'children'),
    Output('plot1', 'figure'),
    Output('plot2', 'figure'),
    Input('inst-dropdown', 'value'),
    Input('gender-dropdown', 'value'),
    Input('age-dropdown', 'value'),
    Input('enrollments-dropdown', 'value'),
    Input('mode-dropdown', 'value'),
    Input('commsatis-dropdown', 'value'),
    Input('travcost-dropdown', 'value'),
    Input('livingsit-dropdown', 'value'),
    Input('householdmem-dropdown', 'value'),
    Input('housetype-dropdown', 'value'),
    Input('autoav-dropdown', 'value'),
    Input('wellbeing-dropdown', 'value'),
    Input('academic-dropdown', 'value'),
    Input('demo-dropdown21', 'value'),
    Input('drop-doublevarvis1', 'value'),
    Input('drop-doublevarvis2', 'value'))

# -- update output graphs and texts based on the dropdown item selected -- 
def text_callback(inst, gender, age, enroll, mode, commsatis, travcost, livingsit, householdmem, housetype, autoav, wellbeing, academic,  visvar, var1, var2):
    
    #  filter and load dataframe
    filteredDf = df

    if(gender is not None):
        filteredDf = filteredDf[filteredDf['Gender'] == gender]
    if(inst is not None):
        filteredDf = filteredDf[filteredDf['Institution'] == inst]
    if(age is not None):
        filteredDf = filteredDf[filteredDf['Age'] == age]
    if(enroll is not None):
        if(filteredDf[filteredDf['psuniversityaffiliation'] == enroll].size == 0):
            filteredDf = filteredDf[filteredDf['pscollegeaffiliation'] == enroll]
        else:
            filteredDf = filteredDf[filteredDf['psuniversityaffiliation'] == enroll]
    if(mode is not None):
        filteredDf = filteredDf[filteredDf['psmainmodefalltypical'] == mode]
    if(commsatis is not None):
        # convert the text to numbers
        questionTitle = ['ps18HadThe____TravelExperience', 'ps19QualityOfTravelWas____', 
                    'ps20TravelWorked_____']

        replacer = {'Worst': 1, 'Bad': 2,'Average': 3, 'Good': 4, 'Best': 5}

        # Replace qualitative values with quantitative numbers in "questionTitle" Columns
        for ques in questionTitle:
            df[ques] = df[ques].replace(replacer)

        # average Q18-20 and create a new column
        filteredDf['commsatisAvg'] = filteredDf[['ps18HadThe____TravelExperience', 'ps19QualityOfTravelWas____', 
                            'ps20TravelWorked_____']].mean(axis=1)

        filteredDf['commsatisAvg'].round(0)

        print(filteredDf['commsatisAvg'])
        print(replacer[commsatis])

        filteredDf = filteredDf[filteredDf['commsatisAvg'] == replacer[commsatis]]
    if(travcost is not None):
        filteredDf = filteredDf[filteredDf['Monthly Transportation Cost ($)'] == travcost]
    if(livingsit is not None):
        filteredDf = filteredDf[filteredDf['hhlivingsituation'] == livingsit]
    if(householdmem is not None): # combine df basd on the household size 
        if(householdmem == "2 or fewer"):
            filteredDf = filteredDf[filteredDf['hhsize'] <= 2]
        elif(householdmem == "5+"):
            filteredDf = filteredDf[filteredDf['hhsize'] > 5]
        else:
            filteredDf = filteredDf[filteredDf['hhsize'] >= 3]
            filteredDf = filteredDf[filteredDf['hhsize'] <= 5]

    if(housetype is not None):
        filteredDf = filteredDf[filteredDf['hhbuildingtype'] == housetype]
    if(autoav is not None):
        filteredDf = filteredDf[filteredDf['psautoavailability'] == autoav]
    if(wellbeing is not None):
        filteredDf = filteredDf[filteredDf['ps21FeelHappy'] == wellbeing]
    if(academic is not None):
        filteredDf = filteredDf[filteredDf['ps25HappyWithAcademicPerformance'] == academic]

    # ======= finish loading the dataframe =======
    # ======= visualize variable =======

    # default option
    if(visvar is None): 
        visvar = 'Location of Residence'
    # historgram if the entries are numbers
    if (str(df[visvar].dtypes) == "float64"):
        fig = px.histogram(filteredDf[visvar],
                           x=visvar, nbins=5, histnorm='percent')

    else:
        filteredDf[visvar] = filteredDf[visvar].str.replace(' ', '') # remove empty space
        table = pd.pivot_table(filteredDf, values='PsKey_', index=[
            visvar], aggfunc='count')

        # total number of people living in that area 
        table['% of Total'] = (table["PsKey_"] / table["PsKey_"].sum() * 100)

        print(table)


        # geo graph
        if(visvar == 'Location of Residence'):

            # # removed the empty slots
            # countEmpty = sum(filteredDf[visvar] == '')
            # print(countEmpty)

            # # total number of people living in that partucykar 
            # table['% of Total'] = (table["PsKey_"] / (table["PsKey_"].sum() - countEmpty) * 100)
            # print(table)

            with open('data/area.geojson') as json_file:
                gdat = json.load(json_file)

            i = 1
            for feature in gdat["features"]:
                feature['id'] = str(i).zfill(2)
                i += 1
            # print(gdat)

            print(table.reset_index())


            fig = px.choropleth_mapbox(table.reset_index(), geojson=gdat, color="% of Total", 
                                       locations="Location of Residence", featureidkey="properties.CFSAUID",
                                       mapbox_style="carto-positron", center={"lat": 43.8732, "lon": -79.3832}, 
                                       zoom=7, height=800,  opacity=0.75, color_continuous_scale="deep")
            

            
            fig.update_geos(center=dict(lon=43.4675, lat=-79.6877), 
                            fitbounds="geojson", visible=True)


        # if not locationOfRes, then pie chart
        else:
            fig = px.pie(table.reset_index(), values="% of Total",
                         names=visvar, title="", hole=0.3)

    fig.update_layout(font_size=18, hoverlabel=dict(
        bgcolor="white",
        font_size=18,
    ))


    if(var1 is None):
        var1 = 'Gender'

    if(var2 is None):
        var2 = 'Main Transportation Mode'

    table1 = pd.pivot_table(filteredDf, values='PsKey_', index=[
        var1, var2], aggfunc='count')
    table1['% of Total'] = (table1["PsKey_"] / table1["PsKey_"].sum() * 100)
    table1['% of ' + var1] = (table1["PsKey_"] /
                            table1.groupby(level=0)["PsKey_"].transform(sum) * 100)

    # maybe bubble chart
    fig2 = px.bar(table1.reset_index(), x=var1,
                  y="% of "+var1, color=var2)

    fig2.update_layout(font_size=18, hoverlabel=dict(
        bgcolor="white",
        font_size=18,), barmode="relative")

    O0 = '$'+str(filteredDf["psmonthlytravelcost"].mean())[0: 6]
    O1 = str(len(filteredDf.index))
    O2 = str(len(filteredDf.index)/len(df.index)*100)[0: 6]+"%"
    O3 = (filteredDf["Main Transportation Mode"].mode())
    O4 = str(filteredDf["networkcommitedistance"].mean()/1000)[0: 4]+" Km"
    O5 = (filteredDf["ps19QualityOfTravelWas____"].mode())

   

    return [O0, O1, O4, O3, O2, O5, fig, fig2]


# Bootstrap Component
if __name__ == "__main__":
    app.run_server()

# if __name__ == '__main__':
    # app.run_server(debug=True)
