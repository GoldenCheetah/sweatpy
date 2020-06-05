import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from scipy.optimize import curve_fit


class CriticalPowerRegressor(BaseEstimator, RegressorMixin):
    """Based on: https://scikit-learn.org/stable/developers/develop.html
    """

    def __init__(self, model="2 param", cp=300, w_prime=20000, p_max=1000):
        self.model = model
        self.cp = cp
        self.w_prime = w_prime
        self.p_max = p_max

    def _2_param_model(self, X, cp, w_prime, *args):
        t = X.T[0]  # X should be a (1, n) array
        return cp + w_prime / t

    def _3_param_model(self, X, cp, w_prime, p_max, *args):
        t = X.T[0]  # X should be a (1, n) array
        return w_prime / (t + (w_prime / (p_max - cp))) + cp

    def _model(self):
        if self.model == "2 param":
            return self._2_param_model
        elif self.model == "3 param":
            return self._3_param_model
        else:
            raise ValueError(f"self.model has an invalid value: {self.model}")

    def fit(self, X, y):
        self.n_features_in_ = 1
        X, y = check_X_y(X, y, ensure_min_samples=2)

        fitted_params, _ = curve_fit(
            f=self._model(), xdata=X, ydata=y, p0=[self.cp, self.w_prime, self.p_max]
        )
        try:
            self.cp_ = fitted_params[0]
            self.w_prime_ = fitted_params[1]
            self.p_max_ = fitted_params[2]
        except IndexError:
            pass

        self.is_fitted_ = True

        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_array(X)

        args = []
        try:
            args.append(self.cp_)
            args.append(self.w_prime_)
            args.append(self.p_max_)
        except AttributeError:
            pass

        return self._model()(X, *args)

    def _more_tags(self):
        return {"poor_score": True}
