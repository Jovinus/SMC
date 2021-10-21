# %%
import pandas as pd
import re
from datatable import fread
from tqdm import tqdm
import numpy as np

# %%

## Minimal to Mild



## Mild to Moderate
mild_to_moderate_0 = re.compile(r"\s*경[가-힣]*\s*중[가-힣]*\s*(사이|\s*)\s*지[가-힣]*\s*")
mild_to_moderate_1 = re.compile(r"\s*mild\s*to\s*mod\w+\s*fat\w+\s*liv\w+\s*")
mild_to_moderate_2 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mild\s*to\s*mode\w+\s*deg\w+\s*")
mild_to_moderate_3 = re.compile(r"\s*지방[가-힣]*\s*([,]|[-])*\s*경[가-힣]*\s*중[가-힣]*\s*")
mild_to_moderate_4 = re.compile(r"\s*지방[가-힣]*\s*진[가-힣]*\s*([,]|[-])*\s*경[가-힣]*\s*중[가-힣]*\s*")
mild_to_moderate_5 = re.compile(r"\s*지방[가-힣]*\s*호[가-힣]*\s*([,]|[-])*\s*경[가-힣]*\s*중[가-힣]*\s*")
mild_to_moderate_6 = re.compile(r"\s*mi\w+\s*to\s*mod\w+\s*fatt\w+\s*liv\w+\s*")
mild_to_moderate_7 = re.compile(r"\s*[(]\s*mi\w+\s*[-][-][>]\s*mod\w+\s*deg\w+\s*")
mild_to_moderate_8 = re.compile(r"\s*mi\w+\s*to\s*mod\w+\s*\w+\s*fatt\w+\s*liv\w+\s*")
mild_to_moderate_9 = re.compile(r"\s*fat\w+\s*liv\w+\s*[(]\s*mild\s*[-][-][>]\s*mild\s*to\s*mod\w+\s*")
mild_to_moderate_10 = re.compile(r"\s*간[가-힣]*\s*경[가-힣]*\s*중[가-힣]*\s*")
mild_to_moderate_11 = re.compile(r"\s*[(]\s*mi\w+\s*[-][>]\s*mod\w+\s*deg\w+\s*")
mild_to_moderate_12 = re.compile(r"\s*mi\w+\s*to\s*mod\w+\s*deg\w+\s*")

## Moderate to Severe
moderate_to_severe_0 = re.compile(r"\s*중[가-힣]*\s*심[가-힣]*\s*지방간\s*")
moderate_to_severe_1 = re.compile(r"\s*mod\w+\s*to\s*sev\w+\s*fatt\w+\s*liv\w+\s*")
moderate_to_severe_2 = re.compile(r"\s*mod\w+\s*to\s*se\w+\s*inho\w+\s*fat\w+\s*liv\w+\s*")
moderate_to_severe_3 = re.compile(r"\s*간에\s*중[가-힣]*에서\s*심[가-힣]*\s*정도의\s*지방[가-힣]*\s*")
moderate_to_severe_4 = re.compile(r"\s*mod\w+\s*to\s*sev\w+\s*deg\w+\s*of\s*fatt\w+\s*liv\w+\s*")
moderate_to_severe_5 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mod\w+\s*to\s*se\w+\s*inho\w+\s*fat\w+\s*liv\w+\s*")
moderate_to_severe_6 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mod\w+\s*to\s*se\w+\s*")
moderate_to_severe_7 = re.compile(r"\s*간[가-힣]*\s*중[가-힣]*\s*심[가-힣]\s*")
moderate_to_severe_8 = re.compile(r"\s*mod\w+\s*to\s*sev\w+\s*")
moderate_to_severe_9 = re.compile(r"\s*[-][>]\s*mod\w+\s*to\s*se\w+\s*")

## Minimal
minimal_0 = re.compile(r"\s*경미[가-힣]*\s*지방[가-힣]*\s*")
minimal_1 = re.compile(r"\s*mini\w+\s*fatt\w+\s*liv\w+\s*")
minimal_2 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mini\w+\s*degr\w+s*")
minimal_3 = re.compile(r"\s*min\w+\s*deg\w+\s*of\s*(the|\s*)*\s*fatt\w+\s*")
minimal_4 = re.compile(r"\s*fat\w+\s*liv\w+\s*of\s*min\w+\s*s*")

## Mild
mild_0 = re.compile(r"\s*경증[가-힣]*\s*지방간\s*")
mild_1 = re.compile(r"\s*mild\s*fat\w+\s*liv\w+\s*")
mild_2 = re.compile(r"\s*no\s*chan\w+\s*of\s*mild\s*fat\w+\s*liv\w+\s*")
mild_3 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mild\s*degr\w+s*")
mild_4 = re.compile(r"\s*mild\s*inhom\w+\s*fatt\w+\s*liv\w+\s*")
mild_5 = re.compile(r"\s*지[가-힣]*\s*([,]|[-])*\s*경증\s*")
mild_6 = re.compile(r"\s*지[가-힣]*\s*호[가-힣]*\s*([,]|[-])*\s*경증\s*")
mild_7 = re.compile(r"\s*[(]\s*mod\w+\s*[-][-][>]\s*mi\w+\s*deg\w+\s*")
mild_8 = re.compile(r"\s*mild\s*fat\w*\s*")
mild_9 = re.compile(r"\s*mild\s*un\w+\s*fat\w*\s*")
mild_10 = re.compile(r"\s*mil\w+\s*deg\w+\s*of\s*(the|\s*)*\s*fatt\w+\s*")
mild_11 = re.compile(r"\s*mild\s*het\w+\s*fat\w*\s*")
mild_12 = re.compile(r"\s*fat\w+\s*liv\w+\s*[(]\s*mod\w+\s*[-][-][>]\s*mild\s*")
mild_13 = re.compile(r"\s*경증[가-힣]*\s*지방[가-힣]*\s*")
mild_14 = re.compile(r"\s*[-][>]\s*mild\s*")
mild_15 = re.compile(r"\smil\w+\s*and\s*dif\w+\s*fat\w+\s*")
mild_16 = re.compile(r"\s*fat\w+\s*liv\w+\s*of\s*mil\w+\s*s*")

## Moderate
moderate_0 = re.compile(r"\s*중[가-힣]*\s*지방간\s*")
moderate_1 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mod\w+\s*deg\w+\s*")
moderate_2 = re.compile(r"\s*mod\w+\s*fatt\w+\s*liv\w+\s*")
moderate_3 = re.compile(r"\s*no\s*cha\w+\s*of\s*mod\w+\s*fat\w+\s*liv\w+\s*")
moderate_4 = re.compile(r"\s*지방[가-힣]*\s*(진[가-힣]*)*\s*([,]|[-])*\s*중[가-힣]*\s*")
moderate_5 = re.compile(r"\s*mod\w+\s*deg\w+\s*of\s*fat\w+\s*liv\w+\s*")
moderate_6 = re.compile(r"\s*mod\w+\s*inho\w+\s*fat\w+\s*liv\w+\s*")
moderate_7 = re.compile(r"\s*fat\w+\s*liv\w+\s*[(]\s*mild\s*[-][-][>]\s*mode\w+\s*")
moderate_8 = re.compile(r"\s*fat\w+\s*liv\w+\s*deg\w+\s*of\s*mode\w+\s*")
moderate_9 = re.compile(r"\s*fat\w+\s*liv\w+\s*of\s*mode\w+\s*")
moderate_10 = re.compile(r"\s*간[가-힣]*\s*중[가-힣]*\s*지[가-힣]\s*")
moderate_11 = re.compile(r"\s*지[가-힣]*\s*호[가-힣]*\s*중[가-힣]*\s*")
moderate_12 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*mild\s*[-]*mod\w+\s*")
moderate_13 = re.compile(r"\s*[-][>]\s*mod\w+\s*deg\w+\s*")

## Severe
severe_0 = re.compile(r"\s*심[가-힣]*\s*지[가-힣]*\s*")
severe_1 = re.compile(r"\s*sev\w+\s*fat\w+\s*liv\w+\s*")
severe_2 = re.compile(r"\s*fat\w+\s*liv\w+\s*[,]*\s*sev\w+\s*deg\w+\s*")
severe_3 = re.compile(r"\s*지[가-힣]*\s*진[가-힣]+\s*심[가-힣]*\s*")
severe_4 = re.compile(r"\s*지[가-힣]*\s*진행[가-힣]*\s*심[가-힣]*\s*")
severe_5 = re.compile(r"\s*지[가-힣]*\s*[-]*\s*심[가-힣]*\s*")
severe_6 = re.compile(r"\s*심[가-힣]*\s*정[가-힣]*\s*지[가-힣]*\s*")

## Normal
normal_0 = re.compile(r"\s*정[가-힣]*\s*상[가-힣]*\s*초[가-힣]*\s*")
normal_1 = re.compile(r"\s*정[가-힣]*\s*범[가-힣]*\s*상[가-힣]*\s*초[가-힣]*\s*")
normal_2 = re.compile(r"\s*int\w+\s*imp\w+\s*pre\w+\s*mild\s*fat\w+\s*liv\w+\s*")
normal_3 = re.compile(r"\s*nor\w+\s*mild\s*fat\w+\s*liv\w+\s*")
normal_4 = re.compile(r"\s*dis\w+\s*pre\w+\s*no\w+\s*fat\w+\s*liv\w+\s*")
normal_5 = re.compile(r"\s*no\s*def\w+\s*abn\w+\s*on\s*liv\w+\s*")
normal_6 = re.compile(r"\s*지방간\s*호[가-힣]*\s*([,]|[-])*\s*정상\s*")
normal_7 = re.compile(r"\s*inte\w+\s*imp\w+\s*fatt\w+\s*liv\w+\s*")
normal_8 = re.compile(r"\s*지방간\s*([,]|[-])*\s*정상\s*")
normal_9 = re.compile(r"\s*inte\w+\s*imp\w+\s*of\s*fatt\w+\s*liv\w+\s*")

def extract_fattyliver_degree(input_txt):
    ## Mild to Moderate
    if re.search(mild_to_moderate_0, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_1, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_2, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_3, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_4, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_5, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_6, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_7, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_8, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_9, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_10, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_11, input_txt) != None:
        return 'Mild to Moderate'
    elif re.search(mild_to_moderate_12, input_txt) != None:
        return 'Mild to Moderate'
    
    ## Moderate to Severe
    if re.search(moderate_to_severe_0, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_1, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_2, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_3, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_4, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_5, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_6, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_7, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_8, input_txt) != None:
        return 'Moderate to Severe'
    elif re.search(moderate_to_severe_9, input_txt) != None:
        return 'Moderate to Severe'
    
    ## Minimal
    if re.search(minimal_0, input_txt) != None:
        return 'Minimal'
    elif re.search(minimal_1, input_txt) != None:
        return 'Minimal'
    elif re.search(minimal_2, input_txt) != None:
        return 'Minimal'
    elif re.search(minimal_3, input_txt) != None:
        return 'Minimal'
    elif re.search(minimal_4, input_txt) != None:
        return 'Minimal'
    
    ## Mild
    if re.search(mild_0, input_txt) != None:
        return 'Mild'  
    elif re.search(mild_1, input_txt) != None:
        return 'Mild'
    elif re.search(mild_2, input_txt) != None:
        return 'Mild'
    elif re.search(mild_3, input_txt) != None:
        return 'Mild'
    elif re.search(mild_4, input_txt) != None:
        return 'Mild'
    elif re.search(mild_5, input_txt) != None:
        return 'Mild'
    elif re.search(mild_6, input_txt) != None:
        return 'Mild'
    elif re.search(mild_7, input_txt) != None:
        return 'Mild'
    elif re.search(mild_8, input_txt) != None:
        return 'Mild'
    elif re.search(mild_9, input_txt) != None:
        return 'Mild'
    elif re.search(mild_10, input_txt) != None:
        return 'Mild'
    elif re.search(mild_11, input_txt) != None:
        return 'Mild'
    elif re.search(mild_12, input_txt) != None:
        return 'Mild'
    elif re.search(mild_13, input_txt) != None:
        return 'Mild'
    elif re.search(mild_14, input_txt) != None:
        return 'Mild'
    elif re.search(mild_15, input_txt) != None:
        return 'Mild'
    elif re.search(mild_16, input_txt) != None:
        return 'Mild'
    
    ## Moderate
    if re.search(moderate_0, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_1, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_2, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_3, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_4, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_5, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_6, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_7, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_8, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_9, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_10, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_11, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_12, input_txt) != None:
        return 'Moderate'
    elif re.search(moderate_13, input_txt) != None:
        return 'Moderate'
    
    ## Severe
    if re.search(severe_0, input_txt) != None:
        return 'Severe'
    elif re.search(severe_1, input_txt) != None:
        return 'Severe'
    elif re.search(severe_2, input_txt) != None:
        return 'Severe'
    elif re.search(severe_3, input_txt) != None:
        return 'Severe'
    elif re.search(severe_4, input_txt) != None:
        return 'Severe'
    elif re.search(severe_5, input_txt) != None:
        return 'Severe'
    elif re.search(severe_6, input_txt) != None:
        return 'Severe'
    
    ## Normal
    if re.search(normal_0, input_txt) != None:
        return 'Absent'
    elif re.search(normal_1, input_txt) != None:
        return 'Absent'
    elif re.search(normal_2, input_txt) != None:
        return 'Absent'
    elif re.search(normal_3, input_txt) != None:
        return 'Absent'
    elif re.search(normal_4, input_txt) != None:
        return 'Absent'
    elif re.search(normal_5, input_txt) != None:
        return 'Absent'
    elif re.search(normal_6, input_txt) != None:
        return 'Absent'
    elif re.search(normal_7, input_txt) != None:
        return 'Absent'
    elif re.search(normal_8, input_txt) != None:
        return 'Absent'
    elif re.search(normal_9, input_txt) != None:
        return 'Absent'

DATAPATH = "../../data/fatty_liver/ABD_SONO_to_2013.csv"
# %%
if __name__ == '__main__':
    df_source = fread(DATAPATH, 
                      encoding='utf-8-sig', 
                      na_strings=['', 'NA']).to_pandas()
    tqdm.pandas()
    df_source['FLD_reg'] = df_source['tmp'].progress_apply(extract_fattyliver_degree)
    df_source['FLD_reg'] = np.where(df_source['FLD_reg'].isnull(), 'Absent', df_source['FLD_reg'])
# %%
    pd.crosstab(df_source['FLD_reg'], df_source['FLD_Degree_NM'])
# %%
