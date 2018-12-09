# Text-Mining PubMed Abstracts to Predict Gene Ontology Annotation from GO Consortium Database
### Aarthi Venkat

## I. Introduction
With the rise of Next-Generation Sequencing, complex and extremely large biological datasets have hit the bioinformatic world by storm, and, as such, the efforts to make sense of that data have simultaneously been put to the test [1]. One particular difficulty is in characterizing the ontology, or class of function, of genes — necessary for a variety of bioinformatic applications, from literature review to drug target identification and prioritization. Many institutions, including by the Gene Ontology Consortium (GO) and the Jackson Laboratory (MGI), have attempted to remedy differences in classifying gene function with a systematic dictionary of annotations. The dictionary is generally considered a tree of terms from the least specific root term to the highly specific leaf term, but it is actually a directed acyclic graph, with many terms belonging to several sub-categories, and the “level” of the term from the root not necessarily correlated to its specificity in annotation due to differences in height/sizes of subtrees (Figure 1) [1,2]. Bioinformatics scientists are attempting to remedy such issues through utilizing text-mining from scientific papers and comparing gene expression profiles between genes to develop similarity indexes and tools to further support such initiatives. In this project, I aim to contribute to these efforts by performing multi-class text classification of web-mined PubMed abstracts to Gene Ontology (GO) sub-categories.

##### Figure 1. Subset of Gene Ontology Annotation DAG with root term <i>biological process</i>
![](/final_figures/biological_process_DAG.JPG)

## II. Data Curation and Cleaning
I was able to [download](http://www.geneontology.org/page/download-go-annotations) GO annotations from the Gene Ontology Consortium database [4] for Homo sapiens (originally from GO) and Mus musculus (originally from MGI). According to GO, these annotations have all been quality-checked and verified. It should be noted that GO is supposed to be species-agnostic, and as such, species should not play a factor in annotation differences so much as different scientists, goals, and consortiums may. I chose datasets for which a GO term was directly connected to a PubMed ID, so that I (1) could web-mine the paper abstract from the ID and (2) directly connect GO IDs to the abstract to write the model.  

The columns of interest to me had the following form: 
"GO:XXXXXX	PMID:XXXXX".

There are several issues with this. First, there are <b>47,338 GO terms</b> in the dictionary, due to the need for high complexity and specificity in gene annotation. However, as a classification problem, it is impossible to expect to train a model with 50,000 datapoints on so many classes. So, I understood that for each GO term, I had to traverse up the tree to a level just below the root term ("level 1"). However, an additional issue arose: imbalanced, overlapping classes (Figure 2) [2]. Notice how the “level 1” terms under root have count of descendants ranging from 100 to 18,000.

##### Figure 2. Imbalanced and Overlapping Level 1 GO Classes 
![](/final_figures/level_1_DAG.JPG)  

While imbalanced classes is not always an issue, and annotating the majority while ignoring the minority may actually be favorable in some use cases, for this purpose, the majority is <i>cellular process</i>, which gives little indication of the gene or protein product’s function. Finally, it is difficult to use level as a feature as it is for such an acyclic graph, due to the fact that there are multiple paths from a single annotation to the root, and multiple levels for a node.  

As such, I turned to GOATOOLS, a Python library for GO analysis designed to, for one use case, group GO terms not by level, but by scientific use and literature [2]. I also performed some additional filtering steps here. First, GOATOOLS had three categories for broad and hard to define abstracts — “Misc.”, “Broad”, and “Grow”. As such, I removed all PubMed entries for which these were the only annotations. Further, many entries had multiple GO terms associated with them, and for these I chose a GO term randomly to assign to avoid multiple classes within an abstract, but I showed preferential treatment against “binding”, which does not express the cell’s specific function. Finally, I removed categories with less than 150 entries and have little to none predictive power in terms of a statistical model. As such, I sectioned my dataset, which initially had <b>17,160 unique GO terms into 44 categories</b>, and attempted to perform multi-class categorization with these categories (Figure 3).  

##### Figure 3. GOATOOLS categories and distribution of abstracts
![](/final_figures/GO_categories.JPG)

The second step to data curation involved web-mining for PubMed abstracts given the ID. Due to time limitation and NCBI restrictions, I could only afford to mine roughly over 50,000 entries in order to still filter out some GO terms. After mining the abstracts and removing entries for which there was no abstract available, I ended up with <b>50,023 PubMed Abstracts</b> with GO categories as labels to them.  

