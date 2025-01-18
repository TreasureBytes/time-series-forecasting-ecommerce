from src.utils.all_imports import *

def download_data():
    """Downloads and extracts data, with user confirmation for cleanup."""
    # Downloading data
    os.system(f"kaggle datasets download -d aslanahmedov/walmart-sales-forecast -p {data_dir}")

    # Extracting the zip file
    with zipfile.ZipFile(zip_file_path, "r") as zip_ref:
        zip_ref.extractall(raw_data_dir)

    # Prompt the user before deleting
    delete_confirmation = input(f"Are you sure you want to delete the file: {zip_file_path}? (yes/no): ").strip().lower()

    if delete_confirmation == "yes":
        os.remove(zip_file_path)
        print(f"Deleted: {zip_file_path}")
    else:
        print(f"File not deleted: {zip_file_path}")
