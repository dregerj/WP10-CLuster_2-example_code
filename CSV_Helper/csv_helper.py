import pandas as pd
import os
import logging
from typing import Optional

#######
# We save all information about scraping in log files
# read_csv_file - read only correctly file 
#######

logger = logging.getLogger(__name__)
logger.setLevel(logging.ERROR)

handler = logging.FileHandler("errors.log")
formatter = logging.Formatter(
    "%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
handler.setFormatter(formatter)

logger.addHandler(handler)

###
## Read CSV file and check the format file
###
@staticmethod
def read_csv_file(file_path:str, sep:str)->Optional[pd.DataFrame]:
    if not os.path.isfile(file_path):
        logger.exception(f"File doesn't exist: {file_path}")
        return None
    try:
        df = pd.read_csv(file_path, sep=sep)
    except pd.errors.ParserError:
        logger.exception(f"Failed to parse file with separator '{sep}'")
        return None
    except Exception as e:
        logger.exception(f"Error reading CSV file: {e}")
        return None
    if df.shape[1] == 0:
        logger.exception("The file has no columns - it's probably not a CSV")
        return None
    return df

