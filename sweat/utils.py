import functools
import inspect
import sys
import types

import numpy as np
import pandas as pd


CAST_TYPES = [list, pd.Series]


def type_casting(func):
    """Type casting
    This decorator casts input arguments of types [list, pandas.Series] to numpy.ndarray
    so the algorithms accept these input arguments.
    As a bonus, the decorator casts the return value of the algorithm to the type of the first
    array-like input argument.

    Parameters
    ----------
    module_or_func : [types.ModuleType, types.FunctionType]
        Module or function that has to be type casted. Can be None.

    Returns
    -------
    function
        Decorated function.
    """

    @functools.wraps(func)
    def func_wrapper(*args, **kwargs):
        output_type = None
        new_args = []

        for arg in args:
            input_type = type(arg)

            if input_type in CAST_TYPES:
                new_args.append(np.asarray(arg))

                if output_type is None:
                    # Type of first array-like argument is used for output casting
                    output_type = input_type
            else:
                new_args.append(arg)

        # There is no use-case for type casting kwargs now.
        # If there is, this can be uncommented and tests can be added.
        # new_kwargs = dict()
        # for key, value in kwargs.items():
        #     input_type = type(value)

        #     if input_type in CAST_TYPES:
        #         new_kwargs[key] = np.asarray(value)

        #         if output_type is None:
        #             # Type of first array-like argument is used for output casting
        #             output_type = input_type
        #     else:
        #         new_kwargs[key] = value
        #
        # output = func(*new_args, **new_kwargs)

        output = func(*new_args)
        if output_type is not None and isinstance(output, np.ndarray):
            return output_type(output)
        else:
            return output

    return func_wrapper


def enable_type_casting(module_or_func=None):
    """Enable type casting
    This method enables casting of input arguments to numpy.ndarray so the algorithms accept
    array-like input arguments of types list and pandas.Series.
    As a bonus, the return value of the algorithm is casted to the type of the first array-like input argument.

    Parameters
    ----------
    module_or_func : [types.ModuleType, types.FunctionType]
        Module or function that has to be type casted. Can be None.

    Returns
    -------
    function
        Decorated function.
    """
    if module_or_func is None:
        # Because sys.modules changes during this operation we cannot loop over sys.modules directly
        key_values = [(key, value) for key, value in sys.modules.items()]
        for key, value in key_values:
            # @TODO this if statement might not cover all cases (or too much cases)
            if (
                key.startswith("sweat.hrm")
                or key.startswith("sweat.pdm")
                or key.startswith("sweat.metrics")
            ):
                enable_type_casting(module_or_func=value)

    elif isinstance(module_or_func, types.ModuleType):
        for name, obj in [
            (name, obj) for name, obj in inspect.getmembers(module_or_func)
        ]:
            if (
                inspect.isfunction(obj)
                and inspect.getmodule(obj).__package__ == module_or_func.__package__
            ):
                func = getattr(module_or_func, name)
                setattr(module_or_func, name, type_casting(func))

    elif isinstance(module_or_func, types.FunctionType):
        return type_casting(module_or_func)

    else:
        raise ValueError(
            "enable_type_casting takes arguments of types [ModuleType, FunctionType]"
        )
