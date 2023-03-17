import matplotlib.pyplot as plt
from sklearn.preprocessing import PolynomialFeatures
import numpy as np
import pandas as pd
import statsmodels.api as sm


N = 200
FIGURE_ROWS = 3
FIGURE_COLUMNS = 3
MAX_POLYNOMIAL_DEGREE = FIGURE_ROWS * FIGURE_COLUMNS


def preprocess_data():
    battery_data = pd.read_csv('../data/battery_train.csv')

    capacity_points = np.array([])
    RUL_points = np.array([])

    # Extract (capacity, RUL) points (over all cycles) for every battery into (capacity_points, RUL_points)
    for column in battery_data:
        if column == 'Cycle':
            continue

        capacities = battery_data[column].dropna()
        total_useful_life = len(capacities)
        RULs = np.arange(total_useful_life - 1, -1, -1) # The first measured capacity corresponds to an RUL of total_useful_life - 1 as the battery has already consumed a cycle of its life
        capacity_points = np.concatenate((capacity_points, capacities))
        RUL_points = np.concatenate((RUL_points, RULs))

    return capacity_points, RUL_points


def plot_polynomial_degrees_grid():
    '''
    Generate grid of plots with training data and predictions for different polynomial degrees
    '''

    capacity_points, RUL_points = preprocess_data()

    for plot_index, polynomial_degree in enumerate(range(1, MAX_POLYNOMIAL_DEGREE + 1)):
        transformer = PolynomialFeatures(degree=polynomial_degree, include_bias=True)
        x = transformer.fit_transform(capacity_points.reshape((-1, 1)))
        y = np.log(RUL_points + 1)
        model = sm.OLS(y, x).fit()

        x_linspace = np.linspace(np.min(capacity_points), np.max(capacity_points), N).reshape((-1, 1))
        x_axis = transformer.fit_transform(x_linspace)
        y_pred = np.exp(model.predict(x_axis)) - 1

        plt.subplot(FIGURE_ROWS, FIGURE_COLUMNS, plot_index + 1)
        plt.scatter(capacity_points, RUL_points, s=0.4)
        plt.plot(x_linspace, y_pred, c='red')
        plt.title(f'Polynomial degree of {polynomial_degree}')
        # plt.xlabel('Capacity ($Ah$)')
        # plt.ylabel('RUL ($cycles$)')
    
    # plt.tight_layout()
    plt.savefig('out/chapter_regression_model/polynomial_degrees_grid.png')
    plt.show()


def plot_polynomial_degrees():
    '''
    Generate plot with training data and predictions for different polynomial degrees
    '''

    capacity_points, RUL_points = preprocess_data()
    plt.scatter(capacity_points, RUL_points, s=0.4)
    
    for polynomial_degree in range(1, MAX_POLYNOMIAL_DEGREE + 1):
        transformer = PolynomialFeatures(degree=polynomial_degree, include_bias=True)
        x = transformer.fit_transform(capacity_points.reshape((-1, 1)))
        y = np.log(RUL_points + 1)
        model = sm.OLS(y, x).fit()
        print(model.summary())

        x_linspace = np.linspace(np.min(capacity_points), np.max(capacity_points), N).reshape((-1, 1))
        x_axis = transformer.fit_transform(x_linspace)
        y_pred = np.exp(model.predict(x_axis)) - 1

        plt.plot(x_linspace, y_pred, label=polynomial_degree)
        plt.xlabel('Capacity ($Ah$)')
        plt.ylabel('RUL ($cycles$)')
    
    plt.legend()
    plt.savefig('out/chapter_regression_model/polynomial_degrees.png')
    plt.show()


def main():
    plot_polynomial_degrees()


if __name__ == '__main__':
    main()