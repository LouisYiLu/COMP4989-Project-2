import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from xgboost import XGBRegressor
from sklearn.model_selection import KFold
import datetime as dt


def main():
    data = pd.read_csv('dataset/complete_with_population.csv')
    data.drop("CountryCode", axis=1, inplace=True)
    data.drop("RegionName", axis=1, inplace=True)
    data.drop("RegionCode", axis=1, inplace=True)
    data.drop("M1_Wildcard", axis=1, inplace=True)
    data = data.loc[:, ~data.columns.str.contains('^Unnamed')]

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
    # XGBR = XGBRegressor(objective="reg:squarederror", random_state=42)
    # learning_rate = [0.0001, 0.001, 0.01, 0.1, 0.2, 0.3]
    # n_estimators = [50, 150, 200, 250, 300, 350]
    # max_depth = [1, 3, 5, 7, 9]
    # param_grid = dict(learning_rate=learning_rate, n_estimators=n_estimators, max_depth=max_depth)
    # kfold = KFold(n_splits=5, random_state=7, shuffle=True)
    # grid_search = GridSearchCV(XGBR, param_grid, scoring="neg_mean_absolute_error", n_jobs=-1, cv=kfold)
    # grid_result = grid_search.fit(X_train, y_train)
    # print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
    '''Best: -324.286113 using {'learning_rate': 0.1, 'max_depth': 9, 'n_estimators': 350}'''

    XGBR = XGBRegressor(objective="reg:squarederror",
                        random_state=42,
                        learning_rate=0.1,
                        max_depth=9,
                        n_estimators=350)
    XGBR.fit(X_train, y_train)
    y_pred = XGBR.predict(X_test)

    mae = np.mean(abs(y_test - y_pred))
    print('Mean Absolute Error = ', mae)


if __name__ == '__main__':
    main()
