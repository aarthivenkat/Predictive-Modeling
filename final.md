# Text-Mining PubMed Abstracts to Predict Gene Ontology Annotation from GO Consortium Database
### Aarthi Venkat

## I. Introduction
With the rise of Next-Generation Sequencing, complex and extremely large biological datasets have hit the bioinformatic world by storm, and, as such, the efforts to make sense of that data have simultaneously been put to the test [1]. One particular difficulty is in characterizing the ontology, or class of function, of genes — necessary for a variety of bioinformatic applications, from literature review to drug target identification and prioritization. Many institutions, including by the Gene Ontology Consortium (GO) and the Jackson Laboratory (MGI), have attempted to remedy differences in classifying gene function with a systematic dictionary of annotations. The dictionary is generally considered a tree of terms from the least specific root term to the highly specific leaf term, but it is actually a directed acyclic graph, with many terms belonging to several sub-categories, and the “level” of the term from the root not necessarily correlated to its specificity in annotation due to differences in height/sizes of subtrees (Figure 1) [1,2]. Bioinformatics scientists are attempting to remedy such issues through utilizing text-mining from scientific papers and comparing gene expression profiles between genes to develop similarity indexes and tools to further support such initiatives. In this project, I aim to contribute to these efforts by performing multi-class text classification of web-mined PubMed abstracts to Gene Ontology (GO) sub-categories.

##### Figure 1. Subset of Gene Ontology Annotation DAG with root term <i>biological process</i>
<img src="/final_figures/biological_process_DAG.JPG" width="780">  

## II. Data Curation and Cleaning
I was able to [download](http://www.geneontology.org/page/download-go-annotations) GO annotations from the Gene Ontology Consortium database [4] for Homo sapiens (originally from GO) and Mus musculus (originally from MGI). According to GO, these annotations have all been quality-checked and verified. It should be noted that GO is supposed to be species-agnostic, and as such, species should not play a factor in annotation differences so much as different scientists, goals, and consortiums may. I chose datasets for which a GO term was directly connected to a PubMed ID, so that I (1) could web-mine the paper abstract from the ID and (2) directly connect GO IDs to the abstract to write the model.  

The columns of interest to me had the following form: 
"GO:XXXXXX	PMID:XXXXX".

There are several issues with this. First, there are <b>47,338 GO terms</b> in the dictionary, due to the need for high complexity and specificity in gene annotation. However, as a classification problem, it is impossible to expect to train a model with 50,000 datapoints on so many classes. So, I understood that for each GO term, I had to traverse up the tree to a level just below the root term ("level 1"). However, an additional issue arose: imbalanced, overlapping classes (Figure 2) [2]. Notice how the “level 1” terms under root have count of descendants ranging from 100 to 18,000.

##### Figure 2. Imbalanced and Overlapping Level 1 GO Classes 
<img src="/final_figures/level_1_DAG.JPG" width="500">  

While imbalanced classes is not always an issue, and annotating the majority while ignoring the minority may actually be favorable in some use cases, for this purpose, the majority is <i>cellular process</i>, which gives little indication of the gene or protein product’s function. Finally, it is difficult to use level as a feature as it is for such an acyclic graph, due to the fact that there are multiple paths from a single annotation to the root, and multiple levels for a node.  

As such, I turned to GOATOOLS, a Python library for GO analysis designed to, for one use case, group GO terms not by level, but by scientific use and literature [2]. I also performed some additional filtering steps here. First, GOATOOLS had three categories for broad and hard to define abstracts — “Misc.”, “Broad”, and “Grow”. As such, I removed all PubMed entries for which these were the only annotations. Further, many entries had multiple GO terms associated with them, and for these I chose a GO term randomly to assign to avoid multiple classes within an abstract, but I showed preferential treatment against “binding”, which does not express the cell’s specific function. Finally, I removed categories with less than 150 entries and have little to none predictive power in terms of a statistical model. As such, I sectioned my dataset, which initially had <b>17,160 unique GO terms into 44 categories</b>, and attempted to perform multi-class categorization with these categories (Figure 3).  

##### Figure 3. GOATOOLS categories and distribution of abstracts
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

## III. Predictive Task  
Modeling from the literature in the field of biomedical text-mining, such as work done by Groth et al with TF-IDF vectorization of phenotypic descriptions of genes and work by Malone et al with phenotypic and expression profiles integrated, I aim to use the text from the abstracts to predict the GO category, so as to alleviate the time and money spent by those painstakingly annotating genes from the literature, not to mention the inaccuracies and differences between groups in these annotations [3,6]. Malone et al evaluated their TF-IDF model with precision, recall, and an F-score for each category, so I maintained the same in this project [Figure 4] [3,5].  

##### Figure 4. Methods for Evaluating Model  
<img src="/final_figures/formulas.JPG" width="500">  

Regarding the features I will use, I will use a <b>TF-IDF Transformer</b> to create a vector representation of the text with unigrams and bigrams. I processed this text by first removing punctuation (except dashes, as these may be useful in biological data), transforming all the characters to lowercase, disregarding English stopwords, and encoding in Latin-1.  

The first step in validating that the text is an accurate representation of the category, and is thus a valid feature to use, is to employ sklearn.feature_selection chi2 to find the the most correlated with each of the products. The results are summarized in Figure 5.

##### Figure 5. Top Correlated Unigrams and Bigrams for each Category  

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
