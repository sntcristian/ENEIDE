import csv
import pandas as pd
import re
import statistics
from sklearn.model_selection import train_test_split



with open("data_zibaldone/all_paragraphs.csv", "r", encoding="utf-8") as f:
    all_paragraphs = csv.DictReader(f)
    all_paragraphs = list(all_paragraphs)
f.close()


with open("data_zibaldone/all_annotations.csv", "r", encoding="utf-8") as f:
    all_annotations = csv.DictReader(f)
    all_annotations = list(all_annotations)
f.close()



length_counts = dict()
filtered_paragraphs = []
filtered_annotations = []
for row in all_paragraphs:
    par_annotations = [anno for anno in all_annotations if anno["doc_id"]==row["doc_id"]]
    if par_annotations:
        text = row["text"]
        doc_id = row["doc_id"]
        length_counts[doc_id] = len(re.split("\W", text))
        if doc_id.startswith("https://digitalzibaldone.net/node/p1"):
            publication_date = 1821
        else:
            publication_date = 1823
        filtered_paragraphs.append(
            {"doc_id":doc_id,
             "text":text,
             "publication_date": publication_date
             }
        )
        for anno in par_annotations:
            filtered_annotations.append({
                "doc_id":anno["doc_id"],
                "surface":anno["surface"],
                "start_pos":anno["start_pos"],
                "end_pos":anno["end_pos"],
                "type":anno["type"],
                "identifier":anno["identifier"]
            })


length_counts_values = list(length_counts.values())

# Calcolo della media e deviazione standard e altre statistiche
mean_length = statistics.mean(length_counts_values)
std_dev_length = statistics.stdev(length_counts_values)
min_length = min(length_counts_values)
max_length = max(length_counts_values)

print("Lunghezza massima: ", max_length)
print("Lunghezza minima: ", min_length)
print("Lunghezza media:", mean_length)
print("Deviazione standard: ", std_dev_length)

# Impostiamo un limite di 2 deviazioni standard per identificare gli outlier
threshold = 2

# Trova i documenti che esulano dalla distribuzione normale
outliers = {
    file: count for file, count in length_counts.items()
    if abs(count - mean_length) > threshold * std_dev_length
}


documents_not_outliers = {
    file for file, count in length_counts.items()
    if file not in outliers
}

filtered_paragraphs = [par for par in filtered_paragraphs if par["doc_id"] in documents_not_outliers]
filtered_annotations = [annotation for annotation in filtered_annotations if annotation["doc_id"] in
                        documents_not_outliers]

filtered_paragraphs = sorted(filtered_paragraphs, key=lambda d: d['doc_id'])
filtered_annotations = sorted(filtered_annotations, key=lambda d: (d['doc_id'], int(d["start_pos"])))

paragraphs_df = pd.DataFrame(filtered_paragraphs)

# Rimuoviamo le righe con valori NaN in 'publication_date' per il campionamento stratificato
paragraphs_df = paragraphs_df.dropna(subset=['publication_date'])

# Divisione in training e testing con stratificazione su 'publication_date'
train_df, test_df = train_test_split(
    paragraphs_df,
    test_size=0.3,
    stratify=paragraphs_df['publication_date'],
    random_state=42
)

dev_df, test_df = train_test_split(
    test_df,
    stratify=test_df['publication_date'],
    test_size=0.5,
    random_state=42
)

train_df = train_df.sort_values(by='doc_id', ascending=True)
dev_df = dev_df.sort_values(by="doc_id", ascending=True)
test_df = test_df.sort_values(by='doc_id', ascending=True)


train_df.to_csv("./DZ/v0.2/paragraphs_train.csv", index=False, encoding="utf-8")
dev_df.to_csv("./DZ/v0.2/paragraphs_dev.csv", index=False, encoding="utf-8")
test_df.to_csv("./DZ/v0.2/paragraphs_test.csv", index=False, encoding="utf-8")



train_annotations = [ann for ann in filtered_annotations if ann["doc_id"] in train_df["doc_id"].values]
dev_annotations = [ann for ann in filtered_annotations if ann["doc_id"] in dev_df["doc_id"].values]
test_annotations = [ann for ann in filtered_annotations if ann["doc_id"] in test_df["doc_id"].values]

keys = filtered_annotations[0].keys()
with open("./DZ/v0.2/annotations_train.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(train_annotations)
f.close()

with open("./DZ/v0.2/annotations_dev.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(dev_annotations)
f.close()

with open("./DZ/v0.2/annotations_test.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(test_annotations)
f.close()