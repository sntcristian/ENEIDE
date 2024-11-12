# DigitalZibaldone (DZ) Entity Linking Dataset

## Description
This dataset has been derived from [Digital Zibaldone](https://digitalzibaldone.net/) the digital edition of *Zibaldone* by Giacomo Leopardi , covering texts written between 1823 and 1824. It includes annotations that reference people, locations, and works, linked where possible to entities in Wikidata. This dataset is designed for entity linking tasks, facilitating the identification and association of text references with entities in a knowledge base.

## Dataset Structure
The dataset is divided into **training** and **test** sets to support model training and evaluation. Each set contains manually annotated paragraphs, where references to specific entity types (persons, locations, and works) have been linked to Wikidata when available. Entities that do not exist in Wikidata (NIL entities) are also indicated, offering additional challenges for entity linking models.

## Dataset Statistics

### Training Set

| Statistic                          | Value |
|------------------------------------|-------|
| Number of paragraphs       | 689   |
| Total number of annotations | 2139  |
| Annotations for persons    | 1096  |
| Annotations for locations  | 407   |
| Annotations for works      | 636   |
| NIL annotations            | 156   |

### Test Set

| Statistic                        | Value |
|----------------------------------|-------|
| Number of paragraphs      | 260   |
| Total number of annotations | 764   |
| Annotations for persons   | 492   |
| Annotations for locations | 61    |
| Annotations for works     | 211   |
| NIL annotations           | 63    |

## Creation Date
November 12, 2024

## Purpose and Use
The **DigitalZibaldone Entity Linking Dataset** serves as a resource for training and evaluating entity linking models, particularly in historical texts. The presence of NIL annotations highlights instances where entities could not be found in existing knowledge bases, challenging models to handle out-of-knowledge-base (OOV) entities.

---

**Note**: This dataset provides a rich environment for testing entity linking systems within historical literary texts, where certain references may lack modern or conventional equivalents in current knowledge graphs like Wikidata.
