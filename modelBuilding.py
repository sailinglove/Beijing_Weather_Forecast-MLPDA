# %%
import pandas as pd

# %% [markdown]
# Read data from clean data csv.

# %%
file = r'data/clean_data.csv'
df = pd.read_csv(file)
df

# %% [markdown]
# Create small sample DataFrame for easier testing.

# %%
tmp = df[['date', 'mintemp', 'meanpres', 'E_wd', 'some']].head(10)
tmp

# %%
# 1 day prior
N = 2

# target measurement of mean temperature
feature = 'mintemp'

# total number of rows
rows = tmp.shape[0]

# a list representing Nth prior measurements of feature
# notice that the front of the list needs to be padded with N
# None values to maintain the constistent rows length for each N
nth_prior_measurements = [None]*N + [tmp[feature][i-N] for i in range(N, rows)]

# make a new column name of feature_N and add to DataFrame
col_name = "{}_{}".format(feature, N)  
tmp[col_name] = nth_prior_measurements  
tmp  

# %% [markdown]
# Function for creating the required feature for the n-th prior day.

# %%
def get_nth_prior(df, feature, n): 
    rows = df.shape[0]
    nth_prior_measurements = [None]*n + [df[feature][i-n] for i in range(n, rows)]
    col_name = "{}_{}".format(feature, n)
    df[col_name] = nth_prior_measurements

# %%
features = [column for column in tmp]
print(features)

for feature in features:
    if feature != 'date':
        for n in range(1, 4):
            get_nth_prior(tmp, feature, n)

tmp

# %%
features = [column for column in df]
print(features)

for feature in features:
    if feature != 'date':
        for n in range(1, 4):
            get_nth_prior(df, feature, n)

df

# %%
df.info(verbose=True)

# %% [markdown]
# Drop rows with null value to ensure the integrity of dataset.

# %%
df_nona = df.dropna()
df_nona

# %%
import re

s = r'._\d'

to_keep = df_nona.columns[df_nona.columns.str.contains(s, regex=True)]
to_remove = [column for column in df_nona.columns if column not in to_keep]
x = df_nona.drop(to_remove, axis=1)
x

# %%
y = df_nona['meantemp']
y

# %%
from sklearn.model_selection import train_test_split

x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)
x_train

# %%
y_train

# %%
from sklearn.linear_model import LinearRegression

regressor = LinearRegression()

regressor.fit(x_train, y_train)

# %%
prediction = regressor.predict(x_test)

# %%
from sklearn.metrics import mean_absolute_error, median_absolute_error  
print("The Explained Variance: %.2f" % regressor.score(x_test, y_test))  
print("The Mean Absolute Error: %.2f degrees celsius" % mean_absolute_error(y_test, prediction))  
print("The Median Absolute Error: %.2f degrees celsius" % median_absolute_error(y_test, prediction))

# %% [markdown]
# ### Testing zone

# %%
test_file = r'data/clean_data_test.csv'
df_test = pd.read_csv(test_file)
df_test = df_test.append({}, ignore_index=True)
df_test

# %%
features = [column for column in df_test]
print(features)

for feature in features:
    if feature != 'date':
        for n in range(1, 4):
            get_nth_prior(df_test, feature, n)

df_test

# %%
df_test_nona = df_test.drop([0,1,2], axis=0).dropna(axis=1)
df_test_nona

# %%
regressor.predict(df_test_nona)

# %% [markdown]
# 20221203 offcial weather forecast:
# 
# ![weather_forecast_20221203](bj20221203weather.png)
# 
# mean temperature: $\frac{2 + (-8)}{2} = -3$
# 
# predicted mean temperature: $-5.47$
# 
# error: $2.47$


