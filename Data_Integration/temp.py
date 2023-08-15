import pandas as pd
import json

# df = pd.read_excel("Buc-ee's Sales Import-Sid.xlsx")

# fields = df.columns
# fields = fields.tolist()

# with open('field_names.json', 'w') as f:
    # json.dump(fields, f, indent=4)
    
f = open("field_names.json")

data = json.load(f)

print(data)
print(type(data[0]))