
import dash
from dash import dcc, html, Input, Output, State, dash_table
import pandas as pd
import plotly.graph_objects as go

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

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=10000)
