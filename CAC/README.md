# ipynb file 내의 결과를 Markdown으로 Export한 결과 입니다.

```python
import pandas as pd
import numpy as np
import re
from IPython.display import display
from tqdm.notebook import tqdm
pd.options.display.max_columns = None
```


```python
df = pd.read_excel("./data/CCS_cleaning.xlsx")
df = df.filter(['처방일자#5', '검사결과내용#6'])
display(df)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-08-02</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2019-02-26</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2019-02-12</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31971</th>
      <td>2018-04-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
    </tr>
    <tr>
      <th>31972</th>
      <td>2019-08-13</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
    </tr>
    <tr>
      <th>31973</th>
      <td>2018-06-21</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
    </tr>
    <tr>
      <th>31974</th>
      <td>2017-04-20</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
    </tr>
    <tr>
      <th>31975</th>
      <td>2018-10-26</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
    </tr>
  </tbody>
</table>
<p>31976 rows × 2 columns</p>
</div>


## 1. 정규표현식을 사용하기 전 사전 준비
1. 탐색 대상의 패턴을 파악한다.
2. 탐색 대상을 소문자로 변환한다.
    * 탐색 대상이 대소문자 여부가 중요하지 않은 경우 소문자로 패턴을 정의하는 것이 효율 적이다.


### 탐색 대상의 패턴 확인하기


```python
print(df.loc[0, "검사결과내용#6"])
```

    ▣ 검사정보 및 소견
    
    CORONARY CT, CALCIUM SCORE (NON-CONTRAST)
    
    Coronary artery의 calcification 이 있음: 
      LAD, RCA,  Left main artery.
    
    Cardiac chamber dimension의 이상 소견이 없음.
    
    Aortic aneurysm (descending thoracic aorta)이 없음.
    Aortic ectasia (ascending thoracic aorta)가 없음.
    
    다른 부위에 석회가 있음: aortic valve,
    
    ▣ 결론 및 진단
    
    Coronary artery calcium score:
    Degree of plaque burden: moderate, 
    AJ 130 = 243
    Volume = 226
    
    Percentile rank: >95%.
    
    ▣ 의견
    
    임상 관찰 또는 추적 검사
    
    ------------------------------------------------------------------------------------------------



```python
print(df.loc[1, "검사결과내용#6"])
```

    ▣ 검사정보 및 소견
    
    
    
    CORONARY CT, CALCIUM SCORE (NON-CONTRAST)
    
    
    
      LAD와 RCA에 segmental dense calcification들이 있음.
    
      Descending thoracic aorta에 multiple calcification들이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    CAC score by AJ-130 = 940.56, volume 130 score = 795.92
    
    High degree of plaque burden.
    
    Percentile rank 95% 이상.
    
    
    
    
    
    


위의 데이터의 경우 AJ-130 Score와 Volume Score를 추출하는 것이 목표이다.  

위의 두 샘플을 봤을 때, 샘플 마다 작성하는 방식이 다른 것을 확인 가능하다.  

* Example 
    * AJ 130 = score,  AJ-130 = socre  


* 현재 진행하고 있는 Task에 대해서는 대소문자가 구분이 중요하지 않은 것으로 파악되기 때문에 소문자로 변환해준다.

### 소문자 변환


```python
df["tmp"] = df["검사결과내용#6"].str.lower()
display(df)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
      <th>tmp</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-08-02</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2019-02-26</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2019-02-12</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31971</th>
      <td>2018-04-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
    </tr>
    <tr>
      <th>31972</th>
      <td>2019-08-13</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
    </tr>
    <tr>
      <th>31973</th>
      <td>2018-06-21</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
    </tr>
    <tr>
      <th>31974</th>
      <td>2017-04-20</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
    </tr>
    <tr>
      <th>31975</th>
      <td>2018-10-26</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
    </tr>
  </tbody>
</table>
<p>31976 rows × 3 columns</p>
</div>


## 2. 대표적인 패턴 모아서 보기


```python
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
```




    '\nCAC score by AJ-130 = (score), volume 130 score = (score)\n\nCAC score = 0\nCAC = 0\n\n석회수치 51\n석회용적 11\n\n석회 수치 = 39\n석회 용적 = 37\n\nCAC score by AJ-130 = 1.7.\n\nCalcium volume = 1.7\n\ncoronary calcium score = 0.\n\n\n\ncoronary arteryies에 calcification 없음.\n\nlimited evaluation for calcium scoring due to cabg\n\n'



위의 패턴은 사전이 미리 조사한 패턴이다.  
다양한 패턴이 있으나 정규 표현식을 잘 정의하면 범용적으로 추출할 수 있을 것이다.  
* Example  
    * 석회 용적, 석회용적 => r"석회\s*용적" 으로 단일 패턴으로 기록이 가능하다.

## 3. 패턴 정의하기

* AJ - 130 Score


```python
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
```

* Volume Score


```python
## Reg_1에 있던 것을 참고하여 패턴을 정의하시오 
vl_0 = re.compile(r"\s*volume\s*130\s*score\s*=\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
vl_1 = re.compile(r"\s*석회용적\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
vl_2 = re.compile(r"\s*석회\s*용적\s*=\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
vl_3 = re.compile(r"\s*volume\s*=\s*(?P<v_score>[0-9]+[.]*[0-9]*)\s*")
```

### 정의한 패턴이 동작하는지 확인


```python
print(df.tmp[0])
```

    ▣ 검사정보 및 소견
    
    coronary ct, calcium score (non-contrast)
    
    coronary artery의 calcification 이 있음: 
      lad, rca,  left main artery.
    
    cardiac chamber dimension의 이상 소견이 없음.
    
    aortic aneurysm (descending thoracic aorta)이 없음.
    aortic ectasia (ascending thoracic aorta)가 없음.
    
    다른 부위에 석회가 있음: aortic valve,
    
    ▣ 결론 및 진단
    
    coronary artery calcium score:
    degree of plaque burden: moderate, 
    aj 130 = 243
    volume = 226
    
    percentile rank: >95%.
    
    ▣ 의견
    
    임상 관찰 또는 추적 검사
    
    ------------------------------------------------------------------------------------------------



```python
aj = re.search(aj_5, df.loc[0, "tmp"])
vl = re.search(vl_3, df.loc[0, "tmp"])
print("AJ-130 score = ", aj.group("a_score"))
print("Volume 130 score = ", vl.group("v_score") )
```

    AJ-130 score =  243
    Volume 130 score =  226


## 4. 모든 Row에 정규 표현식을 적용하여 패턴 찾기 

* AJ-130 Score


```python
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
```


```python
## Pandas Apply 사용하기
df['AJT-130 Score'] = df['tmp'].apply(lambda x: extract_aj_130_score(str(x)))
```

* Volume Score


```python
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
```


```python
## Pandas Apply 사용하기
df['Volume 130 Score'] = df['tmp'].apply(lambda x: extract_volume_score(str(x)))
```

## 5. 추출 결과 리뷰
* 위의 정규 표현식을 적용시에 숮자 뒤에 . 이 붙는 경우를 확인했다.
    * str의 마지막에 '.'이 있는 경우 float으로 변환 못하기 때문에 str의 마지막 부분이 '.'인 경우 제외하는 후처리를 진행한다.


```python
for i in tqdm(range(df.shape[0])):
    if str(df.loc[i, "AJT-130 Score"])[-1] == ".":
        df.loc[i,"AJT-130 Score"] = str(df.loc[i, "AJT-130 Score"])[0:-1]
    if str(df.loc[i, "Volume 130 Score"])[-1] == ".":
        df.loc[i,"Volume 130 Score"] = str(df.loc[i, "Volume 130 Score"])[0:-1]
```


      0%|          | 0/31976 [00:00<?, ?it/s]



```python
df["AJT-130 Score"] = df["AJT-130 Score"].astype(float)
df["Volume 130 Score"] = df["Volume 130 Score"].astype(float)
```

## 5. 최종 결과 확인


```python
display(df)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
      <th>tmp</th>
      <th>AJT-130 Score</th>
      <th>Volume 130 Score</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-08-02</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
      <td>243.00</td>
      <td>226.00</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>940.56</td>
      <td>795.92</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>0.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2019-02-26</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>97.00</td>
      <td>92.00</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2019-02-12</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>747.00</td>
      <td>256.00</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31971</th>
      <td>2018-04-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>482.00</td>
      <td>399.00</td>
    </tr>
    <tr>
      <th>31972</th>
      <td>2019-08-13</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
      <td>0.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31973</th>
      <td>2018-06-21</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>84.00</td>
      <td>24.00</td>
    </tr>
    <tr>
      <th>31974</th>
      <td>2017-04-20</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>0.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31975</th>
      <td>2018-10-26</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
      <td>146.00</td>
      <td>124.00</td>
    </tr>
  </tbody>
</table>
<p>31976 rows × 5 columns</p>
</div>



```python
df.isnull().sum()
```




    처방일자#5                  0
    검사결과내용#6               20
    tmp                    20
    AJT-130 Score          34
    Volume 130 Score    14537
    dtype: int64



## 6. 추출되지 않는 경우를 리뷰
* 추출 되지 않는 경우를 봤을 때, 이는 CABG, Stent와 같이 평가가 불가능한 경우인 것을 확인했다.
    * 결측 이유가 있는 경우기 때문에 Reason과 같이 결측 이유를 적는 컬럼을 추가하다.


```python
for i in df[df["AJT-130 Score"].isnull()].index:
    print("\nIndex: ", i)
    print(df.loc[i, "tmp"],"\n")
```

    
    Index:  198
    ▣ 검사정보 및 소견
    
    
    
    coronary ct, calcium score (non-contrast)
    
    
    
      cabg를 시행 받은 환자로 calcium scoring에 제한적임.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation due to cabg.
    
    multiple calcifications at aortic root and descending thoracic aorta.
    
    
    
    
    
     
    
    
    Index:  678
    ▣ 검사정보 및 소견
    
    
    
    coronary ct, calcium score (non-contrast)
    
    
    
      left main, lad, diagonal, rca에 calcification들이 있으며 lcx는 stent가 implantation 되어 있는 것으로 보임.
    
      lcx의 stent로 인하여 calcium scoring 평가의 제한점이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    s/p pci for lcx.
    
    
    
    
    
     
    
    
    Index:  808
    nan 
    
    
    Index:  884
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      coronary artery bypass graft가 시행되어 있는 환자로 calcium scoring에 적합하지 않음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation for calcium scoring due to cabg.
    
    
    
    
    
     
    
    
    Index:  1448
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      left main, lad, diagonal, lcx, rca, pda에 multiple dense calcifications이 있음.
    
      cabg를 시행받은 환자로 calcium score 평가에 제한점이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    s/p cabg.
    
    multiple calcifications in coronary arteries.
    
    
    
    
    
     
    
    
    Index:  1687
    ▣ 검사정보 및 소견
    
    
    
    coronary ct, calcium score (non-contrast)
    
    
    
      limited evaluation due to coronary stent implantation.
    
      there are multiple small calcifications in the left main, lcx, and rca.
    
      there are also small calcifications in aortic root and descending thoracic aorta.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation due to coronary stent implantation.
    
    multiple small calcifications in left main, lcx and, rca.
    
    
    
    
    
     
    
    
    Index:  2042
    nan 
    
    
    Index:  2827
    nan 
    
    
    Index:  6338
    nan 
    
    
    Index:  7070
    nan 
    
    
    Index:  8498
    nan 
    
    
    Index:  8700
    nan 
    
    
    Index:  9890
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      lad에 stent가 implantation되어 있어 calcium score에 적합하지 않음.
    
      aortic valve에 small calcification이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    stent implantation for proximal lad.
    
    
    
    
    
     
    
    
    Index:  10554
    nan 
    
    
    Index:  10557
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      lad와 lcx에 stent가 implantation되어 있어 calcium score 측정에 제한점이 있음.
    
      descending thoracic aorta에 small calcification이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    stent implantation for lad and lcx.
    
    
    
    
    
     
    
    
    Index:  10608
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      lad와 lcx에 stent가 implantation 되어 있어서 calcium scoring에 적합하지 않음.
    
      lv myocardium은 subendocardial area에 diffuse fat infiltration이 관찰되어서 old mi로 생각됨.
    
      sinotubular junction에 calcification이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    inappropriate indication for calcium scoring due to lad and lcx stent.
    
    old mi in the lv myocardium.
    
    
    
    
    
     
    
    
    Index:  12230
    nan 
    
    
    Index:  12335
    nan 
    
    
    Index:  15143
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      lcx에 stent insertion의 가능성이 있음. clinical correlation하기 바람.
    
      stent는 calcium scoring에 부적합함.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation for calcium scoring due to lcx stent.
    
      --> clinical correlation.
    
    
    
    
    
     
    
    
    Index:  16403
    nan 
    
    
    Index:  17001
    nan 
    
    
    Index:  18359
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      조영 증강을 시행하지 않아 관상동맥 평가에 제한점이 있는데 aorta에서 diagonal과 rca로 연결되는 2개의 free-graft (cabg)가 기시하고 있음. surgical clip과 coronary calcium간의 구분이 어려워 calcium score 평가에 적합하지 않음.
    
      lv free-wall side의 pericardium에 local calcified thickening 소견 있음.
    
      조영 증강 ct로의 평가가 요망됨.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation for calcium scoring due to cabg.
    
    localized pericardial thickening with calcification.
    
    
    
    
    
    ▣ 의견
    
    
    
    coronary ct angiography (cabg protocol) 
    
    
    Index:  19522
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      coronary artery에 stent가 implantation되어 있으며 agatston score 측정에 제한점이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    s/p pci for distal rca.
    
    
    
    
    
     
    
    
    Index:  20156
    nan 
    
    
    Index:  23219
    nan 
    
    
    Index:  23831
    ▣ 검사정보 및 소견
    
    
    
    coronary ct, calcium score (non-contrast)
    
    
    
      lad에 stent가 implantation 되어 있어서 calcium score 평가의 제한적임.
    
      aortic root에 small calclfication이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation due to mid lad stent.
    
    
    
    
    
     
    
    
    Index:  25087
    nan 
    
    
    Index:  26166
    nan 
    
    
    Index:  26746
    ▣ 검사정보 및 소견
    
    
    
    coronary artery ct, calcium score
    
    
    
      lad에 stent가 implantation되어 있는 것으로 보임. calcium scoring에 제한적임.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    s/p pci for lad.
    
    
    
    
    
     
    
    
    Index:  27319
    nan 
    
    
    Index:  28485
    ▣ 검사정보 및 소견
    
    
    
    coronary ct, calcium score (non-contrast)
    
    
    
      coronary artery에 bypass graft를 시행받은 환자로 calcium score 평가에 제한적임.
    
      aortic valve와 descending thoracic aorta에 small calcification이 있음.
    
    
    
    
    
    ▣ 결론 및 진단
    
    
    
    limited evaluation due to coronary artery bypass graft.
    
    
    
    
    
     
    
    
    Index:  28660
    nan 
    
    
    Index:  29827
    nan 
    
    
    Index:  30674
    nan 
    



```python
reason_re_1 = re.compile(r"\s*(?P<reason>cabg)\s*")
reason_re_2 = re.compile(r"\s*(?P<reason>stent)\s*")
```


```python
for i in tqdm(df[df["AJT-130 Score"].isnull()].index):
    
    if re.search(reason_re_1, str(df.loc[i, "tmp"])) != None:
        df.loc[i, "Reason"] = re.search(reason_re_1, str(df.loc[i, "tmp"])).group("reason")
    
    elif re.search(reason_re_2, str(df.loc[i, "tmp"])) != None:
        df.loc[i, "Reason"] = re.search(reason_re_2, str(df.loc[i, "tmp"])).group("reason")
    else: continue

display(df)
```


      0%|          | 0/34 [00:00<?, ?it/s]



<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
      <th>tmp</th>
      <th>AJT-130 Score</th>
      <th>Volume 130 Score</th>
      <th>Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-08-02</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
      <td>243.00</td>
      <td>226.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>940.56</td>
      <td>795.92</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>0.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2019-02-26</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>97.00</td>
      <td>92.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2019-02-12</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>747.00</td>
      <td>256.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31971</th>
      <td>2018-04-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>482.00</td>
      <td>399.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31972</th>
      <td>2019-08-13</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
      <td>0.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31973</th>
      <td>2018-06-21</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>84.00</td>
      <td>24.00</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31974</th>
      <td>2017-04-20</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>0.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31975</th>
      <td>2018-10-26</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>▣ 검사정보 및 소견\n\ncoronary ct, calcium score (non...</td>
      <td>146.00</td>
      <td>124.00</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>31976 rows × 6 columns</p>
</div>


### 결과 확인


```python
df.query('Reason.notnull()', engine='python')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
      <th>tmp</th>
      <th>AJT-130 Score</th>
      <th>Volume 130 Score</th>
      <th>Reason</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>198</th>
      <td>2019-07-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
    </tr>
    <tr>
      <th>678</th>
      <td>2018-08-25</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>884</th>
      <td>2017-12-07</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
    </tr>
    <tr>
      <th>1448</th>
      <td>2017-04-03</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
    </tr>
    <tr>
      <th>1687</th>
      <td>2019-03-25</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>9890</th>
      <td>2017-08-17</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>10557</th>
      <td>2018-03-22</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>10608</th>
      <td>2017-05-18</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>15143</th>
      <td>2018-04-09</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>18359</th>
      <td>2016-09-28</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
    </tr>
    <tr>
      <th>19522</th>
      <td>2018-02-02</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>23831</th>
      <td>2018-09-10</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
    <tr>
      <th>26746</th>
      <td>2018-07-27</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
    </tr>
  </tbody>
</table>
</div>



## 7. 의뢰자가 원하는 형태로 변환해 주기


```python
for i in df[df["Reason"].notnull()].index:
    if df.loc[i, "Reason"] == "stent":
        df.loc[i, "Note"] = "STENT 시술로 측정 불가"
        df.loc[i, "Comment"] = "STENT 상태로 CAC 측정에 제한적임"
    elif df.loc[i, "Reason"] == "cabg":
        df.loc[i, "Note"] = "CABG 수술로 측정 불가"
        df.loc[i, "Comment"] = "CABG 상태로 CAC 측정이 제한적임"
```


```python
df.query('Reason.notnull()', engine='python')
```




<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
      <th>tmp</th>
      <th>AJT-130 Score</th>
      <th>Volume 130 Score</th>
      <th>Reason</th>
      <th>Note</th>
      <th>Comment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>198</th>
      <td>2019-07-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
      <td>CABG 수술로 측정 불가</td>
      <td>CABG 상태로 CAC 측정이 제한적임</td>
    </tr>
    <tr>
      <th>678</th>
      <td>2018-08-25</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>884</th>
      <td>2017-12-07</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
      <td>CABG 수술로 측정 불가</td>
      <td>CABG 상태로 CAC 측정이 제한적임</td>
    </tr>
    <tr>
      <th>1448</th>
      <td>2017-04-03</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
      <td>CABG 수술로 측정 불가</td>
      <td>CABG 상태로 CAC 측정이 제한적임</td>
    </tr>
    <tr>
      <th>1687</th>
      <td>2019-03-25</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>9890</th>
      <td>2017-08-17</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>10557</th>
      <td>2018-03-22</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>10608</th>
      <td>2017-05-18</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>15143</th>
      <td>2018-04-09</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>18359</th>
      <td>2016-09-28</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>cabg</td>
      <td>CABG 수술로 측정 불가</td>
      <td>CABG 상태로 CAC 측정이 제한적임</td>
    </tr>
    <tr>
      <th>19522</th>
      <td>2018-02-02</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>23831</th>
      <td>2018-09-10</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary ct, calcium score ...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
    <tr>
      <th>26746</th>
      <td>2018-07-27</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>▣ 검사정보 및 소견\n\n\n\ncoronary artery ct, calcium...</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>stent</td>
      <td>STENT 시술로 측정 불가</td>
      <td>STENT 상태로 CAC 측정에 제한적임</td>
    </tr>
  </tbody>
</table>
</div>



## 8. 결과 저장하기
* Regular Expression 적용을 위해 임의로 만든 Column을 제거하고서 데이터를 저장하기
* 데이터를 Excel로 저장하거나, DB로 업데이트 하는 방법이 있다. 


```python
df.drop(columns=["Reason", "tmp"], inplace=True)
display(df)
```


<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }

    .dataframe tbody tr th {
        vertical-align: top;
    }

    .dataframe thead th {
        text-align: right;
    }
</style>
<table border="1" class="dataframe">
  <thead>
    <tr style="text-align: right;">
      <th></th>
      <th>처방일자#5</th>
      <th>검사결과내용#6</th>
      <th>AJT-130 Score</th>
      <th>Volume 130 Score</th>
      <th>Note</th>
      <th>Comment</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <th>0</th>
      <td>2019-08-02</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>243.00</td>
      <td>226.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>1</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>940.56</td>
      <td>795.92</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>2</th>
      <td>2019-02-15</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>0.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>3</th>
      <td>2019-02-26</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>97.00</td>
      <td>92.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>4</th>
      <td>2019-02-12</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY CT, CALCIUM SCORE ...</td>
      <td>747.00</td>
      <td>256.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>...</th>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
      <td>...</td>
    </tr>
    <tr>
      <th>31971</th>
      <td>2018-04-04</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>482.00</td>
      <td>399.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31972</th>
      <td>2019-08-13</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>0.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31973</th>
      <td>2018-06-21</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>84.00</td>
      <td>24.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31974</th>
      <td>2017-04-20</td>
      <td>▣ 검사정보 및 소견\n\n\n\nCORONARY ARTERY CT, CALCIUM...</td>
      <td>0.00</td>
      <td>NaN</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
    <tr>
      <th>31975</th>
      <td>2018-10-26</td>
      <td>▣ 검사정보 및 소견\n\nCORONARY CT, CALCIUM SCORE (NON...</td>
      <td>146.00</td>
      <td>124.00</td>
      <td>NaN</td>
      <td>NaN</td>
    </tr>
  </tbody>
</table>
<p>31976 rows × 6 columns</p>
</div>

