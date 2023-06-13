import dash
from dash import dcc
from dash import html
import numpy as np
import plotly.graph_objects as go
import pandas

from database import fetch_all_data_as_df

# Definitions of constants. This projects uses extra CSS stylesheet at `./assets/style.css`
COLORS = ['rgb(67,67,67)', 'rgb(115,115,115)', 'rgb(49,130,189)', 'rgb(189,189,189)']
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css', '/assets/style.css']

# Define the dash app first
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# Define component functions
def page_header():
    """
    Returns the page header as a dash `html.Div`
    """
    return html.Div(id='header', children=[
        html.Div([html.H3('Visualization with datashader and Plotly')],
                 className="ten columns"),
    ], className="row")


def description():
    """
    Returns overall project description in markdown
    """
    return html.Div(children=[dcc.Markdown('''
        # Covid Dashboard
        Since 2020, there have been over 50 million recorded Covid-19 cases in the United States.
        While vaccinations and public safety measures have greatly reduced the spread and impact of 
        covid on daily life, new variants and surges mean that continued testing and vigiliance is called for.

        Most cases currently are asymptotic and minor, meaning that contagious individuals may not get tested.
        This is why reported case counts are not accurate representations of the actual spread of covid within a
        region.

        **This Covid Dashboard estimates the actual prevalence of covid in different states.**
        It can be used to see the new and probable new cases in different areas over time.

        ### Data Source
        This dashboard utilizes case data from the [Centers for Disease Control and Prevention]
        (https://www.cdc.gov/). \n
        The [data source](https://data.cdc.gov/Case-Surveillance/United-States-COVID-19-Cases-and-Deaths-by-State-o/9mfq-cb36) 
        **updates twice every 24 hours**. 
        ''', className='eleven columns', style={'paddingLeft': '5%'})], className="row")


def covid_per_cap(state):
    df = fetch_all_data_as_df(state.lower())
    if df is None:
        return go.Figure()
    
    df['per_new_cases'] = (df['new_case']/df['tot_cases'])

    fig = go.Figure(data=[go.Table(
        header=dict(values=['state', 'total cases', 'new cases', 'per new cases', 'date'],
                    fill_color='paleturquoise',
                    align='left'),
        cells=dict(values=[df.state, df.tot_cases, df.new_case, df.per_new_cases, df.date],
                   fill_color='lavender',
                   align='left'))
    ])
    
    return fig

def covid_tool():
    """
    Returns the covid dashboard tool as a dash `html.Div`. 
    """
    return html.Div(children=[
        html.Div(children=[dcc.Graph(id='cases-figure')], className='nine columns'),

        html.Div(children=[
            html.H5("State/Region:", style={'marginTop': '2rem'}),
            html.Div(children=[
                dcc.Dropdown(
                    id='state-dropdown',
                    options=[
                        {'label': 'Alabama', 'value': 'AL'},
                        {'label': 'Alaska', 'value': 'AK'},
                        {'label': 'American Samoa', 'value': 'AS'},
                        {'label': 'Arizona', 'value': 'AZ'},
                        {'label': 'Arkansas', 'value': 'AR'},
                        {'label': 'California', 'value': 'CA'},
                        {'label': 'Colorado', 'value': 'CO'},
                        {'label': 'Connecticut', 'value': 'CT'},
                        {'label': 'Delaware', 'value': 'DE'},
                        {'label': 'District of Columbia', 'value': 'DC'},
                        {'label': 'Florida', 'value': 'FL'},
                        {'label': 'Federated States of Micronesia', 'value': 'FSM'},
                        {'label': 'Georgia', 'value': 'GA'},
                        {'label': 'Guam', 'value': 'GU'},
                        {'label': 'Hawaii', 'value': 'HI'},
                        {'label': 'Idaho', 'value': 'ID'},
                        {'label': 'Illinois', 'value': 'IL'},
                        {'label': 'Indiana', 'value': 'IN'},
                        {'label': 'Iowa', 'value': 'IA'},
                        {'label': 'Kansas', 'value': 'KS'},
                        {'label': 'Kentucky', 'value': 'KY'},
                        {'label': 'Louisiana', 'value': 'LA'},
                        {'label': 'Maine', 'value': 'ME'},
                        {'label': 'Maryland', 'value': 'MD'},
                        {'label': 'Massachusetts', 'value': 'MA'},
                        {'label': 'Michigan', 'value': 'MI'},
                        {'label': 'Minnesota', 'value': 'MN'},
                        {'label': 'Mississippi', 'value': 'MS'},
                        {'label': 'Missouri', 'value': 'MO'},
                        {'label': 'Montana', 'value': 'MT'},
                        {'label': 'Nebraska', 'value': 'NE'},
                        {'label': 'Nevada', 'value': 'NV'},
                        {'label': 'New Hampshire', 'value': 'NH'},
                        {'label': 'New Jersey', 'value': 'NJ'},
                        {'label': 'New Mexico', 'value': 'NM'},
                        {'label': 'New York', 'value': 'NY'},
                        {'label': 'New York City', 'value': 'NYC'},
                        {'label': 'North Carolina', 'value': 'NC'},
                        {'label': 'North Dakota', 'value': 'ND'},
                        {'label': 'Northern Mariana Islands', 'value': 'MP'},
                        {'label': 'Ohio', 'value': 'OH'},
                        {'label': 'Oklahoma', 'value': 'OK'},
                        {'label': 'Oregon', 'value': 'OR'},
                        {'label': 'Palau', 'value': 'PW'},
                        {'label': 'Pennsylvania', 'value': 'PA'},
                        {'label': 'Puerto Rico', 'value': 'PR'},
                        {'label': 'Rhode Island', 'value': 'RI'},
                        {'label': 'Republic of the Marshall Islands', 'value': 'RMI'},
                        {'label': 'South Carolina', 'value': 'SC'},
                        {'label': 'South Dakota', 'value': 'SD'},
                        {'label': 'Tennessee', 'value': 'TN'},
                        {'label': 'Texas', 'value': 'TX'},
                        {'label': 'Utah', 'value': 'UT'},
                        {'label': 'Vermont', 'value': 'VT'},
                        {'label': 'Virgin Islands', 'value': 'VI'},
                        {'label': 'Virginia', 'value': 'VA'},
                        {'label': 'Washington', 'value': 'WA'},
                        {'label': 'West Virginia', 'value': 'WV'},
                        {'label': 'Wisconsin', 'value': 'WI'},
                        {'label': 'Wyoming', 'value': 'WY'}
                    ],
                    value="NYC"
                )
            ], style={'marginTop': '1rem'}),

            html.Div(id='state-text', style={'marginTop': '1rem'}),

        ], className='three columns', style={'marginLeft': 5, 'marginTop': '10%'}),
    ], className='row eleven columns')


def architecture_summary():
    """
    Returns the text and image of architecture summary of the project.
    """
    return html.Div(children=[
        dcc.Markdown('''
            # Project Architecture
            This project uses MongoDB as the database. All data acquired are stored in raw form to the
            database. An abstract layer is built in `database.py` so all queries can be done via function call.
            For a more complicated app, the layer will also be responsible for schema consistency. 
            A `plot.ly` & `dash` app is serving this web page through. Actions on responsive components
            on the page is redirected to `app.py` which will then update certain components on the page.  
        ''', className='row eleven columns', style={'paddingLeft': '5%'}),

        html.Div(children=[
            html.Img(src="https://docs.google.com/drawings/d/e/2PACX-1vQNerIIsLZU2zMdRhIl3ZZkDMIt7jhE_fjZ6ZxhnJ9bKe1emPcjI92lT5L7aZRYVhJgPZ7EURN0AqRh/pub?w=670&amp;h=457",
                     className='row'),
        ], className='row', style={'textAlign': 'center'}),

        dcc.Markdown('''
        
        ''')
    ], className='row')


# Sequentially add page components to the app's layout
def dynamic_layout():
    return html.Div([
        page_header(),
        html.Hr(),
        description(),
        dcc.Graph(id='covid-trend-graph', figure=covid_per_cap('ri')),
        covid_tool(),
        architecture_summary(),

    ], className='row', id='content')


# set layout to a function which updates upon reloading
app.layout = dynamic_layout


# Defines the dependencies of interactive components

@app.callback(
    dash.dependencies.Output('cases-figure', 'figure'),
    [dash.dependencies.Input('state-dropdown', 'value')])
def covid_handler(state):
    """Changes the region of the covid dashboard graph"""
    df = fetch_all_data_as_df(state.lower())
    df = df.sort_values(by='date')
    x = df['date']
    cases = df['new_case']
    pcases = df['pnew_case']

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=cases, mode='none', name='new cases', line={'width': 2, 'color': 'pink'},
                  fill='tozeroy'))
    fig.add_trace(go.Scatter(x=x, y=pcases, mode='none', name='probable cases', line={'width': 2, 'color': 'orange'},
                  fill='tonexty'))
    fig.update_layout(template='plotly_dark', title='New and Probable Cases in ' + state,
                      plot_bgcolor='#23272c', paper_bgcolor='#23272c', yaxis_title='Cases',
                      xaxis_title='Date')
    return fig


if __name__ == '__main__':
    app.run_server(debug=True, port=1050, host='0.0.0.0')
