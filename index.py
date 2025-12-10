from dash import dcc, html, Input, Output, State, ctx, no_update, callback
import dash_bootstrap_components as dbc
import pandas as pd
import base64, io
from app import app
from pages import home, univariate, bivariate, preprocessing
from data_cleaning import clean_data 

# Validation Layout 
app.validation_layout = html.Div([
    home.home_page(),
    univariate.univariate_page(),
    bivariate.bivariate_page(),
    preprocessing.preprocessing_page(),
])

# Main Layout
app.layout = dbc.Container([
    dcc.Location(id='url', refresh=False),
    dcc.Store(id='stored-data', storage_type='session'),
    dcc.Store(id='stored-filename', storage_type='session'),
    html.Div(id='page-content')
], fluid=True, style={'backgroundColor': '#0a0a0a', 'minHeight': '100vh'})

# Routing
@app.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):
    if pathname == '/univariate':
        return univariate.univariate_page()
    elif pathname == '/bivariate':
        return bivariate.bivariate_page()
    elif pathname == '/preprocessing':
        return preprocessing.preprocessing_page()
    else:
        return home.home_page()

# Upload/Remove Handler
@app.callback(
    Output('stored-data', 'data'),
    Output('stored-filename', 'data'),
    Input('upload-data', 'contents'),
    Input('remove-csv', 'n_clicks'),
    State('upload-data', 'filename'),
    prevent_initial_call=True
)
def handle_upload_remove(contents, remove_clicks, filename):
    triggered = ctx.triggered_id
    
    if triggered == 'remove-csv':
        return None, None
    
    if triggered == 'upload-data' and contents:
        try:
            content_type, content_string = contents.split(',')
            decoded = base64.b64decode(content_string)
            
            try:
                df = pd.read_csv(io.StringIO(decoded.decode('utf-8')))
            except UnicodeDecodeError:
                df = pd.read_csv(io.StringIO(decoded.decode('latin-1')))
            
            if df.empty:
                print("ERROR: Empty CSV file")
                return None, None
            
            if df.shape[0] == 0:
                print("ERROR: CSV has no rows")
                return None, None
            
            if df.shape[1] == 0:
                print("ERROR: CSV has no columns")
                return None, None
            
            # Data Cleaning
            print(f"Raw data loaded: {df.shape[0]} rows × {df.shape[1]} columns")
            df = clean_data(df)
            print(f"Data cleaned: {df.shape[0]} rows × {df.shape[1]} columns")
            
            
            data_json = df.to_json(date_format='iso', orient='split')
            print(f"SUCCESS: Loaded and cleaned {filename} - {df.shape[0]} rows × {df.shape[1]} columns")
            return data_json, filename
            
        except pd.errors.EmptyDataError:
            print("ERROR: CSV file is empty or corrupted")
            return None, None
        except pd.errors.ParserError:
            print("ERROR: Unable to parse CSV file - check file format")
            return None, None
        except Exception as e:
            print(f"ERROR: Unexpected error loading CSV: {str(e)}")
            return None, None
    
    return no_update, no_update

# Update Home Page Display
@app.callback(
    Output('file-status-indicator', 'children'),
    Output('upload-status', 'children'),
    Output('data-display', 'children'),
    Output('data-info-card', 'children'),
    Input('stored-data', 'data'),
    Input('stored-filename', 'data'),
    Input('url', 'pathname')
)
def update_home_display(stored_data, stored_filename, pathname):
    """Update all home page elements when data changes or page loads"""
    
    if pathname != '/':
        return no_update, no_update, no_update, no_update
    
    if stored_data is None:
        no_data_message = dbc.Alert([
            html.I(className="fas fa-info-circle me-2"),
            html.Strong("No data loaded. "),
            "Please upload a CSV file above to begin your analysis."
        ], color="info", className="mt-3")
        return "", no_data_message, "", ""
    
    try:
        # Load DataFrame from JSON string
        df = pd.read_json(io.StringIO(stored_data), orient='split')
        filename = stored_filename if stored_filename else "dataset.csv"
        
        missing_count = df.isnull().sum().sum()
        missing_pct = (missing_count / (df.shape[0] * df.shape[1])) * 100
        
        # File Indicator
        file_indicator = dbc.Alert([
            html.I(className="fas fa-file-csv me-2", style={'fontSize': '1.5rem'}),
            html.Strong("File Loaded: "),
            dbc.Badge(filename, color="light", text_color="dark", className="ms-2 me-2", style={'fontSize': '1rem'}),
            html.Span(f"({len(df)} rows × {len(df.columns)} columns)")
        ], color="success", className="d-flex align-items-center", style={'fontSize': '1.1rem'})
        
        # Status Message
        status_content = [
            html.I(className="fas fa-check-circle me-2"),
            f"Successfully loaded ",
            dbc.Badge(filename, color="light", text_color="primary", className="mx-2"),
            f"with {len(df)} rows and {len(df.columns)} columns"
        ]
        
        if missing_pct > 10:
            status_content.extend([
                html.Br(),
                html.I(className="fas fa-exclamation-triangle me-2", style={'color': '#ffc107'}),
                html.Small(f"Note: Dataset contains {missing_pct:.1f}% missing values. Consider preprocessing.")
            ])
        
        status = dbc.Alert(status_content, color="success")
        
        # Data Info Card
        int_cols = len(df.select_dtypes(include=['int', 'int32', 'int64', 'Int64']).columns)
        float_cols = len(df.select_dtypes(include=['float', 'float64']).columns)
        obj_cols = len(df.select_dtypes(include=['object']).columns)
        cat_cols = len(df.select_dtypes(include=['category']).columns)
        bool_cols = len(df.select_dtypes(include=['bool']).columns)
        
        missing_data = df.isnull().sum()
        missing_data = missing_data[missing_data > 0].sort_values(ascending=False)
        
        data_info_card = dbc.Card([
            dbc.CardHeader(html.H5("📋 Dataset Information", style={'color': '#00d9ff'})),
            dbc.CardBody([
                dbc.Row([
                    dbc.Col([
                        html.H6("📊 Data Types:", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                        html.P([html.I(className="fas fa-hashtag me-2"), html.Strong("Integer: "), f"{int_cols} columns"]),
                        html.P([html.I(className="fas fa-sort-numeric-up me-2"), html.Strong("Float: "), f"{float_cols} columns"]),
                        html.P([html.I(className="fas fa-tag me-2"), html.Strong("Categorical: "), f"{cat_cols} columns"]),
                        html.P([html.I(className="fas fa-font me-2"), html.Strong("Object: "), f"{obj_cols} columns"]),
                        html.P([html.I(className="fas fa-check-square me-2"), html.Strong("Boolean: "), f"{bool_cols} columns"]),
                    ], width=6),
                    dbc.Col([
                        html.H6("⚠️ Missing Values:", style={'color': '#00d9ff', 'marginBottom': '15px'}),
                        html.Div([
                            html.P([
                                html.Strong(f"{col}: "),
                                f"{count} ",
                                dbc.Badge(f"{count/len(df)*100:.1f}%", color="warning", className="ms-2")
                            ], style={'marginBottom': '8px'})
                            for col, count in missing_data.head(10).items()
                        ]) if len(missing_data) > 0 else html.Div([
                            html.I(className="fas fa-check-circle me-2", style={'color': '#00ff00', 'fontSize': '1.5rem'}),
                            html.P("No missing values detected!", style={'color': '#00ff00', 'fontWeight': 'bold', 'display': 'inline'})
                        ])
                    ], width=6)
                ])
            ])
        ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'}, className="mt-3")
        
        # Data Preview
        preview_df = df.head(5)
        if df.shape[1] > 10:
            preview_df = preview_df.iloc[:, :10]
            column_note = html.Small(
                f"Showing first 10 of {df.shape[1]} columns",
                className="text-muted ms-2"
            )
        else:
            column_note = ""
        
        table = dbc.Card([
            dbc.CardHeader([
                html.H5("Dataset Preview (First 5 Rows)", 
                       style={'color': '#00d9ff', 'display': 'inline-block'}),
                dbc.Badge(filename, color="info", className="ms-3"),
                dbc.Badge(f"{df.shape[0]} rows", color="secondary", className="ms-2"),
                dbc.Badge(f"{df.shape[1]} columns", color="secondary", className="ms-2"),
                column_note
            ]),
            dbc.CardBody([
                html.Div([
                    dbc.Table.from_dataframe(preview_df, striped=True, bordered=True, hover=True, className="table-dark")
                ], style={'overflowX': 'auto', 'maxWidth': '100%'})
            ])
        ], style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
        
        return file_indicator, status, table, data_info_card
        
    except pd.errors.EmptyDataError:
        error_alert = dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            html.Strong("Error: "),
            "The uploaded file appears to be empty. Please upload a valid CSV file."
        ], color="danger")
        return "", error_alert, "", ""
        
    except ValueError as e:
        error_alert = dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            html.Strong("Data Error: "),
            f"Unable to process the data. {str(e)}"
        ], color="danger")
        return "", error_alert, "", ""
        
    except Exception as e:
        error_alert = dbc.Alert([
            html.I(className="fas fa-times-circle me-2"),
            html.Strong("Unexpected Error: "),
            "Something went wrong while processing your file. Please try uploading again."
        ], color="danger")
        print(f"Error in update_home_display: {e}")
        return "", error_alert, "", ""

# Run
if __name__ == '__main__':
    run_server(debug=False, host='0.0.0.0', port=8000)