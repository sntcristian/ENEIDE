# ENEIDE Dataset

A diachronic, multi-domain resource for Entity Linking in Italian, spanning two centuries of humanistic documents.

## Overview

The ENEIDE corpus is a comprehensive dataset for Entity Linking (EL) in Italian, semi-automatically extracted from two multi-domain Scholarly Digital Editions (SDEs):

- **Digital Zibaldone (DZ)**: Giacomo Leopardi's *Zibaldone di pensieri* (1817-1832) 
- **Aldo Moro Digitale (AMD)**: Complete works of Italian politician Aldo Moro (1930s-1978) 

This dataset enables the evaluation of EL systems on humanistic documents rich in contextual and diachronic challenges, covering heterogeneous textual genres across the 19th and 20th centuries.

## Dataset Features

### Sources
- **Digital Zibaldone**: 4,500+ pages of intellectual reflections on literature, history, philosophy and philology
- **Aldo Moro Digitale**: Political, legal, and journalistic texts from a prominent Italian politician

### Entity Types
- **DZ**: Person (`PER`), Location (`LOC`), Literary Work (`WORK`)
- **AMD**: Person (`PER`), Location (`LOC`), Organization (`ORG`)

### Key Characteristics
- Diachronic coverage (19th-20th centuries)
- Multi-domain content
- Historical variations in entity surface forms
- Indirect entity references
- NIL (Not-in-Link) entities for entities not covered by Wikidata

## Dataset Statistics

### Overall Distribution
| Dataset | Documents | Annotations | Unique Entities | NIL Entities | Overlap (train+dev vs test) |
|---------|-----------|-------------|----------------|--------------|---------------------------|
| DZ      | 1,050     | 4,279       | 623            | 298          | 93.19%                    |
| AMD     | 1,062     | 4,027       | 583            | 86           | 75.38%                    |

### Split Distribution (Train/Dev/Test: 70/15/15)
| Dataset | Train Docs | Dev Docs | Test Docs | Train Annotations | Dev Annotations | Test Annotations |
|---------|------------|----------|-----------|-------------------|-----------------|------------------|
| DZ      | 735        | 157      | 158       | 2,935             | 727             | 617              |
| AMD     | 743        | 159      | 160       | 2,766             | 604             | 657              |

## Data Quality

Quality assessment conducted by domain experts on 100 samples per dataset:

| Metric    | DZ    | AMD   |
|-----------|-------|-------|
| Precision | 96.8% | 91.6% |
| Recall    | 94.4% | 70.6% |
| F1-Score  | 95.6% | 79.8% |

## Data Curation Process

To improve annotation coverage, a multi-step enhancement pipeline was implemented:
1. Extraction and expert validation of frequent surface forms with Wikidata IDs
2. Tagging of missing mentions in text using an Index of Named Entities
3. Application of Italian StanzaNLP NER model for unannotated entities
4. Final expert validation


## Repository Structure

```
ENEIDE/
├── data/
│   ├── DZ/v1.0/
│   │   ├── v1.0/
│   │   ├── assessment/
│   │   └── README.md
│   └── AMD/
│       ├── v1.0/
│       ├── assessment/
│       └── README.md
├── eval/
│   ├── eval_ed.py
│   ├── eval_el.py
│   ├── eval_ner.py
│   └── results/
├── src/
│   ├── scripts_DZ/
│   ├── scripts_AMD/
│   └── utils/
├── get_stats.ipynb
├── LICENSE
└── README.md
```

## Data Format

Each dataset split is provided in two CSV files:

### Paragraphs CSV (`paragraphs_*.csv`)
Contains information about the text documents:

| Column | Description |
|--------|-------------|
| `doc_id` | Unique document identifier |
| `title` | Document title |
| `text` | Full text content |
| `publication_date` | Publication date (YYYY-MM-DD format) |

**Example:**
```csv
doc_id,title,text,publication_date
document_110001.html,Saluto,"Miei cari aspiranti, chiamato dalla fiducia di mons. Arcivescovo[1] ...",1932-07-01
```

### Annotations CSV (`annotations_*.csv`)
Contains named entity annotations:

| Column | Description |
|--------|-------------|
| `doc_id` | Document identifier (matches paragraphs CSV) |
| `start_pos` | Start character position of entity mention |
| `end_pos` | End character position of entity mention |
| `surface` | Entity surface form/mention text |
| `type` | Entity type (`PER`, `LOC`, `ORG`, `WORK`) |
| `identifier` | Wikidata identifier (or NIL if not in Wikidata) |

**Example:**
```csv
doc_id,start_pos,end_pos,surface,type,identifier
document_110001.html,53,64,Arcivescovo,PER,Q34634425
```

## Usage

### Loading the Dataset

```python
import pandas as pd

# Load DZ training data
dz_paragraphs_train = pd.read_csv('data/DZ/v1.0/paragraphs_train.csv')
dz_annotations_train = pd.read_csv('data/DZ//v1.0/annotations_train.csv')

# Load AMD training data
amd_paragraphs_train = pd.read_csv('data/AMD/v1.0/paragraphs_train.csv')
amd_annotations_train = pd.read_csv('data/AMD/v1.0/annotations_train.csv')

# Example: Get all annotations for a specific document
doc_id = 'document_110001.html'
doc_text = dz_paragraphs_train[dz_paragraphs_train['doc_id'] == doc_id]['text'].iloc[0]
doc_annotations = dz_annotations_train[dz_annotations_train['doc_id'] == doc_id]

print(f"Document: {doc_text[:100]}...")
print(f"Annotations: {len(doc_annotations)} entities found")
```



## Citation

TO BE UPDATED

## License

This dataset is released under MIT License. Please refer to the LICENSE file for more details.

## Acknowledgments

- [Digital Zibaldone](https://digitalzibaldone.net/) project for providing the TEI/XML-encoded edition of Leopardi's work
- [Aldo Moro Digitale](https://aldomorodigitale.unibo.it/) project for the RDFa-encoded corpus of Aldo Moro's works


## Dataset Availability

The ENEIDE dataset will be made fully available upon acceptance.