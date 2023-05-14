import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
from sklearn.metrics import PrecisionRecallDisplay

from pathlib import Path

vegetation_type = "crop"
xtreme = "low"

root_folder = Path("/data/compoundx/anand/PCV/data/")


def clf_estimator(data, winter=True):
    Y = data[:, -1]
    if winter:
        X =data[:, :6]
    else:
        X = data[:, 2:6]
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    clf.fit(X, Y)

    return clf, X, Y

def norm(arr):
    return ((arr - arr.mean(axis=0))/arr.std(axis=0))


csv_folder = root_folder / f"{vegetation_type}_data" / xtreme

for region_fdir in csv_folder.iterdir():
    if ".csv" in str(region_fdir):

        # t2m_winter 0	tp_winter 1	sm_winter 2	
        # t2m_spring 3 tp_spring 4 sm_spring 5 lai_spring 6	
        # t2m_summer 7	tp_summer 8	sm_summer 9	lai_su 10

        # only take weather colums

        keep_col_index = [0, 1, 3, 4, 7, 8, 10]
        data = np.loadtxt(region_fdir)
        data = data[~np.isnan(data).any(axis=1), :]
        data = data[:,keep_col_index]

        X = norm(data[:, :6])
        Y = data[:, -1]
        xtreme_X = X[Y==1]

        labels =  [" " , "t2m_winter", 	"tp_winter", 	"t2m_spring",	"tp_spring", 	"t2m_summer",	"tp_summer"]

        fig, axes = plt.subplots(1,3, figsize = (12,6))
        x_axis = np.arange(7)
        axes[0].boxplot(xtreme_X, showfliers = False)
        axes[0].set_xticks(np.arange(7))
        axes[0].axhline(xmin=0, xmax=7, color = "r", linestyle="--")
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

        plt.savefig(f"/data/compoundx/anand/PCV/images/{vegetation_type}/{xtreme}/only_weather_{xtreme}_{region}.png")

        plt.close()
