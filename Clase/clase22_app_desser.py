import dash
from dash import dcc  # dash core components
from dash import html # dash html components
from dash.dependencies import Input, Output
from pgmpy.readwrite import BIFReader
from pgmpy.inference import VariableElimination

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# Read model from BIF file 
reader = BIFReader("monty.bif")
modelo = reader.get_model()

# Infering the posterior probability
infer = VariableElimination(modelo)


app.layout = html.Div(
    [
    html.H6("Ingrese las puertas seleccionadas por el Jugador y por el Animador"),
    html.Div(["Puerta seleccionada por el Jugador: ",
              dcc.Dropdown(id='puerta-jugador', value='1', options=['1', '2', '3'])]),
    html.Br(),
    html.Div(["Puerta seleccionada por el Animador (diferente a la seleccionada por el Jugador): ",
              dcc.Dropdown(id='puerta-animador', value='2', options=['1', '2', '3'])]),
    html.Br(),
    html.H6("Probabilidad de que el carro esté detrás de cada puerta:"),
    html.Br(),
    html.Div(["Puerta 1:", html.Div(id='output-p1')]),
    html.Div(["Puerta 2:", html.Div(id='output-p2')]),
    html.Div(["Puerta 3:", html.Div(id='output-p3')]),
    ]
)


@app.callback(
    Output(component_id='output-p1', component_property='children'),
    Output(component_id='output-p2', component_property='children'),
    Output(component_id='output-p3', component_property='children'),
    [Input(component_id='puerta-jugador', component_property='value'), 
     Input(component_id='puerta-animador', component_property='value')]
)
def update_output_div(puerta_jugador, puerta_animador ):
    # Check inputs are correct 
    if int(puerta_jugador) - int(puerta_animador) != 0:
        posterior_p = infer.query(["C"], evidence={"U": str(int(puerta_jugador)-1), "A": str(int(puerta_animador)-1)})
        print(posterior_p.values)

        return '{}'.format(posterior_p.values[0]), '{}'.format(posterior_p.values[1]), '{}'.format(posterior_p.values[2])
    
    return 0,0,0


if __name__ == '__main__':
    app.run_server(debug=True)
