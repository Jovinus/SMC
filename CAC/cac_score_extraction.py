# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import numpy as np
import re
from IPython.display import display
from tqdm.notebook import tqdm
pd.options.display.max_columns = None


# %%
df = pd.read_excel("./data/CCS_cleaning.xlsx")
df = df.filter(['처방일자#5', '검사결과내용#6'])
display(df)

# %% [markdown]
# ## 1. 정규표현식을 사용하기 전 사전 준비
# 1. 탐색 대상의 패턴을 파악한다.
# 2. 탐색 대상을 소문자로 변환한다.
#     * 탐색 대상이 대소문자 여부가 중요하지 않은 경우 소문자로 패턴을 정의하는 것이 효율 적이다.
# 
# %% [markdown]
# ### 탐색 대상의 패턴 확인하기

# %%
print(df.loc[0, "검사결과내용#6"])


# %%
print(df.loc[1, "검사결과내용#6"])

# %% [markdown]
# 위의 데이터의 경우 AJ-130 Score와 Volume Score를 추출하는 것이 목표이다.  
# 
# 위의 두 샘플을 봤을 때, 샘플 마다 작성하는 방식이 다른 것을 확인 가능하다.  
# 
# * Example 
#     * AJ 130 = score,  AJ-130 = socre  
# 
# 
# * 현재 진행하고 있는 Task에 대해서는 대소문자가 구분이 중요하지 않은 것으로 파악되기 때문에 소문자로 변환해준다.
# %% [markdown]
# ### 소문자 변환

# %%
df["tmp"] = df["검사결과내용#6"].str.lower()
display(df)

# %% [markdown]
# ## 2. 대표적인 패턴 모아서 보기

# %%
"""
CAC score by AJ-130 = (score), volume 130 score = (score)

CAC score = 0
CAC = 0

석회수치 51
석회용적 11

석회 수치 = 39
석회 용적 = 37

CAC score by AJ-130 = 1.7.

Calcium volume = 1.7

coronary calcium score = 0.



coronary arteryies에 calcification 없음.

limited evaluation for calcium scoring due to cabg

"""

# %% [markdown]
# 위의 패턴은 사전이 미리 조사한 패턴이다.  
# 다양한 패턴이 있으나 정규 표현식을 잘 정의하면 범용적으로 추출할 수 있을 것이다.  
# * Example  
#     * 석회 용적, 석회용적 => r"석회\s*용적" 으로 단일 패턴으로 기록이 가능하다.
# %% [markdown]
# ## 3. 패턴 정의하기
# %% [markdown]
# * AJ - 130 Score

# %%
## Reg_1에 있던 것을 참고하여 패턴을 정의하시오 
aj_0 = re.compile(r"\s*(?P<category>aj[-]130)\s*[=]\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_1 = re.compile(r"\s*cac\s*sc\w+\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_2 = re.compile(r"\s*cac\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_3 = re.compile(r"\s*석회수치\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_4 = re.compile(r"\s*석회\s*수치\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_5 = re.compile(r"\s*aj\s*130\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_6 = re.compile(r"\s*cal\w+\s*s\w+\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_7 = re.compile(r"\s*aj\s*130\s*sc\w*\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")
aj_8 = re.compile(r"\s*n\w*\s*cal\w*\s*in\s*cor\w*\s*art\w*\s*")
aj_9 = re.compile(r"\s*cor\w*\s*ar\w*에\s*cal\w*\s*없\w*\s*")
aj_10 = re.compile(r"\s*aj[-]130\s*sco\w*\s*=\s*(?P<a_score>[0-9]+[.]*[0-9]*)\s*")

# %% [markdown]
# * Volume Score

# %%
## Reg_1에 있던 것을 참고하여 패턴을 정의하시오 
vl_0 = re.compile(r"\s*volume\s*130\s*score\s*=\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
vl_1 = re.compile(r"\s*석회용적\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
vl_2 = re.compile(r"\s*석회\s*용적\s*=\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
vl_3 = re.compile(r"\s*volume\s*=\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")

# %% [markdown]
# ### 정의한 패턴이 동작하는지 확인

# %%
print(df.tmp[0])


# %%
aj = re.search(aj_5, df.loc[0, "tmp"])
vl = re.search(vl_3, df.loc[0, "tmp"])
print("AJ-130 score = ", aj.group("a_score"))
print("Volume 130 score = ", vl.group("v_score") )

# %% [markdown]
# ## 4. 모든 Row에 정규 표현식을 적용하여 패턴 찾기 
# %% [markdown]
# * AJ-130 Score

# %%
## Function 정의
def extract_aj_130_score(input_str):
    if re.search(aj_0, input_str) != None:
        return re.search(aj_0, input_str).group("a_score")
        
    elif re.search(aj_1, input_str) != None:
        return re.search(aj_1, input_str).group("a_score")
        
    elif re.search(aj_2, input_str) != None:
        return re.search(aj_2, input_str).group("a_score")
        
    elif re.search(aj_3, input_str) != None:
        return re.search(aj_3, input_str).group("a_score")
        
    elif re.search(aj_4, input_str) != None:
        return re.search(aj_4, input_str).group("a_score")
        
    elif re.search(aj_5, input_str) != None:
        return re.search(aj_5, input_str).group("a_score")
        
    elif re.search(aj_6, input_str) != None:
        return re.search(aj_6, input_str).group("a_score")
        
    elif re.search(aj_7, input_str) != None:
        return re.search(aj_7, input_str).group("a_score")
        
    elif re.search(aj_8, input_str) != None:
        return "0"
        
    elif re.search(aj_9, input_str) != None:
        return "0"
        
    elif re.search(aj_10, input_str) != None:
        return re.search(aj_10, input_str).group("a_score")
        
    else: return np.nan


# %%
## Pandas Apply 사용하기
df['AJT-130 Score'] = df['tmp'].apply(lambda x: extract_aj_130_score(str(x)))

# %% [markdown]
# * Volume Score

# %%
## Function 정의
def extract_volume_score(input_str):
    if re.search(vl_0, input_str) != None:
        return re.search(vl_0, input_str).group("v_score")
        
    elif re.search(vl_1, input_str) != None:
        return re.search(vl_1, input_str).group("v_score")
        
    elif re.search(vl_2, input_str) != None:
        return re.search(vl_2, input_str).group("v_score")
        
    elif re.search(vl_3, input_str) != None:
        return re.search(vl_3, input_str).group("v_score")
        
    else: return np.nan


# %%
## Pandas Apply 사용하기
df['Volume 130 Score'] = df['tmp'].apply(lambda x: extract_volume_score(str(x)))

# %% [markdown]
# ## 5. 추출 결과 리뷰
# * 위의 정규 표현식을 적용시에 숮자 뒤에 . 이 붙는 경우를 확인했다.
#     * str의 마지막에 '.'이 있는 경우 float으로 변환 못하기 때문에 str의 마지막 부분이 '.'인 경우 제외하는 후처리를 진행한다.

# %%
for i in tqdm(range(df.shape[0])):
    if str(df.loc[i, "AJT-130 Score"])[-1] == ".":
        df.loc[i,"AJT-130 Score"] = str(df.loc[i, "AJT-130 Score"])[0:-1]
    if str(df.loc[i, "Volume 130 Score"])[-1] == ".":
        df.loc[i,"Volume 130 Score"] = str(df.loc[i, "Volume 130 Score"])[0:-1]


# %%
df["AJT-130 Score"] = df["AJT-130 Score"].astype(float)
df["Volume 130 Score"] = df["Volume 130 Score"].astype(float)

# %% [markdown]
# ## 5. 최종 결과 확인

# %%
display(df)


# %%
df.isnull().sum()

# %% [markdown]
# ## 6. 추출되지 않는 경우를 리뷰
# * 추출 되지 않는 경우를 봤을 때, 이는 CABG, Stent와 같이 평가가 불가능한 경우인 것을 확인했다.
#     * 결측 이유가 있는 경우기 때문에 Reason과 같이 결측 이유를 적는 컬럼을 추가하다.

# %%
for i in df[df["AJT-130 Score"].isnull()].index:
    print("\nIndex: ", i)
    print(df.loc[i, "tmp"],"\n")


# %%
reason_re_1 = re.compile(r"\s*(?P<reason>cabg)\s*")
reason_re_2 = re.compile(r"\s*(?P<reason>stent)\s*")


# %%
for i in tqdm(df[df["AJT-130 Score"].isnull()].index):
    
    if re.search(reason_re_1, str(df.loc[i, "tmp"])) != None:
        df.loc[i, "Reason"] = re.search(reason_re_1, str(df.loc[i, "tmp"])).group("reason")
    
    elif re.search(reason_re_2, str(df.loc[i, "tmp"])) != None:
        df.loc[i, "Reason"] = re.search(reason_re_2, str(df.loc[i, "tmp"])).group("reason")
    else: continue

display(df)

# %% [markdown]
# ### 결과 확인

# %%
df.query('Reason.notnull()', engine='python')

# %% [markdown]
# ## 7. 의뢰자가 원하는 형태로 변환해 주기

# %%
for i in df[df["Reason"].notnull()].index:
    if df.loc[i, "Reason"] == "stent":
        df.loc[i, "Note"] = "STENT 시술로 측정 불가"
        df.loc[i, "Comment"] = "STENT 상태로 CAC 측정에 제한적임"
    elif df.loc[i, "Reason"] == "cabg":
        df.loc[i, "Note"] = "CABG 수술로 측정 불가"
        df.loc[i, "Comment"] = "CABG 상태로 CAC 측정이 제한적임"


# %%
df.query('Reason.notnull()', engine='python')

# %% [markdown]
# ## 8. 결과 저장하기
# * Regular Expression 적용을 위해 임의로 만든 Column을 제거하고서 데이터를 저장하기
# * 데이터를 Excel로 저장하거나, DB로 업데이트 하는 방법이 있다. 

# %%
df.drop(columns=["Reason", "tmp"], inplace=True)
display(df)


