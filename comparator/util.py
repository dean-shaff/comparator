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


def plot_operator_result(
    comparator_result: dict,
    op_name: str = None
) -> typing.Tuple[list, list]:
    """
    Create a plot of the operation result from comparator objects.
    The number of subplots depends on the number of arguments that the
    operator uses. Right now, this is limited to operators that take either
    one or two arguments.
    Args:
        comparator_result (dict): An object containing the result of
            applying comparator operators to some arrays. If
        op_name (str, optional): The name of a specific operation to plot.
            If provided, all other operations are ignored.
    Returns:
        tuple: list of figures and list of axes
    """
    fig_objs, axes_objs = [], []

    def get_subplot_dims(arr: list, res: list = None) -> list:
        if res is None:
            res = []
        if isinstance(arr[0], np.ndarray):
            res.append(len(arr))
            return res
        else:
            res.append(len(arr))
            return get_subplot_dims(arr[0], res)

    def create_subplots(subplot_dims: list) -> tuple:

        if len(subplot_dims) == 2:
            rows, n_z = subplot_dims
            fig, axes = plt.subplots(n_z*rows)
        elif len(subplot_dims) == 3:
            rows, cols, n_z = subplot_dims
            fig, axes = plt.subplots(n_z*rows, cols)

        if not hasattr(axes, "ndim"):
            axes = np.array([axes])

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
                ax.set_ylabel(f"Complex component {z+1}")

        return fig, axes

    def single_op_plot(op_name):
        module_logger.debug(f"corner_plot: plotting op {op_name}")
        res_op = comparator_result[op_name]

        subplot_dims = get_subplot_dims(res_op)
        if len(subplot_dims) > 3:
            msg = (f"{__name__}.plot_operator_result doesn't support "
                   "operators that take more than two arguments")
            module_logger.error(msg)
            raise RuntimeError(msg)

        module_logger.debug((f"corner_plot: op {op_name} has "
                             f"{subplot_dims} dims"))

        fig, axes = create_subplots(subplot_dims)

        fig.suptitle(op_name)

        if len(subplot_dims) == 2:
            rows, n_z = subplot_dims
            for i in range(rows):
                sub_res_op = res_op[i]
                for z in range(n_z):
                    ax = axes[z*rows + i]
                    if res_op.labels is not None:
                        ax.set_ylabel(res_op.labels[i])
                    if not (i == rows - 1 and z == n_z-1):
                        plt.setp(ax.get_xticklabels(), visible=False)
                    if sub_res_op is None:
                        ax.set_axis_off()
                    else:
                        ax.plot(sub_res_op[z])

        elif len(subplot_dims) == 3:
            rows, cols, n_z = subplot_dims
            for i in range(rows):
                for j in range(cols):
                    sub_res_op = res_op[i][j]
                    for z in range(n_z):
                        ax = axes[(z*rows) + j][i]
                        if res_op.labels is not None and i == rows-1:
                            ax.yaxis.set_label_position("right")
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

        fig_objs.append(fig)
        axes_objs.append(axes)

    if op_name is None:
        for op_name in comparator_result:
            single_op_plot(op_name)

    else:
        single_op_plot(op_name)

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
