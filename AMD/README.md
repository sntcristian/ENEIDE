# AMD Entity Linking Dataset

## Description
This dataset has been built using the digital edition of *Aldo Moro Digitale*, which contains texts produced between 1936 and 1978. The texts include manual annotations that highlight references to people, places, and organizations linked to entities on Wikidata, thus providing a valuable resource for *entity linking* tasks.

## Sampling Process
The dataset was sampled by selecting the first paragraph of each work in the edition. To ensure data quality and maintain a balanced distribution, paragraphs with an anomalous word count relative to a normal distribution were excluded.

## Dataset Statistics

| Statistic                        | Value |
|----------------------------------|-------|
| Number of documents              | 1033  |
| Total number of annotations      | 2616  |
| References to people             | 785   |
| References to places             | 1007  |
| References to organizations      | 824   |
| Entities not in Wikidata (NIL)   | 64    |

## Creation Date
November 12, 2024

## To Do
- **Split the dataset into training and testing**: To properly support model training and evaluation for entity linking, the dataset will be divided into two subsets, one for training and one for testing. The split will be done in a way that ensures the representativeness of the different annotation categories within the dataset.

---

**Note**: This dataset represents a valuable resource for developing entity linking models, offering references to real entities linked to a knowledge graph (Wikidata). The dataset also includes entities not present in Wikidata (NIL), providing a research opportunity for identifying entities outside known knowledge graphs.
