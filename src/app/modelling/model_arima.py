import pandas as pd
from scipy import stats
import statsmodels.api as sm

from itertools import product

import pickle
import warnings


data = pd.read_csv('data.csv', parse_dates=True, index_col=[0], dayfirst=True, sep=';')
data.info()

# ресэмплирование данных по дням
data_res = data.resample('1D').mean()
# сделаем преобразование Бокса-Кокса для стабилизации дисперсии
data_res['values_box'], lmbda = stats.boxcox(data_res['values'])

path_estimator = 'model_arima.pickle'

# Начальные приближения: Q=0; q=1; P=1; p=10 (p<12)
ps = range(0, 11)
d = 1
qs = range(0, 2)
Ps = range(0, 2)
D = 1
Qs = range(0, 1)

parameters = product(ps, qs, Ps, Qs)
parameters_list = list(parameters)


def model_fit(data_res):
    """
    Функция для обучения модели.

    :param data_res: датасет для обучения.
    :return: обученная модель.
    """
    results = []
    best_aic = float("inf")
    warnings.filterwarnings('ignore')
    best_model = None

    for param in parameters_list:
        # try except нужен, потому что на некоторых наборах параметров модель не обучается
        try:
            model = sm.tsa.statespace.SARIMAX(
                data_res['values_box'], order=(param[0], d, param[1]),
                seasonal_order=(param[2], D, param[3], 12)
            ).fit(disp=-1)
        # выводим параметры, на которых модель не обучается и переходим к следующему набору
        except ValueError:
            print('wrong parameters:', param)
            continue
        # Информационный критерий Акаике (AIC)
        aic = model.aic
        # сохраняем лучшую модель, aic, параметры
        if aic < best_aic:
            best_model = model
            best_aic = aic
            _best_param = param
        results.append([param, model.aic])

    warnings.filterwarnings('default')

    result_table = pd.DataFrame(results)
    result_table.columns = ['parameters', 'aic']
    print(result_table.sort_values(by='aic', ascending=True).head())

    return best_model


def main(path_estimator, data_res):

    best_model = model_fit(data_res)
    pickle.dump(
        best_model,
        open(path_estimator, "wb"),
    )


if __name__ == "__main__":
    main(path_estimator, data_res)
