import numpy as np

class LinearRegression:
    @staticmethod
    def predict(x):
        n = len(x)
        months = np.array([i for i in range(0, n)])
        y = np.array(x)
        sum_x = np.sum(months)
        sum_y = np.sum(y)
        sum_xy = np.sum(months*y)
        sum_x_squared = np.sum(months ** 2)
        slope = (n * sum_xy - sum_x * sum_y) / (n * sum_x_squared - sum_x ** 2)
        intercept = (sum_y - slope * sum_x) / n
        return round(intercept + slope * n, 2)

        
