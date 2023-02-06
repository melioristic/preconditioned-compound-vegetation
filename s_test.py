from pcv.stats import SEMStats

import xarray as xr


model_num = 5
sem_data = xr.open_dataset(f"/data/compoundx/anand/PCV/data/sem_data_{model_num}.nc")

sem_stats = SEMStats(sem_data)
x = sem_stats.link_ranking_region()
print(x)

