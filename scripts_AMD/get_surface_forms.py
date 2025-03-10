import os
import glob
from bs4 import BeautifulSoup
import statistics
import re
import json

output = []
all_paragraphs = []

raw_data_directory = '../AMD/raw_html'


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


for filepath in glob.glob(os.path.join(raw_data_directory, '*.html')):
    # Estrae il nome del file dal percorso
    file_name = os.path.basename(filepath)

    # Apre e legge il contenuto del file
    with open(filepath, 'r', encoding='utf-8') as file:
        content = file.read()
    file.close()

    # Usa BeautifulSoup per il parsing del contenuto HTML
    soup = BeautifulSoup(content, 'html.parser')
    meta_with_resource = soup.find_all('meta', attrs={'resource': True})
    id_to_wikidata = {}
    for element in meta_with_resource:
        _id = element["about"]
        resource = re.match(r".*?(Q\w+)", element["resource"]).group(1)
        id_to_wikidata[_id]=resource


    full_text = ""
    title_text = re.sub(r"\s+", " ", soup.find("h1").text)
    counter = 0
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
            counter += len(surface)
        else:
            element_text = re.sub(r"\s+", " ", element if isinstance(element, str) else element.get_text())
            counter += len(element_text)
            full_text += element_text

    if len(annotations)>0:
        output.extend(annotations)
        max_date = get_date(soup)
        mention_counts[file_name] = len(annotations)
        all_paragraphs.append({"doc_id":file_name, "title":title_text, "text":full_text, "publication_date":max_date})
        length_counts[file_name]=len(re.split("\W", full_text))



length_counts_values = list(length_counts.values())

# Calcolo della media e deviazione standard
mean_length = statistics.mean(length_counts_values)
std_dev_length = statistics.stdev(length_counts_values)

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



all_paragraphs = [par for par in all_paragraphs if par["doc_id"] in documents_not_outliers]
output = [annotation for annotation in output if annotation["doc_id"] in documents_not_outliers]




surface_to_type_dict = dict()
surface_to_id_dict = dict()


for anno in output:
    surface_form = anno["surface"]
    if surface_form in surface_to_id_dict:
        if anno["identifier"] in surface_to_id_dict[surface_form]:
            surface_to_id_dict[surface_form][anno["identifier"]]+=1
        else:
            surface_to_id_dict[surface_form][anno["identifier"]] = 1
    else:
        surface_to_id_dict[surface_form] = {anno["identifier"]: 1}

    if surface_form in surface_to_type_dict:
        if anno["type"] in surface_to_type_dict[surface_form]:
            surface_to_type_dict[surface_form][anno["type"]]+=1
        else:
            surface_to_type_dict[surface_form][anno["type"]] = 1
    else:
        surface_to_type_dict[surface_form] = {anno["type"]: 1}


output_dict = dict()
for key, value in surface_to_id_dict.items():
    max_freq_id = 0
    max_id = ""
    max_freq_type = 0
    max_type = ""
    for q_id in value.keys():
        if value[q_id]>max_freq_id:
            max_freq_id = value[q_id]
            max_id = q_id
    for _type in surface_to_type_dict[key]:
        if surface_to_type_dict[key][_type] > max_freq_type:
            max_freq_type = surface_to_type_dict[key][_type]
            max_type = _type

    output_dict[key]={"type":max_type, "identifier":max_id, "valid":"no"}

with open("AMD/v0.1/surface_form_dict.json", "w", encoding="utf-8") as out_f:
    json.dump(output_dict, out_f, indent=4, sort_keys=True, ensure_ascii=False)







