import pandas as pd


def main():
    # read 3 files
    policy_tracker = pd.read_csv('../datasets_resource/OxCGRT_latest.csv')
    mobility = pd.read_csv('../datasets_resource/Global_Mobility_Report.csv')
    covid_track_data = pd.read_csv("../datasets_resource/owid-covid-data.csv")

    unique_countries_in_policy_tracker = policy_tracker.loc[:, 'CountryName'].unique()
    unique_countries_in_mobility = mobility.loc[:, 'country_region'].unique()
    unique_countries_in_covid_tracker = covid_track_data.loc[:, 'location'].unique()

    # placeholder for country exist in both dataset
    countries_in_both = []

    # find country exist in both dataset
    for country in unique_countries_in_policy_tracker:
        if country in unique_countries_in_mobility:
            countries_in_both.append(country)

    # make sure covid cases dataset has all countries in countries_in_both; remove if not
    temp_arr_country_to_del = []
    for country in countries_in_both:
        if country not in unique_countries_in_covid_tracker:
            temp_arr_country_to_del.append(country)

    for country in temp_arr_country_to_del:
        countries_in_both.remove(country)

    # 3 new dataset contain only countries exist in both set
    mobility_data = mobility.loc[mobility['country_region'].isin(countries_in_both)]
    policy_data = policy_tracker.loc[policy_tracker['CountryName'].isin(countries_in_both)]
    covid_track_data = covid_track_data.loc[covid_track_data['location'].isin(countries_in_both)]

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

    # change dtype to Datetime64
    date_series = pd.to_datetime(mobility_data['date'])
    mobility_data['date'] = date_series

    # Step1: keep consistency of country that contains all data within 2020-02-15 to 2020-11-01
    inconsistent_countries = []
    for country in mobility_data.loc[:, 'country_region'].unique():
        number_row_of_country = mobility_data.loc[(mobility_data['country_region'] == country)].shape[0]
        if number_row_of_country != 261:
            inconsistent_countries.append(country)

    mobility_data = mobility_data.sort_values(by=['country_region', 'date'])
    mobility_data = mobility_data.reset_index(drop=True)
    mobility_data = mobility_data.rename(columns={'country_region': 'CountryName', 'date': 'Date'})

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

    policy_data = policy_data.sort_values(by=['CountryName', 'Date'])
    policy_data = policy_data.reset_index(drop=True)

    # ============================COVID-19 CASES PREPROCESS================================

    covid_track_data = covid_track_data.rename(columns={'location': 'CountryName', 'date': 'Date'})
    # subset select to only feature we need
    covid_track_data = covid_track_data.loc[:, ('CountryName', 'Date', 'new_cases')]

    # only want data within range 2020-02-15 to 2020-11-01
    date_series = pd.to_datetime(covid_track_data['Date'])
    covid_track_data['Date'] = date_series
    covid_track_data = covid_track_data.loc[(covid_track_data['Date'] >= start_time)
                                            & (covid_track_data['Date'] <= end_time)]

    # Step1: keep consistency of country that contains all data within 2020-02-15 to 2020-11-01
    for country in covid_track_data.loc[:, 'CountryName'].unique():
        number_row_of_country = covid_track_data.loc[(covid_track_data['CountryName'] == country)].shape[0]
        if number_row_of_country != 261:
            inconsistent_countries.append(country)

    covid_track_data = covid_track_data.sort_values(by=['CountryName', 'Date'])
    covid_track_data = covid_track_data.reset_index(drop=True)

    # ===========================3 dataset final clean-up===================================

    # Step2: remove inconsistent country
    for inconsistent_country in inconsistent_countries:
        mobility_data = mobility_data.loc[(mobility_data['CountryName'] != inconsistent_country)]
        policy_data = policy_data.loc[(policy_data['CountryName'] != inconsistent_country)]
        covid_track_data = covid_track_data.loc[(covid_track_data['CountryName'] != inconsistent_country)]

    print("policy # of countries: {}\nmobility # of countries: {}\ncases # of countries: {}".format(
        policy_data.loc[:, 'CountryName'].unique().shape[0],
        mobility_data.loc[:, 'CountryName'].unique().shape[0],
        covid_track_data.loc[:, 'CountryName'].unique().shape[0],
    ))
    print("================================")
    print("policy # of rows: {}\nmobility # of rows: {}\ncases # of rows: {}".format(
        policy_data.shape[0], mobility_data.shape[0], covid_track_data.shape[0]
    ))

    # join 3 DataFrames
    result = pd.merge(policy_data, mobility_data, on=['CountryName', 'Date'])
    result = pd.merge(result, covid_track_data, on=['CountryName', 'Date'])

    result.to_csv("../complete_new_version.csv")


if __name__ == '__main__':
    main()
