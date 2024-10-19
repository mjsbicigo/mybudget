import dash
import dash_bootstrap_components as dbc
from flask import Flask
from .config import Settings

estilos = ["https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css", 
           "https://fonts.googleapis.com/icon?family=Material+Icons"
           "https://use.fontawesome.com/releases/v5.10.2/css/all.css",
           dbc.themes.QUARTZ,
           "https://cdn.jsdelivr.net/gh/AnnMarieW/dash-bootstrap-templates@V1.0.4/dbc.min.css",
           "assets/css/styles.css"]

flask_server = Flask(__name__)
flask_server.config.from_object(Settings)

#Dash
app = dash.Dash(__name__, prevent_initial_callbacks="initial_duplicate", external_stylesheets=estilos, server=flask_server)
app.config['suppress_callback_exceptions'] = True