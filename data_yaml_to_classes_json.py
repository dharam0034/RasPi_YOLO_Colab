import yaml
import json
import os
import argparse

def generate_classes(input_yaml_path, output_json_path):
    # Read the data.yaml file
    with open(input_yaml_path, 'r') as file:
        data = yaml.safe_load(file)

    # Create a dictionary mapping names to indices
    classes = {name: idx for idx, name in enumerate(data['names'])}

    # Ensure the output directory exists
    os.makedirs(os.path.dirname(output_json_path), exist_ok=True)

    # Write the dictionary to classes.json
    with open(output_json_path, 'w') as file:
        json.dump(classes, file, indent=2)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate classes.json from data.yaml')
    parser.add_argument('--input_yaml', required=True, help='Path to input data.yaml file')
    parser.add_argument('--output_json', required=True, help='Path to output classes.json file')

    # Parse arguments
    args = parser.parse_args()

    # Call generate_classes with provided arguments
    generate_classes(args.input_yaml, args.output_json)

if __name__ == '__main__':
    main()
