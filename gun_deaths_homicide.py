# -*- coding: utf-8 -*-
"""
@author: rerwin21
"""

#%%
import pandas as pd
import re
import os
import seaborn


#%%
os.chdir("/home/rerwin21/gun_deaths/")


#%%
homicides = pd.read_csv("homicide_rate.csv")
guns = pd.read_csv("guns_100_ppl.csv")


#%% clean out garbage of string data
def clean_guns(string):
    string = re.sub("\[.*\]","", string)
    string = re.sub(u"\xc2\xa0", "", string)
    string = string.strip()
    return string


#%% clean up data and sort
guns = guns.applymap(clean_guns)
homicides["Country"] = homicides["Country"].apply(clean_guns)

guns.sort_values("Country", inplace=True)
homicides.sort_values("Country", inplace=True)


#%% join them together
homicide_guns = pd.merge(homicides,
                         guns,
                         on="Country",
                         how="left")
                         

#%%
# how many NaN's
homicide_guns.isnull().sum()


#%% which ones where missed
misses = homicide_guns[homicide_guns["Guns per 100 People"].isnull()]


#%% drop for now: go with the matches
# I'll check to see if I can manually find any additional matches later
homicide_guns = homicide_guns.dropna()


#%% change the column type to float
homicide_guns.loc[:, "Guns per 100 People"] = homicide_guns.loc[:, "Guns per 100 People"].apply(lambda x: float(x))


#%%
preg = seaborn.regplot("Guns per 100 People",
                       "Homicide Rate",
                       data=homicide_guns)

preg.text(95, 5, "United States", withdash=True)                
preg.figure
preg.figure.savefig('preg.png')

                
#%%
pjnt = seaborn.jointplot("Guns per 100 People", 
                         "Homicide Rate", 
                         data=homicide_guns, 
                         kind="reg")                   