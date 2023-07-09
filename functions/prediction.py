import numpy as np
import warnings

from sys import stdout
from sklearn.cross_decomposition import PLSRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.model_selection import cross_val_predict

warnings.simplefilter("ignore")


def search_minimal_component_number(X, y):
    list_mse = []
    # n_comp = int(X.shape[1] / 10)
    n_comp = 40
    component = np.arange(1, n_comp + 1)

    for i in component:
        pls = PLSRegression(n_components=i)

        # Cross-validation
        y_cv = cross_val_predict(pls, X, y, cv=10)
        # Root Mean Square Error of Precision
        mse = mean_squared_error(y, y_cv, squared=True)
        list_mse.append(mse)

        comp = 100 * (i + 1) / n_comp
        # Trick to update status on the same line
        stdout.write("\r%d%% completed" % comp)
        stdout.flush()

    stdout.write("\n")

    # Calculate and print the position of minimum in MSE
    mse_min = np.argmin(list_mse)
    # print('Suggested number of components: ', mse_min + 1)
    # stdout.write("\n")
    return mse_min


def minimal_scores(X, y, n_comp):
    # Define PLS object with optimal number of components
    pls_opt = PLSRegression(n_components=n_comp)

    # Fit to the entire dataset
    pls_opt.fit(X, y)
    y_c = pls_opt.predict(X)

    # Cross-validation
    y_cv = cross_val_predict(pls_opt, X, y, cv=10)

    # Calculate scores for calibration and cross-validation
    score_c = r2_score(y, y_c)
    score_cv = r2_score(y, y_cv)

    # Calculate mean squared error for calibration and cross validation
    mse_c = mean_squared_error(y, y_c)
    mse_cv = mean_squared_error(y, y_cv)

    result = {
        'pls': pls_opt,
        'R2 calib': score_c,
        'R2 CV': score_cv,
        'MSE calib': mse_c,
        'MSE CV': mse_cv,
    }
    return result


def search_optimal_components(X, y):
    max_comp = int(X.shape[1] / 10)

    # Define MSE array to be populated
    mse = np.zeros((max_comp, X.shape[1]))

    # Loop over the number of PLS components
    for i in range(max_comp):

        # Regression with specified number of components, using full spectrum
        pls1 = PLSRegression(n_components=i + 1)
        pls1.fit(X, y)

        # Indices of sort variables to ascending absolute value of PLS coefficients
        sorted_ind = np.argsort(np.abs(pls1.coef_[:, 0]))

        # Sort variables accordingly
        Xc = X[:, sorted_ind]

        # Discard one variable at a time of the sorted variables,
        # regress, and calculate the MSE cross-validation
        for j in range(Xc.shape[1] - (i + 1)):
            pls2 = PLSRegression(n_components=i + 1)
            pls2.fit(Xc[:, j:], y)

            y_cv = cross_val_predict(pls2, Xc[:, j:], y, cv=5)

            mse[i, j] = mean_squared_error(y, y_cv)

        comp = 100 * (i + 1) / max_comp
        stdout.write('\r%d%% completed' % comp)
        stdout.flush()

    stdout.write('\n')

    # Calculate and print the position of minimum in MSE
    mse_min_x, mse_min_y = np.where(mse == np.min(mse[np.nonzero(mse)]))

    print('Optimised number of PLS components:', mse_min_x[0] + 1)
    print('Variables to be discarded', mse_min_y[0])
    print('Optimised MSEP', '%8.6f' % mse[mse_min_x, mse_min_y][0])
    stdout.write('\n')

    return mse_min_x, mse_min_y


def optimal_scores(X, y, n_comp, x_drop):
    # Calculate PLS with optimal components and export values
    pls = PLSRegression(n_components=n_comp)

    pls.fit(X, y)
    index_sorted = np.argsort(np.abs(pls.coef_[:, 0]))
    Xc = X[:, index_sorted]
    Xc_opt = Xc[:, x_drop:]

    pls.fit(Xc_opt, y)
    y_c = pls.predict(Xc_opt)

    # Cross-Validation
    y_cv = cross_val_predict(pls, Xc_opt, y, cv=10)

    # Calculate scores for Calibration and Cross-Validation
    score_c = r2_score(y, y_c)
    score_cv = r2_score(y, y_cv)

    # Calculate mean square error for calibration and cross validation
    mse_c = mean_squared_error(y, y_c)
    mse_cv = mean_squared_error(y, y_cv)

    result = {
        'pls': pls,
        'R2 calib': score_c,
        'R2 CV': score_cv,
        'MSE calib': mse_c,
        'MSE CV': mse_cv,
        'index_sorted': index_sorted,
    }
    return result
