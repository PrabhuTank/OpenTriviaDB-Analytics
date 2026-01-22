# Interacting with the Python runtime environment.
import sys
# Interacting with the operating system, such as file paths and directories.
import os

### Specify the path where function files are stored
wd = "D:/Projects/Python/TriviaDB"
# wd = os.getcwd()
srcpath = os.path.join(wd,"scripts")

### Add the path to the system path
sys.path.append(srcpath)

### Loading the custom libraries
from functions_etl_pipeline import extract_data, transform_data, load_data

### Running the ETL pipeline.
print("⏳ Executing the ETL pipeline...")

print(" ⏳ Extract...")
raw_data = extract_data()
print(" ✅ Extract complete!")
 
print(" ⏳ Transform...")
df_questions = transform_data(raw_data)
print(" ✅ Transform complete!")
    
print(" ⏳ Load...")
load_data(df_questions)
print(" ✅ Load complete!")
    
print("✅ Completed the ETL pipeline...")

