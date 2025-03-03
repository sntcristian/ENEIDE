import csv
import json
from sklearn.model_selection import train_test_split
import pandas as pd

with open("./AMD/v0.1/paragraphs_train.csv", "r", encoding="utf-8") as f1:
    dict_reader = csv.DictReader(f1)
    paragraphs_train = list(dict_reader)
f1.close()


with open("./AMD/v0.1/paragraphs_dev.csv", "r", encoding="utf-8") as f2:
    dict_reader = csv.DictReader(f2)
    paragraphs_dev = list(dict_reader)
f2.close()

with open("./AMD/v0.1/paragraphs_test.csv", "r", encoding="utf-8") as f3:
    dict_reader = csv.DictReader(f3)
    paragraphs_test = list(dict_reader)
f3.close()


paragraphs = paragraphs_train + paragraphs_dev + paragraphs_test

with open("./AMD/v0.1/annotations_train.csv", "r", encoding="utf-8") as f1:
    dict_reader = csv.DictReader(f1)
    annotations_train = list(dict_reader)
f1.close()


with open("./AMD/v0.1/annotations_dev.csv", "r", encoding="utf-8") as f2:
    dict_reader = csv.DictReader(f2)
    annotations_dev = list(dict_reader)
f2.close()

with open("./AMD/v0.1/annotations_test.csv", "r", encoding="utf-8") as f3:
    dict_reader = csv.DictReader(f3)
    annotations_test = list(dict_reader)
f3.close()


annotations = annotations_train + annotations_dev + annotations_test


with open("./AMD/semi-auto/extra_annotations1.csv", "r", encoding="utf-8") as f1:
    dict_reader = csv.DictReader(f1)
    extra_annotations1 = list(dict_reader)
f1.close()


with open("./AMD/semi-auto/extra_annotations2.csv", "r", encoding="utf-8") as f2:
    dict_reader = csv.DictReader(f2)
    extra_annotations2 = list(dict_reader)
f2.close()


with open("./AMD/semi-auto/extra_annotations3.csv", "r", encoding="utf-8") as f3:
    dict_reader = csv.DictReader(f3)
    extra_annotations3 = list(dict_reader)
f3.close()

extra_annotations = extra_annotations1 + extra_annotations2 + extra_annotations3


with open("./AMD/semi-auto/surface_form_dict.json", "r", encoding="utf-8") as f1:
    surface_form_dict = json.load(f1)

valid_surface_forms = set([key for key in surface_form_dict.keys() if surface_form_dict[key]["valid"]=="yes"])

new_paragraphs = []
new_annotations = []

for row in paragraphs:
    doc_id = row["doc_id"]
    annotations1 = [row for row in annotations if row["doc_id"]==doc_id]
    annotations2 = [row for row in extra_annotations if row["doc_id"]==doc_id]
    valid_annotations = []
    for anno in annotations1:
        if anno["surface"] in valid_surface_forms:
            item = {"doc_id": doc_id, "start_pos": int(anno["start_pos"]), "end_pos": int(anno["end_pos"]),
                "surface": anno["surface"], "type": anno["type"], "identifier": anno["identifier"]}
            valid_annotations.append(item)
    for anno in annotations2:
        if anno["valid"]!="no":
            if anno["source"]=="AMD":
                item = {"doc_id":doc_id, "start_pos": int(anno["start_pos"]), "end_pos": int(anno["end_pos"]),
                        "surface":anno["surface"], "type":anno["type"], "identifier":anno["identifier"]}
                valid_annotations.append(item)
            elif anno["source"]=="NER":
                if any(x.isupper() for x in anno["surface"]) or anno["surface"] in valid_surface_forms:
                    item = {"doc_id": doc_id, "start_pos": int(anno["start_pos"]), "end_pos": int(anno["end_pos"]),
                            "surface": anno["surface"], "type": anno["type"], "identifier": anno["identifier"]}
                    valid_annotations.append(item)

    valid_annotations = sorted(valid_annotations, key=lambda x: x["start_pos"])
    if len(valid_annotations)>0:
        new_paragraphs.append(row)
        new_annotations.extend(valid_annotations)


paragraphs_df = pd.DataFrame(new_paragraphs)


paragraphs_df = paragraphs_df.dropna(subset=['publication_date'])


train_df, test_df = train_test_split(
    paragraphs_df,
    test_size=0.3,
    stratify=paragraphs_df['publication_date'],
    random_state=42
)

dev_df, test_df = train_test_split(
    test_df,
    test_size=0.5,
    random_state=42
)

train_df = train_df.sort_values(by='doc_id', ascending=True)
dev_df = dev_df.sort_values(by="doc_id", ascending=True)
test_df = test_df.sort_values(by='doc_id', ascending=True)

# Salvataggio dei dati su file
train_df.to_csv("./AMD/v0.2/paragraphs_train.csv", index=False, encoding="utf-8")
dev_df.to_csv("./AMD/v0.2/paragraphs_dev.csv", index=False, encoding="utf-8")
test_df.to_csv("./AMD/v0.2/paragraphs_test.csv", index=False, encoding="utf-8")



train_annotations = [ann for ann in new_annotations if ann["doc_id"] in train_df["doc_id"].values]
dev_annotations = [ann for ann in new_annotations if ann["doc_id"] in dev_df["doc_id"].values]
test_annotations = [ann for ann in new_annotations if ann["doc_id"] in test_df["doc_id"].values]

keys = new_annotations[0].keys()
with open("./AMD/v0.2/annotations_train.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(train_annotations)
f.close()

with open("./AMD/v0.2/annotations_dev.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dev_annotations)
f.close()

with open("./AMD/v0.2/annotations_test.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(test_annotations)
f.close()