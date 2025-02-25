import csv

import rdflib
import re

g = rdflib.Graph()

g.parse("./documenti_moro/dataset.ttl", format="turtle")



def normalize_date_string(date_str):
    date_str = date_str.strip()
    match_dd_mm_yyyy = re.match(r'^(\d{1,2})-(\d{1,2})-(\d{4})$', date_str)
    if match_dd_mm_yyyy:
        dd, mm, yyyy = match_dd_mm_yyyy.groups()
        # converto in formato YYYY-MM-DD
        return f"{yyyy}-{mm.zfill(2)}-{dd.zfill(2)}"

    match_yyyy_mm = re.match(r'^(\d{4})-(\d{1,2})$', date_str)
    if match_yyyy_mm:
        yyyy, mm = match_yyyy_mm.groups()
        return f"{yyyy}-{mm.zfill(2)}-01"


    match_mm_yyyy = re.match(r'^(\d{1,2})-(\d{4})$', date_str)
    if match_mm_yyyy:
        mm, yyyy = match_mm_yyyy.groups()
        return f"{yyyy}-{mm.zfill(2)}-01"


    match_yyyy = re.match(r'^(\d{4})$', date_str)
    if match_yyyy:
        yyyy = match_yyyy.group(1)
        return f"{yyyy}-01-01"
    return date_str




def find_date(g, row):
    FRBR = rdflib.Namespace("http://purl.org/vocab/frbr/core#")
    DCTERMS = rdflib.Namespace("http://purl.org/dc/terms/")
    doc_id = row["doc_id"]
    title = row["title"]
    text = row["text"]
    pub_date = row["publication_date"]
    doc_num = doc_id.replace("document_", "").replace(".html", "")
    doc_uri = rdflib.URIRef(f"https://w3id.org/moro/enoam/data/{doc_num}/v1/1.html")
    subjects_for_doc = list(g.subjects(FRBR.embodiment, doc_uri))
    if not subjects_for_doc:
        print(f"[INFO] Nessun soggetto corrispondente a {doc_uri} trovato nel grafo per il file HTML {doc_id}.")
    else:
        subject = subjects_for_doc[0]
        dates = list(g.objects(subject, DCTERMS.date))
        if not dates:
            print(f"[INFO] Non è presente alcuna data (dcterms:date) per il documento '{doc_id}' (URI: {subject}).")
        else:
            d = dates[0]
            d = normalize_date_string(d)
            print(f"[FOUND] Per il documento '{doc_id}' è stata trovata la data: {d}")
            pub_date = d
    new_row = {"doc_id":doc_id, "title":title, "text":text, "publication_date":pub_date}
    return new_row


with open("./AMD/v0.2/paragraphs_test.csv", "r", encoding="utf-8") as f1:
    dict_reader = csv.DictReader(f1)
    paragraphs = list(dict_reader)

paragraphs = [find_date(g, row) for row in paragraphs]

with open("./AMD/v0.2/paragraphs_test2.csv", "w", encoding="utf-8") as f2:
    dict_writer = csv.DictWriter(f2, paragraphs[0].keys())
    dict_writer.writeheader()
    dict_writer.writerows(paragraphs)
