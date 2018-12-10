# Text-Mining PubMed Abstracts to Predict Gene Ontology Annotation from GO Consortium Database
### Aarthi Venkat

## I. Abstract
After web-mining PubMed Abstracts and assigning a single high-level GO term to each PubMed abstract, I used a TF-IDF vectorization and LinearSVC Model to perform Multi-Class Categorization of 50,000 PubMed Abstracts. Using precision, recall, and F-score as metrics for success of the model, I acheived average success (F=0.44), expected considering the overlapping and hierarchical nature of the annotation of the abstracts, indicating the need for further integrated approaches with quantitative data, as well as annotation systems with a classical tree structure that allows for intuitive categorization by level.  

## II. Introduction
With the rise of Next-Generation Sequencing, complex and extremely large biological datasets have hit the bioinformatic world by storm, and, as such, the efforts to make sense of that data have simultaneously been put to the test [1]. One particular difficulty is in characterizing the ontology, or class of function, of genes — necessary for a variety of bioinformatic applications, from literature review to drug target identification and prioritization. Many institutions, including by the Gene Ontology Consortium (GO) and the Jackson Laboratory (MGI), have attempted to remedy differences in classifying gene function with a systematic dictionary of annotations. The dictionary is generally considered a tree of terms from the least specific root term to the highly specific leaf term, but it is actually a directed acyclic graph, with many terms belonging to several sub-categories, and the “level” of the term from the root not necessarily correlated to its specificity in annotation due to differences in height/sizes of subtrees (Figure 1) [1,2]. Bioinformatics scientists are attempting to remedy such issues through utilizing text-mining from scientific papers and comparing gene expression profiles between genes to develop similarity indexes and tools to further support such initiatives. In this project, I aim to contribute to these efforts by performing multi-class text classification of web-mined PubMed abstracts to Gene Ontology (GO) sub-categories.  

Similar datasets and similar tasks have been published, utilizing integrated datasets with multiple text-mined phenotypic accounts, gene expression profiles, and published network and association accounts to corroborate the models [3,6]. The conclusions from similar works attest that you can get an average degree of accuracy from phenotypic text accounts, but in order to apply high confidence to the model, you would need a more precise, quantitative measure by which to analyze genes. I was not able to include gene expression profiles due to the limitations of this assignment (memory and time, largely), but these would be important features to add if I were to create a tool or module for this purpose. That being said, for the purposes of this project - an exploratory, fun and introductory analysis - text-mining PubMed Abstracts seems like a good starting point.  

##### Figure 1. Subset of Gene Ontology Annotation DAG with root term <i>biological process</i>
<img src="/final_figures/biological_process_DAG.JPG" width="780">  

## III. Data Curation and Cleaning
I was able to [download](http://www.geneontology.org/page/download-go-annotations) GO annotations from the Gene Ontology Consortium database [4] for Homo sapiens (originally from GO) and Mus musculus (originally from MGI). According to GO, these annotations have all been quality-checked and verified. It should be noted that GO is supposed to be species-agnostic, and as such, species should not play a factor in annotation differences so much as different scientists, goals, and consortiums may. I chose datasets for which a GO term was directly connected to a PubMed ID, so that I (1) could web-mine the paper abstract from the ID and (2) directly connect GO IDs to the abstract to write the model.  

The columns of interest to me had the following form: 
"GO:XXXXXX	PMID:XXXXX".

There are several issues with this. First, there are <b>47,338 GO terms</b> in the dictionary, due to the need for high complexity and specificity in gene annotation. However, as a classification problem, it is impossible to expect to train a model with 50,000 datapoints on so many classes. So, I understood that for each GO term, I had to traverse up the tree to a level just below the root term ("level 1"). However, an additional issue arose: imbalanced, overlapping classes (Figure 2) [2]. Notice how the “level 1” terms under root have count of descendants ranging from 100 to 18,000.

##### Figure 2. Imbalanced and Overlapping Level 1 GO Classes 
<img src="/final_figures/level_1_DAG.JPG" width="500">  

While imbalanced classes is not always an issue, and annotating the majority while ignoring the minority may actually be favorable in some use cases, for this purpose, the majority is <i>cellular process</i>, which gives little indication of the gene or protein product’s function. Finally, it is difficult to use level as a feature as it is for such an acyclic graph, due to the fact that there are multiple paths from a single annotation to the root, and multiple levels for a node.  

As such, I turned to GOATOOLS, a Python library for GO analysis designed to, for one use case, group GO terms not by level, but by scientific use and literature [2]. I also performed some additional filtering steps here. First, GOATOOLS had three categories for broad and hard to define abstracts — “Misc.”, “Broad”, and “Grow”. As such, I removed all PubMed entries for which these were the only annotations. Further, many entries had multiple GO terms associated with them, and for these I chose a GO term randomly to assign to avoid multiple classes within an abstract, but I showed preferential treatment against “binding”, which does not express the cell’s specific function. Finally, I removed categories with less than 150 entries and have little to none predictive power in terms of a statistical model. As such, I sectioned my dataset, which initially had <b>17,160 unique GO terms into 44 categories</b>, and attempted to perform multi-class categorization with these categories (Table 1).  

##### Table 1. GOATOOLS categories and distribution of abstracts
| Category                      | PubMed Abstract Count |
|-------------------------------|-----------------------|
| ATPase                        | 272                   |
| Bacteria/Virus                | 1020                  |
| Cell Death                    | 2266                  |
| Cytokine                      | 848                   |
| DNA Binding                   | 1192                  |
| DNA Repair                    | 362                   |
| Golgi                         | 410                   |
| Immune                        | 757                   |
| Immune Adaptive               | 331                   |
| Immune Innate                 | 462                   |
| Lipid                         | 806                   |
| Reproduction                  | 433                   |
| Signaling                     | 1286                  |
| Binding                       | 8960                  |
| Carbohydrate                  | 330                   |
| Carboxylic                    | 229                   |
| Cell Adhesion                 | 859                   |
| Cell Activation               | 229                   |
| Chromatin                     | 1157                  |
| Chromosome                    | 386                   |
| Clotting                      | 203                   |
| Cofactor                      | 162                   |
| Cytoskeleton                  | 2225                  |
| Cytosol                       | 778                   |
| Detoxification                | 975                   |
| Differentiation/Proliferation | 2689                  |
| Embryo                        | 3452                  |
| Endoplasmic Reticulum         | 762                   |
| Enzyme                        | 388                   |
| Extracellular                 | 929                   |
| Homeostasis                   | 487                   |
| Hormone                       | 517                   |
| Hydrolase                     | 231                   |
| Ion                           | 1370                  |
| Membrane                      | 2885                  |
| Neuro                         | 1740                  |
| Nucleus                       | 2557                  |
| Peptide                       | 474                   |
| Protein                       | 1080                  |
| Protein Breakdown             | 1304                  |
| Receptor                      | 433                   |
| Stimulus                      | 238                   |
| Transcription                 | 1501                  |
| Vesicle                       | 225                   |

The second step to data curation involved web-mining for PubMed abstracts given the ID. Due to time limitation and NCBI restrictions, I could only afford to mine roughly over 50,000 entries in order to still filter out some GO terms. After mining the abstracts and removing entries for which there was no abstract available, I ended up with <b>50,200 PubMed Abstracts</b> with GO categories as labels to them.  

## IV. Predictive Task  
Modeling from the literature in the field of biomedical text-mining, such as work done by Groth et al with TF-IDF vectorization of phenotypic descriptions of genes and work by Malone et al with phenotypic and expression profiles integrated, I aim to use the text from the abstracts to predict the GO category, so as to alleviate the time and money spent by those painstakingly annotating genes from the literature, not to mention the inaccuracies and differences between groups in these annotations [3,6]. Malone et al evaluated their TF-IDF model with precision, recall, and an F-score for each category, so I maintained the same in this project [Figure 4] [3,5].  

##### Figure 4. Methods for Evaluating Model  
<img src="/final_figures/formulas.JPG" width="500">  

Regarding the features I will use, I will use a <b>TF-IDF Transformer</b> to create a vector representation of the text with unigrams and bigrams. I processed this text by first removing punctuation (except dashes, as these may be useful in biological data), transforming all the characters to lowercase, disregarding English stopwords, and encoding in Latin-1.  

The first step in validating that the text is an accurate representation of the category, and is thus a valid feature to use, is to employ sklearn.feature_selection chi2 to find the the most correlated with each of the products. The results are summarized in Table 2.

##### Table 2. Top Correlated Unigrams and Bigrams for each Category  

| Category                      | Top 2 Unigrams                 | Top 2 Bigrams                                      |   |
|-------------------------------|--------------------------------|----------------------------------------------------|---|
| ATPase                        | atpase, myo19                  | atpase activity, dependent atpase                  |   |
| Bacteria/Virus                | infection, lps                 | antimicrobial activity, gram positive              |   |
| Cell Death                    | apoptosis, death               | cell death, induced apoptosis                      |   |
| Cytokine                      | il, ifn                        | ifn gamma, il 12                                   |   |
| DNA Binding                   | dna, promoter                  | dna binding, single stranded                       |   |
| DNA Repair                    | repair, nhej                   | dna repair, excision repair                        |   |
| Golgi                         | golgi, tgn                     | golgi apparatus, trans golgi                       |   |
| Immune                        | hypermutation, cat2            | antibody responses, autoimmune lesions             |   |
| Immune Adaptive               | thymocyte, thymocytes          | thymocyte development, single positive             |   |
| Immune Innate                 | hair, follicle                 | hair follicle, hair cell                           |   |
| Lipid                         | fatty, cholestorol             | fatty acid, beta oxidation                         |   |
| Reproduction                  | sperm, male                    | germ cells, zona pellucida                         |   |
| Signaling                     | ltp, synaptic                  | term potentiation, mossy fiber                     |   |
| Binding                       | interaction, crystal           | crystal structure, sh2 domain                      |   |
| Carbohydrate                  | glucose, fructose              | hepatic glucose, glucose production                |   |
| Carboxylic                    | mthfs, qprtase                 | mk 886, microsomal gst                             |   |
| Cell Adhesion                 | adhesion, integrin             | cell adhesion, cell cell                           |   |
| Cell Activation               | csr, hobit                     | class switch, switch recombination                 |   |
| Chromatin                     | histone, chromatin             | histone h3, histone h4                             |   |
| Chromosome                    | kinetochore, kinetochores      | synaptonemal complex, chromosome alignment         |   |
| Clotting                      | platelet, platelets            | platelet aggregation, platelet activation          |   |
| Cofactor                      | mocs1, coq                     | molybdenum cofactor, cofactor moco                 |   |
| Cytoskeleton                  | actin, centrosome              | mitotic spindle, actin cytoskeleton                |   |
| Cytosol                       | bloc, cytosol                  | 6a rna, rna methylation                            |   |
| Detoxification                | reductase, dehydrogenase       | aldehyde dehydrogenase, trans retinal              |   |
| Differentiation/Proliferation | proliferation, differentiation | cell proliferation, progenitor cells               |   |
| Embryo                        | embryos, patterning            | mutant embryos, neural tube                        |   |
| Endoplasmic Reticulum         | er, reticulum                  | endoplasmic reticulum, reticulum er                |   |
| Enzyme                        | myo9b, pinx1                   | gap activity, myosin ixb                           |   |
| Extracellular                 | secreted, exosomes             | variable region, sequence variable                 |   |
| Homeostasis                   | erythropoiesis, erythroid      | erythroid differentiation, xbp ls                  |   |
| Hormone                       | insulin, glucose               | insulin secretion, stimulated insulin              |   |
| Hydrolase                     | gcase, ssej                    | astrocytes mast, rasgrp ras                        |   |
| Ion                           | copper, mcu                    | calcium binding, 12 activation                     |   |
| Membrane                      | transporter, membrane          | plasma membrane, xenopus oocytes                   |   |
| Neuro                         | neurons, learning              | learning memory, excitatory inhibitory             |   |
| Nucleus                       | nuclear, nucleus               | nuclear localization, pre mrna                     |   |
| Peptide                       | translation, ribosomal         | mitochondrial translation, mitochrondrial ribosome |   |
| Protein                       | cskmt, kinase                  | oxall ctt, assemble clathrin                       |   |
| Protein Breakdown             | ubiquitin, e3                  | ubiquitin ligase, e3 ubiquitin                     |   |
| Receptor                      | ht5a, hmc3r                    | effects kainate, oocytes yields                    |   |
| Stimulus                      | ethanol, scn12a                | d3 ko, protein apobec                              |   |
| Transcription                 | promoter, transcription        | dna binding, transcription factor                  |   |
| Vesicle                       | melanosome, melanosomes        | melanosome transport, hsp60 related                |   |

## V. Results and Discussion  

I fit parameters to the training set and transformed the dataset to get the feature matrix, and used this and the label vector to fit a <b>LinearSVC model</b> due to the need for large-scale multi-class classification. I optimized this model by training with different parameters, such as only unigrams, only bigrams, and both, and with and without punctuation. I ultimately found the model worked best without punctuation and including dashes, as well as with both unigrams and bigrams. The strength of this model is that is that it is designed to scale to multi-class classification better than methods such as Random Forest Classifier [3], and the weakness is that it takes a while to train and it, also like the others, lacks significant predictive power simply due to the variety in scientific text and lack of data for this project. Nonetheless, for an exploratory task like this personal project, it will suffice as a starting point. The precision, recall and F-score for each category, as well as the average of all the categories, is presented in Table 3.  

##### Table 3. Precision, Recall and F-score for LinearSVC for each category  

| Category                      | Precision | Recall | F-score | Support |
|-------------------------------|-----------|--------|---------|---------|
| binding                       | 0.35      | 0.14   | 0.20    | 98      |
| enzyme                        | 0.54      | 0.63   | 0.58    | 350     |
| chromatin                     | 0.52      | 0.68   | 0.59    | 3017    |
| protein_breakdown             | 0.58      | 0.32   | 0.42    | 108     |
| embryo                        | 0.56      | 0.13   | 0.21    | 71      |
| differentiation_proliferation | 0.30      | 0.09   | 0.14    | 79      |
| neuro                         | 0.48      | 0.38   | 0.43    | 304     |
| cytoskeleton                  | 0.53      | 0.61   | 0.57    | 729     |
| DNA_binding                   | 0.51      | 0.44   | 0.47    | 390     |
| nucleus                       | 0.53      | 0.32   | 0.40    | 136     |
| chromosome                    | 0.52      | 0.49   | 0.50    | 65      |
| Cell Death                    | 0.65      | 0.16   | 0.26    | 67      |
| cofactor                      | 0.36      | 0.30   | 0.32    | 269     |
| cell adhesion                 | 0.56      | 0.60   | 0.58    | 734     |
| ion                           | 0.39      | 0.08   | 0.13    | 261     |
| homeostasis                   | 0.50      | 0.67   | 0.58    | 298     |
| carboxylic                    | 0.38      | 0.49   | 0.43    | 833     |
| Signaling                     | 0.38      | 0.31   | 0.34    | 391     |
| Immune_innate                 | 0.53      | 0.62   | 0.57    | 130     |
| clotting                      | 0.48      | 0.70   | 0.57    | 1134    |
| hormone                       | 0.50      | 0.47   | 0.49    | 257     |
| Golgi                         | 0.43      | 0.16   | 0.23    | 128     |
| receptor                      | 0.42      | 0.31   | 0.36    | 299     |
| detoxification                | 0.49      | 0.41   | 0.44    | 150     |
| cell_activation               | 0.31      | 0.12   | 0.17    | 170     |
| Cytokine                      | 0.34      | 0.25   | 0.29    | 168     |
| cytosol                       | 0.45      | 0.06   | 0.11    | 80      |
| membrane                      | 0.33      | 0.19   | 0.24    | 246     |
| Immune                        | 0.46      | 0.37   | 0.41    | 115     |
| peptide                       | 0.30      | 0.11   | 0.16    | 142     |
| transcription                 | 0.46      | 0.30   | 0.36    | 435     |
| extracellular                 | 0.39      | 0.46   | 0.42    | 245     |
| Reproduction                  | 0.41      | 0.55   | 0.47    | 941     |
| protein                       | 0.45      | 0.58   | 0.51    | 570     |
| vesicle                       | 0.42      | 0.39   | 0.40    | 854     |
| hydrolase                     | 0.44      | 0.22   | 0.29    | 149     |
| endoplasmic_reticulum         | 0.25      | 0.07   | 0.11    | 359     |
| Bacteria/virus                | 0.38      | 0.33   | 0.35    | 405     |
| Lipid                         | 0.00      | 0.00   | 0.00    | 95      |
| DNA_repair                    | 0.43      | 0.41   | 0.42    | 148     |
| ATPase                        | 0.35      | 0.15   | 0.20    | 447     |
| stimulus                      | 0.18      | 0.03   | 0.05    | 67      |
| carbohydrate                  | 0.33      | 0.32   | 0.33    | 499     |
| Immune_adaptive               | 0.48      | 0.14   | 0.22    | 79      |
| avg / total                   | 0.45      | 0.46   | 0.44    | 16512   |

It is interesting to note that binding has an F-score of 0.2, which is poor considering it is the most frequent in the dataset by far. Looking at the categories for which the F-score is highest, including enzyme, immune_innate, protein, and cell adhesion, I can infer that categories that are not so specific so as to only have a few entries, but are not so broad so as to have much diversity within the category performed the best. The average precision was 0.45, the average recall 0.46, and the average F-score 0.44.  

The main issue with further optimization of my model was that many of the PubMed abstracts overlapped in at least one category. Intuitively, hormone and signaling will overlap, as will other pathways, regulatory elements, and reviews on a large variety of topics. While the initial preprocessed data was highly specific (recall, over 40000 GO terms exist, each with their own particular definition), it has little predictive power. On the other hand, aggregating categories to the point where they overlap or don’t have much biological significance (e.g. cellular process) has little necessity. For future purposes, it would be good to systematically clean the data to maintain gene names with punctuation or important capitalization, as well as reconcile the overlapping categories with a more complex model. Future projects should also use other types of data, such as more precise, quantitative features, and try to avoid using different species or consortiums, as these would be confounding factors to the analysis.  

Machine learning and predictive models have a profound application in bioinformatics and biotechnology, and I welcome the challenge of complex and high-dimensional datasets in order to work towards intelligent predictive solutions in biotechnology and healthcare. Finally, of all the interesting conclusions to be made, the one I can be certain of is that systematized annotation is a step in the right direction, but requires much more than phenotypic text.  

## VI. References  

http://www.geneontology.org/
https://www.nature.com/articles/s41598-018-28948-z
https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-10-S11-S20
http://www.geneontology.org/gene-associations/gene_association.mgi.gz
https://medinform.jmir.org/2015/3/e28/
https://bmcbioinformatics.biomedcentral.com/articles/10.1186/1471-2105-9-136

