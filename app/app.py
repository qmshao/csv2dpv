#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Sun Feb  9 11:38:43 2020

@author: QuanMin
"""
import base64
import os
import io
from urllib.parse import quote as urlquote

from flask import Flask, send_from_directory
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import dash_bootstrap_components as dbc
from lib.HysysCSV2PDV import csv2pdv
from lib.util import delete_folder


DOWNLOAD_DIRECTORY = "../downloads"

if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)


# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])


@server.route("/downloads/<path:path>")
def download(path):
    """Serve a file from the upload directory."""
    return send_from_directory(DOWNLOAD_DIRECTORY, path, as_attachment=True)

@server.route("/list")
def list():
    filelist = uploaded_files()
    return '<br>'.join(filelist)

@server.route("/deleteall")
def deleteall():
    delete_folder(DOWNLOAD_DIRECTORY)
    delete_folder('../data')
    return 'OK'

app.layout = html.Div(
    [
        dbc.NavbarSimple(    
            brand="Clound Computation",
            brand_href="#",
            color="dark",
            dark=True,
        ),
        dbc.Container([
            html.H1("HYSYS CSV to PDV File Conversion"),
            html.H2("Upload"),
            dcc.Upload(
                id="upload-data",
                children=html.Div([
                    'Drag and Drop or ',
                    html.A('Select Files')
                ]),
                style={
                    "width": "100%",
                    "max-width": "600px",
                    "height": "60px",
                    "lineHeight": "60px",
                    "borderWidth": "1px",
                    "borderStyle": "dashed",
                    "borderRadius": "5px",
                    "textAlign": "center",
                    "margin": "10px",
                },
                className="mx-auto",
                multiple=False,
            ),
            html.H2("File List"),
            html.Ul(id="file-list"),
        ])
    ],
    style = {"width": "100%"}
)


def save_file(name, content):
    """Decode and store a file uploaded with Plotly Dash."""
    data = content.encode("utf8").split(b";base64,")[1]
    with open(os.path.join(DOWNLOAD_DIRECTORY, name), "wb") as fp:
        fp.write(base64.decodebytes(data))


def uploaded_files():
    """List the files in the upload directory."""
    files = []
    for filename in os.listdir(DOWNLOAD_DIRECTORY):
        path = os.path.join(DOWNLOAD_DIRECTORY, filename)
        if os.path.isfile(path):
            files.append(filename)
    return files


def file_download_link(filename):
    """Create a Plotly Dash 'A' element that downloads a file from the app."""
    location = "/downloads/{}".format(urlquote(filename))
    return html.A(filename, href=location)


@app.callback(
    Output("file-list", "children"),
    [Input("upload-data", "filename"), Input("upload-data", "contents")],
)
def update_output(filename, contents):
    """Save uploaded files and regenerate the file list."""

    zipfile = None
    if contents:    
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            if '.csv' in filename.lower():
                # Assume that the user uploaded a CSV file
                zipfile = csv2pdv(io.BytesIO(decoded), filename)
        except Exception as e:
            print(e)
            
    if zipfile:
        return [html.Li(file_download_link(zipfile))]
    else:
        return [html.Li("No file uploaded yet!")]

# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=3800)