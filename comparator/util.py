import json
import typing
import logging

import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    "plot_operator_result",
    "NumpyEncoder"
]

module_logger = logging.getLogger(__name__)

_complex_representations = {
    "cartesian": lambda a: (a.real, a.imag),
    "polar": lambda a: (np.abs(a), np.angle(a))
}

_complex_labels = {
    "cartesian": ["Real", "Imaginary"],
    "polar": ["Magnitude", "Phase"]
}

_complex_rep_type = typing.Union[
    str, typing.Tuple[typing.Callable, typing.List]]


def _ensure_ndarray(l):
    if not hasattr(l, "ndim"):
        return np.array([l])
    else:
        return l


def plot_operator_result(
    comparator_result: typing.Any,
    complex_rep: _complex_rep_type = "cartesian",
    corner_plot: bool = False,
    **subplot_kwargs
) -> typing.Tuple[list, list]:
    """
    Create a plot of the operation result from comparator objects.
    The number of subplots depends on the number of arguments that the
    operator uses. Right now, this is limited to operators that take either
    one or two arguments.

    Examples:

    .. code-block:: python

        >>> res_op, res_prod = comp(*data)
        >>> plot_operator_result(res_op) # plot everything
        >>> plot_operator_result(res_op["this"]) # just the "this" operator


    Args:
        comparator_result (dict): An object containing the result of
            applying comparator operators to some arrays. If
        complex_rep: (str, tuple): str to lookup complex representation
            function and labels, or tuple with (function, labels)
        kwargs (dict): Passed to plt.subplots
    Returns:
        tuple: list of figures and list of axes
    """
    fig_objs, axes_objs = {}, {}

    if hasattr(complex_rep, "format"):
        if complex_rep in _complex_representations:
            complex_labels = _complex_labels[complex_rep]
            complex_rep = _complex_representations[complex_rep]
        else:
            msg = f"Can't find {complex_rep} in default representations"
            module_logger.error(msg)
            raise RuntimeError(msg)
    else:
        complex_rep, complex_labels = complex_rep

    def get_subplot_dims(arr: list, res: list = None) -> list:
        if res is None:
            res = []
        if isinstance(arr[0], np.ndarray):
            res.append(len(arr))
            z_dim = 1
            if np.iscomplexobj(arr[0]):
                z_dim = 2
            res.append(z_dim)

            return res
        else:
            res.append(len(arr))
            return get_subplot_dims(arr[0], res)

    def create_subplots(subplot_dims: list) -> tuple:
        if len(subplot_dims) == 2:
            rows, n_z = subplot_dims
            fig, axes = plt.subplots(n_z*rows, **subplot_kwargs)
            axes = _ensure_ndarray(axes)

        elif len(subplot_dims) == 3:
            rows, cols, n_z = subplot_dims
            if corner_plot:
                rows -= 1
                cols -= 1
            fig, axes = plt.subplots(n_z*rows, cols, **subplot_kwargs)
            axes = _ensure_ndarray(axes)
            axes = axes.reshape((n_z*rows, cols))

        for ax in axes.flatten():
            ax.tick_params(axis='both', which='major', labelsize=6)
            ax.tick_params(axis='both', which='minor', labelsize=4)
            ax.grid(True)

        if n_z == 2:
            for z in range(n_z):
                ax = fig.add_subplot(2, 1, z+1, frameon=False)
                plt.tick_params(
                    labelcolor="none",
                    top=False,
                    bottom=False,
                    left=False,
                    right=False
                )
                ax.grid(False)
                ax.set_ylabel(f"{complex_labels[z]}")

        return fig, axes

    def single_op_plot(res_op):
        op_name = res_op.name
        if op_name is None:
            op_name = ""
        module_logger.debug((f"{__name__}.plot_operator_result: "
                             f"plotting op {op_name}"))

        subplot_dims = get_subplot_dims(res_op)

        if len(subplot_dims) > 3:
            msg = (f"{__name__}.plot_operator_result doesn't support "
                   "operators that take more than two arguments")
            module_logger.error(msg)
            raise RuntimeError(msg)

        rep = lambda a: (a, )
        if subplot_dims[-1] == 2:
            rep = complex_rep

        module_logger.debug((f"{__name__}.plot_operator_result: "
                             f"op {op_name} subplot_dims={subplot_dims}"))

        fig, axes = create_subplots(subplot_dims)
        fig.suptitle(op_name)

        if len(subplot_dims) == 2:
            rows, n_z = subplot_dims
            for i in range(rows):
                sub_res_op = rep(res_op[i])
                for z in range(n_z):
                    ax = axes[z*rows + i]
                    if res_op.labels is not None:
                        ax.yaxis.set_label_position("right")
                        ax.set_ylabel(res_op.labels[i])
                    if not (i == rows - 1 and z == n_z-1):
                        plt.setp(ax.get_xticklabels(), visible=False)
                    if sub_res_op is None:
                        ax.set_axis_off()
                    else:
                        ax.plot(sub_res_op[z])

        elif len(subplot_dims) == 3:
            n_z = subplot_dims[-1]
            rows, cols = axes.shape
            rows //= n_z
            for i in range(rows):
                for j in range(cols):
                    for z in range(n_z):
                        row_idx, col_idx = (z*rows) + j, i
                        ax = axes[row_idx][col_idx]
                        if corner_plot:
                            sub_res_op = rep(res_op[i][j+1])
                            if i > j:
                                ax.set_axis_off()
                                continue
                        else:
                            sub_res_op = rep(res_op[i][j])
                        if res_op.labels is not None and i == 0:
                            ax.set_ylabel(res_op.labels[j])
                        if not (j == rows - 1 and z == n_z-1):
                            plt.setp(ax.get_xticklabels(), visible=False)
                        else:
                            if res_op.labels is not None:
                                ax.set_xlabel(res_op.labels[i])
                        if sub_res_op is None:
                            ax.set_axis_off()
                        else:
                            ax.plot(sub_res_op[z])

        fig_objs[op_name] = fig
        axes_objs[op_name] = axes

    if hasattr(comparator_result, "keys"):
        for name in comparator_result:
            single_op_plot(comparator_result[name])
    else:
        single_op_plot(comparator_result)

    return fig_objs, axes_objs


class NumpyEncoder(json.JSONEncoder):

    int_types = (np.int64, np.int32, np.int16, np.int8)
    float_types = (np.float64, np.float32, np.float16)

    def default(self, obj):
        if any([isinstance(obj, i) for i in self.int_types]):
            return int(obj)

        if any([isinstance(obj, f) for f in self.float_types]):
            return float(obj)

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return super(NumpyEncoder, self).default(obj)
