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
import dash_uploader as du
import uuid

import logging
import os

import dash_bootstrap_components as dbc
from lib.HysysCSV2DPV import csv2dpv
from lib.util import delete_folder


DOWNLOAD_DIRECTORY = "../downloads"
UPLOAD_DIRECTORY = "../uploads"
LOG_DIRECTORY = "../log"

if not os.path.exists(DOWNLOAD_DIRECTORY):
    os.makedirs(DOWNLOAD_DIRECTORY)

if not os.path.exists(LOG_DIRECTORY):
    os.makedirs(LOG_DIRECTORY)
    with open(LOG_DIRECTORY+'/app.log', 'w') as fp:
        pass

logging.basicConfig(filename=LOG_DIRECTORY+'/app.log', format='%(asctime)s  %(levelname)s:  %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

# Normally, Dash creates its own Flask server internally. By creating our own,
# we can create a route for downloading files directly:
server = Flask(__name__)
app = dash.Dash(server=server, external_stylesheets=[dbc.themes.BOOTSTRAP])
du.configure_upload(app, UPLOAD_DIRECTORY)


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


@server.route("/log")
def readlog():
    with open(LOG_DIRECTORY + '/app.log', 'r') as f:
        return f.read().replace('\n','<br>')

app.layout = html.Div(
    [
        dbc.NavbarSimple(    
            brand="Clound Computation",
            brand_href="#",
            color="dark",
            dark=True,
        ),
        dbc.Container([
            html.H1("HYSYS CSV to DPV File Conversion"),
            html.H2("Upload"),
            du.Upload(
                id="dash-uploader",
                max_file_size=1800,  # 1800 Mb
                filetypes=['csv'],
                max_files=1,
                upload_id=uuid.uuid1(),  # Unique session id
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

@du.callback(
    Output("file-list", "children"),
    id='dash-uploader',
)
def process_csv(filenames):
    """Save uploaded files and regenerate the file list."""
    print(filenames)
    SUCCESS = False
    zipfile = None
    try:
        zipfile = csv2dpv(filenames[0])
        SUCCESS = True
    except Exception as e:
        logging.error(str(e))
        zipfile = e
            
    if SUCCESS:
        return [html.Li(file_download_link(zipfile))]
    elif zipfile:
        return [html.Li('File Read ERROR: please check your file format'), html.Li(str(zipfile))]
    else:
        return [html.Li("No file uploaded yet!")]


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True, host='0.0.0.0', port=3800)