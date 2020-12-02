import pandas as pd
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_validate
import datetime as dt


def main():
    data = pd.read_csv('../complete_new_version.csv')
    data.drop("CountryCode", axis=1, inplace=True)
    data.drop("RegionName", axis=1, inplace=True)
    data.drop("RegionCode", axis=1, inplace=True)
    data.drop("M1_Wildcard", axis=1, inplace=True)

    # Remove Flag Columns
    for (colName, colData) in data.iteritems():
        if "flag" in colName.lower():
            data.drop(colName, axis=1, inplace=True)
        if "index" in colName.lower():
            data.drop(colName, axis=1, inplace=True)

    # remove any rows that contain 'nan'
    data.dropna(axis=0, how='any', inplace=True)

    # change datatype of Date from int to DateTime64
    date_series = pd.to_datetime(data['Date'])
    data['Date'] = date_series.map(dt.datetime.toordinal)

    # encoding country name
    data = pd.get_dummies(data, columns=['CountryName'],
                          prefix=['CountryName'])

    # for (colName, colData) in data.iteritems():
    #     if "countryname" in colName.lower():
    #         data.drop(colName, axis=1, inplace=True)
    print(data.info())


    # separate feature and label
    data_feature = data.drop(['ConfirmedCases', 'ConfirmedDeaths',
                              'new_cases'], axis=1, inplace=False)
    data_label_cases_perDay = data.loc[:, 'new_cases']

    X_train, X_test, y_train, y_test = train_test_split(data_feature,
                                                        data_label_cases_perDay,
                                                        test_size=0.25,
                                                        random_state=42)
    RFR = RandomForestRegressor()
    # cross_val = cross_val_score(RFR, X_train, y_train, cv=5)
    # scores = cross_validate(RFR, X_train, y_train, scoring='neg_mean_absolute_error')
    # print(scores)

    RFR.fit(X_train, y_train)
    y_pred = RFR.predict(X_test)
    mae = np.mean(abs(y_test - y_pred))
    print('Mean Absolute Error = ', mae)


if __name__ == '__main__':
    main()
