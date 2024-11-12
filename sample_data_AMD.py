import os
import glob
from bs4 import BeautifulSoup
import csv
import statistics
import re

output = []
all_paragraphs = []

directory = './documenti_moro'


class2type_dict = {
    "place":"LOC",
    "person": "PER",
    "organization": "ORG"
}


length_counts = {}
mention_counts = {}

def get_date(soup_element):
    max_date = 0
    meta_elements = soup_element.find_all("meta", attrs={'content': True})
    for element in meta_elements:
        content = element["content"]
        dates = re.findall(r"19\d{2}", content)
        if len(dates)>0:
            for date in dates:
                date_integer = int(date)
                if date_integer>max_date:
                    max_date = date_integer
    if max_date==0:
        max_date = None
    return max_date


for filepath in glob.glob(os.path.join(directory, '*.html')):
    # Estrae il nome del file dal percorso
    file_name = os.path.basename(filepath)

    # Apre e legge il contenuto del file
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()

    # Usa BeautifulSoup per il parsing del contenuto HTML
    soup = BeautifulSoup(content, 'html.parser')
    meta_with_resource = soup.find_all('meta', attrs={'resource': True})
    id_to_wikidata = {}
    for element in meta_with_resource:
        _id = element["about"]
        resource = re.match(r".*?(Q\w+)", element["resource"]).group(1)
        id_to_wikidata[_id]=resource


    full_text = ""
    title_text = re.sub(r"\s+", " ", soup.find("h1").text)+". "
    full_text += title_text
    counter = len(full_text)
    first_paragraph = soup.find('p', id="p-1")
    annotations = []
    for element in first_paragraph.children:
        if element.name == "span" and element.get('class', [])[0].startswith('mention'):
            start_pos = counter
            surface = re.sub("\s+", " ", element.get_text()).strip()
            end_pos = counter+len(surface)
            _type = class2type_dict[element["class"][1]]
            referenced_entity = element["resource"]
            if referenced_entity in id_to_wikidata.keys():
                wiki_id = id_to_wikidata[referenced_entity]
            else:
                wiki_id = "NIL"
            annotations.append({
                "doc_id":file_name,
                "surface":surface,
                "start_pos":start_pos,
                "end_pos":end_pos,
                "type":_type,
                "identifier":wiki_id
            })
            full_text += surface
            counter += len(element.get_text())
        else:
            element_text = re.sub(r"\s+", " ", element if isinstance(element, str) else element.get_text())
            counter += len(element_text)
            full_text += element_text

    if len(annotations)>0:
        output.extend(annotations)
        max_date = get_date(soup)
        mention_counts[file_name] = len(annotations)
        all_paragraphs.append({"doc_id":file_name, "text":full_text, "publication_date":max_date})
        length_counts[file_name]=len(re.split("\W", full_text))



length_counts_values = list(length_counts.values())

# Calcolo della media e deviazione standard
mean_length = statistics.mean(length_counts_values)
std_dev_length = statistics.stdev(length_counts_values)

# Impostiamo un limite di 1.5 deviazioni standard per identificare gli outlier
threshold = 1.5

# Trova i documenti che esulano dalla distribuzione normale
outliers = {
    file: count for file, count in length_counts.items()
    if abs(count - mean_length) > threshold * std_dev_length
}


print(f'Media delle numero di parole: {mean_length}')
print(f'Deviazione standard del numero di parole: {std_dev_length}')


documents_not_outliers = {
    file for file, count in length_counts.items()
    if file not in outliers
}

mention_counts_values = list([value for key, value in mention_counts.items() if key in documents_not_outliers])

# Calcolo della media e deviazione standard nelle annotazioni
mean_mentions = statistics.mean(mention_counts_values)
std_dev_mentions = statistics.stdev(mention_counts_values)
max_mentions = max(mention_counts_values)


print(f'Media dei conteggi: {mean_mentions}')
print(f'Deviazione standard dei conteggi: {std_dev_mentions}')
print(f"Valore massimo dei conteggi: {max_mentions}")


all_paragraphs = [par for par in all_paragraphs if par["doc_id"] in documents_not_outliers]
output = [annotation for annotation in output if annotation["doc_id"] in documents_not_outliers]

keys = output[0].keys()
with open("./AMD/annotations.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(output)
f.close()

keys = all_paragraphs[0].keys()
with open("./AMD/paragraphs.csv", "w", encoding="utf-8") as f:
    dict_writer = csv.DictWriter(f, keys)
    dict_writer.writeheader()
    dict_writer.writerows(all_paragraphs)
f.close()

print(len(all_paragraphs))
print(len(output))

per_annotations = [annotation for annotation in output if annotation["type"]=="PER"]
loc_annotations = [annotation for annotation in output if annotation["type"]=="LOC"]
org_annotations = [annotation for annotation in output if annotation["type"]=="ORG"]
nil_annotations = [annotation for annotation in output if annotation["identifier"]=="NIL"]

print(f"Number of annotations for persons: {len(per_annotations)}")
print(f"Number of annotations for locations: {len(loc_annotations)}")
print(f"Number of annotations for organizations: {len(org_annotations)}")
print(f"NIL annotations: {len(nil_annotations)}")




