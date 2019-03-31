import json
import typing
import logging

import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    "corner_plot",
    "NumpyEncoder"
]

module_logger = logging.getLogger(__name__)


def _plot_row():
    pass


def corner_plot(comparator_result: dict) -> typing.Tuple[list, list]:
    """
    Create a (corner) plot of the operation result from comparator objects.
    The number of subplots depends on the number of arguments that the
    operator uses. Right now, this is limited to operators that take either
    one or two arguments
    Args:
        comparator_result (dict): A dictionary containing the result of
            applying comparator operators to some arrays.
    Returns:
        tuple: list of figures and list of axes
    """
    fig_objs, axes_objs = [], []

    def get_subplot_dims(arr, res=None):
        if res is None:
            res = []
        if isinstance(arr[0], np.ndarray):
            return res
        else:
            res.append(len(arr))
            return get_subplot_dims(arr[0], res)

    for op_name in comparator_result:
        module_logger.debug(f"corner_plot: plotting op {op_name}")
        res_op = comparator_result[op_name]
        subplot_dims = get_subplot_dims(res_op)
        # rows, cols, n_z = len(res_op), len(res_op[0]), len(res_op[0][0])
        module_logger.debug((f"corner_plot: op {op_name} has "
                             f"{subplot_dims} dims"))
        fig, axes = plt.subplots(*subplot_dims)
        return
        # fig.tight_layout()
        fig.suptitle(op_name)
        if not hasattr(axes, "ndim"):
            axes = [[axes]]
        else:
            axes = axes.reshape((n_z*rows, cols))
        for i in range(rows):
            for j in range(cols):
                sub_res_op = res_op[i][j]
                module_logger.debug(sub_res_op.shape)
                for z in range(n_z):
                    ax = axes[(z*rows) + j][i]
                    if j != rows - 1:
                        plt.setp(ax.get_xticklabels(), visible=False)
                    ax.grid(True)
                    if sub_res_op is None:
                        ax.set_axis_off()
                    else:
                        ax.plot(sub_res_op[z])
        fig_objs.append(fig)
        axes_objs.append(axes)
    return fig_objs, axes_objs


class NumpyEncoder(json.JSONEncoder):

    def default(self, obj):
        if isinstance(obj, np.int64):
            return int(obj)

        if isinstance(obj, np.ndarray):
            return obj.tolist()

        return super(NumpyEncoder, self).default(obj)
