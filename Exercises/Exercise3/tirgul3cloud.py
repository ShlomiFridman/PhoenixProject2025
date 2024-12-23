# -*- coding: utf-8 -*-
"""tirgul3Cloud.ipynb

Automatically generated by Colab.
"""

url = 'https://data.gov.il/api/3/action/datastore_search?resource_id=053cea08-09bc-40ec-8f7a-156f0677aff3'
Tozeret = "" # @param [""]
Kinuy_Mishari = "" # @param [""]

import requests
import pandas as pd
pd.set_option("display.max_columns", None)
response = requests.get(url)
data = response.json()
df = pd.DataFrame(data)


# Create a DataFrame from the 'records' in the JSON response
data_df = pd.DataFrame(data['result']['records'])

import ipywidgets as widgets

ts = data_df['tozeret_nm'].unique()
ts.sort()
tozeret_dropdown = widgets.Dropdown(
    options=ts,
    description="Tozeret: ",
    style={'description_width': "auto"}
)
nickname_dropdown = widgets.Dropdown(
    options=[],
    description="Kinuy Mishari: ",
    style={'description_width': "auto"}
)
output_res = widgets.Output()

def update_nicknames(changeData):
  output_res.clear_output()
  if not changeData.new:
    return
  t = changeData.new
  ns = data_df[data_df['tozeret_nm'] == t]["kinuy_mishari"].unique()
  ns.sort()
  nickname_dropdown.options = ns

def update_data(changeData):
  output_res.clear_output()
  if not changeData.new:
    return
  n = changeData.new
  t = tozeret_dropdown.value
  res = data_df[(data_df['tozeret_nm'] == t) & (data_df['kinuy_mishari'] == n)]
  with output_res:
    print(f"Total Records: {res.shape[0]}")
    print(f"Unique Ramat Gimur: {res['ramat_gimur'].unique()}")

tozeret_dropdown.observe(update_nicknames, names="value")
nickname_dropdown.observe(update_data, names="value")
display(tozeret_dropdown, nickname_dropdown, output_res)
tozeret_dropdown.value = data_df['tozeret_nm'].unique()[1]