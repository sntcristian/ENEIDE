import pandas as pd
import spacy
import json
from tqdm import tqdm
import os

# Load the uploaded CSV files
paragraphs_train = pd.read_csv('./AMD/v0.3/paragraphs_train.csv')
annotations_train = pd.read_csv('./AMD/v0.3/annotations_train.csv')
paragraphs_dev = pd.read_csv('./AMD/v0.3/paragraphs_dev.csv')
annotations_dev = pd.read_csv('./AMD/v0.3/annotations_dev.csv')



# Load Spacy model for tokenization
nlp = spacy.load("it_core_news_lg")


# Function to process each document
def process_document(paragraph_id, text, annotations):
    doc = nlp(text)
    tokenized_text = [token.text for token in doc]
    if len(tokenized_text)<=700:
        ner = []
        for _, row in annotations.iterrows():
            start = int(row['start_pos'])
            end = int(row['end_pos'])
            entity_type = row['type']
            if entity_type=="PER":
                entity_type="persona"
            elif entity_type=="LOC":
                entity_type="luogo"
            elif entity_type=="WORK":
                entity_type="opera"
            elif entity_type=="ORG":
                entity_type="organizzazione"
            token_start = None
            token_end = None

            # Finding token boundaries for the annotation
            for i, token in enumerate(doc):
                if token.idx == start:
                    token_start = i
                if token.idx + len(token.text) - 1 == end - 1:
                    token_end = i

            if token_start is not None and token_end is not None:
                ner.append([token_start, token_end, entity_type])
        if len(ner)>0:
            return {
                "id":paragraph_id,
                "tokenized_text": tokenized_text,
                "ner": ner
            }
        else:
            return None
    else:
        return None

pbar = tqdm(total=len(paragraphs_train))

# Merge and process the data
result_train = []
for _, row in paragraphs_train.iterrows():
    paragraph_id = row['doc_id']
    text = row['text']
    annotations = annotations_train[annotations_train['doc_id'] == paragraph_id]
    processed_data = process_document(paragraph_id, text, annotations)
    if processed_data != None:
        result_train.append(processed_data)
    pbar.update(1)
pbar.close()
print(len(result_train))

if not os.path.exists("./AMD/v0.3/json_data"):
    os.makedirs("./AMD/v0.3/json_data")


output_path = os.path.join('./AMD/v0.3/json_data', 'train.json')
with open(output_path, 'w', encoding="utf-8") as f:
    json.dump(result_train, f, ensure_ascii=False)



pbar = tqdm(total=len(paragraphs_dev))

result_dev = []
for _, row in paragraphs_dev.iterrows():
    paragraph_id = row['doc_id']
    text = row['text']
    annotations = annotations_dev[annotations_dev['doc_id'] == paragraph_id]
    processed_data = process_document(paragraph_id, text, annotations)
    if processed_data != None:
        result_dev.append(processed_data)
    pbar.update(1)

print(len(result_dev))

output_path = os.path.join('./AMD/v0.3/json_data', 'dev.json')
with open(output_path, 'w', encoding="utf-8") as f:
    json.dump(result_train, f, ensure_ascii=False)