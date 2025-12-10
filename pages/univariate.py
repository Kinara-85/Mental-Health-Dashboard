from dash import html, dcc, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import io
from app import app


def is_categorical_column(series):
    return pd.api.types.is_categorical_dtype(series) or pd.api.types.is_object_dtype(series) or pd.api.types.is_string_dtype(series)


def is_numeric_column(series):
    return pd.api.types.is_numeric_dtype(series) and not pd.api.types.is_bool_dtype(series)


def univariate_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1([html.I(className="fas fa-chart-bar"), " Univariate Analysis"],
                        className="text-center mb-4 mt-3",
                        style={'color': '#00d9ff'}),
                html.Hr(style={'borderColor': '#00d9ff', 'borderWidth': '2px'}),
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Select Variable", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dcc.Dropdown(id='univariate-column', placeholder="Choose a column to analyze...", style={'color': 'black'})
                    ])
                ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Chart Type", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dcc.RadioItems(
                            id='univariate-chart-type',
                            options=[
                                {'label': ' Histogram', 'value': 'histogram'},
                                {'label': ' Box Plot', 'value': 'box'},
                                {'label': ' Violin Plot', 'value': 'violin'},
                                {'label': ' Bar Chart', 'value': 'bar'},
                                {'label': ' Pie Chart', 'value': 'pie'},
                            ],
                            value='histogram',
                            labelStyle={'display': 'block', 'margin': '10px'},
                            style={'fontSize': '1.1rem'}
                        )
                    ])
                ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=6),
            
            dbc.Col([
                html.Div(id='bins-control', children=[
                    dbc.Card([
                        dbc.CardHeader(html.H5("Number of Bins", style={'color': '#00d9ff'})),
                        dbc.CardBody([
                            dbc.Input(id='histogram-bins', type='number', min=5, max=200, step=1, value=30, placeholder="Enter bins (5-200)", style={'fontSize': '1.2rem', 'textAlign': 'center', 'height': '50px'}),
                            html.Div([
                                html.Small("Min: 5  •  Max: 200  •  Default: 30", 
                                          className="text-muted mt-2", 
                                          style={'display': 'block', 'textAlign': 'center'})
                            ])
                        ])
                    ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
                ])
            ], width=6)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Loading(id="loading-univariate", children=dcc.Graph(id='univariate-plot', style={'height': '600px'}))
                    ])
                ], style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Div(id='univariate-stats')
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Button([html.I(className="fas fa-home"), " Back to Home"], 
                          href="/", color="secondary", size="lg", className="m-2"),
                dbc.Button([html.I(className="fas fa-arrow-right"), " Bivariate Analysis"], 
                          href="/bivariate", color="primary", size="lg", className="m-2"),
                dbc.Button([html.I(className="fas fa-cogs"), " Preprocessing"], 
                          href="/preprocessing", color="success", size="lg", className="m-2")
            ], className="text-center")
        ])
    ], fluid=True)


# Bins control
@app.callback(
    Output('bins-control', 'style'),
    Input('univariate-chart-type', 'value')
)
def toggle_bins_control(chart_type):
    if chart_type == 'histogram':
        return {'display': 'block'}
    return {'display': 'none'}


# Dropdown options
@app.callback(
    Output('univariate-column', 'options'),
    Input('stored-data', 'data')
)
def update_univariate_options(stored_data):
    if stored_data is None:
        return []
    
    try:
        if isinstance(stored_data, str):
            df = pd.read_json(io.StringIO(stored_data), orient='split')
        elif isinstance(stored_data, dict):
            df = pd.DataFrame(stored_data)
        else:
            return []
        
        options = [{'label': col, 'value': col} for col in df.columns]
        return options
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return []


# Plot and stats
@app.callback(
    Output('univariate-plot', 'figure'),
    Output('univariate-stats', 'children'),
    Input('univariate-column', 'value'),
    Input('univariate-chart-type', 'value'),
    Input('histogram-bins', 'value'),
    Input('stored-data', 'data')
)
def update_univariate_plot(column, chart_type, bins, stored_data):
    
    if stored_data is None:
        fig = go.Figure()
        fig.add_annotation(text="Please upload data first", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""
    
    if column is None:
        fig = go.Figure()
        fig.add_annotation(text="Please select a column", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""
    
    try:
        if isinstance(stored_data, str):
            df = pd.read_json(io.StringIO(stored_data), orient='split')
        elif isinstance(stored_data, dict):
            df = pd.DataFrame(stored_data)
        else:
            raise ValueError(f"Unexpected data type: {type(stored_data)}")
        
        if column not in df.columns:
            fig = go.Figure()
            fig.add_annotation(text=f"Column '{column}' not found", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return fig, ""
        
        is_numeric = is_numeric_column(df[column])
        is_categorical = is_categorical_column(df[column])
        
        if bins is None or bins < 5 or bins > 200:
            bins = 30
        
        fig = go.Figure()
        stats_card = None
        
        # Histogram
        if chart_type == 'histogram':
            if is_numeric:
                df_plot = df.dropna(subset=[column])
                
                if len(df_plot) == 0:
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    fig = px.histogram(df_plot, x=column, nbins=bins, title=f"Histogram of {column}")
                    fig.update_traces(marker=dict(line=dict(color='#00d9ff', width=1)))
                
                stats_card = create_numeric_stats_card(df[column], column)
            else:
                fig.add_annotation(text="Histogram requires numeric data. Try Bar Chart or Pie Chart for categorical data.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        
        # Box Plot
        elif chart_type == 'box':
            if is_numeric:
                df_plot = df.dropna(subset=[column])
                
                if len(df_plot) == 0:
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    fig = px.box(df_plot, y=column, title=f"Box Plot of {column}")
                
                stats_card = create_numeric_stats_card(df[column], column)
            else:
                fig.add_annotation(text="Box Plot requires numeric data. Try Bar Chart or Pie Chart for categorical data.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        
        # Violin Plot
        elif chart_type == 'violin':
            if is_numeric:
                df_plot = df.dropna(subset=[column])
                
                if len(df_plot) == 0:
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    fig = px.violin(df_plot, y=column, box=True, title=f"Violin Plot of {column}")
                
                stats_card = create_numeric_stats_card(df[column], column)
            else:
                fig.add_annotation(text="Violin Plot requires numeric data. Try Bar Chart or Pie Chart for categorical data.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        
        # Bar Chart
        elif chart_type == 'bar':
            if is_categorical or not is_numeric:
                df_plot = df[[column]].copy()
                df_plot = df_plot.dropna(subset=[column])
                
                if len(df_plot) == 0:
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[column] = df_plot[column].astype(str)
                    
                    value_counts = df_plot[column].value_counts().reset_index()
                    value_counts.columns = [column, 'Count']
                    
                    fig = px.bar(value_counts, x=column, y='Count', title=f"Bar Chart of {column}")
                    fig.update_traces(marker=dict(line=dict(color='#00d9ff', width=1)))
                
                stats_card = create_categorical_stats_card(df[column], column)
            else:
                df_plot = df.dropna(subset=[column])
                
                if len(df_plot) == 0:
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    fig = px.histogram(df_plot, x=column, nbins=20, title=f"Bar Chart of {column}")
                    fig.update_traces(marker=dict(line=dict(color='#00d9ff', width=1)))
                
                stats_card = create_numeric_stats_card(df[column], column)
        
        # Pie Chart
        elif chart_type == 'pie':
            if is_categorical or not is_numeric:
                df_plot = df[[column]].copy()
                df_plot = df_plot.dropna(subset=[column])
                
                if len(df_plot) == 0:
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[column] = df_plot[column].astype(str)
                    
                    value_counts = df_plot[column].value_counts().reset_index()
                    value_counts.columns = [column, 'Count']
                    
                    fig = px.pie(value_counts, names=column, values='Count', title=f"Pie Chart of {column}")
                
                stats_card = create_categorical_stats_card(df[column], column)
            else:
                fig.add_annotation(text="Pie Chart works best with categorical data. Try Histogram for numeric data.", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=600)
        
        return fig, stats_card if stats_card else ""
        
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error creating visualization: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""


def create_numeric_stats_card(series, column_name):
    series_clean = series.dropna()
    
    if len(series_clean) == 0:
        return dbc.Alert("No valid data available for statistics", color="warning")
    
    stats = {
        'Count': len(series_clean),
        'Mean': series_clean.mean(),
        'Median': series_clean.median(),
        'Std Dev': series_clean.std(),
        'Min': series_clean.min(),
        'Max': series_clean.max(),
        'Q1': series_clean.quantile(0.25),
        'Q3': series_clean.quantile(0.75),
        'Missing': series.isna().sum(),
        'Missing %': (series.isna().sum() / len(series) * 100)
    }
    
    return dbc.Card([
        dbc.CardHeader(html.H5(f"📊 Statistics for {column_name}", style={'color': '#00d9ff'})),
        dbc.CardBody([
            dbc.Row([
                dbc.Col([
                    html.P([html.Strong("Count: "), f"{stats['Count']}"]),
                    html.P([html.Strong("Mean: "), f"{stats['Mean']:.2f}"]),
                    html.P([html.Strong("Median: "), f"{stats['Median']:.2f}"]),
                ], width=4),
                dbc.Col([
                    html.P([html.Strong("Std Dev: "), f"{stats['Std Dev']:.2f}"]),
                    html.P([html.Strong("Min: "), f"{stats['Min']:.2f}"]),
                    html.P([html.Strong("Q1: "), f"{stats['Q1']:.2f}"]),
                ], width=4),
                dbc.Col([
                    html.P([html.Strong("Q3: "), f"{stats['Q3']:.2f}"]),
                    html.P([html.Strong("Max: "), f"{stats['Max']:.2f}"]),
                    html.P([html.Strong("Missing: "), f"{stats['Missing']} ({stats['Missing %']:.1f}%)"]),
                ], width=4)
            ])
        ])
    ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})


def create_categorical_stats_card(series, column_name):
    series_clean = series.dropna()
    
    if len(series_clean) == 0:
        return dbc.Alert("No valid data available for statistics", color="warning")
    
    series_str = series_clean.astype(str)
    value_counts = series_str.value_counts()
    
    missing_count = series.isna().sum()
    missing_pct = (missing_count / len(series) * 100)
    
    return dbc.Card([
        dbc.CardHeader(html.H5(f"📊 Statistics for {column_name}", style={'color': '#00d9ff'})),
        dbc.CardBody([
            html.P([html.Strong("Total Values: "), f"{len(series)}"]),
            html.P([html.Strong("Valid Values: "), f"{len(series_clean)}"]),
            html.P([html.Strong("Unique Categories: "), f"{len(value_counts)}"]),
            html.P([html.Strong("Most Common: "), f"{value_counts.index[0]} ({value_counts.iloc[0]} occurrences)"]),
            html.P([html.Strong("Missing Values: "), f"{missing_count} ({missing_pct:.1f}%)"]),
            html.Hr(),
            html.H6("Category Distribution (Valid Data Only):", style={'color': '#00d9ff'}),
            html.Div([
                html.P(f"{cat}: {count} ({count/len(series_clean)*100:.1f}%)")
                for cat, count in value_counts.head(10).items()
            ])
        ])
    ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})