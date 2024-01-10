import numpy as np
from sklearn.linear_model import LogisticRegression
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
from pcv.io import read_ipcc_region_csv
from pathlib import Path
from sklearn.metrics import roc_auc_score

vegetation_type = "crop"
xtreme = "high"

root_folder = Path("/data/compoundx/anand/PCV/data/")

def clf_estimator(data, winter=True):
    
    Y = np.int8(train_data[:, -1])
    if winter:
        X = train_data[:, :6]
    else:
        X = train_data[:, 2:6]
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    clf.fit(X, Y)
    return clf, X, Y

csv_folder = root_folder / f"{vegetation_type}_data" / xtreme

version = "v3"
header = []

auc_winter = []
auc_without_winter = []
n_pixel = []
for region_fdir in csv_folder.iterdir():
    if (f"_{version}.csv" in str(region_fdir)) and ("logreg" not in str(region_fdir)):
        print(f"Working for region {region_fdir}")
        #year 0 # t2m_winter 1 tp_winter 2	sm_winter 3	sd_winter 4
        # t2m_sp 5 tp_sp 6 sm_sp 7 sd_sp 8 lai_sp 9 	
        # t2m_su 10	tp_su 11 sm_su 12 sd_su 13 lai_su 14

        # only take weather colums

        train_frac = 0.9
        
        keep_col_index = [1, 2, 5, 6, 10, 11, 14]
        train_data, test_data = read_ipcc_region_csv(region_fdir, train_frac)        
        train_data = train_data[:,keep_col_index, 0]
        test_data = test_data[:,keep_col_index, 0]
        train_data[~np.isnan(train_data).any(axis=1), :]
        test_data[~np.isnan(test_data).any(axis=1), :]
        
        data = np.vstack([train_data, test_data])

        X = data[:, :6]
        Y = data[:, -1]
        xtreme_X = X[Y==1]
        labels =  [" " , "t2m_winter", 	"tp_winter", 	"t2m_spring",	"tp_spring", 	"t2m_summer",	"tp_summer"]

        fig, axes = plt.subplots(1,2, figsize = (12,6))
        x_axis = np.arange(7)
        axes[0].boxplot(xtreme_X, showfliers = False, notch=True)
        axes[0].set_xticks(np.arange(7))
        axes[0].axhline(xmin=0, xmax=7, color = "r", linestyle="--")
        axes[0].set_xticklabels(labels, rotation=90)

        clf_est_w = clf_estimator(train_data, winter=True)
        
    
        Y_score_w = clf_est_w[0].predict_proba(X[:,:6])[:,1]
        auc_winter.append(roc_auc_score(Y, Y_score_w))

        clf_est = clf_estimator(train_data, winter=False)
        Y_score = clf_est[0].predict_proba(X[:,2:6])[:,1]
        auc_without_winter.append(roc_auc_score(Y, Y_score))


        RocCurveDisplay.from_estimator(*clf_est_w , ax=axes[1], **{"color":"r", "alpha":0.5})
        RocCurveDisplay.from_estimator(*clf_est , ax=axes[1], **{"color":"b", "alpha":0.5})

        n_pixel.append(int(data.shape[0]))

        region = str(region_fdir).split("/")[-1][:-4]
        header.append(region)

        fig.suptitle(f"{xtreme}_{region} | With Winter = Red | Without Winter = Blue")
        plt.tight_layout()
        print(f"Saved Figure for the region {region}")
        plt.savefig(f"/data/compoundx/anand/PCV/images/{vegetation_type}/{xtreme}/weather_train_{xtreme}_{region}.png")
        plt.close()

data = np.stack([auc_without_winter, auc_winter, n_pixel])

header = "".join([each+"\t" for each in header])
np.savetxt(f"/data/compoundx/anand/PCV/data/{vegetation_type}_data/{xtreme}/auc_{vegetation_type}_{xtreme}_{version}.csv", data , fmt='%1.3f', delimiter="\t", header=header)