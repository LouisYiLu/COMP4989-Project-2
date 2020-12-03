import pandas as pd
import datetime as dt
from sklearn.ensemble import StackingRegressor, RandomForestRegressor, GradientBoostingRegressor, ExtraTreesRegressor
from sklearn.svm import LinearSVR
from sklearn.metrics import mean_absolute_error
from sklearn.preprocessing import RobustScaler
from sklearn.model_selection import train_test_split


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

    # remove any rows that contain 'nan'
    data.dropna(axis=0, how='any', inplace=True)

    # change datatype of Date from int to DateTime64
    date_series = pd.to_datetime(data['Date'].astype(str), format='%Y-%m-%d')
    data['Date'] = date_series.map(dt.datetime.toordinal)
    # encoding country name
    data = pd.get_dummies(data, columns=['CountryName'],
                          prefix=['CountryName'])

    for (colName, colData) in data.iteritems():
        if "countryname" in colName.lower():
            data.drop(colName, axis=1, inplace=True)
    print(data.info())

    # separate feature and label
    data_feature = data.drop(['ConfirmedCases', 'new_cases', 'ConfirmedDeaths'], axis=1, inplace=False)
    data_label_total_cases = data.loc[:, 'ConfirmedCases']
    data_label_total_deaths = data.loc[:, 'ConfirmedDeaths']
    data_label_cases_perDay = data.loc[:, 'new_cases']

    scaler = RobustScaler()
    features = scaler.fit_transform(data_feature)

    X_train, X_test, y_train, y_test = train_test_split(features,
                                                        data_label_cases_perDay,
                                                        test_size=0.25,
                                                        random_state=42)

    estimators = [
        ('rfr', RandomForestRegressor(random_state=42, n_estimators=50)),
        ('gbr', GradientBoostingRegressor(random_state=42)),
        ('lsvr', LinearSVR(random_state=42, max_iter=1000)),
        ('etr', ExtraTreesRegressor(random_state=42, criterion='mae', n_estimators=50))
    ]

    model = StackingRegressor(
        estimators=estimators,
        final_estimator=ExtraTreesRegressor(random_state=42, n_estimators=50)
    )

    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mae = mean_absolute_error(y_test, y_pred)
    print("MAE: " + str(mae))



if __name__ == '__main__':
    # Code takes a while to run. Expect at least 15 minutes or longer.
    main()
