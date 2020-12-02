import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def scatterPlot(feature1_name, feature1, feature2_name, feature2):
    plt.scatter(feature1, feature2)
    plt.xlabel(feature1_name)
    plt.ylabel(feature2_name)
    plt.title("{} versus {}".format(feature1.name, feature2.name))
    plt.show()


def barChart(feature_name, feature):
    feature, counts = np.unique(feature, return_counts=True)
    plt.bar(feature, counts)
    plt.title("population of {}".format(feature_name))
    plt.xlabel(feature)
    plt.ylabel('number of data points')
    plt.show()


def main():
    data = pd.read_csv("../complete_new_version.csv")
    features_dict = {}
    case_label = data.loc[:, 'new_cases']
    death_label = data.loc[:, 'ConfirmedDeaths']

    features_dict['school_closing'] = data.loc[:, 'C1_School closing']
    features_dict['workplace_closing'] = data.loc[:, 'C2_Workplace closing']
    features_dict['cancel_event'] = data.loc[:, 'C3_Cancel public events']
    features_dict['restrictions_on_gatherings'] = data.loc[:, 'C4_Restrictions on gatherings']
    features_dict['close_transport'] = data.loc[:, 'C5_Close public transport']
    features_dict['stay_home_req'] = data.loc[:, 'C6_Stay at home requirements']
    features_dict['internal_movement_restrictions'] = data.loc[:, 'C7_Restrictions on internal movement']
    features_dict['international_travel_controls'] = data.loc[:, 'C8_International travel controls']
    features_dict['income_support'] = data.loc[:, 'E1_Income support']
    features_dict['debt_relief'] = data.loc[:, 'E2_Debt/contract relief']
    features_dict['fiscal_measures'] = data.loc[:, 'E3_Fiscal measures']
    features_dict['international_support'] = data.loc[:, 'E4_International support']
    features_dict['public_info_campaigns'] = data.loc[:, 'H1_Public information campaigns']
    features_dict['testing_policy'] = data.loc[:, 'H2_Testing policy']
    features_dict['contact_tracing'] = data.loc[:, 'H3_Contact tracing']
    features_dict['emergency_investment_healthcare'] = data.loc[:, 'H4_Emergency investment in healthcare']
    features_dict['investment_vaccines'] = data.loc[:, 'H5_Investment in vaccines']
    features_dict['facial_coverings'] = data.loc[:, 'H6_Facial Coverings']
    features_dict['wildcard'] = data.loc[:, 'M1_Wildcard']
    features_dict['retail_and_recreation_percent_change_from_baseline'] = \
        data.loc[:, 'retail_and_recreation_percent_change_from_baseline']
    features_dict['grocery_and_pharmacy_percent_change_from_baseline'] = \
        data.loc[:, 'grocery_and_pharmacy_percent_change_from_baseline']
    features_dict['parks_percent_change_from_baseline'] = \
        data.loc[:, 'parks_percent_change_from_baseline']
    features_dict['transit_stations_percent_change_from_baseline'] = \
        data.loc[:, 'transit_stations_percent_change_from_baseline']
    features_dict['workplaces_percent_change_from_baseline'] = \
        data.loc[:, 'workplaces_percent_change_from_baseline']
    features_dict['residential_percent_change_from_baseline'] = \
        data.loc[:, 'residential_percent_change_from_baseline']

    for key, value in features_dict.items():
        scatterPlot(key, value, "Number Of Confirmed Cases", case_label)
        # barChart(key, value)

    # for key, value in features_dict.items():
    #     scatterPlot(key, value, "Number Of Confirmed Cases Daily", case_changed_label)
    #     barChart(key, value)


if __name__ == '__main__':
    main()
