COMP4989 Project2 Group 5
Team member: Jame Pike, John Gilpin, Jaskamal Singh, Yi(Louis) Lu
==================================================================

Requirement
-----------
- Please install library: XGBoost (pip install XGBoost)
- Please make sure dataset folder were in the current folder
- When running python codes, no argument is needed


File Explanation
-----------------
- Dataset used are in dataset folder
    - complete.csv and complete_with_population.csv are the merged file we created

- BuildDataset.py is used to merge policy_tracker_data, global_mobility_data and global_COVID-19_cases_tracker.

- add_population.py is used to merge complete.csv with population columns

- Various Model Tuning (ExtraTreeRegressor, RandomForestRegressor, XGBRegressor)
    - cross validation for parameter tuning has been commented out because it was taking quite a long time to process.
    - Output for those file were the mae after parameter tuning.
    - CountryName and its categorical encoding has been removed for faster process.

- StackingRegressor.py was not used in FinalModelSelection. It takes too long to run even without cross validation for
  parameter tuning.

- Final ModelSelection
    - Cross validation for model selection has been commented out as it's taking long time.
    - Output:
    `# Final Model is the best model result from corss validation`
    `# Final Model's mae on complete_with_population.csv`



