import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import re


colorSet = {
    "open" : 'MediumSeaGreen',
    "development": 'Yellow',
    'not-operational': 'LightGrey',
    'bus':  'DodgerBlue',
    'truck': 'Navy',
    'truckstop': 'Red',
    'transithub': 'Pink'
}

nameSet = {
    "open" : 'Open Station',
    "development": 'In Devolopment',
    'not-operational': 'Not Operational',
    'bus':  'Bus',
    'truck': 'Truck',
    'truckstop': 'Truck Stop',
    'transithub': 'Transit Hub'
}


def generateFilter(defaultFilter):
    filter = dcc.Dropdown(
        id = "map-filter",
        options=[
            {'label': 'Open Station', 'value': 'open'},
            # {'label': 'Retail: Limited', 'value': 'limited'},
            {'label': 'In Devolopment', 'value': 'development'},
            {'label': 'Not Operational', 'value': 'not-operational'},
            {'label': 'Bus', 'value': 'bus'},
            {'label': 'Truck', 'value': 'truck'},
            {'label': 'Truck Stop', 'value': 'truckstop'},
            {'label': 'Transit Hub', 'value': 'transithub'},
        ],
        multi=True,
        value=defaultFilter,
    )  
    return filter




def generateMap(stationInfo, typeList, selected):
    lat0 = (max(stationInfo['lat']) + min(stationInfo['lat']))/2
    lon0 = (max(stationInfo['lon']) + min(stationInfo['lon']))/2

    traces = []
    alldata = []

    for Type in selected:
        trace = go.Scattermapbox(
            lat=stationInfo['lat'][typeList[Type]],
            lon=stationInfo['lon'][typeList[Type]],
            mode="markers",
            name=nameSet[Type],
            marker = dict(
                    size=20,
                    color=colorSet[Type],
                ),
            hovertext=stationInfo['name'][typeList[Type]],
            hoverinfo = "text",

        )
        traces.append(trace)
        alldata.extend(typeList[Type])

    tracebg = go.Scattermapbox(
        lat=stationInfo['lat'][alldata],
        lon=stationInfo['lon'][alldata],
        mode="markers",
        marker = dict(
                size=25,
                color='black',
            ),
        hoverinfo = "none",
        showlegend = False,
    )


    
    layout = go.Layout(
        mapbox_style="open-street-map",
        margin={"r":0,"t":0,"l":0,"b":0},
        mapbox = dict(
            zoom=5,
            center=dict(lat=lat0,lon=lon0),
            pitch=0,
            style='light'
        ),
        legend=dict(
            bgcolor="#1f2c56",
            orientation="v",
            font=dict(color="white"),
            x=0,
            y=0,
            yanchor="bottom",
        ),
    )
    return go.Figure(data=[tracebg, *traces], layout=layout)



def filterCell(content):
    content = re.sub(r'<div(.*?)</div>', '', content)
    link = re.search(r'"(http://.*?)"(.*?)>(.*?)<', content)
    if link:
        content = html.A(link.group(3), href=link.group(1))

    return content


def makeDashTable(data, Id=None):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []

    for i in range(len(data)):
        el = html.Td(filterCell(data[i]))
        if i%2:
            html_row.append(el)
            table.append(html.Tr(html_row))
        else:
            html_row = [el]
        
    
    return html.Table(table, id = Id)


def makeFlexTable(data, Id = None):
    """ Return a dash definition of an HTML table for a Pandas dataframe """
    table = []

    for i in range(len(data)):
        if i>=8:
            break

        if i%2:
            continue
        cell = html.Table(html.Tr(
            children = [
                html.Td(filterCell(data[i])),
                html.Td(html.Div('Online', style={"background-color":"green"})),
            ],
        ))
        table.append(cell)


                
    return html.Div(children = table, id = Id, 
        style={"display":"flex", "flex-wrap":"wrap","justify-content": "center"})


def generateModal():
    return html.Div(
        id="markdown",
        className="modal",
        children=(
            html.Div(
                id="markdown-container",
                className="markdown-container",
                children=[
                    html.Div(
                        className="close-container",
                        children=html.Button(
                            "Close",
                            id="markdown_close",
                            n_clicks=0,
                            className="closeButton",
                        ),
                    ),
                    html.Div(
                        className="markdown-text",
                        children=dcc.Markdown(
                            children=(
                                """
                                    MODAL TEST!!!!!
                                """
                            )
                        ),
                    ),
                ],
            )
        ),
    )