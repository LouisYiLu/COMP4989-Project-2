import matplotlib.pyplot as plt
import pandas as pd
import enum

# Read all data from CSV
data = pd.read_csv("complete.csv")
print(data.columns)
# ['CountryName', 'CountryCode', 'RegionName', 'RegionCode', 'Date',
#     'C1_School closing', 'C1_Flag', 'C2_Workplace closing', 'C2_Flag',
#     'C3_Cancel public events', 'C3_Flag', 'C4_Restrictions on gatherings',
#     'C4_Flag', 'C5_Close public transport', 'C5_Flag',
#     'C6_Stay at home requirements', 'C6_Flag',
#     'C7_Restrictions on internal movement', 'C7_Flag',
#     'C8_International travel controls', 'E1_Income support', 'E1_Flag',
#     'E2_Debt/contract relief', 'E3_Fiscal measures',
#     'E4_International support', 'H1_Public information campaigns',
#     'H1_Flag', 'H2_Testing policy', 'H3_Contact tracing',
#     'H4_Emergency investment in healthcare', 'H5_Investment in vaccines',
#     'H6_Facial Coverings', 'H6_Flag', 'M1_Wildcard', 'ConfirmedCases',
#     'number_of_cases_each_day', 'ConfirmedDeaths', 'StringencyIndex',
#     'StringencyIndexForDisplay', 'StringencyLegacyIndex',
#     'StringencyLegacyIndexForDisplay', 'GovernmentResponseIndex',
#     'GovernmentResponseIndexForDisplay', 'ContainmentHealthIndex',
#     'ContainmentHealthIndexForDisplay', 'EconomicSupportIndex',
#     'EconomicSupportIndexForDisplay',
#     'retail_and_recreation_percent_change_from_baseline',
#     'grocery_and_pharmacy_percent_change_from_baseline',
#     'parks_percent_change_from_baseline',
#     'transit_stations_percent_change_from_baseline',
#     'workplaces_percent_change_from_baseline',
#     'residential_percent_change_from_baseline']

# Important Columns: CountryCode, Date, C1 to C8, H1 to H6, ConfirmedCases, ConfirmedDeaths, ContainmentHealthIndex
data = data[['C1_School closing', 'C2_Workplace closing',
             'C3_Cancel public events', 'C4_Restrictions on gatherings',
             'C5_Close public transport', 'C6_Stay at home requirements',
             'C7_Restrictions on internal movement',
             'C8_International travel controls', 'E1_Income support',
             'E2_Debt/contract relief', 'E3_Fiscal measures',
             'E4_International support', 'H1_Public information campaigns',
             'H2_Testing policy', 'H3_Contact tracing',
             'H4_Emergency investment in healthcare', 'H5_Investment in vaccines',
             'H6_Facial Coverings', "CountryName", "Date", 'ConfirmedCases',
             'number_of_cases_each_day', 'ConfirmedDeaths', "StringencyIndex",
             "GovernmentResponseIndex", 'ContainmentHealthIndex', 'EconomicSupportIndex']]

# Format Date
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')
print(data.shape)


class GroupIndex(enum.Enum):
    STRINGENCY = "StringencyIndex"
    GOVERNMENT_RESPONSE = "GovernmentResponseIndex"
    CONTAINMENT_HEALTH = "ContainmentHealthIndex"
    ECONOMIC_SUPPORT = "EconomicSupportIndex"


class Index(enum.Enum):
    C1 = "C1_School closing"
    C2 = "C2_Workplace closing"
    C3 = "C3_Cancel public events"
    C4 = "C4_Restrictions on gatherings"
    C5 = "C5_Close public transport"
    C6 = "C6_Stay at home requirements"
    C7 = "C7_Restrictions on internal movement"
    C8 = "C8_International travel controls"
    E1 = "E1_Income support"
    E2 = "E2_Debt/contract relief"
    E3 = "E3_Fiscal measures"
    E4 = "E4_International support"
    H1 = "H1_Public information campaigns"
    H2 = "H2_Testing policy"
    H3 = "H3_Contact tracing"
    H4 = "H4_Emergency investment in healthcare"
    H5 = "H5_Investment in vaccines"
    H6 = "H6_Facial Coverings"


def get_country(country):
    data_country = data[data['CountryName'] == country]
    data_country = data_country.set_index("Date")
    return data_country


def plot_grouped_indices_vs_cases(country):
    data_country = get_country(country)
    for index in GroupIndex:
        data_country_index = data_country[[index.value,
                                           "number_of_cases_each_day"]]
        data_country_index.plot(subplots=True)
        plt.title(f"{index.value} VS Daily Cases in {country}")
        plt.savefig(f'./gilpin/figures/{country}_{index.name}.png')


def plot_indices_vs_cases(country):
    data_country = get_country(country)
    for index in Index:
        data_country_index = data_country[[index.value,
                                           "number_of_cases_each_day"]]
        data_country_index.plot(subplots=True)
        plt.title(f"{index.value[3:]} VS Daily Cases in {country}")
        plt.savefig(f'./gilpin/figures/{country}_{index.name}.png')


# ======= CANADA ========
data_canada = data[data['CountryName'] == 'Canada']
data_canada = data_canada.set_index("Date")

# plot_grouped_indices_vs_cases("Canada")
plot_indices_vs_cases("Canada")


# ======= USA ========
data_usa = data[data['CountryName'] == 'United States']
data_usa = data_usa.set_index("Date")

# plot_grouped_indices_vs_cases("United States")
plot_indices_vs_cases("United States")


# ======= FRANCE ========
data_france = data[data['CountryName'] == 'France']
data_france = data_france.set_index("Date")

# plot_grouped_indices_vs_cases("France")
plot_indices_vs_cases("France")


# ======= United Kingdome ========
data_uk = data[data['CountryName'] == 'United Kingdom']
data_uk = data_uk.set_index("Date")

# plot_grouped_indices_vs_cases("United Kingdom")
plot_indices_vs_cases("United Kingdom")


# ======= TAIWAN ========
data_taiwan = data[data['CountryName'] == 'Taiwan']
data_taiwan = data_taiwan.set_index("Date")

# plot_grouped_indices_vs_cases("Taiwan")
plot_indices_vs_cases("Taiwan")
