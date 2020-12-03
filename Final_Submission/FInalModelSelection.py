import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_validate
from sklearn.ensemble import RandomForestRegressor, ExtraTreesRegressor
from sklearn.linear_model import LinearRegression
from xgboost import XGBRegressor
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
    # split train set(0.75) and test set(0.25)
    X_train, X_test, y_train, y_test = train_test_split(data_feature,
                                                        data_label_cases_perDay,
                                                        test_size=0.25,
                                                        random_state=42)
    # Cross Validation to select model (taking long time, see the result in the block-comment below)
    # RFR = RandomForestRegressor(n_estimators=300, random_state=42)
    # XGBR = XGBRegressor(objective="reg:squarederror",
    #                     random_state=42,
    #                     learning_rate=0.1,
    #                     max_depth=9,
    #                     n_estimators=350)
    # ExtraTR = ExtraTreesRegressor(n_estimators=300, random_state=42)
    # LinR = LinearRegression()
    # RFR_mae = max(cross_validate(RFR, X_train, y_train, cv=5,
    #                              scoring='neg_mean_absolute_error')['test_score'])
    # print("Random Forest cross validation done")
    # ExtraTR_mae = max(cross_validate(XGBR, X_train, y_train, cv=5,
    #                                  scoring='neg_mean_absolute_error')['test_score'])
    # print("Extra Tree cross validation done")
    # XGBR_mae = max(cross_validate(ExtraTR, X_train, y_train, cv=5,
    #                               scoring='neg_mean_absolute_error')['test_score'])
    # print("XGBoost cross validation done")
    # LinR_mae = max(cross_validate(LinR, X_train, y_train, cv=5,
    #                               scoring='neg_mean_absolute_error')['test_score'])
    # score_dict = {RFR: RFR_mae, XGBR: XGBR_mae, ExtraTR: ExtraTR_mae, LinR: LinR_mae}
    # print("Linear Regression cross validation done")

    final_model = XGBRegressor(learning_rate=0.1, max_depth=9, n_estimators=350)
    # final_model = max(score_dict, key=score_dict.get)
    print(final_model)
    final_model.fit(X_train, y_train)
    y_pred = final_model.predict(X_test)
    mae = np.mean(abs(y_test - y_pred))
    print('Mean Absolute Error = ', mae)


if __name__ == '__main__':
    main()
