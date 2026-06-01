from CSV_Helper.csv_helper import read_csv_file
from Scrrapper.scrapp_helper import start_scrap
from pathlib import Path
import asyncio

#####
# Main part of code.
# VARAIBLE:
## FILE_PATH_Clear - Path to file who have a URL to scrap file must by in csv format
## FILE_PATH_OUTPUT - output file name with path
## SEP - separator to csv file
## TO_FIND_PHRASES - Phasyes for find on webpage, who have a info about company some like 'about','company', 'about-us', 'find-us'
## MAX_LEN = "value for length text from webpage who will scrapped"
## BATCH_SIZE - how many record we save to file. I's for save scrap before we loss all data on error
#####


FILE_PATH_CLEAR = "source.csv"
FILE_PATH_OUTPUT = "output.csv"

SEP = ";"
USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
    "AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/121.0.0.0 Safari/537.36"
)
TO_FIND_PHRASES = [
    "onas",
    "o-nas",
    "o_nas",
    "o nas",
    "firma",
    "o-firmie",
    "o_firmie",
    "about",
    "about-us",
    "company",
    "o-marce",
    "o_marce",
    "poznaj-nas",
]
MAX_LEN = 500  # length of contest

BATCH_SIZE = 400  ## how many records we save for one shot

if Path(FILE_PATH_OUTPUT).exists():
    print("Reading from file: Output")
    pd = read_csv_file(FILE_PATH_OUTPUT, SEP)
    if pd is not None:
        data = asyncio.run(start_scrap(pd, TO_FIND_PHRASES, MAX_LEN, BATCH_SIZE))
else:
    print("Create new file named: Output")
    pd = read_csv_file(FILE_PATH_CLEAR, SEP)
    if pd is not None:
        pd["Description"] = None
        pd["URL_SCRAP"] = None
        data = asyncio.run(start_scrap(pd, TO_FIND_PHRASES, MAX_LEN, BATCH_SIZE))
