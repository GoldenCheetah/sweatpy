import numpy as np
from lmfit import Parameters, minimize


def _heartrate_model_predict(model_params, power):
    power = power + power.cumsum() * model_params["hr_drift"]
    hr_lin = power * model_params["dhr"] + model_params["hr_rest"]
    hr_ss = np.minimum(model_params["hr_max"], hr_lin)

    dhr = np.insert(np.diff(power), 0, 0)
    tau = np.where((dhr <= 0), model_params["tau_fall"], model_params["tau_rise"])

    predicted_hr = []
    hr_previous = model_params["hr_rest"]
    for h, t in zip(hr_ss, tau):
        hr_previous = hr_previous + (h - hr_previous) / t
        predicted_hr.append(hr_previous)

    return predicted_hr


def _heartrate_model_residuals(model_params, power, heartrate):
    model = _heartrate_model_predict(model_params, power)
    return heartrate - model


def heartrate_model(heartrate, power, **kwargs):
    """
    Source:
    De Smet et al., Heart rate modelling as a potential physical finess assessment for runners and cyclists.
    http://ceur-ws.org/Vol-1842/paper_13.pdf
    """
    # Initial model parameters
    model_params = Parameters()
    model_params.add_many(
        ("hr_rest", kwargs.get("hr_rest", 75)),
        ("hr_max", kwargs.get("hr_max", 200)),
        ("dhr", kwargs.get("dhr", 0.30)),
        ("tau_rise", kwargs.get("tau_rise", 24)),
        ("tau_fall", kwargs.get("tau_fall", 30)),
        ("hr_drift", kwargs.get("hr_drift", 3 * 10 ** -5)),
    )

    model = minimize(
        fcn=_heartrate_model_residuals,
        params=model_params,
        method="nelder",  # Nelder-Mead
        args=(power, heartrate),
    )

    predictions = _heartrate_model_predict(model.params, power)

    return model, predictions
