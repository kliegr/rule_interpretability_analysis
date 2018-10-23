
# coding: utf-8

# In[10]:


import re
wordlistforsplit={"normalizedlosses":["normalized","loss"],"fueltype":["fuel","type"],"numofdoors":["number","of","doors"],
                 "bodystyle":["body","style"],"enginetype":["engine","type"],"numofcylinders":["number","of","cylinders"],"fuelsystem":["fuel","system"],"enginelocation":["engine","location"],"wheelbase":["wheel","base"],"curbweight":["curb","weight"],"enginesize":["engine","size"],"compressionratio":["compression","ratio"],"horsepower":["horse","power"],"peakrpm":["peak","rpm"],"citympg":["city","mpg"],"highwaympg":["highway","mpg"]}

#splitAttName("normalized_losses")
#splitAttName("normalizedlosses")
#splitAttName("normalized")
def splitAttName(wholename):
    wholename=wholename.lower()
    tokens=re.split('_|-',wholename)
    if len(tokens)>1:
        tokens.append(wholename)
    if wholename in wordlistforsplit:
        tokens.extend(wordlistforsplit[wholename])
    return tokens

