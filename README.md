# Rule interpretability analysis (including semantic coherence)
This repository presents a collection of scripts for analyzing results of user experiments aimed at evaluating interepretability of inductively learnt rules.

In addition to basic interpretability metrics like average antecedent length, this library computes *semantic coherence* using method described in:

    Gabriel, A., Paulheim, H., and Janssen, F.  Learning semantically coherent rules.  ECML/PKDD-14.  International Workshop on Interactions between Data Mining and Natural Language Processing , pp. 49–63, Nancy, France, September 2014. CEUR Workshop Proceedings


The analysis is done in two phases.
1. `compute_pairwise_sim.py` Attribute names are extracted from input datasets (.csv) and semantic similarity is precomputed between all pairs of attribute names and stored into a file, which is saved to each dataset's directory
2. `compute_rule_list_sim.py` parses input rule lists (plain text), extracts attribute names, counts number of attributes in the antecedent, and computes semantic coherence. The results are averages across all rules in in the input rule list.



## Inputs and outputs
The scripts assume the following directory structure
* data/{datasetname}/data.csv  - dataset, from which the rules were learnt
* data/{datasetname}/rules/{user-id}/mined.txt  - list of discovered rules
* data/{datasetname}/rules/{user-id}/modified.txt - list of rules after user intervention

The script `compute_pairwise_sim.py` saves pair-wise similarities for attribute names to:
* data/{datasetname}/word-pairs.csv

The script `compute_rule_list_sim.py` saves results to:
* [results.csv](results.csv)

## Sample datasets
The scripts come with some results of a proof-of-concept user study on UCI datasets used in the Gabriel et al paper. These are stored in the data folder.