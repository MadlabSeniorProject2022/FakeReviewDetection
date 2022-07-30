import os
from environment import load_environment_variables
load_environment_variables()

# DATA_DIR
DATA_DIR = os.getenv('DATA_DIR') or '../data'
