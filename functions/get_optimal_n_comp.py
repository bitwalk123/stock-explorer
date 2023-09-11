import numpy as np
from sklearn.model_selection import GridSearchCV


def get_optimal_n_comp(model, X, y, n_comp_max, cv=10) -> dict:
    # range of serach
    param = {
        'n_components': np.arange(1, n_comp_max)
    }
    # instance od\f grid search
    model_grid = GridSearchCV(
        model,
        param_grid=param,
        cv=cv
    )

    # grid search
    model_grid.fit(X, y)

    # optimal parameter
    print(model_grid.best_score_)
    return model_grid.best_params_
