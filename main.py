import os

import requests
import pandas as pd
from sqlalchemy import create_engine
import logging
from dotenv import load_dotenv

# Setup professional logging
logging.basicConfig(
    level=logging.INFO, 
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Load environment variables from .env file
load_dotenv()


# Extraction layer
def extract_weather_data(url:str,params:dict)->dict:
    """Fetches raw JSON data from the Weather API."""
    logging.info(f"Extracting data from API for location: {params.get('q')}")
     
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()  # Automatically raises an exception for 4xx/5xx errors
        return response.json()
    except requests.exceptions.RequestException as e:
        logging.error(f"Extraction failed: {e}")
        raise
#transformation layer 
def transform_weather_data(raw_data: dict) -> pd.DataFrame:
    """Normalizes, cleans, and casts data types for the target schema."""
    logging.info("Transforming raw data...")
    
    # Flatten the nested JSON structure
    df = pd.json_normalize(raw_data)
    
    # Data Cleaning (Reassigning ensures changes stick)
    df = df.dropna()
    df = df.drop_duplicates()
    
    # Convert string timestamps to datetime objects
    if 'location.localtime' in df.columns:
        df['location.localtime'] = pd.to_datetime(df['location.localtime'])
        
    return df

#loading layer
def load_to_postgres(df: pd.DataFrame) -> None:
    """Loads the transformed DataFrame into the PostgreSQL database."""
    logging.info("Loading data into PostgreSQL...")
    
    # Securely retrieve database credentials from environment variables
    db_user = os.getenv("DB_USER")
    db_password = os.getenv("DB_PASSWORD")
    db_host = os.getenv("DB_HOST")
    db_port = os.getenv("DB_PORT")
    db_name = os.getenv("DB_NAME")
    
    connection_string = f'postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}'
    
    try:
        engine = create_engine(connection_string)
        df.to_sql(name='weather', con=engine, if_exists='append', index=False)
        logging.info("Database load completed successfully.")
    except Exception as e:
        logging.error(f"Database loading failed: {e}")
        raise


if __name__ == '__main__':
    # Configuration
    API_URL = 'https://api.weatherapi.com/v1/current.json'
    
    # Grab the API key securely from environment variables, fallback to your key if empty
    API_KEY = os.getenv("WEATHER_API_KEY", "c738577dde8143b681664022261206")
    
    API_PARAMS = {
        'key': API_KEY,
        'q': 'Cairo',
        'lang': 'english'
    }
    
    # Orchestrate the ETL Pipeline sequentially
    try:
        logging.info("Starting Weather ETL Pipeline")
        
        raw_json = extract_weather_data(API_URL, API_PARAMS)
        transformed_df = transform_weather_data(raw_json)
        load_to_postgres(transformed_df)
        
        logging.info("ETL Pipeline finished running successfully.")
        
    except Exception as pipeline_error:
        logging.critical(f"Pipeline failed completely: {pipeline_error}")









