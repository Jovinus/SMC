# %% Load Package
import pandas as pd
pd.set_option('display.max_columns', None)
# %%

df_cc_male = pd.read_csv("./data/BMD_FAT_cc_man.csv")
df_cc_male['SM_DATE'] = (pd.to_timedelta(df_cc_male.acq_time, unit='D') + pd.to_datetime('1899-12-30')).astype('str').str.slice(start=0, stop=10)

df_cc_female = pd.read_csv("./data/BMD_FAT_cc_woman.csv")
df_cc_female['SM_DATE'] = (pd.to_timedelta(df_cc_female.acq_time, unit='D') + pd.to_datetime('1899-12-30')).astype('str').str.slice(start=0, stop=10)

df_mc_all = pd.read_csv("./data/BMD_FAT_sample.csv")
# %%
df_bmd = pd.concat([df_cc_male, df_cc_female, df_mc_all], axis=0)
df_bmd.to_csv("./data/BMD_SMC.csv", index=False, encoding='utf-8-sig')
# %%
