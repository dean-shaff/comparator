import json
import typing

import numpy as np
import matplotlib.pyplot as plt

__all__ = [
    "corner_plot"
]


def corner_plot(comparator_result: dict) -> typing.Tuple[list, list]:
    fig_objs, axes_objs = [], []
    for op_name in comparator_result:
        res_op = comparator_result[op_name]
        rows, cols, n_z = len(res_op), len(res_op[0]), len(res_op[0][0])
        fig, axes = plt.subplots(n_z*rows, cols)
        # fig.tight_layout()
        fig.suptitle(op_name)
        if not hasattr(axes, "ndim"):
            axes = [[axes]]
        else:
            axes = axes.reshape((n_z*rows, cols))
        for i in range(rows):
            for j in range(cols):
                sub_res_op = res_op[i][j]
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
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return super(NumpyEncoder, self).default(obj)
