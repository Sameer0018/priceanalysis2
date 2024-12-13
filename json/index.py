import json
import os

def parse_esim_data(filename):
    # Read the contents of the file with UTF-8 encoding
    with open(filename, 'r', encoding='utf-8', errors='ignore') as file:
        data = file.read()
    
    # Split the input data into lines
    lines = data.splitlines()

    # Initialize a list to store eSIM plans
    plans = []

    i = 0
    while i < len(lines):
        # Skip empty lines
        if not lines[i].strip():
            i += 1
            continue
        
        # Initialize plan dictionary
        plan = {}

        # Extract relevant data fields
        # Popularity (could be something like "Popular #1")
        if i < len(lines):
            plan['popularity'] = lines[i].strip()
            i += 1
        
        # Price (e.g., "$35.00")
        if i < len(lines):
            plan['price'] = lines[i].strip()
            i += 1
        
        # Data (e.g., "15GB")
        if i < len(lines):
            plan['data'] = lines[i].strip()
            i += 1
        
        # Validity (e.g., "30 Days")
        if i < len(lines):
            plan['validity'] = lines[i].strip()
            i += 1
        
        # Name of the provider (e.g., "Jetpac")
        if i < len(lines):
            plan['name'] = lines[i].strip()
            i += 1
        
        # Optional: If the plan has additional notes or information
        if i < len(lines) and lines[i].strip():
            plan['notes'] = lines[i].strip()
            i += 1
        
        # Add the plan to the list only if it has valid data
        if len(plan) > 1:  # This ensures we only add the plan if it has data
            plans.append(plan)

    # Create the final JSON structure
    result = {"eSIM_plans": plans}
    
    # Output the result as a JSON string
    return json.dumps(result, indent=2)

# Specify the path to your file (index.txt)
filename = r'D:\AI-Web-Scraper-main\AI-Web-Scraper-main\json\index.txt'  # Use raw string for the path

# Parse the eSIM data and print the JSON
json_output = parse_esim_data(filename)
print(json_output)

# Optionally, write the output to a file
with open("esim_plans.json", "w", encoding="utf-8") as json_file:
    json_file.write(json_output)
