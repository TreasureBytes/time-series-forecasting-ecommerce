from src.all_imports import *
from src.params import *
from src.utils.data_utils import *


def exploratory_data_analysis(df):
    """
    
    """
    file = 'train' if 'weekly_sales' in df.columns else 'test'
    logging.info(f"Exploratory Data Analysis: {file.upper()}")

    # get summary stats
    logging.info("Summary Statistics: ")
    summary_statistics(df)
 
    if file=='train':
        # get distribution
        logging.info("Distribution Plot:")
        visualize_distributions(df)
        interactive_visualize_distributions(df)

        # sales trends over time
        logging.info("Sales Trends:")
        sales_trend(df)
        interactive_sales_trend(df)

        # correlation matrix
        logging.info("Heat Map:")
        plot_correlation_matrix(df)
        interactive_plot_correlation_matrix(df)

        # create lag features
        logging.info("Creating Lag features")
        df = add_lag_features(df)

        # create rolling features
        logging.info("Creating Rolling features")
        df = add_rolling_features(df)
    
    # adding date features
    logging.info("Adding Date features")
    df = add_date_features(df)

    # encoding the cat and bool variables
    logging.info("Encoding the variables")
    df = pd.get_dummies(df, columns=['type'])
    df = encode_categorical(df, ['type_A', 'type_B', 'type_C', 'isholiday'])

    logging.info("Data Analysis is done!")
    return df