import csv
import json
import stanza
import re
from tqdm import tqdm

with open("AMD/v0.1/paragraphs_test.csv", "r", encoding="utf-8") as f:
    data = csv.DictReader(f)
    text_data = list(data)
f.close()

with open("AMD/v0.1/annotations_test.csv", "r", encoding="utf-8") as f:
    data = csv.DictReader(f)
    annotations_data = list(data)
f.close()

with open("AMD/semi-auto/surface_form_dict.json", "r", encoding="utf-8") as f:
    surface_form_dict = json.load(f)
f.close()

extra_annotations = []


stanza.download('it')
nlp = stanza.Pipeline('it')


pbar = tqdm(total=len(text_data))
for row in text_data:
    doc_id = row["doc_id"]
    text = row["text"]
    doc_annotations = [anno for anno in annotations_data if anno["doc_id"]==doc_id]
    doc_annotations = [anno for anno in doc_annotations if anno["surface"] in surface_form_dict.keys() and
                       surface_form_dict[anno["surface"]]["valid"]=="yes"]
    position_tuple_list = [(int(anno["start_pos"]), int(anno["end_pos"])) for anno in doc_annotations]
    annotated_positions = [pos for pos_tup in position_tuple_list for pos in range(pos_tup[0], pos_tup[1]+1)]
    annotated_positions = set(annotated_positions)
    found_entities = list()
    for key, value in surface_form_dict.items():
        if value["valid"] == "yes":
            for match in re.finditer(re.escape(key), text):
                start_pos, end_pos = match.span()
                annotated_text = text[start_pos: end_pos]
                _type = surface_form_dict[key]["type"]
                identifier = surface_form_dict[key]["identifier"]
                source = "AMD"
                match_set = set(range(start_pos, end_pos))
                if not match_set & annotated_positions:
                    found_entities.append({"doc_id":doc_id, "surface":annotated_text, "start_pos":start_pos,
                    "end_pos":end_pos, "type":_type, "identifier":identifier, "source":source, "valid":"no"})
                    annotated_positions.update(match_set)

    doc = nlp(text)
    for ent in doc.ents:
        start_pos, end_pos = ent.start_char, ent.end_char
        entity_positions = set(range(start_pos, end_pos))
        if not entity_positions & annotated_positions:
            annotated_text = ent.text
            _type = ent.type
            identifier = ""
            source = "NER"
            found_entities.append({"doc_id": doc_id, "surface": annotated_text, "start_pos": start_pos,
                                   "end_pos": end_pos, "type": _type, "identifier": identifier, "source": source,
                                   "valid": "no"})
            annotated_positions.update(entity_positions)
    extra_annotations.extend(found_entities)
    pbar.update(1)
pbar.close()

with open("../../AMD/semi-auto/annotations_test.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, extra_annotations[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(extra_annotations)
