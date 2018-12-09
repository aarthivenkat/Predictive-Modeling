# Text-Mining PubMed Abstracts to Predict Gene Ontology Annotation from GO Consortium Database
### Aarthi Venkat

## I. Introduction
With the rise of Next-Generation Sequencing, complex and extremely large biological datasets have hit the bioinformatic world by storm, and, as such, the efforts to make sense of that data have simultaneously been put to the test [1]. One particular difficulty is in characterizing the ontology, or class of function, of genes — necessary for a variety of bioinformatic applications, from literature review to drug target identification and prioritization. Many institutions, including by the Gene Ontology Consortium (GO) and the Jackson Laboratory (MGI), have attempted to remedy differences in classifying gene function with a systematic dictionary of annotations. The dictionary is generally considered a tree of terms from the least specific root term to the highly specific leaf term, but it is actually a directed acyclic graph, with many terms belonging to several sub-categories, and the “level” of the term from the root not necessarily correlated to its specificity in annotation due to differences in height/sizes of subtrees (Figure 1) [1,2]. Bioinformatics scientists are attempting to remedy such issues through utilizing text-mining from scientific papers and comparing gene expression profiles between genes to develop similarity indexes and tools to further support such initiatives. In this project, I aim to contribute to these efforts by performing multi-class text classification of web-mined PubMed abstracts to Gene Ontology (GO) sub-categories.

##### Figure 1. Subset of Gene Ontology Annotation DAG with root term <i>biological process</i>
![](/final_figures/biological_process_DAG.JPG)