import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import PrecisionRecallDisplay

from pathlib import Path

vegetation_type = "forest"
xtreme = "low"

root_folder = Path("/data/compoundx/anand/PCV/data/")


def clf_estimator(data, winter=True):
    Y = data[:, -1]
    if winter:
        X =data[:, :10]
    else:
        X = data[:, 3:10]
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    clf.fit(X, Y)

    return clf, X, Y

def norm(arr):
    return ((arr - arr.mean(axis=0))/arr.std(axis=0))


csv_folder = root_folder / f"{vegetation_type}_data" / xtreme

for region_fdir in csv_folder.iterdir():
    if ".csv" in str(region_fdir):

        data = np.loadtxt(region_fdir)
        data = data[~np.isnan(data).any(axis=1), :]

        X = norm(data[:, :10])
        Y = data[:, -1]
        xtreme_X = X[Y==1]

        labels =  [" " , "t2m_winter", 	"tp_winter",	"sm_winter", 	"t2m_spring",	"tp_spring", 	"sm_spring", "lai_spring",	"t2m_summer",	"tp_summer",	"sm_summer"]

        fig, axes = plt.subplots(1,3, figsize = (12,6))
        x_axis = np.arange(7)
        axes[0].boxplot(xtreme_X, showfliers = False)
        axes[0].set_xticks(np.arange(11))
        axes[0].axhline(xmin=0, xmax=10, color = "r", linestyle="--")
        axes[0].set_xticklabels(labels, rotation=90)

        try:
            RocCurveDisplay.from_estimator(*clf_estimator(data, winter=True) , ax=axes[1],**{"color":"r"} )
            PrecisionRecallDisplay.from_estimator(*clf_estimator(data, winter=True) , ax=axes[2], **{"color":"r"})
            RocCurveDisplay.from_estimator(*clf_estimator(data, winter=False) , ax=axes[1],**{"color":"b"} )
            PrecisionRecallDisplay.from_estimator(*clf_estimator(data, winter=False) , ax=axes[2], **{"color":"b"})
        except:
            pass
        region = str(region_fdir).split("/")[-1][:-4]

        fig.suptitle(f"{xtreme}_{region} | With Winter = Red | Wihout Winter = Blue")
        plt.tight_layout()

        plt.savefig(f"/data/compoundx/anand/PCV/images/{vegetation_type}/{xtreme}/{xtreme}_{region}.png")

        plt.close()
