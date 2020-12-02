import matplotlib.pyplot as plt
import pandas as pd
import enum


COUNTRIES = ['Canada', 'United States', 'United Kingdom', 'France', 'Taiwan']


class GroupIndex(enum.Enum):
    STRINGENCY = "StringencyIndex"
    GOVERNMENT_RESPONSE = "GovernmentResponseIndex"
    CONTAINMENT_HEALTH = "ContainmentHealthIndex"
    ECONOMIC_SUPPORT = "EconomicSupportIndex"


class Index(enum.Enum):
    C1_SCHOOL_CLOSE = "C1_School closing"
    C2_WORKPLACE_CLOSE = "C2_Workplace closing"
    C3_CANCEL_PUBLIC_EVENTS = "C3_Cancel public events"
    C4_RESTRICT_GATHERINGS = "C4_Restrictions on gatherings"
    C5_CLOSE_PUBLIC_TRANSPORT = "C5_Close public transport"
    C6_STAY_HOME = "C6_Stay at home requirements"
    C7_RESTRICT_INTERNAL_MOVEMENT = "C7_Restrictions on internal movement"
    C8_INTERNATIONAL_TRAVEL = "C8_International travel controls"
    E1_INCOME_SUPPORT = "E1_Income support"
    E2_DEBT_RELIEF = "E2_Debt/contract relief"
    E3_FISCAL_MEASURES = "E3_Fiscal measures"
    E4_INTERNATIONAL_SUPPORT = "E4_International support"
    H1_PUBLIC_INFO_CAMPAIGNS = "H1_Public information campaigns"
    H2_TESTING_POLICY = "H2_Testing policy"
    H3_CONTACT_TRACING = "H3_Contact tracing"
    H4_HEALTH_CARE_INVESTMENT = "H4_Emergency investment in healthcare"
    H5_VACCINE_INVESTMENT = "H5_Investment in vaccines"
    H6_FACIAL_COVERINGS = "H6_Facial Coverings"


def get_country(data, country):
    data_country = data[data['CountryName'] == country]
    data_country = data_country.set_index("Date")
    return data_country


def plot_indices_vs_cases(data_country, country, index_enum):
    for index in index_enum:
        data_country_index = data_country[[index.value,
                                           "number_of_cases_each_day"]]
        data_country_index.plot(subplots=True)
        plt.title(f"{index.name} VS Daily Cases in {country}")
        plt.savefig(f'./gilpin/figures/{country}_{index.name}.png')


def main():
    # Read all data from CSV
    data = pd.read_csv("complete.csv")

    # Important Columns: CountryCode, Date, C1 to C8, H1 to H6, ConfirmedCases, ConfirmedDeaths, ContainmentHealthIndex
    data = data[["CountryName", "Date", 'C1_School closing', 'C2_Workplace closing',
                 'C3_Cancel public events', 'C4_Restrictions on gatherings',
                 'C5_Close public transport', 'C6_Stay at home requirements',
                 'C7_Restrictions on internal movement',
                 'C8_International travel controls', 'E1_Income support',
                 'E2_Debt/contract relief', 'E3_Fiscal measures',
                 'E4_International support', 'H1_Public information campaigns',
                 'H2_Testing policy', 'H3_Contact tracing',
                 'H4_Emergency investment in healthcare', 'H5_Investment in vaccines',
                 'H6_Facial Coverings', "StringencyIndex",
                 "GovernmentResponseIndex", 'ContainmentHealthIndex', 'EconomicSupportIndex'
                 'ConfirmedCases', 'number_of_cases_each_day', 'ConfirmedDeaths']]

    # Format Date
    data['Date'] = pd.to_datetime(data['Date'], format='%Y%m%d')

    # Visualize data for all countries
    for country in COUNTRIES:
        country_data = get_country(data, country)
        plot_indices_vs_cases(country_data, country, GroupIndex)
        plot_indices_vs_cases(country_data, country, Index)


if __name__ == '__main__':
    main()
