import os
import json
import subprocess 
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from the .env file
load_dotenv()

# Set up the OpenAI API key
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# Path to the main folder (the "icons" folder)
main_folder = "./icons"

# JSON file where synonyms will be stored
synonyms_json_file = "./icons/icons-keywords.json"

# Load the JSON file if it already exists
if os.path.exists(synonyms_json_file):
    with open(synonyms_json_file, "r", encoding="utf-8") as f:
        synonyms_dictionary = json.load(f)
else:
    synonyms_dictionary = {}

# Remove common style indicators from the filename and return
def preprocess_filename(filename):
    return filename.replace("-filled.svg", "").replace("-light.svg", "").replace("-regular.svg", "")

# Function to recursively list all unique SVG filenames without their paths
def list_concepts(folder):
    concepts = set()  # Use a set to avoid duplicates
    for root, dirs, files in os.walk(folder):
        # Filter and preprocess SVG filenames before adding to the set
        for file in files:
            if file.endswith('.svg') and not file.startswith('.'):
                processed_file = preprocess_filename(file)
                concepts.add(processed_file)
    return list(concepts)  # Convert set to list before returning

# Function to generate synonyms using GPT
def generate_synonyms(concept):
    prompt = f"Generate 12 synonyms for the concept '{concept}' mixing English, Spanish, Portuguese, and German (in this order). Return them as a plain list of words, without quotes, numbering, or separation by language. the order of the synonyms should be English, Spanish, Portuguese, and German. For example: alert lamp cross, warning light plus, signal illumination cross, luz de alarma cruz, luz de advertencia plus, iluminación de señal cruz, Alarmleuchte Kreuz, Warnlicht plus, Signalbeleuchtung Kreuz"

    response = client.chat.completions.create(model="gpt-4", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ],
    max_tokens=100,
    temperature=0.7)

    # Get the generated response
    raw_synonyms = response.choices[0].message.content.strip()

    # Clean the output, removing unnecessary characters and convert it to a list
    synonyms = [synonym.strip(' "[]') for synonym in raw_synonyms.split(',')]

    return synonyms

# Get concepts from the icons folder
concepts = set(list_concepts(main_folder))  # Convert to set for efficiency

# Counter to know how many new concepts have been processed
new_concepts = 0

# Remove entries in synonyms_dictionary that no longer have corresponding icons
keys_to_remove = [key for key in synonyms_dictionary if key not in concepts]
for key in keys_to_remove:
    del synonyms_dictionary[key]
    print(f"Concept removed: {key}")

# Update the JSON file only with new concepts
for concept in concepts:
    if concept not in synonyms_dictionary:
        print(f"Generating synonyms for: {concept}")
        try:
            # Generate synonyms using GPT
            generated_synonyms = generate_synonyms(concept)
            # Save the synonyms in the dictionary
            synonyms_dictionary[concept] = generated_synonyms
            new_concepts += 1
            print(f"Concept generated: {concept} - Synonyms: {generated_synonyms}")
        except Exception as e:
            print(f"Error generating synonyms for {concept}: {e}")
            # In case of error, save generic synonyms to avoid leaving it empty
            synonyms_dictionary[concept] = ["synonym1", "synonym2", "synonym3"]
            print(f"Concept generated with generic synonyms: {concept}")

# Only save if there are new concepts or if concepts have been removed
if new_concepts > 0 or keys_to_remove:
    # Save the updated and alphabetically sorted dictionary in the JSON file
    with open(synonyms_json_file, "w", encoding="utf-8") as f:
        json.dump(synonyms_dictionary, f, ensure_ascii=False, indent=4, sort_keys=True)
    print(f"{new_concepts} new concepts have been generated.")
    print(f"{len(keys_to_remove)} obsolete concepts have been removed.")
else:
    print("No new concepts or obsolete concepts found.")

# Run Prettier to format the JSON file
try:
    subprocess.run(["npx", "prettier", "--write", synonyms_json_file], check=True)
    print(f"The file {synonyms_json_file} has been formatted with Prettier.")
except subprocess.CalledProcessError as e:
    print(f"Error formatting the file with Prettier: {e}")

# Count the total number of concepts
total_concepts = len(concepts)
print(f"Total concepts processed: {total_concepts}")
print("Process completed. The icons-keywords.json file has been updated and sorted alphabetically.")
