from src.all_imports import *

# paths to various directories
root_dir = os.getcwd()
data_dir = f"{root_dir}/data"
raw_data_dir = f"{data_dir}/raw"
zip_file_path = f"{data_dir}/walmart-sales-forecast.zip"
visuals_path = f"{root_dir}/reports/visuals"
os.makedirs(visuals_path,exist_ok=True)

interactive_visuals_path = f"{root_dir}/reports/interactive_visuals"
os.makedirs(interactive_visuals_path,exist_ok=True)

# given list of major holidays
major_holidays = [
    '2010-02-12', '2011-02-11', '2012-02-10', '2013-02-08', # Super Bowl
    '2010-09-10', '2011-09-09', '2012-09-07', '2013-09-06', # Labor Day
    '2010-11-26', '2011-11-25', '2012-11-23', '2013-11-29', # Thanksgiving
    '2010-12-31', '2011-12-30', '2012-12-28', '2013-12-27', # Christmas
]

# markdown columns list
markdown_cols = [f"markdown{i}" for i in range(1, 6)]