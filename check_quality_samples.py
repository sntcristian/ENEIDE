import json
import random
import os


sample_path = "DZ/v0.1/assessment"

with open(os.path.join(sample_path, "assessment.json"), "r", encoding="utf-8") as f:
    json_data = json.load(f)
f.close()

annotations = 0
tot_wrong_annotations = 0
tot_missing_annotations = 0
tot_wrong_identifiers = 0
tot_wrong_boundaries = 0
tot_wrong_types = 0
tot_partially_wrong_identifiers = 0
tot_partially_wrong_types = 0

for item in json_data:
    annotations += len(item["annotations"])
    tot_wrong_annotations += item["assessment"].get("wrong_annotations", 0)
    tot_wrong_boundaries += item["assessment"].get("wrong_boundaries")
    tot_wrong_types += item["assessment"]["wrong_types"]
    tot_wrong_identifiers += item["assessment"]["wrong_identifiers"]
    tot_partially_wrong_types += item["assessment"]["partially_wrong_types"]
    tot_partially_wrong_identifiers += item["assessment"]["partially_wrong_identifiers"]
    tot_missing_annotations += item["assessment"]["missing_annotations"]

num_correct_annotations = annotations - (tot_wrong_annotations + tot_wrong_boundaries + tot_wrong_identifiers +
                                        tot_wrong_types + tot_partially_wrong_types + tot_partially_wrong_identifiers)

num_all_labels = annotations + tot_missing_annotations

precision = num_correct_annotations/annotations
recall = num_correct_annotations/num_all_labels
f1 = 2 * ((precision * recall) / (precision+recall))

with open(os.path.join(sample_path, "statistics.txt"), "w", encoding="utf-8") as f:
    f.write("All annotations: " + str(annotations) + "\n")
    f.write("Wrong annotations (false positives): " + str(tot_wrong_annotations + tot_wrong_boundaries +
                                                          tot_wrong_identifiers + tot_wrong_types +
                                                          tot_partially_wrong_types +
                                                          tot_partially_wrong_identifiers) + "\n")
    f.write("Missing annotations: " + str(tot_missing_annotations)+ "\n")
    f.write("Precision: "+str(precision)+"\n")
    f.write("Recall: " + str(recall) + "\n")
    f.write("F1 score: " + str(f1))
    f.close()

