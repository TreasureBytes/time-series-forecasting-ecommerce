from src.all_imports import *
from src.params import *
from src.utils.data_utils import *


def clean_data(df, file):
    """
        input: raw dataframe
        output: cleaned dataframe
        function:
            - stardarize the column names
            - correcting data types
            - asserts if the holidays are correct in the respective tables
    """
    # standardizing the column names
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    # correcting the date datatype
    if 'date' in df.columns:
        df.date = pd.to_datetime(df.date)
    
    # making sure if 'isholiday' is correctly filled in given major holidays range
    if 'isholiday' in df.columns:
        invalid_holidays = df[df["isholiday"] == True][~df["date"].isin(major_holidays)]
        assert invalid_holidays.empty, (
            f"{file} contains invalid holiday dates: {invalid_holidays['date'].tolist()}"
        )
    
    return df

def impute_missing_data(df, file):
    """Imputes missing values in the dataframe using appropriate strategies."""
    # check if dataframe has missing data
    logging.info(f"Checking for missing values in: '{raw_data_dir}/{file}'")
    if check_data_missing(df):
        logging.info(f"File '{file}' has no missing values in it.")
        return df
    
    # find the columns in which the data is missing
    logging.info(f"Imputing missing values in: '{file}'")
    data_cols_missing = [col for col in df.columns if df[col].isna().sum()>0]

    # numeric and categorical column separation
    num_cols = [col for col in data_cols_missing if df[col].dtype in ["float64", "int64"]]
    cat_cols = [col for col in data_cols_missing if df[col].dtype == "object"]

    if file=="features":
        # fill holiday weeks first with higher values
        for col in markdown_cols:
            if col in num_cols:
                holiday_median = df[df['isholiday']][col].median()
                df.loc[df['isholiday'] & df[col].isna(), col] = holiday_median
        
        # impute remaining missing markdown values using KNN
        imputer_knn = KNNImputer(n_neighbors=5)
        df[markdown_cols] = imputer_knn.fit_transform(df[markdown_cols])

        # removing markdown columns from numeric missing columns
        num_cols = [col for col in num_cols if col not in markdown_cols]
    
    # impute numeric columns
    if len(num_cols)>0:
        imputer_median = SimpleImputer(strategy="median")
        df[num_cols] = imputer_median.fit_transform(df[num_cols])

    # impute categorical columns
    if len(cat_cols)>0:
        object_imputer = SimpleImputer(strategy='most_frequent')
        df[cat_cols] = object_imputer.fit_transform(df[cat_cols])

    logging.info(f"Missing values imputed for file: '{file}'")
    return df

def merge_datasets(df, features, stores):
    """Merges the df with features and stores to get final df for data analysis."""
    # Merge train and features on 'store_id' and 'date'
    merged = df.merge(features.drop(columns=['isholiday']), on=['store', 'date'], how='left')
    
    # Merge with stores on 'store_id'
    merged = merged.merge(stores, on='store', how='left')
    
    return merged

def data_processing():
    """
        1. loads the raw data
        2. cleans the raw data
        3. imputes missing values in the data
        4. merges the data to get train and test data
    """
    logging.info("Data Pipeline")
    # listing the files in the raw data folder
    files = os.listdir(raw_data_dir)

    # loading the raw data into datadictionary
    logging.info(f"Loading data from: {raw_data_dir}")
    dfs = {file.split(".")[0]:load_data(f"{raw_data_dir}/{file}") for file in files}
    logging.info(f"All data files are loaded!")

    # cleaning the raw data
    logging.info("Data preparation started:")
    cleaned_dfs = {file:clean_data(df, file) for file, df in dfs.items()}

    # preprocess the data
    processed_data = {file:impute_missing_data(df, file) for file, df in cleaned_dfs.items()}
    logging.info(f"Missing data imputation is done!")

    # check if missing values are filled completely
    for file, df in processed_data.items():
        if not check_data_missing(df):
            raise ValueError(
                f"Processed data for '{file}' still contains missing values."
            )
    logging.info("All processed data files have no missing values.")

    # train and test data
    logging.info("Merging test, features, stores to get test data")
    test = merge_datasets(
        processed_data["test"], 
        processed_data["features"], 
        processed_data["stores"]
    )
    logging.info(f"Test data shape: {test.shape}")

    logging.info("Merging train, features, stores to get test data")
    train = merge_datasets(
        processed_data["train"], 
        processed_data["features"], 
        processed_data["stores"]
    )
    logging.info(f"Train data shape: {train.shape}")
    logging.info(f"Data preparation is done!")
    return train, test
   