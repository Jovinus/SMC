# %%
import pandas as pd
# %%

map_rslt_code_to_degree = {1 : 'Absent', 
                 2 : 'Moderate', 
                 3 : 'Mild', 
                 7 : 'Minimal', 
                 54 : 'Severe', 
                 56 : 'Minimal to Mild', 
                 57 : 'Mild to Moderate', 
                 58 : 'Moderate to Severe'}
    
map_degree_to_code = {'Absent' : 1, 
                 'Moderate' : 3, 
                 'Mild' : 2, 
                 'Minimal' : 1.5, 
                 'Severe' : 4, 
                 'Minimal to Mild' : 1.5, 
                 'Mild to Moderate' : 2.5, 
                 'Moderate to Severe' : 3.5}

source_col_to_merge = ['ID', '처방일', 'tmp']
result_col_to_merge = ['ID', '처방일', 'FLD_Degree_NM', 'FLD_Degree_CODE']

# %%
if __name__ == '__main__':
    df_source = pd.read_csv("../../data/fatty_liver/fattyliver_to_2016.csv", encoding='CP949')
    df_result = pd.read_csv("../../data/fatty_liver/RSLT_CD/SONO_RESULTS.csv")
    
    ## Rename Nessasary Column to English
    df_result = df_result.rename({
        '환자번호#1' : 'ID',
        '처방일자#2' : '처방일',
        '건강검진결과코드#5' : 'RSLT_CODE'}, axis=1)
    
    df_result_fl = df_result.query('RSLT_CODE == [1, 2, 3, 7, 54, 56, 57, 58]')
    df_result_fl['FLD_Degree_NM'] = df_result_fl['RSLT_CODE'].map(map_rslt_code_to_degree)
    df_result_fl['FLD_Degree_CODE'] = df_result_fl['FLD_Degree_NM'].map(map_degree_to_code)
    
    df_dataset = pd.merge(df_source[source_col_to_merge], 
                          df_result_fl[result_col_to_merge], 
                          how='left', 
                          on=['ID', '처방일']).rename({'처방일':'SM_DATE'})
    
    df_dataset['FLD_Degree_NM'] = df_dataset['FLD_Degree_NM'].fillna('Absent')
    df_dataset['FLD_Degree_CODE'] = df_dataset['FLD_Degree_CODE'].fillna(1)
    
    df_dataset.to_csv("../../data/fatty_liver/ABD_SONO_to_2016.csv", 
                      index=False, 
                      encoding='utf-8-sig')
