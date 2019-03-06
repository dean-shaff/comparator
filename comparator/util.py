import typing

import matplotlib.pyplot as plt

__all__ = [
    "corner_plot"
]


def corner_plot(comparator_result: dict) -> typing.Tuple[list, list]:
    fig_objs, axes_objs = [], []
    for op_name in comparator_result:
        res_op = comparator_result[op_name]
        rows, cols = len(res_op), len(res_op[0])
        fig, axes = plt.subplots(rows, cols)
        # fig.tight_layout()
        fig.suptitle(op_name)
        if not hasattr(axes, "ndim"):
            axes = [[axes]]
        else:
            axes = axes.reshape((rows, cols))
        for i in range(rows):
            for j in range(cols):
                sub_res_op = res_op[i][j]
                ax = axes[j][i]
                if j != rows - 1:
                    plt.setp(ax.get_xticklabels(), visible=False)
                ax.grid(True)
                if sub_res_op is None:
                    ax.set_axis_off()
                else:
                    for z in range(len(sub_res_op)):
                        ax.plot(sub_res_op[z][0])
        fig_objs.append(fig)
        axes_objs.append(axes)
    return fig_objs, axes_objs
