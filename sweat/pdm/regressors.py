import numpy as np
from sklearn.base import BaseEstimator, RegressorMixin
from sklearn.utils.validation import check_X_y, check_array, check_is_fitted
from scipy.optimize import curve_fit


class PowerDurationRegressor(BaseEstimator, RegressorMixin):
    """Based on: https://scikit-learn.org/stable/developers/develop.html"""

    def __init__(
        self,
        model="2 param",
        cp=300,
        w_prime=20000,
        p_max=1000,
        tau=300,
        tcp_max=1800,
        a=50,
    ):
        self.model = model
        self.cp = cp
        self.w_prime = w_prime
        self.p_max = p_max
        self.tau = tau
        self.tcp_max = tcp_max
        self.a = a

    def _2_param_model(self, X, cp, w_prime, *args):
        t = X.T[0]  # X should be a (1, n) array
        return cp + w_prime / t

    def _3_param_model(self, X, cp, w_prime, p_max, *args):
        t = X.T[0]  # X should be a (1, n) array
        return w_prime / (t + (w_prime / (p_max - cp))) + cp

    def _exp_model(self, X, cp, p_max, tau, *args):
        """
        Source: Hopkins, W. G., Edmond, I. M., Hamilton, B. H., Macfarlane, D. J., & Ross, B. H. (1989). Relation between power and endurance for treadmill running of short duration. Ergonomics, 32(12), 1565-1571.
        """
        t = X.T[0]  # X should be a (1, n) array
        return (p_max - cp) * np.exp(-t / tau) + cp

    def _omni_model(self, X, cp, p_max, w_prime, a, *args):
        """
        Source: Puchowicz, M. J., Baker, J., & Clarke, D. C. (2020). Development and field validation of an omni-domain power-duration model. Journal of Sports Sciences, 38(7), 801-813.
        """
        t = X.T[0]  # X should be a (1, n) array

        result = w_prime / t * (1 - np.exp(-t * (p_max - cp) / w_prime)) + cp

        return np.where(
            t <= self.tcp_max, result, result - a * np.log(t / self.tcp_max)
        )

    def _model_selection(self):
        if self.model == "2 param":
            func = self._2_param_model
            params = ["cp", "w_prime"]
            return func, params
        elif self.model == "3 param":
            func = self._3_param_model
            params = ["cp", "w_prime", "p_max"]
            return func, params
        elif self.model == "exponential":
            func = self._exp_model
            params = ["cp", "p_max", "tau"]
            return func, params
        elif self.model == "omni":
            func = self._omni_model
            params = ["cp", "p_max", "w_prime", "a"]
            return func, params
        else:
            raise ValueError(f"self.model has an invalid value: {self.model}")

    def fit(self, X, y):
        self.n_features_in_ = 1
        X, y = check_X_y(X, y, ensure_min_samples=2)

        func, params = self._model_selection()

        initial_params = [getattr(self, param_name) for param_name in params]
        fitted_params, _ = curve_fit(f=func, xdata=X, ydata=y, p0=initial_params)

        for name, value in zip(params, fitted_params):
            setattr(self, f"{name}_", value)

        self.is_fitted_ = True

        return self

    def predict(self, X):
        check_is_fitted(self)
        X = check_array(X)

        func, params = self._model_selection()

        args = []
        for param_name in params:
            args.append(getattr(self, f"{param_name}_"))

        return func(X, *args)

    def _more_tags(self):
        return {"poor_score": True}
