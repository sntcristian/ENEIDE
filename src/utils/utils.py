import csv
import os
import json



def reshape_data_input(data, annotations):
    output = []
    for row1 in data:
        annotations_list = [row2 for row2 in annotations if row2["doc_id"] == row1["doc_id"]]
        if len(annotations_list)>0:
            doc = {
                "id":row1["doc_id"],
                "text":row1["text"],
                "annotations":annotations_list,
                "publication_date":row1["publication_date"]
            }
            output.append(doc)
    return output


def load_csv_datasets(dataset_path):
    with open(os.path.join(dataset_path, "paragraphs_train.csv"), "r", encoding="utf-8") as f1:
        paragraphs_train = csv.DictReader(f1)
        paragraphs_train = list(paragraphs_train)
    f1.close()
    with open(os.path.join(dataset_path, "annotations_train.csv"), "r", encoding="utf-8") as f2:
        annotations_train = csv.DictReader(f2)
        annotations_train = list(annotations_train)
    f2.close()
    with open(os.path.join(dataset_path, "paragraphs_dev.csv"), "r", encoding="utf-8") as f3:
        paragraphs_dev = csv.DictReader(f3)
        paragraphs_dev = list(paragraphs_dev)
    f3.close()
    with open(os.path.join(dataset_path, "annotations_dev.csv"), "r", encoding="utf-8") as f4:
        annotations_dev = csv.DictReader(f4)
        annotations_dev = list(annotations_dev)
    f4.close()
    with open(os.path.join(dataset_path, "paragraphs_test.csv"), "r", encoding="utf-8") as f5:
        paragraphs_test = csv.DictReader(f5)
        paragraphs_test = list(paragraphs_test)
    f3.close()
    with open(os.path.join(dataset_path, "annotations_test.csv"), "r", encoding="utf-8") as f6:
        annotations_test = csv.DictReader(f6)
        annotations_test = list(annotations_test)
    f4.close()

    input_train = reshape_data_input(paragraphs_train, annotations_train)
    input_dev = reshape_data_input(paragraphs_dev, annotations_dev)
    input_test = reshape_data_input(paragraphs_test, annotations_test)

    return input_train, input_dev, input_test