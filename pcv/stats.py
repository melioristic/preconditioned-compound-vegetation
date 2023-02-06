from pcv.cfg import IPCC_REGION_SHPFILE, CLIM_MASK_PATH 
import os
import numpy as np

class SEMStats():
    def __init__(self, sem_data) -> None:
        self.sem_data = sem_data
        self.clim_mask_path = CLIM_MASK_PATH

        
    def link_ranking_region(self):
        variable_list = []
        for link in self.sem_data.variables:
            if "_Estimate" in link and not("~~" in link):
                variable_list.append(link)

        sem_link_estimate = self.sem_data[variable_list].to_array("link_estimate").to_numpy()
        arg_sorted = np.float32(np.absolute(np.argsort(sem_link_estimate, axis = 0)))
        mask = np.sum(sem_link_estimate, axis=0)!= np.nan

        arg_sorted[:,~mask] = np.nan

        clim_mask_path = "/data/compoundx/anand/PCV/data/clim_mask/"
        clim_files = [clim_mask_path + file for file in os.listdir(clim_mask_path) if ".npy" in file ]
        

        rank_var_dict = {}

        rank_var_dict["var_list"] = variable_list

        for _, files in enumerate(clim_files):
            
            mask_clim = np.load(files)

            if sum(sum(mask_clim))>10:
                region_name = files.split("/")[-1][:-4]
                rank_var_dict[region_name] = {}
                for i in range(arg_sorted.shape[0]):
                
                    region_data = arg_sorted[i,mask_clim]

                    rank_var_dict[region_name][i] = np.unique(region_data, return_counts=True)

        return rank_var_dict