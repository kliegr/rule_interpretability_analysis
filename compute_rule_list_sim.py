
# coding: utf-8

# In[ ]:


import re
import logging
import pandas as pd
import itertools
import pdb
import numpy as np
from splitattname import splitAttName
from ruleanalysissettings import *

logging.basicConfig(filename='compute.log',level=logging.DEBUG)
rootLogger = logging.getLogger()
logFormatter = logging.Formatter("%(asctime)s [%(threadName)-12.12s] [%(levelname)-5.5s]  %(message)s")

# print also to console
consoleHandler = logging.StreamHandler()
consoleHandler.setFormatter(logFormatter)
rootLogger.addHandler(consoleHandler)


def parseRule(rule):
    rule=rule.lower().split("=>")[0]
    return getAttNames(rule)

def getAttNames(text):
    return re.findall(r"[^ (]+(?=\()",text)


def getPairwiseAttSimForRule(rule):  
    logging.debug("processing rule:" + rule)
    attNames=parseRule(rule)
    list_pairs=list(itertools.combinations(attNames,2))
    logging.debug("att pairs:" + str(list_pairs))
    pairsimilarities = [None] * len(list_pairs)

    for i in range(0,len(list_pairs)):
        # we assume that both attribute names can be composed of multiword expressions
        # we will compute similarity between pairs words from both attribute names and output the average similarity
        w1tokens=splitAttName(list_pairs[i][0])            
        w2tokens=splitAttName(list_pairs[i][1])            
        # remove words which are not indexed
        # word1 and word2 should contain the same unique words
        for word in w1tokens:
            if sum(df_sims.word1==word)==0:                
                w1tokens.remove(word)
        for word in w2tokens:
            if sum(df_sims.word1==word)==0:                
                w2tokens.remove(word)
        if  len(w1tokens) == 0 or len(w2tokens) == 0 :
            # this attribute pair has no word pair with available sim value, setting average similarity to 0.
            avgsim=0
        else:    
            pairs=list(itertools.product(w1tokens,w2tokens))
            logging.debug("word pairs:" + str(pairs))        
            # there might be multiple rows matching the condition, we select the first one with .iloc[0]                    
            try:
                # avgsim=np.mean(list(map(lambda x: df_sims[(df_sims.word1==x[0]) & (df_sims.word2==x[1])].iloc[0].similarity,pairs)))
                total=0
                for pair in pairs:
                    simvalues=df_sims[(df_sims.word1==pair[0]) & (df_sims.word2==pair[1])]
                    total+=simvalues.iloc[0].similarity
                avgsim=total/len(pairs)
                
                
            except:
                pdb.set_trace()
        pairsimilarities[i] = avgsim
    # remove pair similarities which were previously marked for removal
    # pairsimilarities = [sim for sim in pairsimilarities if sim != -1]
    return(len(attNames),pairsimilarities)

def getPairwiseAttSimForRuleList(text): 
    lines = text.split("\n")
    startFlag=False
    pairwSims=[]
    semCoherence=[]
    rulecount=0
    totalAttCount = 0    
    for line in lines:
        if not(startFlag) and line=="":
            startFlag=True
        if startFlag:
            if line.startswith("*"):
                rulecount=rulecount+1
                continue #skip default rule
            if line.strip()=="":
                continue
            rulecount=rulecount+1
            attCount,pairwforrule=getPairwiseAttSimForRule(line)
            totalAttCount=totalAttCount+attCount
            pairwSims.append(pairwforrule)
            semCoherence.append(np.mean(pairwforrule))
    if startFlag==False:
        raise Exception("Error: Empty line delimiting header and list of rules not found")
    return(rulecount,totalAttCount,semCoherence,pairwSims)
    


# In[ ]:

filename_wordpairsims="data/{}/word-pairs.csv"
filename_mined="data/{}/rules/{}/mined.txt"
filename_modified="data/{}/rules/{}/modified.txt"
datasetnames=list()
original= list()
modified = list()
df = pd.DataFrame()

p_IDs = []
p_datasets = []
p_versions = []
p_avgSemCoherences_orig = []
p_avgSemCoherences_mod = []
p_totalAttCounts_orig = []
p_totalAttCounts_mod = []
p_totalRuleListCounts_orig = []
p_totalRuleListCounts_mod = []

for rulelist in rulelists:
    folders=rulelists[rulelist]
    for folder in folders:        
        version = 1 if "A" in folder else 2  
        
        simfile=filename_wordpairsims.format(rulelist)
        logging.debug(simfile)
        df_sims=pd.read_csv(simfile)
        mfn=filename_mined.format(rulelist,folder)
        logging.debug(mfn)
        mined_file = open(mfn,'r')
        text_mined=mined_file.read()
        rulecount_orig,totalAttCount_orig,semCoherence_orig,pairwSims_orig=getPairwiseAttSimForRuleList(text_mined)
        # we skip nans when computing mean because for some rules we get nan as semantic coherence, this is largely caused by the corresponding rules having length of 1
        p_avgSemCoherences_orig.append(np.nanmean(semCoherence_orig))
        datasetnames.append(rulelist)
        print("total average semantic coherence for original rule list",p_avgSemCoherences_orig[-1])
        
        
        modfn=filename_modified.format(rulelist,folder)
        modified_file = open(modfn,'r')
        logging.debug(modfn)
        text_modified=modified_file.read()
        rulecount_mod,totalAttCount_mod,semCoherence_mod,pairwSims_mod=getPairwiseAttSimForRuleList(text_modified)
        # we skip nans when computing mean because for some rules we get nan as semantic coherence, this is largely caused by the corresponding rules having length of 1
        p_avgSemCoherences_mod.append(np.nanmean(semCoherence_mod))
        print("total average semantic coherence for modified rule list",p_avgSemCoherences_mod[-1])

        p_IDs.append(folder)
        p_datasets.append(rulelist)
        p_versions.append(version)
        
        p_totalAttCounts_orig.append(totalAttCount_orig)
        p_totalAttCounts_mod.append(totalAttCount_mod)
        
        p_totalRuleListCounts_orig.append(rulecount_orig)
        p_totalRuleListCounts_mod.append(rulecount_mod)             
                
df=pd.DataFrame(data={"id":p_IDs,"dataset":p_datasets,"version":p_versions,"attributes_orig":p_totalAttCounts_orig,"attributes_mod":p_totalAttCounts_mod,"rules_orig": p_totalRuleListCounts_orig,"rules_mod": p_totalRuleListCounts_mod,"coherence_orig": p_avgSemCoherences_orig,"coherence_mod": p_avgSemCoherences_mod}, columns=['id', 'dataset', 'version', 'attributes_orig', 'attributes_mod', 'rules_orig', 'rules_mod', 'coherence_orig', 'coherence_mod'])
df.to_csv("results.csv")
