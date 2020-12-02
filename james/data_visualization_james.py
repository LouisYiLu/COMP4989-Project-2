import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


labels = ["ConfirmedCases", "ConfirmedDeaths"]

file = pd.read_csv("../complete.csv")


def plot_data_numerical(data, main_label):
    print(main_label)
    # numeric_data_types = ["Date", "C1_School closing", "C1_Flag", "C2_Workplace closing", "C2_Flag",
    #                       "C3_Cancel public events", "C3_Flag", "C4_Restrictions on gatherings", "C4_Flag",
    #                       "C5_Close public transport", "C5_Flag", "C6_Stay at home requirements", "C6_Flag",
    #                       "C7_Restrictions on internal movement", "C7_Flag", "C8_International travel controls",
    #                       "E1_Income support", "E1_Flag", "E2_Debt/contract relief", "E3_Fiscal measures",
    #                       "E4_International support", "H1_Public information campaigns", "H1_Flag", "H2_Testing policy",
    #                       "H3_Contact tracing", "H4_Emergency investment in healthcare", "H5_Investment in vaccines",
    #                       "H6_Facial Coverings", "H6_Flag", "StringencyIndex", "StringencyIndexForDisplay",
    #                       "StringencyLegacyIndex", "StringencyLegacyIndexForDisplay", "GovernmentResponseIndex",
    #                       "GovernmentResponseIndexForDisplay", "ContainmentHealthIndex",
    #                       "ContainmentHealthIndexForDisplay",
    #                       "EconomicSupportIndex", "EconomicSupportIndexForDisplay"]
    numeric_data_types = ["retail_and_recreation_percent_change_from_baseline",
                          "grocery_and_pharmacy_percent_change_from_baseline", "parks_percent_change_from_baseline",
                          "transit_stations_percent_change_from_baseline", "workplaces_percent_change_from_baseline",
                          "residential_percent_change_from_baseline"]
    # # Line Plots
    for d in numeric_data_types:
        fig, ax1 = plt.subplots()

        ax1.set_xlabel('Data Row')
        ax1.set_ylabel(main_label)
        ax1.plot(main_label, 'b-', data=data)
        ax1.tick_params(axis='y', labelcolor='blue')

        ax2 = ax1.twinx()
        ax2.set_ylabel(d.title().replace("_", " "))
        ax2.plot(d, 'r-', data=data)
        ax2.tick_params(axis='y', labelcolor='red')

        fig.tight_layout()

        plt.title(d.title().replace("_", " "))
        plt.show()

    # # Scatter Plots
    for d in numeric_data_types:
        plt.scatter(d, main_label, data=data)
        plt.title(d.replace("_", " ") + " compared to " + main_label)
        plt.ylabel(main_label)
        plt.xlabel(d.replace("_", " "))
        plt.show()

    for d in numeric_data_types:
        plt.hist(data.loc[:, d])
        plt.title("Histogram of " + d.replace("_", " "))
        plt.xlabel(d.replace("_", " "))
        plt.ylabel("Count of " + d.replace("_", " ") + " in each Bin")
        plt.show()


for label in labels:
    plot_data_numerical(data=file, main_label=label)


def plot_data_categorical(data):
    # categorical_data_types = ["CountryName", "CountryCode"]
    # numeric_data_types = ["Date", "C1_School closing", "C1_Flag", "C2_Workplace closing", "C2_Flag",
    #                       "C3_Cancel public events", "C3_Flag", "C4_Restrictions on gatherings", "C4_Flag",
    #                       "C5_Close public transport", "C5_Flag", "C6_Stay at home requirements", "C6_Flag",
    #                       "C7_Restrictions on internal movement", "C7_Flag", "C8_International travel controls",
    #                       "E1_Income support", "E1_Flag", "E2_Debt/contract relief", "E3_Fiscal measures",
    #                       "E4_International support", "H1_Public information campaigns", "H1_Flag", "H2_Testing policy",
    #                       "H3_Contact tracing", "H4_Emergency investment in healthcare", "H5_Investment in vaccines",
    #                       "H6_Facial Coverings", "H6_Flag", "StringencyIndex", "StringencyIndexForDisplay",
    #                       "StringencyLegacyIndex", "StringencyLegacyIndexForDisplay", "GovernmentResponseIndex",
    #                       "GovernmentResponseIndexForDisplay", "ContainmentHealthIndex",
    #                       "ContainmentHealthIndexForDisplay",
    #                       "EconomicSupportIndex", "EconomicSupportIndexForDisplay"]
    numeric_data_types = ["retail_and_recreation_percent_change_from_baseline",
                          "grocery_and_pharmacy_percent_change_from_baseline", "parks_percent_change_from_baseline",
                          "transit_stations_percent_change_from_baseline", "workplaces_percent_change_from_baseline",
                          "residential_percent_change_from_baseline"]
    for d in numeric_data_types:
        plt.xticks(rotation="vertical")
        data_type, counts = np.unique(data.loc[:, d], return_counts=True)
        plt.bar(data_type, counts)
        plt.title("Count of " + d)
        plt.xlabel(d)
        plt.ylabel("Count")
        plt.show()


# plot_data_categorical(data=file)
