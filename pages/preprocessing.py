from dash import html, dcc, Input, Output, State
import dash
import dash_bootstrap_components as dbc
import pandas as pd
from sklearn.preprocessing import StandardScaler, MinMaxScaler, LabelEncoder
from sklearn.model_selection import train_test_split
from app import app
import io


# Helper function to safely load DataFrame from stored data
def load_dataframe(data):
    """Load DataFrame from stored data, handling both JSON string and dict/list formats"""
    if isinstance(data, str):
        return pd.read_json(io.StringIO(data), orient='split')
    else:
        return pd.DataFrame(data)


def preprocessing_page():
    return dbc.Container([
        dcc.Store(id='preprocessing-data', storage_type='memory'),
        dcc.Download(id='download-dataframe-csv'),
        
        dbc.Row([
            dbc.Col([
                html.H1([html.I(className="fas fa-cogs"), " Data Preprocessing Pipeline"], 
                       className="text-center mb-4 mt-3",
                       style={'color': '#00d9ff'}),
                html.Hr(style={'borderColor': '#00d9ff', 'borderWidth': '2px'}),
            ], width=12)
        ]),
        
        # Drop Columns Section - NEW
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("1. Drop Columns", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        html.P("Select columns to remove from your dataset:", 
                               className="mb-3", 
                               style={'fontSize': '1rem'}),
                        
                        dcc.Dropdown(
                            id='drop-column-dropdown',
                            multi=True,
                            placeholder="Select columns to drop...",
                            style={'color': 'black'},
                            className="mb-3"
                        ),
                        
                        dbc.Button(
                            [html.I(className="fas fa-trash me-2"), "Drop Selected Columns"],
                            id='drop-columns-btn',
                            n_clicks=0,
                            color="warning"
                        ),
                        
                        html.Div(id='drop-column-status', className="mt-3")
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Missing Values - ENHANCED
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("2. Missing Values", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dbc.Button("Check Missing Values", id='check-missing', color="info", className="mb-3"),
                        html.Div(id='missing-output'),
                        
                        # Missing value handling section
                        html.Div(id='missing-handling-section', children=[
                            html.Hr(),
                            html.H6("Handle Missing Values:", className="mt-3 mb-2", style={'color': '#00d9ff'}),
                            
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='missing-column-select',
                                        placeholder="Select column to handle...",
                                        style={'color': 'black'},
                                        className="mb-2"
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='missing-method-select',
                                        options=[
                                            {'label': 'Drop Rows', 'value': 'drop'},
                                            {'label': 'Fill with Mean', 'value': 'mean'},
                                            {'label': 'Fill with Median', 'value': 'median'},
                                            {'label': 'Fill with Mode', 'value': 'mode'},
                                            {'label': 'Fill with Zero', 'value': 'zero'},
                                            {'label': 'Forward Fill', 'value': 'ffill'},
                                            {'label': 'Backward Fill', 'value': 'bfill'},
                                            {'label': 'Fill with Custom Value', 'value': 'custom'}
                                        ],
                                        placeholder="Select method...",
                                        style={'color': 'black'},
                                        className="mb-2"
                                    ),
                                ], width=6),
                            ]),
                            
                            # Custom value input (shown conditionally)
                            dbc.Row([
                                dbc.Col([
                                    dbc.Input(
                                        id='custom-fill-value',
                                        placeholder="Enter custom value...",
                                        className="mb-2",
                                        style={'display': 'none'}
                                    ),
                                ], width=6),
                            ]),
                            
                            dbc.Row([
                                dbc.Col([
                                    dbc.Button(
                                        "Apply to Selected Column",
                                        id='apply-missing-single',
                                        color="success",
                                        className="me-2"
                                    ),
                                    dbc.Button(
                                        "Apply to All Columns",
                                        id='apply-missing-all',
                                        color="warning"
                                    ),
                                ], width=12),
                            ]),
                            
                            html.Div(id='missing-action-output', className="mt-3")
                        ], style={'display': 'none'})  # Hidden by default
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Data Types
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("3. Data Type Issues", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dbc.Button("Check Data Types", id='check-dtypes', color="info", className="mb-3"),
                        html.Div(id='dtype-output'),
                        
                        # Data type conversion section
                        html.Div(id='dtype-handling-section', children=[
                            html.Hr(),
                            html.H6("Convert Data Types:", className="mt-3 mb-2", style={'color': '#00d9ff'}),
                            
                            dbc.Row([
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='dtype-column-select',
                                        placeholder="Select column...",
                                        style={'color': 'black'},
                                        className="mb-2"
                                    ),
                                ], width=6),
                                dbc.Col([
                                    dcc.Dropdown(
                                        id='dtype-target-select',
                                        options=[
                                            {'label': 'Integer (int)', 'value': 'int'},
                                            {'label': 'Float', 'value': 'float'},
                                            {'label': 'String (object)', 'value': 'str'},
                                            {'label': 'DateTime', 'value': 'datetime'},
                                            {'label': 'Category', 'value': 'category'},
                                            {'label': 'Boolean', 'value': 'bool'}
                                        ],
                                        placeholder="Convert to...",
                                        style={'color': 'black'},
                                        className="mb-2"
                                    ),
                                ], width=6),
                            ]),
                            
                            dbc.Button(
                                "Apply Conversion",
                                id='apply-dtype-conversion',
                                color="success",
                                className="mb-2"
                            ),
                            
                            html.Div(id='dtype-action-output', className="mt-3")
                        ], style={'display': 'none'})
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Discretization
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("4. Discretization", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dcc.Dropdown(id='discretize-column', placeholder="Select column to discretize...",
                                    style={'color': 'black'}, className="mb-2"),
                        dbc.Input(id='n-bins', type='number', placeholder="Number of bins", 
                                 value=5, className="mb-2"),
                        dbc.Button("Apply Discretization", id='apply-discretize', color="success"),
                        html.Div(id='discretize-output', className="mt-3")
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Normalization
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("5. Normalization", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dcc.RadioItems(
                            id='normalization-type',
                            options=[
                                {'label': ' Standard Scaler (Z-score)', 'value': 'standard'},
                                {'label': ' Min-Max Scaler', 'value': 'minmax'}
                            ],
                            value='standard',
                            className="mb-3"
                        ),
                        dbc.Button("Apply Normalization", id='apply-normalize', color="success"),
                        html.Div(id='normalize-output', className="mt-3")
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Encoding
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("6. Categorical Encoding", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dcc.RadioItems(
                            id='encoding-type',
                            options=[
                                {'label': ' Label Encoding', 'value': 'label'},
                                {'label': ' One-Hot Encoding', 'value': 'onehot'}
                            ],
                            value='label',
                            className="mb-3"
                        ),
                        dbc.Button("Apply Encoding", id='apply-encoding', color="success"),
                        html.Div(id='encoding-output', className="mt-3")
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Train-Test Split
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5("7. Train-Test Split", style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        dbc.Label("Test Size (%)"),
                        dcc.Slider(id='test-size', min=10, max=40, step=5, value=20,
                                  marks={i: f'{i}%' for i in range(10, 45, 5)}),
                        dbc.Label("Random State", className="mt-3"),
                        dbc.Input(id='random-state', type='number', value=42, className="mb-3"),
                        dbc.Button("Perform Split", id='apply-split', color="success"),
                        html.Div(id='split-output', className="mt-3")
                    ])
                ], className="mb-3", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Download Section
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader(html.H5([html.I(className="fas fa-download me-2"), "Download Processed Data"], 
                                          style={'color': '#00d9ff'})),
                    dbc.CardBody([
                        html.P("Download your transformed dataset after applying preprocessing steps", 
                              className="text-muted mb-3"),
                        dbc.Button(
                            [html.I(className="fas fa-file-download me-2"), "Download CSV"],
                            id='btn-download-csv',
                            color="success",
                            size="lg",
                            className="me-2"
                        ),
                        html.Span(id='download-status', className="ms-3")
                    ])
                ], className="mb-4", style={'backgroundColor': 'rgba(0, 217, 255, 0.1)', 'border': '1px solid #00d9ff'})
            ], width=12)
        ]),
        
        # Navigation
        dbc.Row([
            dbc.Col([
                dbc.Button([html.I(className="fas fa-arrow-left"), " Bivariate Analysis"], 
                          href="/bivariate", color="info", size="lg", className="m-2"),
                dbc.Button([html.I(className="fas fa-home"), " Back to Home"], 
                          href="/", color="secondary", size="lg", className="m-2")
            ], className="text-center mb-5")
        ])
    ], fluid=True)


# =================== LOAD DATA INTO LOCAL STORE ===================
@app.callback(
    Output('preprocessing-data', 'data'),
    Input('stored-data', 'data')
)
def load_preprocessing_data(stored_data):
    return stored_data


# =================== POPULATE DROPDOWN OPTIONS (UPDATED) ===================
@app.callback(
    [Output('discretize-column', 'options'),
     Output('missing-column-select', 'options'),
     Output('dtype-column-select', 'options'),
     Output('drop-column-dropdown', 'options')],
    Input('preprocessing-data', 'data')
)
def update_preprocessing_options(data):
    if data is None:
        return [], [], [], []
    
    try:
        df = load_dataframe(data)
        options = [{'label': col, 'value': col} for col in df.columns]
        return options, options, options, options
    except:
        return [], [], [], []


# =================== DROP COLUMNS CALLBACK ===================
@app.callback(
    [Output('drop-column-status', 'children'),
     Output('preprocessing-data', 'data', allow_duplicate=True)],
    Input('drop-columns-btn', 'n_clicks'),
    [State('drop-column-dropdown', 'value'),
     State('preprocessing-data', 'data')],
    prevent_initial_call=True
)
def drop_selected_columns(n_clicks, columns_to_drop, data):
    if n_clicks == 0 or not columns_to_drop or data is None:
        return "", data
    
    try:
        df = load_dataframe(data)
        original_columns = len(df.columns)
        
        df = df.drop(columns=columns_to_drop)
        updated_data = df.to_json(date_format='iso', orient='split')
        
        success_msg = dbc.Alert([
            html.I(className="fas fa-check-circle me-2"),
            html.Strong(f"Successfully dropped {len(columns_to_drop)} column(s)"),
            html.Hr(),
            html.P([
                f"Columns removed: {', '.join(columns_to_drop)}",
                html.Br(),
                f"Dataset now has {len(df.columns)} columns (was {original_columns})"
            ])
        ], color="success", dismissable=True)
        
        return success_msg, updated_data
        
    except Exception as e:
        error_msg = dbc.Alert([
            html.I(className="fas fa-exclamation-triangle me-2"),
            f"Error: {str(e)}"
        ], color="danger", dismissable=True)
        return error_msg, data


# =================== SHOW/HIDE CUSTOM VALUE INPUT ===================
@app.callback(
    Output('custom-fill-value', 'style'),
    Input('missing-method-select', 'value')
)
def toggle_custom_input(method):
    if method == 'custom':
        return {'display': 'block'}
    return {'display': 'none'}


# =================== DOWNLOAD CSV CALLBACK ===================
@app.callback(
    Output('download-dataframe-csv', 'data'),
    Output('download-status', 'children'),
    Input('btn-download-csv', 'n_clicks'),
    State('preprocessing-data', 'data'),
    prevent_initial_call=True
)
def download_csv(n_clicks, data):
    if data is None:
        return None, dbc.Badge("⚠ No data to download", color="warning")
    
    try:
        df = load_dataframe(data)
        csv_string = df.to_csv(index=False, encoding='utf-8')
        
        return (
            dict(content=csv_string, filename="processed_data.csv"),
            dbc.Badge("✓ Download started!", color="success")
        )
    except Exception as e:
        return None, dbc.Badge(f"✗ Error: {str(e)}", color="danger")


# =================== CHECK MISSING VALUES ===================
@app.callback(
    [Output('missing-output', 'children'),
     Output('missing-handling-section', 'style')],
    Input('check-missing', 'n_clicks'),
    State('preprocessing-data', 'data')
)
def check_missing(n_clicks, data):
    if n_clicks is None or data is None:
        return "", {'display': 'none'}
    
    try:
        df = load_dataframe(data)
        missing = df.isnull().sum()
        missing_pct = (df.isnull().sum() / len(df) * 100).round(2)
        
        missing_df = pd.DataFrame({
            'Column': missing.index,
            'Missing Values': missing.values,
            'Percentage': missing_pct.values
        })
        
        has_missing = missing.sum() > 0
        section_style = {'display': 'block'} if has_missing else {'display': 'none'}
        
        if has_missing:
            alert = dbc.Alert(
                f"⚠ Found {missing.sum()} missing values across {(missing > 0).sum()} columns",
                color="warning",
                className="mb-3"
            )
        else:
            alert = dbc.Alert(
                "✓ No missing values found in the dataset!",
                color="success",
                className="mb-3"
            )
        
        table = dbc.Table.from_dataframe(
            missing_df,
            striped=True,
            bordered=True,
            hover=True,
            className="table-dark"
        )
        
        return html.Div([alert, table]), section_style
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), {'display': 'none'}


# =================== HANDLE MISSING VALUES ===================
@app.callback(
    [Output('missing-action-output', 'children'),
     Output('preprocessing-data', 'data', allow_duplicate=True)],
    [Input('apply-missing-single', 'n_clicks'),
     Input('apply-missing-all', 'n_clicks')],
    [State('missing-column-select', 'value'),
     State('missing-method-select', 'value'),
     State('custom-fill-value', 'value'),
     State('preprocessing-data', 'data')],
    prevent_initial_call=True
)
def handle_missing_values(n_single, n_all, column, method, custom_value, data):
    if data is None or method is None:
        return "", data
    
    try:
        df = load_dataframe(data)
        original_missing = df.isnull().sum().sum()
        
        ctx = dash.callback_context
        if not ctx.triggered:
            return "", data
        
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]
        
        if button_id == 'apply-missing-single':
            if column is None:
                return dbc.Alert("Please select a column", color="warning"), data
            columns_to_process = [column]
        else:
            columns_to_process = df.columns[df.isnull().any()].tolist()
        
        for col in columns_to_process:
            if method == 'drop':
                df = df.dropna(subset=[col])
            elif method == 'mean':
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].mean(), inplace=True)
            elif method == 'median':
                if pd.api.types.is_numeric_dtype(df[col]):
                    df[col].fillna(df[col].median(), inplace=True)
            elif method == 'mode':
                mode_val = df[col].mode()
                if len(mode_val) > 0:
                    df[col].fillna(mode_val[0], inplace=True)
            elif method == 'zero':
                df[col].fillna(0, inplace=True)
            elif method == 'ffill':
                df[col].fillna(method='ffill', inplace=True)
            elif method == 'bfill':
                df[col].fillna(method='bfill', inplace=True)
            elif method == 'custom':
                if custom_value:
                    df[col].fillna(custom_value, inplace=True)
        
        updated_data = df.to_json(date_format='iso', orient='split')
        new_missing = df.isnull().sum().sum()
        
        message = f"✓ Handled missing values using '{method}' method. "
        message += f"Missing values reduced from {original_missing} to {new_missing}. "
        message += f"Processed {len(columns_to_process)} column(s)."
        
        return dbc.Alert(message, color="success"), updated_data
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), data


# =================== CHECK DATA TYPES ===================
@app.callback(
    [Output('dtype-output', 'children'),
     Output('dtype-handling-section', 'style')],
    Input('check-dtypes', 'n_clicks'),
    State('preprocessing-data', 'data')
)
def check_dtypes(n_clicks, data):
    if n_clicks is None or data is None:
        return "", {'display': 'none'}
    
    try:
        df = load_dataframe(data)
        dtypes_df = pd.DataFrame({
            'Column': df.dtypes.index,
            'Data Type': df.dtypes.values.astype(str),
            'Non-Null Count': df.count().values,
            'Null Count': df.isnull().sum().values
        })
        
        table = dbc.Table.from_dataframe(
            dtypes_df,
            striped=True,
            bordered=True,
            hover=True,
            className="table-dark"
        )
        
        return html.Div([table]), {'display': 'block'}
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), {'display': 'none'}


# =================== CONVERT DATA TYPES ===================
@app.callback(
    [Output('dtype-action-output', 'children'),
     Output('preprocessing-data', 'data', allow_duplicate=True)],
    Input('apply-dtype-conversion', 'n_clicks'),
    [State('dtype-column-select', 'value'),
     State('dtype-target-select', 'value'),
     State('preprocessing-data', 'data')],
    prevent_initial_call=True
)
def convert_dtype(n_clicks, column, target_type, data):
    if n_clicks is None or data is None or column is None or target_type is None:
        return "", data
    
    try:
        df = load_dataframe(data)
        original_type = df[column].dtype
        
        if target_type == 'int':
            df[column] = pd.to_numeric(df[column], errors='coerce').fillna(0).astype(int)
        elif target_type == 'float':
            df[column] = pd.to_numeric(df[column], errors='coerce')
        elif target_type == 'str':
            df[column] = df[column].astype(str)
        elif target_type == 'datetime':
            df[column] = pd.to_datetime(df[column], errors='coerce')
        elif target_type == 'category':
            df[column] = df[column].astype('category')
        elif target_type == 'bool':
            df[column] = df[column].astype(bool)
        
        updated_data = df.to_json(date_format='iso', orient='split')
        
        return dbc.Alert(
            f"✓ Converted '{column}' from {original_type} to {target_type}",
            color="success"
        ), updated_data
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), data


# =================== DISCRETIZATION ===================
@app.callback(
    Output('discretize-output', 'children'),
    Output('preprocessing-data', 'data', allow_duplicate=True),
    Input('apply-discretize', 'n_clicks'),
    State('discretize-column', 'value'),
    State('n-bins', 'value'),
    State('preprocessing-data', 'data'),
    prevent_initial_call=True
)
def discretize_column(n_clicks, column, bins, data):
    if n_clicks is None or data is None or column is None:
        return "", data
    
    try:
        df = load_dataframe(data)
        
        if not pd.api.types.is_numeric_dtype(df[column]):
            return dbc.Alert("Error: Column must be numeric for discretization", color="danger"), data
        
        df[column + '_binned'] = pd.cut(df[column], bins=bins)
        updated_data = df.to_json(date_format='iso', orient='split')
        
        return dbc.Alert(
            f"✓ Column '{column}' has been discretized into {bins} bins. New column: '{column}_binned'", 
            color="success"
        ), updated_data
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), data


# =================== NORMALIZATION ===================
@app.callback(
    Output('normalize-output', 'children'),
    Output('preprocessing-data', 'data', allow_duplicate=True),
    Input('apply-normalize', 'n_clicks'),
    State('normalization-type', 'value'),
    State('preprocessing-data', 'data'),
    prevent_initial_call=True
)
def normalize_data(n_clicks, norm_type, data):
    if n_clicks is None or data is None:
        return "", data
    
    try:
        df = load_dataframe(data)
        numeric_cols = df.select_dtypes(include='number').columns
        
        if len(numeric_cols) == 0:
            return dbc.Alert("Error: No numeric columns found to normalize", color="warning"), data
        
        if norm_type == 'standard':
            scaler = StandardScaler()
        else:
            scaler = MinMaxScaler()
        
        df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
        updated_data = df.to_json(date_format='iso', orient='split')
        
        return dbc.Alert(
            f"✓ Applied {norm_type} normalization to {len(numeric_cols)} numeric columns.", 
            color="success"
        ), updated_data
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger"), data


# =================== ENCODING (FIXED) ===================
@app.callback(
    Output('encoding-output', 'children'),
    Output('preprocessing-data', 'data', allow_duplicate=True),
    Input('apply-encoding', 'n_clicks'),
    State('encoding-type', 'value'),
    State('preprocessing-data', 'data'),
    prevent_initial_call=True
)
def encode_data(n_clicks, enc_type, data):
    if n_clicks is None or data is None:
        return "", data
    
    try:
        df = load_dataframe(data)
        
        # Get categorical columns (both object and category types)
        categorical_cols = df.select_dtypes(include=['object', 'category']).columns.tolist()
        
        if len(categorical_cols) == 0:
            return dbc.Alert("Error: No categorical columns found to encode", color="warning"), data
        
        # CRITICAL FIX: Convert all categorical columns to string to avoid dict/category issues
        for col in categorical_cols:
            df[col] = df[col].astype(str)
        
        if enc_type == 'label':
            for col in categorical_cols:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col])
        else:  # one-hot
            df = pd.get_dummies(df, columns=categorical_cols)
        
        updated_data = df.to_json(date_format='iso', orient='split')
        
        return dbc.Alert(
            f"✓ Applied {enc_type} encoding to {len(categorical_cols)} categorical columns.", 
            color="success"
        ), updated_data
        
    except Exception as e:
        import traceback
        traceback.print_exc()
        return dbc.Alert(f"Error: {str(e)}", color="danger"), data


# =================== TRAIN-TEST SPLIT ===================
@app.callback(
    Output('split-output', 'children'),
    Input('apply-split', 'n_clicks'),
    State('test-size', 'value'),
    State('random-state', 'value'),
    State('preprocessing-data', 'data')
)
def split_data(n_clicks, test_size, random_state, data):
    if n_clicks is None or data is None:
        return ""
    
    try:
        df = load_dataframe(data)
        test_frac = test_size / 100
        train_df, test_df = train_test_split(df, test_size=test_frac, random_state=random_state)
        
        return dbc.Alert([
            html.H5("✓ Train-Test Split Complete", className="alert-heading"),
            html.Hr(),
            html.P([
                f"Training Set: {len(train_df)} rows ({100-test_size}%)",
                html.Br(),
                f"Testing Set: {len(test_df)} rows ({test_size}%)"
            ])
        ], color="success")
        
    except Exception as e:
        return dbc.Alert(f"Error: {str(e)}", color="danger")


# Register the page
dash.register_page(__name__, path="/preprocessing")
layout = preprocessing_page()