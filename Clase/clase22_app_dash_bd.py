import dash
from dash import dcc  # dash core components
from dash import html  # dash html components
from dash.dependencies import Input, Output
import psycopg2
from dotenv import load_dotenv
import os

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# path to env file
env_path = 'env\\app.env'
# load env
load_dotenv(dotenv_path=env_path)
# extract env variables
USER = os.getenv('USER')
PASSWORD = os.getenv('PASSWORD')
HOST = os.getenv('HOST')
PORT = os.getenv('PORT')
DBNAME = os.getenv('DBNAME')

# connect to DB
engine = psycopg2.connect(
    dbname=DBNAME,
    user=USER,
    password=PASSWORD,
    host=HOST,
    port=PORT
)

cursor = engine.cursor()


app.layout = html.Div(
    [
        html.H6("Seleccione un continente"),
        html.Div(["Continente: ",
                  dcc.Dropdown(id='continente', value='Africa',
                               options=['Africa', 'Antarctica', 'Asia', 'Europe', 'North America', 'Oceania', 'South America'])]),
        html.Br(),
        html.Br(),
        html.H6("Estadísticas:"),
        html.Br(),
        html.Div(["Superficie promedio (km^2):", html.Div(id='output-sup')]),
        html.Div(["Población promedio:", html.Div(id='output-pob')]),
    ]
)


@app.callback(
    Output(component_id='output-sup', component_property='children'),
    Output(component_id='output-pob', component_property='children'),
    Input(component_id='continente', component_property='value')
)
def update_output_div(continente):
    query = """
    select avg(surface_area) as surface
    from country
    group by continent
    having continent='{}';""".format(continente)
    cursor.execute(query)
    result = cursor.fetchall()
    print(result[0][0])
    surface = result[0][0]

    query = """
    select avg(population) as pop
    from country
    group by continent
    having continent='{}';""".format(continente)
    cursor.execute(query)
    result = cursor.fetchall()
    print(result[0][0])
    pop = result[0][0]

    return '{:.2f}'.format(surface), '{:.2f}'.format(pop)


if __name__ == '__main__':
    app.run_server(debug=True)
