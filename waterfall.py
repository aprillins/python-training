import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter

def money(x, pos):
    return "${:,.0f}".format(x)

formatter = FuncFormatter(money)
index = ['sales', 'returns', 'credit fees', 'rebates', 'late charges', 'shipping']
data = {'amount': [350000, -30000, -7500, -25000, 95000, -7000]}

trans = pd.DataFrame(data=data, index=index)
blank = trans.amount.cumsum().shift(1).fillna(0)

total = trans.sum().amount
trans.loc["net"] = total
blank.loc["net"] = total

step = blank.reset_index(drop=True).repeat(3).shift(-1)
step[1::3] = np.nan

blank.loc["net"] = 0

my_plot = trans.plot(kind='bar', stacked=True, bottom=blank, legend=None, figsize=(10, 5), title="2014 Sales Waterfall")
my_plot.plot(step.index, step.values, 'k')
my_plot.set_xlabel("Transaction Types")

my_plot.yaxis.set_major_formatter(formatter)

y_height = trans.amount.cumsum().shift(1).fillna(0)

max = trans.max(0)
neg_offset = max/25
pos_offset = max/50
plot_offset = int(max/15)

loop = 0
for index, row in trans.iterrows():
    if row['amount'] == total:
        y = y_height[loop]
    else:
        y = y_height[loop] + row['amount']

    if row['amount'] > 0:
        y += pos_offset
    else:
        y -= neg_offset

    my_plot.annotate("{:,.0f}".format(row['amount']), (loop,y), ha="center")
    loop += 1

my_plot.set_ylim(0, blank.max()+int(plot_offset))
my_plot.set_xticklabels(trans.index, rotation=0)
my_plot.get_figure().savefig("waterfall.png", dpi=200, bbox_inches="tight")

