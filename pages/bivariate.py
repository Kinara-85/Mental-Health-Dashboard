from dash import html, dcc, Input, Output
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


def bivariate_page():
    return dbc.Container([
        dbc.Row([
            dbc.Col([
                html.H1([html.I(className="fas fa-chart-line"), " Bivariate Analysis"],
                        className="text-center mb-4 mt-3",
                        style={'color': '#00d9ff'}),
                html.Hr(style={'borderColor': '#00d9ff', 'borderWidth': '2px'}),
            ], width=12)
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("Analysis Type", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dcc.RadioItems(
                            id='analysis-type',
                            options=[
                                {'label': ' Two Variable Analysis', 'value': 'two_var'},
                                {'label': ' Correlation Heatmap (All Variables)', 'value': 'heatmap'}
                            ],
                            value='two_var',
                            labelStyle={'display': 'block', 'margin': '10px'},
                            style={'fontSize': '1.1rem'}
                        )
                    ])
                ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ], className="mb-4"),
        
        html.Div(id='two-var-controls', children=[
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("X-Axis Variable", style={'color': '#00d9ff'})),
                        dbc.CardBody([
                            dcc.Dropdown(id='bivariate-x', placeholder="Select X variable...", style={'color': 'black'})
                        ])
                    ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
                ], width=6),
                
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Y-Axis Variable", style={'color': '#00d9ff'})),
                        dbc.CardBody([
                            dcc.Dropdown(id='bivariate-y', placeholder="Select Y variable...", style={'color': 'black'})
                        ])
                    ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
                ], width=6)
            ], className="mb-4"),
            
            dbc.Row([
                dbc.Col([
                    dbc.Card([
                        dbc.CardHeader(html.H5("Chart Type", style={'color': '#00d9ff'})),
                        dbc.CardBody([
                            dcc.RadioItems(
                                id='bivariate-chart-type',
                                options=[
                                    {'label': ' Scatter Plot', 'value': 'scatter'},
                                    {'label': ' Bar Chart', 'value': 'bar'},
                                    {'label': ' Grouped Bar Chart', 'value': 'grouped_bar'},  
                                    {'label': ' Stacked Bar Chart', 'value': 'stacked_bar'},
                                    {'label': ' Box Plot', 'value': 'box'},
                                    {'label': ' Violin Plot', 'value': 'violin'},
                                ],
                                value='scatter',
                                labelStyle={'display': 'block', 'margin': '10px'}
                            )
                        ])
                    ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
                ], width=12)
            ], className="mb-4"),
        ]),
        
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        dcc.Loading(id="loading-bivariate", children=dcc.Graph(id='bivariate-plot', style={'height': '600px'}))
                    ])
                ], style={'backgroundColor': 'rgba(0,0,0,0)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                html.Div(id='correlation-info')
            ], width=12)
        ], className="mb-4"),
        
        dbc.Row([
            dbc.Col([
                dbc.Button([html.I(className="fas fa-arrow-left"), " Univariate Analysis"], 
                          href="/univariate", color="primary", size="lg", className="m-2"),
                dbc.Button([html.I(className="fas fa-home"), " Back to Home"], 
                          href="/", color="secondary", size="lg", className="m-2"),
                dbc.Button([html.I(className="fas fa-arrow-right"), " Preprocessing"], 
                          href="/preprocessing", color="success", size="lg", className="m-2")
            ], className="text-center")
        ])
    ], fluid=True)


# Controls visibility
@app.callback(
    Output('two-var-controls', 'style'),
    Input('analysis-type', 'value')
)
def toggle_controls(analysis_type):
    if analysis_type == 'heatmap':
        return {'display': 'none'}
    return {'display': 'block'}


# Dropdown options
@app.callback(
    Output('bivariate-x', 'options'),
    Output('bivariate-y', 'options'),
    Input('stored-data', 'data')
)
def update_bivariate_options(stored_data):
    if stored_data is None:
        return [], []

    try:
        if isinstance(stored_data, str):
            df = pd.read_json(io.StringIO(stored_data), orient='split')
        elif isinstance(stored_data, dict):
            df = pd.DataFrame(stored_data)
        else:
            return [], []
        
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options
        
    except Exception as e:
        print(f"Error loading data: {e}")
        return [], []


# Visualization
@app.callback(
    Output('bivariate-plot', 'figure'),
    Output('correlation-info', 'children'),
    Input('analysis-type', 'value'),
    Input('bivariate-x', 'value'),
    Input('bivariate-y', 'value'),
    Input('bivariate-chart-type', 'value'),
    Input('stored-data', 'data')
)
def update_visualization(analysis_type, x_col, y_col, chart_type, stored_data):
    
    # Initialize info as empty
    info = ""
    
    if stored_data is None:
        fig = go.Figure()
        fig.add_annotation(text="Please upload data first", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""

    try:
        if isinstance(stored_data, str):
            df = pd.read_json(io.StringIO(stored_data), orient='split')
        elif isinstance(stored_data, dict):
            df = pd.DataFrame(stored_data)
        else:
            raise ValueError(f"Unexpected data type: {type(stored_data)}")
            
    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error loading data: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""

    # Heatmap
    if analysis_type == 'heatmap':
        try:
            numeric_df = df.select_dtypes(include=['number'])
            
            if numeric_df.shape[1] < 2:
                fig = go.Figure()
                fig.add_annotation(text="Need at least 2 numeric columns for correlation heatmap", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
                return fig, ""
            
            corr_matrix = numeric_df.corr()
            
            fig = go.Figure(data=go.Heatmap(
                z=corr_matrix.values, 
                x=corr_matrix.columns, 
                y=corr_matrix.columns, 
                colorscale='RdBu', 
                zmid=0, 
                text=corr_matrix.values.round(2), 
                texttemplate='%{text}', 
                textfont={"size": 10}, 
                colorbar=dict(title="Correlation")
            ))
            
            fig.update_layout(
                title="Correlation Heatmap", 
                xaxis_title="Variables", 
                yaxis_title="Variables", 
                plot_bgcolor='rgba(0,0,0,0)', 
                paper_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='white'), 
                height=600
            )
            
            info = dbc.Card([
                dbc.CardHeader(html.H5("📊 Correlation Analysis Info", style={'color': '#00d9ff'})),
                dbc.CardBody([
                    html.P([
                        html.Strong("How to read: "),
                        "Values range from -1 to +1"
                    ]),
                    html.Ul([
                        html.Li("1.0 = Perfect positive correlation (values increase together)"),
                        html.Li("0.0 = No correlation"),
                        html.Li("-1.0 = Perfect negative correlation (one increases, other decreases)"),
                    ]),
                    html.P([
                        html.Strong("Number of numeric variables: "),
                        f"{numeric_df.shape[1]}"
                    ], className="mb-0")
                ])
            ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            
            return fig, info
            
        except Exception as e:
            fig = go.Figure()
            fig.add_annotation(text=f"Error creating heatmap: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            return fig, ""

    if x_col is None or y_col is None:
        fig = go.Figure()
        fig.add_annotation(text="Please select X & Y columns", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""

    try:
        # Scatter
        if chart_type == 'scatter':
            if is_numeric_column(df[x_col]) and is_numeric_column(df[y_col]):
                df_plot = df[[x_col, y_col]].dropna()
                
                if len(df_plot) == 0:
                    fig = go.Figure()
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                    info = ""
                else:
                    fig = px.scatter(df_plot, x=x_col, y=y_col, trendline="ols", title=f"Scatter Plot: {x_col} vs {y_col}")
                    
                    corr = df_plot[[x_col, y_col]].corr().iloc[0, 1]
                    
                    info = dbc.Alert([
                        html.Strong("Correlation Coefficient: "),
                        f"{corr:.3f}",
                        html.Br(),
                        html.Small(f"Strength: {'Strong' if abs(corr) > 0.7 else 'Moderate' if abs(corr) > 0.4 else 'Weak'}")
                    ], color="info")
                
            else:
                fig = go.Figure()
                fig.add_annotation(text="Scatter plot requires both columns to be numeric", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                info = ""

        # Bar
        elif chart_type == 'bar':
            if is_categorical_column(df[x_col]) and is_numeric_column(df[y_col]):
                df_plot = df[[x_col, y_col]].dropna()
                
                if len(df_plot) == 0:
                    fig = go.Figure()
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[x_col] = df_plot[x_col].astype(str)
                    
                    grouped = df_plot.groupby(x_col)[y_col].mean().reset_index()
                    fig = px.bar(grouped, x=x_col, y=y_col, title=f"Bar Chart: {x_col} vs {y_col}")
                    fig.update_traces(marker=dict(line=dict(color='#00d9ff', width=1)))
                info = ""
            else:
                fig = go.Figure()
                fig.add_annotation(text="Bar chart requires X categorical and Y numeric", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                info = ""

        # Grouped Bar Chart (for categorical vs categorical)
        elif chart_type == 'grouped_bar':
            if is_categorical_column(df[x_col]) and is_categorical_column(df[y_col]):
                df_plot = df[[x_col, y_col]].dropna()
                
                if len(df_plot) == 0:
                    fig = go.Figure()
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[x_col] = df_plot[x_col].astype(str)
                    df_plot[y_col] = df_plot[y_col].astype(str)
                    
                    crosstab = pd.crosstab(df_plot[x_col], df_plot[y_col])
                    
                    fig = go.Figure()
                    for col in crosstab.columns:
                        fig.add_trace(go.Bar(
                            name=col,
                            x=crosstab.index,
                            y=crosstab[col],
                            marker=dict(line=dict(color='#00d9ff', width=1))
                        ))
                    
                    fig.update_layout(
                        barmode='group',  # Bars side-by-side
                        title=f"Grouped Bar Chart: {x_col} vs {y_col}",
                        xaxis_title=x_col,
                        yaxis_title="Count"
                    )
                info = ""
            else:
                fig = go.Figure()
                fig.add_annotation(text="Grouped bar chart requires both X and Y to be categorical", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                info = ""

        # Stacked Bar
        elif chart_type == 'stacked_bar':
            if is_categorical_column(df[x_col]) and is_categorical_column(df[y_col]):
                df_plot = df[[x_col, y_col]].dropna()
                
                if len(df_plot) == 0:
                    fig = go.Figure()
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[x_col] = df_plot[x_col].astype(str)
                    df_plot[y_col] = df_plot[y_col].astype(str)
                    
                    crosstab = pd.crosstab(df_plot[x_col], df_plot[y_col])
                    
                    fig = go.Figure()
                    for col in crosstab.columns:
                        fig.add_trace(go.Bar(
                            name=col, 
                            x=crosstab.index, 
                            y=crosstab[col], 
                            marker=dict(line=dict(color='#00d9ff', width=1))
                        ))
                    
                    fig.update_layout(
                        barmode='stack',  # Bars stacked on top
                        title=f"Stacked Bar Chart: {x_col} vs {y_col}", 
                        xaxis_title=x_col, 
                        yaxis_title="Count"
                    )
                info = ""
            else:
                fig = go.Figure()
                fig.add_annotation(text="Stacked bar chart requires both X and Y to be categorical", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                info = ""

        # Box
        elif chart_type == 'box':
            if is_categorical_column(df[x_col]) and is_numeric_column(df[y_col]):
                df_plot = df[[x_col, y_col]].dropna()
                
                if len(df_plot) == 0:
                    fig = go.Figure()
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[x_col] = df_plot[x_col].astype(str)
                    
                    fig = px.box(df_plot, x=x_col, y=y_col, title=f"Box Plot: {x_col} vs {y_col}")
                info = ""
            else:
                fig = go.Figure()
                fig.add_annotation(text="Box plot requires X categorical and Y numeric", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                info = ""

        # Violin
        elif chart_type == 'violin':
            if is_categorical_column(df[x_col]) and is_numeric_column(df[y_col]):
                df_plot = df[[x_col, y_col]].dropna()
                
                if len(df_plot) == 0:
                    fig = go.Figure()
                    fig.add_annotation(text="No data available after removing missing values", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                else:
                    df_plot[x_col] = df_plot[x_col].astype(str)
                    
                    fig = px.violin(df_plot, x=x_col, y=y_col, box=True, title=f"Violin Plot: {x_col} vs {y_col}")
                info = ""
            else:
                fig = go.Figure()
                fig.add_annotation(text="Violin plot requires X categorical and Y numeric", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
                info = ""
        
        else:
            # Unknown chart type
            fig = go.Figure()
            fig.add_annotation(text="Unknown chart type selected", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
            info = ""

        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)', font=dict(color='white'), height=600)
        return fig, info

    except Exception as e:
        fig = go.Figure()
        fig.add_annotation(text=f"Error creating visualization: {str(e)}", xref="paper", yref="paper", x=0.5, y=0.5, showarrow=False, font=dict(color="white", size=16))
        fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
        return fig, ""