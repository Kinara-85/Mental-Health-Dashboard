import dash
from dash import dcc, html
import dash_bootstrap_components as dbc

dash.register_page(__name__, path="/")   

def home_page():
    return dbc.Container([
        # Header
        dbc.Row([
            dbc.Col([
                html.Div([
                    html.H1("🧠 Mental Health in Tech Survey 2014",
                            className="text-center mb-3 mt-5",
                            style={'color': '#00d9ff', 'fontWeight': 'bold'}),
                    html.P("Data Science Dashboard for Mental Health Analysis",
                           className="text-center text-muted mb-4",
                           style={'fontSize': '1.2rem'})
                ])
            ], width=12)
        ]),

        html.Hr(style={'borderColor': '#00d9ff', 'borderWidth': '2px'}),

        # Business Use Case
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H3("📊 Business Use Case", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        html.H4("Overview", style={'color': '#00d9ff', 'marginBottom': '15px', 'fontWeight': '600'}),
                        html.P([
                            "This dashboard provides comprehensive analytics on mental health patterns within the technology sector, ",
                            "leveraging the OSMI Mental Health in Tech Survey 2014 dataset. The platform enables data-driven ",
                            "decision-making for HR professionals, organizational leaders, and mental health advocates working to ",
                            "improve workplace wellbeing in tech companies."
                        ], style={'fontSize': '1.05rem', 'marginBottom': '25px', 'lineHeight': '1.6'}),
                        
                        html.H4("Key Objectives", style={'color': '#00d9ff', 'marginBottom': '15px', 'fontWeight': '600'}),
                        html.Ol([
                            html.Li("Predict Mental Health Treatment Needs Using Machine Learning Models",
                                    style={'marginBottom': '10px', 'fontSize': '1.05rem'}),
                            html.Li("Identify Critical Workplace Risk Factors and Policy Gaps",
                                    style={'marginBottom': '10px', 'fontSize': '1.05rem'}),
                            html.Li("Visualize Mental Health Patterns Across Demographics",
                                    style={'marginBottom': '10px', 'fontSize': '1.05rem'}),
                            html.Li("Optimize Mental Health Resource Allocation and Investments",
                                    style={'marginBottom': '10px', 'fontSize': '1.05rem'}),
                            html.Li("Enable Interactive Data-Driven Decision Making",
                                    style={'marginBottom': '10px', 'fontSize': '1.05rem'}),
                        ], style={'paddingLeft': '20px'}),
                    ])
                ], className="mb-4",
                   style={'backgroundColor': 'rgba(0, 217, 255, 0.1)',
                          'border': '1px solid #00d9ff'})
            ], width=12)
        ]),

        # Upload Section 
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(
                        html.H3("📁 Upload Dataset", style={'color': '#00d9ff'})
                    ),
                    dbc.CardBody([
                        # File status indicator 
                        html.Div(id='file-status-indicator', className="mb-3"),
                        
                        dcc.Upload(
                            id='upload-data',
                            children=html.Div([
                                html.I(className="fas fa-cloud-upload-alt", style={'fontSize': '2rem'}),
                                html.Br(),
                                'Drag and Drop or ',
                                html.A('Select CSV File',
                                       style={'color': '#00d9ff', 'fontWeight': 'bold'})
                            ]),
                            style={
                                'width': '100%',
                                'height': '100px',
                                'lineHeight': '100px',
                                'borderWidth': '3px',
                                'borderStyle': 'dashed',
                                'borderRadius': '15px',
                                'textAlign': 'center',
                                'backgroundColor': 'rgba(0, 217, 255, 0.05)',
                                'borderColor': '#00d9ff',
                                'cursor': 'pointer',
                                'marginBottom': '20px'
                            },
                            multiple=False
                        ),

                        html.Div(id='upload-status', className="mb-3"),
                        
                        # Remove CSV button 
                        dbc.Button(
                            [html.I(className="fas fa-trash-alt me-2"), "Remove CSV"],
                            id='remove-csv',
                            n_clicks=0,
                            color="danger",
                            size="lg",
                            style={'width': '200px'}
                        )
                    ])
                ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)',
                          'border': '1px solid #00d9ff'})
            ], width=12)
        ], className="mb-4"),

        # Data info card
        dbc.Row([
            dbc.Col([
                html.Div(id='data-info-card')  
            ], width=12)
        ], className="mb-4"),

        
        dbc.Row([
            dbc.Col([
                html.Div(id='data-display')
            ], width=12)
        ]),

        # Navigation Buttons 
        dbc.Row([
            dbc.Col([
                html.H4("🚀 Get Started with Analysis", className="text-center mb-3", style={'color': '#00d9ff'}),
                dbc.ButtonGroup([
                    dbc.Button(
                        [html.I(className="fas fa-chart-bar"), " Univariate Analysis"],
                        href="/univariate",
                        color="primary",
                        size="lg",
                        className="m-2"
                    ),
                    dbc.Button(
                        [html.I(className="fas fa-chart-line"), " Bivariate Analysis"],
                        href="/bivariate",
                        color="info",
                        size="lg",
                        className="m-2"
                    ),
                    dbc.Button(
                        [html.I(className="fas fa-cogs"), " Preprocessing Pipeline"],
                        href="/preprocessing",
                        color="success",
                        size="lg",
                        className="m-2"
                    )
                ], className="d-flex justify-content-center")
            ], width=12, className="text-center mt-5 mb-5")
        ])
    ], fluid=True)

layout = home_page()