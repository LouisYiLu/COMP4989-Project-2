import matplotlib.pyplot as plt
import pandas as pd

# Read all data from CSV
data = pd.read_csv('complete.csv')
print(data.columns)

''' All Columns
['CountryName', 'CountryCode', 'RegionName', 'RegionCode', 'Date',
       'C1_School closing', 'C1_Flag', 'C2_Workplace closing', 'C2_Flag',
       'C3_Cancel public events', 'C3_Flag', 'C4_Restrictions on gatherings',
       'C4_Flag', 'C5_Close public transport', 'C5_Flag',
       'C6_Stay at home requirements', 'C6_Flag',
       'C7_Restrictions on internal movement', 'C7_Flag',
       'C8_International travel controls', 'E1_Income support', 'E1_Flag',
       'E2_Debt/contract relief', 'E3_Fiscal measures',
       'E4_International support', 'H1_Public information campaigns',
       'H1_Flag', 'H2_Testing policy', 'H3_Contact tracing',
       'H4_Emergency investment in healthcare', 'H5_Investment in vaccines',
       'H6_Facial Coverings', 'H6_Flag', 'M1_Wildcard', 'ConfirmedCases',
       'ConfirmedDeaths', 'StringencyIndex', 'StringencyIndexForDisplay',
       'StringencyLegacyIndex', 'StringencyLegacyIndexForDisplay',
       'GovernmentResponseIndex', 'GovernmentResponseIndexForDisplay',
       'ContainmentHealthIndex', 'ContainmentHealthIndexForDisplay',
       'EconomicSupportIndex', 'EconomicSupportIndexForDisplay',
       'retail_and_recreation_percent_change_from_baseline',
       'grocery_and_pharmacy_percent_change_from_baseline',
       'parks_percent_change_from_baseline',
       'transit_stations_percent_change_from_baseline',
       'workplaces_percent_change_from_baseline',
       'residential_percent_change_from_baseline']
'''


# Important Columns: CountryCode, Date, C1 to C8, H1 to H6, ConfirmedCases, ConfirmedDeaths, ContainmentHealthIndex
data = data[["CountryName", "Date", 'ConfirmedCases', 'ConfirmedDeaths', 'ContainmentHealthIndex']]

# Format Date
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')


# CANADA
data_canada = data[data['CountryName'] == 'Canada']
print(data_canada)
data_canada['Date'] = pd.to_datetime(data_canada['Date'], format='%Y%m%d')
data_canada = data_canada.set_index("Date")
data_canada = data_canada[["ContainmentHealthIndex", "ConfirmedCases"]]

data_canada.plot(subplots=True)
plt.title("C/H Index and COVID Numbers (Cumulative) in Canada")
plt.show()

# USA
data_usa = data[data['CountryName'] == 'United States']
print(data_usa)
data_usa['Date'] = pd.to_datetime(data_usa['Date'], format='%Y%m%d')
data_usa = data_usa.set_index("Date")
data_usa = data_usa[["ContainmentHealthIndex", "ConfirmedCases"]]

data_usa.plot(subplots=True)
plt.title("C/H Index and COVID Numbers (Cumulative) in USA")
plt.show()
