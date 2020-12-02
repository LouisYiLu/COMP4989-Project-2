import pandas as pd
import numpy as np
from sklearn.experimental import enable_hist_gradient_boosting
from sklearn.preprocessing import OneHotEncoder
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import cross_val_score, cross_validate
import datetime as dt
from sklearn.ensemble import StackingRegressor
from sklearn.ensemble import RandomForestRegressor, AdaBoostRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.linear_model import RidgeCV
from sklearn.svm import LinearSVR
from sklearn.linear_model import LassoLars
from sklearn.linear_model import BayesianRidge, TheilSenRegressor, RANSACRegressor, ARDRegression, LogisticRegressionCV
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import RobustScaler
from sklearn.preprocessing import StandardScaler, MaxAbsScaler, MinMaxScaler


def main():
    data = pd.read_csv('../complete.csv')
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
    date_series = pd.to_datetime(data['Date'].astype(str), format='%Y%m%d')
    data['Date'] = date_series.map(dt.datetime.toordinal)
    # encoding country name
    data = pd.get_dummies(data, columns=['CountryName'],
                          prefix=['CountryName'])

    for (colName, colData) in data.iteritems():
        if "countryname" in colName.lower():
            data.drop(colName, axis=1, inplace=True)
    print(data.info())


    # separate feature and label
    data_feature = data.drop(['ConfirmedCases', 'number_of_cases_each_day', 'ConfirmedDeaths'], axis=1, inplace=False)
    data_label_total_cases = data.loc[:, 'ConfirmedCases']
    data_label_total_deaths = data.loc[:, 'ConfirmedDeaths']
    data_label_cases_perDay = data.loc[:, 'number_of_cases_each_day']

    # No scaler: 1475.0454814814816
    scaler = RobustScaler()  # 1489.337
    # scaler = StandardScaler()  # 1506.1972222222223
    # scaler = MinMaxScaler()  # 1491.3644444444444
    # scaler = MaxAbsScaler()  # 1523.0809259259258
    features = scaler.fit_transform(data_feature)
    # # test_features = scaler.fit_transform(y_train)

    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        data_label_cases_perDay,
                                                        test_size=0.25,
                                                        random_state=42)

    # estimators = [
    #     ('rcv', RidgeCV()),
    #     # ('ll', LassoLars()),
    #     # ('svr', LinearSVR(random_state=42)),
    #     ('br', BayesianRidge(fit_intercept=True, normalize=True))
    # ]
    #
    # model = StackingRegressor(
    #     estimators=estimators,
    #     final_estimator=RandomForestRegressor(n_estimators=100,
    #                                           random_state=42)
    # )
    #
    # model.fit(X_train, y_train)
    # y_pred = model.predict(X_test)
    # mae = mean_absolute_error(y_test, y_pred)
    # print("MAE: " + str(mae))

    # RFR = RandomForestRegressor(random_state=42)
    # RFR = AdaBoostRegressor()
    # RFR = GradientBoostingRegressor()
    RFR = ExtraTreesRegressor(random_state=42)
    # RFR = BayesianRidge()
    # RFR = TheilSenRegressor()
    # RFR = RANSACRegressor()
    # RFR = ARDRegression()
    # RFR = LogisticRegressionCV(max_iter=1000)
    # cross_val = cross_val_score(RFR, X_train, y_train, cv=5)
    # scores = cross_validate(RFR, X_train, y_train, scoring='neg_mean_absolute_error')
    # print(scores)

    RFR.fit(X_train, y_train)
    y_pred = RFR.predict(X_test)
    mae = np.mean(abs(y_test - y_pred))
    print('Mean Absolute Error = ', mae)


if __name__ == '__main__':
    main()
