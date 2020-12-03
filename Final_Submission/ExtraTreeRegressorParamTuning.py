import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import ExtraTreesRegressor
from sklearn.model_selection import KFold
import datetime as dt


def main():
    data = pd.read_csv('dataset/complete.csv')
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

    data = data.fillna(method='ffill')
    # remove any rows that contain 'nan'
    data.dropna(axis=0, how='any', inplace=True)

    # change datatype of Date from int to DateTime64
    date_series = pd.to_datetime(data['Date'])
    data['Date'] = date_series.map(dt.datetime.toordinal)

    # encoding country name
    data = pd.get_dummies(data, columns=['CountryName'],
                          prefix=['CountryName'])

    for (colName, colData) in data.iteritems():
        if "countryname" in colName.lower():
            data.drop(colName, axis=1, inplace=True)
    print(data.info())

    # separate feature and label
    data_feature = data.drop(['ConfirmedCases', 'ConfirmedDeaths',
                              'new_cases'], axis=1, inplace=False)
    data_label_cases_perDay = data.loc[:, 'new_cases']

    X_train, X_test, y_train, y_test = train_test_split(data_feature,
                                                        data_label_cases_perDay,
                                                        test_size=0.25,
                                                        random_state=42)
    # Parameters tuning (Note: taking long time)
    EXTR = ExtraTreesRegressor(random_state=42)
    n_estimators = [50, 100, 150, 200, 250, 300]
    param_grid = dict(n_estimators=n_estimators)
    kfold = KFold(n_splits=10, random_state=7, shuffle=True)
    grid_search = GridSearchCV(EXTR, param_grid, scoring="neg_mean_absolute_error", n_jobs=-1, cv=kfold)
    grid_result = grid_search.fit(X_train, y_train)
    print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))

    EXTR = ExtraTreesRegressor(n_estimators=50, random_state=42)
    EXTR.fit(X_train, y_train)
    y_pred = EXTR.predict(X_test)

    mae = np.mean(abs(y_test - y_pred))
    print('Mean Absolute Error = ', mae)


if __name__ == '__main__':
    main()
