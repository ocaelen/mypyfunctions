

## https://stackoverflow.com/questions/48139899/correlation-matrix-plot-with-coefficients-on-one-side-scatterplots-on-another

import matplotlib.pyplot as plt
from scipy import stats
import seaborn as sns
import numpy as np


def chartcorrelation(X):
    
    X = X.select_dtypes('number')

    def corrdot(*args, **kwargs):
        corr_r = args[0].corr(args[1], 'pearson')
        corr_text = round(corr_r, 2)
        ax = plt.gca()
        font_size = abs(corr_r) * 15 + 15
        ax.annotate(corr_text, [.5, .5,],  xycoords="axes fraction",
                    ha='center', va='center', fontsize=font_size)

    def corrfunc(x, y, **kws):
        _flag = ~(np.isnan(x) | np.isnan(y))
        r, p = stats.pearsonr(x[_flag], y[_flag])
        p_stars = ''
        if p <= 0.05:
            p_stars = '*'
        if p <= 0.01:
            p_stars = '**'
        if p <= 0.001:
            p_stars = '***'
        ax = plt.gca()
        ax.annotate(p_stars, xy=(0.65, 0.6), xycoords=ax.transAxes,
                    color='red', fontsize=25)

    sns.set(style='white', font_scale=1.6)
    g = sns.PairGrid(X, aspect=1.5, diag_sharey=False, despine=False)
    
    g.map_lower(sns.regplot, lowess=True, ci=False,
                line_kws={'color': 'red', 'lw': 1},
                scatter_kws={'color': 'black', 's': 20})
    g.map_diag(sns.histplot, color='blue')
    g.map_diag(sns.rugplot, color='black')
    g.map_upper(corrdot)
    g.map_upper(corrfunc)
    g.fig.subplots_adjust(wspace=0, hspace=0)

    # Remove axis labels
    for ax in g.axes.flatten():
        ax.set_ylabel('')
        ax.set_xlabel('')

    # Add titles to the diagonal axes/subplots
    for ax, col in zip(np.diag(g.axes), X.columns):
        ax.set_title(col, y=0.82, fontsize=15)


if __name__ == '__main__':
    dataset = sns.load_dataset('mpg')
    chartcorrelation(dataset)


    #r, p = stats.pearsonr(dataset.iloc[:,0], dataset.iloc[:,3])
    

        
    