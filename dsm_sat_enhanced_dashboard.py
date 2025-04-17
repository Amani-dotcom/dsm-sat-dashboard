
import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import plotly.graph_objects as go
<<<<<<< HEAD

# Load ECCH data automatically (pre-cleaned)
df = pd.read_csv('data.csv')

# Preprocess and classify
mean_usage = df['Consumption'].mean()
df['Persona'] = df['Consumption'].apply(
    lambda x: 'Saver' if x < mean_usage * 0.8 else ('Overconsumer' if x > mean_usage * 1.2 else 'Moderate')
)
persona_counts = df['Persona'].value_counts().to_dict()

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "DSM+SAT | Auto-Loaded ECCH Dashboard"

# Layout
app.layout = html.Div([
    html.H2("DSM+SAT Dashboard – ECCH Energy Insights", style={'textAlign': 'center', 'color': '#0f62fe'}),
    html.Div([
        html.H4("Behavioral Personas Summary"),
        html.P(f"Mean Consumption: {mean_usage:.2f} kWh"),
        html.Ul([html.Li(f"{k}: {v} households") for k, v in persona_counts.items()])
    ], style={'textAlign': 'center'}),

    dcc.Graph(
        id='boxplot',
        figure=go.Figure(
            data=[go.Box(
                y=df[df['Persona'] == persona]['Consumption'],
                name=persona,
                boxpoints='all',
                jitter=0.3,
                marker=dict(size=4),
                line=dict(width=1.5)
            ) for persona in df['Persona'].unique()],
            layout=go.Layout(
                title="Consumption Boxplot by Persona",
                yaxis_title="Monthly Consumption (kWh)",
                template="plotly_white"
            )
        )
    ),

    dcc.Graph(
        id='radar',
        figure=go.Figure(
            data=[
                go.Scatterpolar(
                    r=df['Consumption'].tolist()[:6],
                    theta=df['Location'].tolist()[:6],
                    fill='toself',
                    name='Sample CO₂ Offset'
                )
            ],
            layout=go.Layout(
                polar=dict(radialaxis=dict(visible=True)),
                title="Radar Chart – Simulated CO₂ Offset per Location",
                showlegend=False
            )
        )
    ),

    html.H4("Full Household Data Table"),
    dash_table.DataTable(
        data=df.to_dict('records'),
        page_size=10,
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left'}
    )
])

=======
import io
import base64

# Initialize Dash app
app = dash.Dash(__name__)
app.title = "DSM+SAT Advanced Dashboard"

# App layout
app.layout = html.Div([
    html.H2("DSM+SAT | Enhanced DSM Analytics with Satellite Intelligence", style={'textAlign': 'center', 'color': '#0f62fe'}),
    
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            '📁 Drag and Drop or ',
            html.A('Select ECCH CSV File')
        ]),
        style={
            'width': '95%',
            'height': '80px',
            'lineHeight': '80px',
            'borderWidth': '2px',
            'borderStyle': 'dashed',
            'borderRadius': '10px',
            'textAlign': 'center',
            'margin': '20px auto',
            'backgroundColor': '#f0f4ff'
        },
        multiple=False
    ),
    html.Div(id='file-info', style={'textAlign': 'center', 'marginBottom': 20}),
    dcc.Loading(html.Div(id='output-graphs'), type="circle")
])

# Parse uploaded content and generate visualizations
@app.callback(
    [Output('file-info', 'children'),
     Output('output-graphs', 'children')],
    Input('upload-data', 'contents'),
    State('upload-data', 'filename')
)
def update_output(contents, filename):
    if contents is None:
        return "", ""

    content_type, content_string = contents.split(',')
    decoded = base64.b64decode(content_string)
    try:
        df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
    except Exception as e:
        return "Error reading file. Ensure it is a CSV.", ""

    # Create advanced visuals
    visuals = []

    if 'Cluster' in df.columns and 'Monthly Consumption (kWh)' in df.columns:
        fig_box = go.Figure()
        for cluster in df['Cluster'].unique():
            cluster_data = df[df['Cluster'] == cluster]['Monthly Consumption (kWh)']
            fig_box.add_trace(go.Box(
                y=cluster_data,
                name=cluster,
                boxpoints='all',
                jitter=0.5,
                marker=dict(size=4),
                line=dict(width=1.5)
            ))
        fig_box.update_layout(title="Advanced Boxplot: Monthly Consumption by Cluster",
                              yaxis_title="kWh",
                              template="plotly_white")
        visuals.append(dcc.Graph(figure=fig_box))

    if 'Location' in df.columns and 'CO2 Offset (kg)' in df.columns:
        fig_radar = go.Figure()
        categories = df['Location'].tolist()[:6]
        values = df['CO2 Offset (kg)'].tolist()[:6]
        fig_radar.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name='CO₂ Offset'
        ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True)),
            title="CO₂ Offset (Radar Chart)",
            showlegend=False,
            template="seaborn"
        )
        visuals.append(dcc.Graph(figure=fig_radar))

    # Behavioral analytics summary
    summary = df.describe().to_dict()
    sample_size = len(df)
    mean_usage = df['Consumption'].mean()
    df['Persona'] = df['Consumption'].apply(
        lambda x: 'Saver' if x < mean_usage * 0.8 else ('Overconsumer' if x > mean_usage * 1.2 else 'Moderate'))

    persona_counts = df['Persona'].value_counts().to_dict()

    visuals.insert(0, html.Div([
        html.H4(f"Summary for {filename} (records: {sample_size})"),
        html.P(f"Mean Consumption: {mean_usage:.2f} kWh"),
        html.Ul([html.Li(f"{k}: {v} users") for k, v in persona_counts.items()]),
        dash_table.DataTable(data=df.to_dict('records'), page_size=5, style_table={'overflowX': 'auto'})
    ]))

    return f"File uploaded: {filename}", visuals

# Run the app
>>>>>>> 702fc4f1d738e178e43c587431a289cce9159ed1
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
