import numpy as np
from sklearn.linear_model import LogisticRegression
from pcv.io import read_ipcc_region_csv
from pathlib import Path
from sklearn.metrics import roc_auc_score
from sklearn.metrics import log_loss
from scipy.stats.distributions import chi2

vegetation_type = "forest"
xtreme = "low"

root_folder = Path("/data/compoundx/anand/PCV/data/")

def get_ll(X, winter=True):
    Y = np.int8(train_data[:, -1])
    
    if winter:
        X = train_data[:, :6]
    else:
        X = train_data[:, 2:6]
    
    clf = LogisticRegression(max_iter=5000, class_weight="balanced")
    clf.fit(X, Y)
    Y_pred = clf.predict(X)

    return -log_loss(Y, Y_pred)*len(Y)

def norm(arr):
    return ((arr - arr.mean(axis=0))/arr.std(axis=0))

csv_folder = root_folder / f"{vegetation_type}_data" / xtreme

version = "v3"
for region_fdir in csv_folder.iterdir():
    if (f"_{version}.csv" in str(region_fdir)) and ("logreg" not in str(region_fdir)):
        region = str(region_fdir).split("/")[-1][:-4]

        print(f"Working for {vegetation_type}, {xtreme}, {region}")
        #year 0 # t2m_winter 1 tp_winter 2	sm_winter 3	sd_winter 4
        # t2m_sp 5 tp_sp 6 sm_sp 7 sd_sp 8 lai_sp 9 	
        # t2m_su 10	tp_su 11 sm_su 12 sd_su 13 lai_su 14

        # only take weather colums

        keep_col_index = [1, 2, 5, 6, 10, 11, 14]
        train_data, test_data = read_ipcc_region_csv(region_fdir)        
        train_data = train_data[:,keep_col_index, 0]
        test_data = test_data[:,keep_col_index, 0]
        train_data[~np.isnan(train_data).any(axis=1), :]
        test_data[~np.isnan(test_data).any(axis=1), :]
        
        data = np.vstack([train_data, test_data])
        X = data[:, :6]
        Y = data[:, -1]
        xtreme_X = X[Y==1]
        labels =  [" " , "t2m_winter", 	"tp_winter", 	"t2m_spring",	"tp_spring", 	"t2m_summer",	"tp_summer"]

        ## 
        LL1 = get_ll(X, winter=False)
        LL2 = get_ll(X, winter=True)
        print(LL1, LL2)
        LR = 2 * (LL2 - LL1)
        p = chi2.sf(LR,2)
        print(LR)
        print(p)
        print(f"Significant {p<0.05}")
        print(50*"==")
