# %%
import pandas as pd
import matplotlib.pyplot as plt
from IPython.display import display
import seaborn as sns
pd.set_option("display.max_columns", None)

# %%

def regplot_with_corr(data, x, y):
    corr = data.corr().loc[x, y]
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    sns.regplot(x=x, 
                y=y, 
                data=data, 
                ax=ax, 
                line_kws={'color':'r'})
    plt.title(f'Pearson Correlation = {corr:.2f}')
    plt.grid()
    plt.show()

# %%
if __name__ == '__main__':
    df_bmd = pd.read_csv("./data/BMD_SMC.csv")
    df_bmd['SM_DATE'] = df_bmd['SM_DATE'].astype('datetime64')
    df_bmd = df_bmd.query('label == [0, 1, 2]')
    column_mask = ['CDW_ID', 'SM_DATE', 'label', 'tissue_pfat']
    df_bmd = df_bmd[column_mask].pivot_table(index=['CDW_ID', 'SM_DATE'], columns='label', values='tissue_pfat').reset_index()
    df_bmd.columns.name = None
    df_bmd.rename(columns={0:'bmd_spine_fat', 1:'bmd_total_body_estimated_fat', 2:'bmd_femur_fat'}, inplace=True)
    display(df_bmd.head())
    # %%
    df_inbody_full = pd.read_csv("./data/inbody_cleaned.csv")
    df_inbody_full['SM_DATE'] = df_inbody_full['SM_DATE'].astype('datetime64')
    display(df_inbody_full.head())
    # %%
    df_merged_set = pd.merge(df_inbody_full, df_bmd, left_on=['ID', 'SM_DATE'], right_on=['CDW_ID', 'SM_DATE'], how='inner')
    df_merged_set = df_merged_set.rename({'체지방률':'inbody_fat_percentage'}, axis=1)
    display(df_merged_set.head())

    # %%
    regplot_with_corr(data=df_merged_set, x='inbody_fat_percentage', y='bmd_total_body_estimated_fat')
    regplot_with_corr(data=df_merged_set, x='inbody_fat_percentage', y='bmd_spine_fat')
    regplot_with_corr(data=df_merged_set, x='inbody_fat_percentage', y='bmd_femur_fat')

# %%
