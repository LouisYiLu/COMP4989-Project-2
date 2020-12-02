import pandas as pd


def main():
    # read 2 files
    policy_tracker = pd.read_csv('../datasets_resource/OxCGRT_latest.csv')
    mobility = pd.read_csv('../datasets_resource/Global_Mobility_Report.csv')

    unique_countries_in_policy_tracker = policy_tracker.loc[:, 'CountryName'].unique()
    unique_countries_in_mobility = mobility.loc[:, 'country_region'].unique()

    # placeholder for country exist in both dataset
    countries_in_both = []

    # find country exist in both dataset
    for country in unique_countries_in_policy_tracker:
        if country in unique_countries_in_mobility:
            countries_in_both.append(country)

    # 2 new dataset contain only countries exist in both set
    mobility_data = mobility.loc[mobility['country_region'].isin(countries_in_both)]
    policy_data = policy_tracker.loc[policy_tracker['CountryName'].isin(countries_in_both)]

    # delete 2 big csv reading
    del policy_tracker
    del mobility

    # =======================MOBILITY PREPROCESS========================

    # only need country in general, not targeted region
    mobility_data = mobility_data[mobility_data["sub_region_1"].isnull()]
    mobility_data = mobility_data[mobility_data["sub_region_2"].isnull()]
    mobility_data = mobility_data[mobility_data["metro_area"].isnull()]

    # drop irrelevant features
    mobility_data = mobility_data.drop(columns=['sub_region_1',
                                                'sub_region_2',
                                                'metro_area',
                                                'iso_3166_2_code',
                                                'census_fips_code',
                                                'country_region_code'])
    mobility_data = mobility_data.loc[:, ~mobility_data.columns.str.contains('^Unnamed')]

    date_series = pd.to_datetime(mobility_data['date'])
    mobility_data['date'] = date_series

    # Step1: keep consistency of country that contains all data within 2020-02-15 to 2020-11-01
    inconsistent_countries = []
    for country in mobility_data.loc[:, 'country_region'].unique():
        number_row_of_country = mobility_data.loc[(mobility_data['country_region'] == country)].shape[0]
        if number_row_of_country != 261:
            inconsistent_countries.append(country)

    # ===============================POLICY PREPROCESS================================

    # only need country in general, not targeted region
    policy_data = policy_data[policy_data["RegionName"].isnull()]

    # only want data within range 2020-02-15 to 2020-11-01
    date_series = pd.to_datetime(policy_data['Date'].astype(str), format='%Y%m%d')
    policy_data['Date'] = date_series
    start_time = pd.to_datetime("2020-02-15")
    end_time = pd.to_datetime("2020-11-01")
    policy_data = policy_data.loc[(policy_data['Date'] >= start_time) & (policy_data['Date'] <= end_time)]

    # Step1: keep consistency of country that contains all data within 2020-02-15 to 2020-11-01
    for country in policy_data.loc[:, 'CountryName'].unique():
        number_row_of_country = policy_data.loc[(policy_data['CountryName'] == country)].shape[0]
        if number_row_of_country != 261:
            inconsistent_countries.append(country)

    # Step2: remove inconsistent country
    for inconsistent_country in inconsistent_countries:
        mobility_data = mobility_data.loc[(mobility_data['country_region'] != inconsistent_country)]
        policy_data = policy_data.loc[(policy_data['CountryName'] != inconsistent_country)]

    print("policy # of rows: {}\nmobility # of rows: {}".format(
        policy_data.shape[0], mobility_data.shape[0]
    ))



    mobility_data = mobility_data.sort_values(by=['country_region', 'date'])
    mobility_data = mobility_data.reset_index(drop=True)
    policy_data = policy_data.sort_values(by=['CountryName', 'Date'])
    policy_data = policy_data.reset_index(drop=True)

    #join 2 dataframe
    mobility_data = mobility_data.rename(columns={'country_region': 'CountryName', 'date': 'Date'})
    result = pd.merge(policy_data, mobility_data, on=['CountryName', 'Date'])

    result.to_csv("complete.csv")


if __name__ == '__main__':
    main()
