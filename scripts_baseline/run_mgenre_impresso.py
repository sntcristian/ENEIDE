from transformers import AutoTokenizer
from transformers import pipeline
import csv
from tqdm import tqdm
import os

NEL_MODEL_NAME = "impresso-project/nel-mgenre-multilingual"

nel_tokenizer = AutoTokenizer.from_pretrained("impresso-project/nel-mgenre-multilingual")



nel_pipeline = pipeline("generic-nel", model=NEL_MODEL_NAME,
                        tokenizer=nel_tokenizer,
                        trust_remote_code=True,
                        device='cpu')




with open("../DZ/v0.1/paragraphs_test.csv", "r", encoding="utf-8") as f1:
    paragraphs = csv.DictReader(f1)
    paragraphs = list(paragraphs)

with open("../DZ/v0.1/annotations_test.csv", "r", encoding="utf-8") as f2:
    all_spans = csv.DictReader(f2)
    all_spans = list(all_spans)



output = []

pbar = tqdm(total=len(paragraphs))
for item in paragraphs:
    text = item["text"]
    doc_id = item["doc_id"]
    surface_forms = [(int(ent["start_pos"]), int(ent["end_pos"]), ent["type"]) for ent in all_spans \
                     if ent["doc_id"] == doc_id]
    for ent in surface_forms:
        start_pos = ent[0]
        end_pos = ent[1]
        if start_pos >= 500:
            history_start = start_pos - 500
        else:
            history_start = 0
        if end_pos + 500 <= len(text):
            future_end = end_pos + 500
        else:
            future_end = len(text)
        label = ent[2]
        mention = text[history_start:start_pos] + "[START] " + text[start_pos:end_pos] + " [END]" + text[end_pos:future_end]
        linked_entity = nel_pipeline(mention)
        # example: [{'surface': 'Un1ted Press', 'wkd_id': 'Q493845', 'wkpedia_pagename': 'United Press International', 'wkpedia_url': 'https://en.wikipedia.org/wiki/United_Press_International', 'type': 'UNK', 'confidence_nel': 55.89, 'lOffset': 7, 'rOffset': 21}]
        identifier = linked_entity[0]["wkd_id"]
        score = linked_entity[0]["confidence_nel"]
        output.append({
            "doc_id":item["doc_id"],
            "surface":text[start_pos:end_pos],
            "start_pos":start_pos,
            "end_pos":end_pos,
            "type":label,
            "identifier":identifier,
            "score":score
        })
    pbar.update(1)
pbar.close()


o_keys = output[0].keys()
if not os.path.exists("../results/DZ/mgenre_impresso_ed"):
    os.makedirs("../results/DZ/mgenre_impresso_ed")

with open('../results/DZ/mgenre_impresso_ed/output.csv', 'w', encoding='utf-8') as f:
    dict_writer = csv.DictWriter(f, o_keys)
    dict_writer.writeheader()
    dict_writer.writerows(output)

