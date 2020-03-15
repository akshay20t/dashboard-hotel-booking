import os

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import pandas as pd

df = pd.read_csv('hotel_bookings.csv')
available_countries = list(df['country'].unique())
available_countries.pop(6)

def generate_table(dataframe, max_rows=10):
    return html.Table([
        html.Thead(
            html.Tr([html.Th(col) for col in dataframe.columns])
        ),
        html.Tbody([
            html.Tr([
                html.Td(dataframe.iloc[i][col]) for col in dataframe.columns
            ]) for i in range(min(len(dataframe), max_rows))
        ])
    ])

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server

app.layout = html.Div(children=[
    html.Div([html.H1(children='Hotel Bookings')],
             style={'textAlign': 'center',
                    'padding-left': '100px',
                    'padding-right': '100px'
    }),

    html.Div(children='''
        Have you ever wondered when the best time of year to book a hotel room is? Or the optimal length of stay in order to get
        the best daily rate? What if you wanted to predict whether or not a hotel was likely to receive a disproportionately high
        number of special requests?
        This hotel booking dataset can help you explore those questions!
    '''),

    html.Div([
        html.Div(children='''
            This Dashboard represents the data for number of hotel stays in a particular month in a particular country and the
            type of hotel preferred.
        ''')], style={'padding-top': '30px',
                      'padding-bottom': '30px'}),

    html.Div([
        html.Div([
            html.Label('Select Country'),
            dcc.Dropdown(
                id='country',
                options=[{'label': i, 'value': i} for i in available_countries],
                value='PRT'
            )], style={'width': '30%', 'display': 'inline-block', 'padding-left': '100px'}),

        html.Div([
            html.Label('Select Stay Type'),
            dcc.RadioItems(
                id='stay_type',
                options=[{'label': 'Weekend Nights', 'value': 'stays_in_weekend_nights'},
                         {'label': 'Week Nights', 'value': 'stays_in_week_nights'}],
                value='stays_in_weekend_nights')
        ], style={'width': '45%', 'float': 'right', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
            id='graph',
            figure={
                'layout': {
                    'title': 'Graph'
                }
            }
        ),
        html.Label('Year'),
        dcc.Slider(
            id='year-slider',
            min=df['arrival_date_year'].min(),
            max=df['arrival_date_year'].max(),
            marks={str(i): str(i) for i in df['arrival_date_year'].unique()},
            value=df['arrival_date_year'].min(),
        )
        ], style={'width': '80%',
                  'fontSize': '20px',
                  'padding-left': '100px',
                  'padding-right': '100px',
                  'padding-top': '30px',
                  'padding-bottom': '30px',
                  'display': 'inline-block'}),]),


    html.Div(children=[
        html.H4(children='Hotel Bookings Data'),
        generate_table(df)
    ], style={'width':'90%',
              'textAlign': 'center',
              'align': 'center',
              'padding-top': '20px',
              'padding-bottom': '20px',
              'padding-left': '20px',
              'padding-right': '20px',
              }
    )
])


@app.callback(
    Output('graph', 'figure'),
    [Input('country', 'value'),
     Input('stay_type', 'value'),
     Input('year-slider', 'value')])
def update_figure(country_name, stay_type, selected_year):
    filtered_df = df[df.arrival_date_year == selected_year]
    traces = []
    for i in filtered_df.hotel.unique():
        df_by_hotel = filtered_df[filtered_df['hotel'] == i]
        traces.append(dict(
            x=df_by_hotel['arrival_date_month'],
            y=df_by_hotel[df_by_hotel['country']==country_name][stay_type],
            text=df_by_hotel[df_by_hotel['country']==country_name]['country'],
            mode='markers',
            opacity=0.7,
            marker={
                'size': 15,
                'line': {'width': 0.5, 'color': 'white'}
            },
            name=i
        ))

    return {
        'data': traces,
        'layout': dict(
            xaxis={'title': 'Arrival Month'},
                   #'range': ['January', 'December']},
            yaxis={'title': stay_type.replace('_',' '), 'range': [0, 50]},
            #margin={'l': 40, 'b': 40, 't': 10, 'r': 10},
            legend={'x': 1, 'y': 0},
            hovermode='closest',
            transition={'duration': 500},
        )
    }


if __name__ == '__main__':
    app.run_server(debug=True)