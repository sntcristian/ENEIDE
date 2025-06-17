import json
from utils import load_csv_datasets
import random
import os

dataset_path = "DZ/v0.1/"
output_path = "DZ/v0.1/assessment"

train_data, dev_data, test_data = load_csv_datasets(dataset_path=dataset_path)

full_dataset = train_data + dev_data + test_data

hundred_samples = random.sample(full_dataset, 100)
list_to_dump = []

for item in hundred_samples:
    item["assessment"]=dict()
    item["assessment"]["wrong_boundaries"]=0
    item["assessment"]["wrong_types"]=0
    item["assessment"]["wrong_identifiers"]=0
    item["assessment"]["partially_wrong_types"]=0
    item["assessment"]["partially_wrong_identifiers"]=0
    item["assessment"]["missing_annotations"]=0
    item["assessment"]["notes"]="Place to write in plain text potential comments."
    list_to_dump.append(item)


if not os.path.exists(output_path):
    os.makedirs(output_path)

with open(os.path.join(output_path, "assessment.json"), "w", encoding="utf-8") as f:
    json.dump(list_to_dump, f, ensure_ascii=False, indent=4)