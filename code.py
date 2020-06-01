# Use the following data for this assignment:
# Add this line bellow if used in a Jupyter Notebook: 
# %matplotlib notebook
import matplotlib.pyplot as plt
from scipy import stats as sts
import pandas as pd
import numpy as np

np.random.seed(12345)

df = pd.DataFrame([np.random.normal(32000,200000,3650), 
                   np.random.normal(43000,100000,3650), 
                   np.random.normal(43500,140000,3650), 
                   np.random.normal(48000,70000,3650)], 
                  index=[1992,1993,1994,1995])
#
# Calculate the 95% confidence interval for the population means
#
def mean_confidence_interval(data, confidence=0.95):
    a = 1.0 * np.array(data)
    n = len(a)
    m, se = np.mean(a), sts.sem(a)
    h = se * sts.t.ppf((1 + confidence) / 2., n-1)
    return m, h
#
# Values to be plotted
#
labels = list(df.index)
means = [mean_confidence_interval(df.iloc[x])[0] for x in range(4)]
errors = [mean_confidence_interval(df.iloc[x])[1] for x in range(4)]
print('\nClick anywhere in the graphic to set the new Value to compare')

import matplotlib.patches as mpatches
#
# Barplot function
#
def Barcomp(Value):
    # Bar Colors
    Color = []
    for x in range(4):
        if Value > means[x] and Value > (means[x] + errors[x]):
            Color.append("blue")
        elif Value > means[x] and Value < (means[x]+ errors[x]):
            Color.append("ghostwhite")
        elif Value < means[x]  and Value > (means[x]- errors[x]):
            Color.append("floralwhite")
        elif Value < means[x]  and Value < (means[x]- errors[x]):
            Color.append("red")
    #Plot the barplot
    plt.bar(range(4), means,yerr=errors,error_kw={'ecolor':'0.3','capsize':4},alpha=0.7, color= Color, edgecolor='k')
    plt.axhline(y=Value)
    plt.xticks(range(4),labels)
    plt.ylim((0,65000))
    #Remove top and right sidelines
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['top'].set_visible(False)
    # Add the legend explaining the color code
    blue_patch = mpatches.Patch(color='b', label='High Value')
    ghostwhite_patch = mpatches.Patch(color='ghostwhite', label='Value > mean < top CI limit')
    floralwhite_patch = mpatches.Patch(color='floralwhite',  label='Value < mean > bottom CI limit')
    red_patch = mpatches.Patch(color='r', label='Low Value')
    plt.legend(handles=[blue_patch, ghostwhite_patch, floralwhite_patch, red_patch], loc="upper right", prop={'size': 8})
    plt.show()
    
#
#Introduce a value to test
Barcomp(41000)
#
# Change the y value by clicking somewhere
def onclick(event):
    plt.cla()
    plt.gca().set_title('You have selected the value of Y = {}'.format(event.ydata))
    Barcomp(event.ydata)
plt.gcf().canvas.mpl_connect('button_press_event', onclick)
