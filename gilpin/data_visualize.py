import matplotlib.pyplot as plt
import pandas as pd
import enum

# Read all data from CSV
data = pd.read_csv("complete.csv")
print(data.columns)


# Important Columns: CountryCode, Date, C1 to C8, H1 to H6, ConfirmedCases, ConfirmedDeaths, ContainmentHealthIndex
data = data[["CountryName", "Date", 'ConfirmedCases', 'number_of_cases_each_day', 'ConfirmedDeaths',
             "StringencyIndex", "GovernmentResponseIndex", 'ContainmentHealthIndex', 'EconomicSupportIndex']]

# Format Date
data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')


class Index(enum.Enum):
    STRINGENCY = "StringencyIndex"
    GOVERNMENT_RESPONSE = "GovernmentResponseIndex"
    CONTAINMENT_HEALTH = "ContainmentHealthIndex"
    ECONOMIC_SUPPORT = "EconomicSupportIndex"


def plot_indices_vs_cases(country):
    data_country = data[data['CountryName'] == country]
    data_country = data_country.set_index("Date")

    for index in Index:
        data_country_index = data_country[[index.value,
                                           "number_of_cases_each_day"]]
        data_country_index.plot(subplots=True)
        plt.title(f"{index.value} VS Daily Cases in {country}")
        plt.show()
        plt.savefig(f'./gilpin/figures/{country}_{index.value}.png')


# ======= CANADA ========
data_canada = data[data['CountryName'] == 'Canada']
data_canada = data_canada.set_index("Date")

plot_indices_vs_cases("Canada")


# ======= USA ========
data_usa = data[data['CountryName'] == 'United States']
data_usa = data_usa.set_index("Date")

plot_indices_vs_cases("United States")


# ======= FRANCE ========
data_france = data[data['CountryName'] == 'France']
data_france = data_france.set_index("Date")

plot_indices_vs_cases("France")


# ======= United Kingdome ========
data_uk = data[data['CountryName'] == 'United Kingdom']
data_uk = data_uk.set_index("Date")

plot_indices_vs_cases("United Kingdom")
