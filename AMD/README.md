# Aldo Moro Digitale (AMD) Entity Linking Dataset

## Description
This dataset has been built using the digital edition of [*Aldo Moro Digitale*](https://aldomorodigitale.unibo.it/), which contains texts produced 
between 1936 and 1978. The texts include manual annotations that highlight references to people, places, and organizations linked to entities on Wikidata, thus providing a valuable resource for *entity linking* tasks.

## Sampling Process
The dataset was sampled by selecting the first paragraph of each work in the edition. To ensure data quality and 
maintain a balanced distribution, paragraphs with an anomalous word count relative to a normal distribution were 
excluded. In order to divide dataset in training, development and testing, the data was split with a 70/15/15 ratio 
using a 
stratified sampling strategy based on the creation date of the documents.

## Entity Tagset

List of annotated entities (coarse level only):

* Person (PER)
* Location (LOC)
* Organisation (ORG)

## Dataset Statistics

### Training Set

| Statistic                     | Value |
|-------------------------------|-------|
| Number of documents           | 751   |
| Total number of annotations   | 1,997 |
| Annotations for people        | 581   |
| Annotations for locations     | 764   |
| Annotations for organizations | 652   |
| NIL annotations               | 46    |


### Development Set

| Statistic                     | Value |
|-------------------------------|-------|
| Number of documents           | 161   |
| Total number of annotations   | 427   |
| Annotations for people        | 116   |
| Annotations for locations     | 163   |
| Annotations for organizations | 148   |
| NIL annotations               | 10    |

### Test Set

| Statistic                     | Value |
|-------------------------------|-------|
| Number of documents           | 161   |
| Total number of annotations   | 404   |
| Annotations for people        | 132   |
| Annotations for locations     | 157   |
| Annotations for organizations | 115   |
| NIL annotations               | 12    |

## Creation Date
December 12, 2024

---

**Note**: This dataset represents a valuable resource for developing entity linking models, offering references to real entities linked to a knowledge graph (Wikidata). The dataset also includes entities not present in Wikidata (NIL), providing a research opportunity for identifying entities outside known knowledge graphs.
