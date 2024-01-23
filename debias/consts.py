import hashlib
import os
import pathlib
import pickle
import time
import uuid

import pandas as pd

TRUE_CUR_PATH = os.path.dirname(__file__)
TRUE_CUR_PATH = TRUE_CUR_PATH if TRUE_CUR_PATH != '' else '.'

# TRUE_CUR_PATH = pathlib.Path.cwd()

pl_TRUE_CUR_PATH = pathlib.Path(TRUE_CUR_PATH)
BASE_PATH = pl_TRUE_CUR_PATH.parent

# Check the auto root path is correct
try:
    assert BASE_PATH.name == 'debias'
except Exception as e:
    print('Base dir should be something like ....../debias/: ', BASE_PATH)
    print('Important! Ensure TRUE_CUR_PATH is your working directory:', TRUE_CUR_PATH)
    print("Exception:", e)

DATA_PATH = BASE_PATH / 'data'
OPENAI_WORKSPACE = DATA_PATH / 'openai_res'
TEST_CSV_PATH = DATA_PATH / 'example_test_data.csv'
EXPORT_METRIC_CSV_PATH = DATA_PATH / 'export_metric.csv'
assert DATA_PATH.exists()