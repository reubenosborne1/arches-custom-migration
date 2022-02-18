import json
import uuid
import os
import inspect
import pandas as pd

APP_ROOT = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))


people_file = APP_ROOT + '/mappings/personorg_mapping.csv'


df = pd.read_csv(people_file)

print(df.head())

# Grid ID
# ResourceID
# E00N26-31