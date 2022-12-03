import joblib

# retrive data
model_file = r'models/basicLinearRegression.model'

x_test = joblib.load(r'models/x_test.dataset')
y_test = joblib.load(r'models/y_test.dataset')

regressor = joblib.load(model_file)

# 测试模型
prediction = regressor.predict(x_test)

from sklearn.metrics import mean_absolute_error, median_absolute_error  
print("The Explained Variance: %.2f" % regressor.score(x_test, y_test))  
print("The Mean Absolute Error: %.2f degrees celsius" % mean_absolute_error(y_test, prediction))  
print("The Median Absolute Error: %.2f degrees celsius" % median_absolute_error(y_test, prediction))
