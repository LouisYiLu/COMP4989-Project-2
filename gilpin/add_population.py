import pandas as pd
import os
import numpy as np

# Complete CSV
data = pd.read_csv(os.path.abspath('../complete.csv'))

# Get & Format Population Data
populations = pd.read_csv(
    os.path.abspath('../datasets_resource/population_by_country_2020.csv')
)
populations = populations[[
    "Country (or dependency)", "Population (2020)", "Density (P/Km²)", "Urban Pop %"
]]
populations = populations.rename(columns={
    "Country (or dependency)": "CountryName",
    "Population (2020)": "Population",
    "Density (P/Km²)": "Density",
    "Urban Pop %": "UrbanPercentage"
})
populations = populations.set_index('CountryName')
populations = populations.replace(to_replace='N.A.', value=np.NaN)
populations["UrbanPercentage"] = populations["UrbanPercentage"].str.rstrip("%").astype('float') / 100

# Add Population, Density, and UrbanPercentage Columns to COMPLETE DATA
data.insert(2, 'Population', np.NaN)
data.insert(3, 'Density', np.NaN)
data.insert(4, 'UrbanPercentage', np.NaN)
for country in populations.index:
    data.loc[data['CountryName'] == country, 'Population'] = populations.loc[country, 'Population']
    data.loc[data['CountryName'] == country, 'Density'] = populations.loc[country, 'Density']
    data.loc[data['CountryName'] == country, 'UrbanPercentage'] = populations.loc[country, 'UrbanPercentage']

# SAVE DATA TO CSV
data.to_csv(os.path.abspath('complete_with_population.csv'))
