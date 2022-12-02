import pandas as pd
import re
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

# prepare data
file = r'data/clean_data.csv'
df = pd.read_csv(file)

def get_nth_prior(df, feature, n): 
    rows = df.shape[0]
    nth_prior_measurements = [None]*n + [df[feature][i-n] for i in range(n, rows)]
    col_name = "{}_{}".format(feature, n)
    df[col_name] = nth_prior_measurements

features = [column for column in df]
print(features)

for feature in features:
    if feature != 'date':
        for n in range(1, 4):
            get_nth_prior(df, feature, n)

df_nona = df.dropna()

s = r'._\d'

to_keep = df_nona.columns[df_nona.columns.str.contains(s, regex=True)]
to_remove = [column for column in df_nona.columns if column not in to_keep]
# x: features
x = df_nona.drop(to_remove, axis=1)
# y: target
y = df_nona['meantemp']

# 分出训练集和测试集，测试集约20%
x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2, random_state=42)

regressor = LinearRegression()
# 训练模型
regressor.fit(x_train, y_train)

# 测试模型
prediction = regressor.predict(x_test)

from sklearn.metrics import mean_absolute_error, median_absolute_error  
print("The Explained Variance: %.2f" % regressor.score(x_test, y_test))  
print("The Mean Absolute Error: %.2f degrees celsius" % mean_absolute_error(y_test, prediction))  
print("The Median Absolute Error: %.2f degrees celsius" % median_absolute_error(y_test, prediction))
