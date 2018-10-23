
# coding: utf-8

# In[1]:


import itertools
import os
import pandas as pd
import re
import numpy as np
from  splitattname import splitAttName
from sematch.semantic.similarity import WordNetSimilarity
from ruleanalysissettings import *
wns = WordNetSimilarity()
simscores=[]
def processDataFile(path):
    df=pd.read_csv(path+"data.csv")
    # omit class label
    colnames=df.columns.values[0:-1].tolist()
    # if there are multi-word expressions, break them to single words    
    ## templist=list(map(lambda x: re.split('_|-',x.lower()),colnames))
    
    names = list()
    for colname in colnames:
        print(colname)
        names.extend(splitAttName(colname))
        print(names)

    list_pairs=list(itertools.permutations(names,2))
    simscores=list(map(lambda x: wns.word_similarity(x[0], x[1],"lin"), list_pairs))
    df_pairs = pd.DataFrame.from_records(list_pairs, columns=["word1","word2"])
    df_pairs["similarity"]=simscores
    
    #similarity of word with itself is 1.0
    simwithitself = pd.DataFrame(
    {'word1': names,
     'word2': names,
     "similarity":list(np.ones(len(names)))
    })
    df_pairs=df_pairs.append(simwithitself, ignore_index=True)
    df_pairs.to_csv(path+"word-pairs.csv",index=False,sep=",")
    return(df_pairs)

initial_path=os.getcwd()
for dataset in datasets:
    print("computing similarity for word pairs in dataset " + dataset)
    os.chdir(initial_path)
    os.chdir(basepath+os.sep+dataset)
    df=processDataFile("."+os.sep)

