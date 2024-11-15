# Aldo Moro Digitale (AMD) Entity Linking Dataset

## Description
This dataset has been built using the digital edition of *Aldo Moro Digitale*, which contains texts produced between 1936 and 1978. The texts include manual annotations that highlight references to people, places, and organizations linked to entities on Wikidata, thus providing a valuable resource for *entity linking* tasks.

## Sampling Process
The dataset was sampled by selecting the first paragraph of each work in the edition. To ensure data quality and 
maintain a balanced distribution, paragraphs with an anomalous word count relative to a normal distribution were 
excluded. In order to divide dataset in training and testing, the data was split with a 75/25 ratio using a 
stratified sampling strategy based on the publication dates of the documents.

## Dataset Statistics

### Training Set

| Statistic                     | Value |
|-------------------------------|-------|
| Number of paragraphs          | 774   |
| Total number of annotations   | 1947  |
| Annotations for people        | 569   |
| Annotations for locations     | 766   |
| Annotations for organizations | 612   |
| NIL annotations               | 51    |

### Test Set

| Statistic                     | Value |
|-------------------------------|-------|
| Number of paragraphs          | 259   |
| Total number of annotations   | 669   |
| Annotations for people        | 216   |
| Annotations for locations     | 241   |
| Annotations for organizations | 212   |
| NIL annotations               | 15    |

## Creation Date
November 12, 2024

---

**Note**: This dataset represents a valuable resource for developing entity linking models, offering references to real entities linked to a knowledge graph (Wikidata). The dataset also includes entities not present in Wikidata (NIL), providing a research opportunity for identifying entities outside known knowledge graphs.
