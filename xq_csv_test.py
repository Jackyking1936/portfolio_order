#%%

import pandas as pd

df = pd.read_csv('ETF50_picker.csv', encoding='cp950', skiprows=3)
# %%
otc_df = pd.read_csv('OTC200_picker.csv', encoding='cp950', skiprows=3)
# %%
