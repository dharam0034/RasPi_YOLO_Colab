import yaml
import json

# Read the data.yaml file
with open('path_to_data_yaml_file, 'r') as file:
    data = yaml.safe_load(file)

# Create a dictionary mapping names to indices
classes = {name: idx for idx, name in enumerate(data['names'])}

# Write the dictionary to classes.json
with open('classes.json', 'w') as file:
    json.dump(classes, file, indent=2)
