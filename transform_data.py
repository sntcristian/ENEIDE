import csv

with open("DZ/annotations_test.csv", "r", encoding="utf-8") as f1:
    annotations = csv.DictReader(f1)
    annotations = list(annotations)

with open("disambiguation_results/DZ/mgenre/output.csv", "r", encoding="utf-8") as f2:
    output_mgenre = csv.DictReader(f2)
    output_mgenre = list(output_mgenre)

new_output = []

for annotation, res in zip(annotations, output_mgenre):
    doc_id = annotation["doc_id"]
    start_pos = annotation["start_pos"]
    end_pos = annotation["end_pos"]
    surface = annotation["surface"]
    _type = annotation["type"]
    identifier = res["identifier"]
    score = res["score"]
    new_output.append({
        "doc_id":doc_id,
        "start_pos":start_pos,
        "end_pos":end_pos,
        "surface":surface,
        "type":_type,
        "identifier":identifier,
        "score":score
    })

with open("disambiguation_results/DZ/mgenre/output.csv", "w", encoding="utf-8") as out_f:
    keyz = new_output[0].keys()
    dict_writer = csv.DictWriter(out_f, keyz)
    dict_writer.writeheader()
    dict_writer.writerows(new_output)
