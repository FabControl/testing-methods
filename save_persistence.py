import paths
from CLI_helpers import separator
import json

# Load persistence
with open("persistence.json", mode='r') as file:
    persistence = json.load(file)

with open(paths.cwd + separator("jsons") + persistence["material"]["manufacturer"] + " " + persistence["material"]["name"] + " " + str(persistence["machine"]["nozzle"]["size_id"]*1000) + " um" + ".json", mode="w") as file:
    output = json.dumps(persistence, indent=4, sort_keys=False)
    file.write(output)
