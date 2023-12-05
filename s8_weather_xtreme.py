import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import average_precision_score
import matplotlib.pyplot as plt
from sklearn.metrics import RocCurveDisplay
from pcv.io import read_ipcc_region_csv
from pathlib import Path
from sklearn.metrics import roc_auc_score

vegetation_type = "forest"
xtreme = "high"

root_folder = Path("/data/compoundx/anand/PCV/data/")

def clf_estimator(train_data, val_data, winter=True):
    Y = np.int8(train_data[:, -1])
    if winter:
        X = train_data[:, :6]
    else:
        X = train_data[:, 2:6]
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    clf.fit(X, Y)
    Y = np.int8(val_data[:, -1])
    if winter:
        X = val_data[:, :6]
    else:
        X = val_data[:, 2:6]
    return clf, X, Y

def norm(arr):
    return ((arr - arr.mean(axis=0))/arr.std(axis=0))


csv_folder = root_folder / f"{vegetation_type}_data" / xtreme

for region_fdir in csv_folder.iterdir():
    if ("_v7.csv" in str(region_fdir)) and ("logreg" not in str(region_fdir)):
        print(f"Working for region {region_fdir}")
        #year 0 # t2m_winter 1	tp_winter 2	sm_winter 3	
        # t2m_spring 4 tp_spring 5 sm_spring 6 lai_spring 7	
        # t2m_summer 8	tp_summer 9	sm_summer 10 lai_su 11

        # only take weather colums

        keep_col_index = [1, 2, 5, 6, 10, 11, 14]
        train_data, val_data, test_data = read_ipcc_region_csv(region_fdir)        
        train_data = train_data[:,keep_col_index, 0]
        val_data = val_data[:,keep_col_index, 0]
        test_data = test_data[:,keep_col_index, 0]
        print(train_data.shape)
        X = norm(train_data[:, :6])
        Y = train_data[:, -1]
        xtreme_X = X[Y==1]
        labels =  [" " , "t2m_winter", 	"tp_winter", 	"t2m_spring",	"tp_spring", 	"t2m_summer",	"tp_summer"]

        fig, axes = plt.subplots(1,3, figsize = (12,6))
        x_axis = np.arange(7)
        axes[0].boxplot(xtreme_X, showfliers = False, notch=True)
        axes[0].set_xticks(np.arange(7))
        axes[0].axhline(xmin=0, xmax=7, color = "r", linestyle="--")
        axes[0].set_xticklabels(labels, rotation=90)

        # PrecisionRecallDisplay.from_estimator(*clf_estimator(train_data, val_data, winter=True) , ax=axes[2], **{"color":"r", "alpha":0.5})
        # PrecisionRecallDisplay.from_estimator(*clf_estimator(train_data, val_data, winter=False) , ax=axes[2], **{"color":"b", "alpha":0.5})

        auc_winter = []
        auc_without_winter = []

        winter_coefficient = np.zeros((100, 8))
        coefficient = np.zeros((100,6))
        for n in range(100):
            train_data, val_data, test_data = read_ipcc_region_csv(region_fdir)        
            train_data = train_data[:,keep_col_index, 0]
            val_data = val_data[:,keep_col_index, 0]
            test_data = test_data[:,keep_col_index, 0]
            clf, X, Y = clf_estimator(train_data, val_data, winter=True)
            Y_score = clf.predict_proba(X)[:,1]
            auc = roc_auc_score(Y, Y_score)
            auc_winter.append(auc)
            winter_coefficient[n, 0] = clf.intercept_
            winter_coefficient[n, 1:7] = clf.coef_
            winter_coefficient[n, 7] = auc

            clf, X, Y = clf_estimator(train_data, val_data, winter=False)
            Y_score = clf.predict_proba(X)[:,1]
            auc = roc_auc_score(Y, Y_score)
            auc_without_winter.append(auc)
            
            coefficient[n, 0] = clf.intercept_
            coefficient[n, 1:5] = clf.coef_
            coefficient[n, 5] = auc

            RocCurveDisplay.from_estimator(*clf_estimator(train_data, val_data, winter=True) , ax=axes[1],**{"color":"r", "alpha":0.2} )
            RocCurveDisplay.from_estimator(*clf_estimator(train_data, val_data, winter=False) , ax=axes[1],**{"color":"b", "alpha":0.2} )
            
            axes[1].get_legend().remove()

        region = str(region_fdir).split("/")[-1][:-4]

        header_1 = "a0\tt2m_winter\ttp_winter\tt2m_spring\ttp_spring\tt2m_summer\ttp_summer\tAUC"
        header_2 = "a0\tt2m_spring\ttp_spring\tt2m_summer\ttp_summer\tAUC"

        np.savetxt(f"/data/compoundx/anand/PCV/data/{vegetation_type}_data/{xtreme}/logreg_winter_{xtreme}_{region}.csv", winter_coefficient, fmt='%1.3f', delimiter="\t", header=header_1)
        np.savetxt(f"/data/compoundx/anand/PCV/data/{vegetation_type}_data/{xtreme}/logreg_{xtreme}_{region}.csv", coefficient, fmt='%1.3f', delimiter="\t", header=header_2)
        
        axes[2].hist(auc_winter, color = "red", bins=20, alpha=0.5)
        axes[2].hist(auc_without_winter, color="blue", bins=20, alpha=0.5)
        axes[2].axvline(np.percentile(auc_without_winter, 90), color = "k", linestyle = "--", label = "90th percentile AUC | Without Winter ")
        axes[2].axvline(np.mean(auc_winter), color="k", label = "mean AUC | With Winter ")
        axes[2].legend()


        fig.suptitle(f"{xtreme}_{region} | With Winter = Red | Without Winter = Blue")
        plt.tight_layout()
        print(f"Saved Figure for the region {region}")
        plt.savefig(f"/data/compoundx/anand/PCV/images/{vegetation_type}/{xtreme}/only_weather_{xtreme}_{region}.png")
        plt.close()
