from src.all_imports import *
from src.params import *


def load_data(file):
    """
        Input: path to the flat file (csv)
        Output: dataframe
        Function: reads the csv file from given path and return the dataframe
    """
    logging.info(f"Loading '{file}'...")
    return pd.read_csv(file)

def check_data_missing(df):
    """Returns True if no missing values, otherwise False."""
    return df.isna().sum().sum() == 0

def summary_statistics(df):
    # Summary statistics
    print("\nSummary Stats:")
    stats = df.describe()
    print(tabulate(stats, headers='keys', tablefmt='fancy_grid'))
    
    # Check missing values
    print("\nMissing Values:")
    missing_data = df.isnull().sum().to_frame()
    missing_data.columns = ["missing_values"]
    print(tabulate(missing_data, headers='keys', tablefmt='fancy_grid'))

def visualize_distributions(df):
    # visualize target variable
    plt.figure(figsize=(12, 8))
    sns.histplot(df['weekly_sales'], bins=50, kde=True)
    plt.title('Sales Distribution')
    plt.xlabel('Sales')
    plt.ylabel('Frequency')
    plt.savefig(f'{visuals_path}/sales_distribution.png')

def interactive_visualize_distributions(df):
    # interactive sales distribution
    fig = px.histogram(df, x='weekly_sales', nbins=50, marginal='box', 
                       title='Sales Distribution',
                       labels={'weekly_sales': 'Sales'},
                       template='plotly_white')
    fig.update_layout(
        xaxis_title='Sales',
        yaxis_title='Frequency'
    )
    fig.write_html(f'{interactive_visuals_path}/sales_distribution.html')

def sales_trend(df):
    # plot sales trends over time
    df['date'] = pd.to_datetime(df['date'])
    sales_trend = df.groupby('date')['weekly_sales'].sum().reset_index()
    plt.figure(figsize=(12, 8))
    plt.plot(sales_trend['date'], sales_trend['weekly_sales'])
    plt.title('Sales Trend Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Sales')
    plt.savefig(f'{visuals_path}/sales_trends.png')

def interactive_sales_trend(df):
    # interactive plot
    df['date'] = pd.to_datetime(df['date'])
    sales_trend = df.groupby('date')['weekly_sales'].sum().reset_index()
    fig = px.line(sales_trend, x='date', y='weekly_sales', title='Sales Trend Over Time',
                  labels={'date': 'Date', 'weekly_sales': 'Total Sales'},
                  template='plotly_white')
    fig.write_html(f'{interactive_visuals_path}/sales_trends.html')

def plot_correlation_matrix(df):
    corr_matrix = df.select_dtypes(include=['float64', 'int64']).corr()
    plt.figure(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm')
    plt.title('Correlation Heatmap')
    plt.savefig(f'{visuals_path}/heat_map.png')

def interactive_plot_correlation_matrix(df):
    # interactive correlation matrix
    corr_matrix = df.select_dtypes(include=['float64', 'int64']).corr()
    fig = go.Figure(data=go.Heatmap(
        z=corr_matrix.values,
        x=corr_matrix.columns,
        y=corr_matrix.columns,
        colorscale='RdBu',
        zmin=-1, zmax=1,
        colorbar=dict(title="Correlation")
    ))
    
    fig.update_layout(title_text='Correlation Heatmap', title_x=0.5)
    fig.write_html(f'{interactive_visuals_path}/heat_map.html')

def add_date_features(df):
    df['year'] = df['date'].dt.year
    df['month'] = df['date'].dt.month
    df['week'] = df['date'].dt.isocalendar().week
    df['day_of_week'] = df['date'].dt.dayofweek
    df['is_weekend'] = (df['day_of_week'] >= 5).astype(int)
    return df

def scale_numeric_features(df, numeric_cols):
    scaler = StandardScaler()
    df[numeric_cols] = scaler.fit_transform(df[numeric_cols])
    return df

def encode_categorical(data, cols):
    encoder = LabelEncoder()
    for col in cols:
        data[col] = encoder.fit_transform(data[col])
    return data

def add_lag_features(data, lag_days=[1, 2, 4]):
    for lag in lag_days:
        data[f'sales_lag_{lag}'] = data.groupby('store')['weekly_sales'].shift(lag)
    return data

def add_rolling_features(data, window_sizes=[1, 2]):
    for window in window_sizes:
        data[f'sales_roll_{window}'] = data.groupby('store')['weekly_sales'].shift(1).rolling(window).mean()
    return data

def download_data():
    """Downloads and extracts data, with user confirmation for cleanup."""
    try:
        # Check if Kaggle API credentials exist
        if not os.path.exists(os.path.expanduser("~/.kaggle/kaggle.json")):
            raise FileNotFoundError("kaggle.json not found. Configure Kaggle API credentials first.")
        
        # Downloading data
        os.system(f"kaggle datasets download -d aslanahmedov/walmart-sales-forecast -p {data_dir}")

        # Extracting the zip file
        with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
            zip_ref.extractall(raw_data_dir)
        logging.info(f"Extracted walmart-sales-forecast.zip to: {raw_data_dir}")

        # Prompt for file deletion
        delete_confirmation = input(f"Delete the zip file ({zip_file_path})? (yes/no): ").strip().lower()
        if delete_confirmation in ["yes", "y"]:
            os.remove(zip_file_path)
            logging.info(f"Deleted: {zip_file_path}")
        else:
            logging.info(f"File retained: {zip_file_path}")
    except Exception as e:
        logging.error(f"Error in download_data: {e}")

