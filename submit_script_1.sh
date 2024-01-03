#!/bin/bash

#SBATCH --job-name=v3
#SBATCH --time=0-00:30:00
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=1

# output files
#SBATCH -o sem_v3.out
#SBATCH -e sem_v3.err

ml purge
# ml load GCC/12.2.0  OpenMPI/4.1.4
# ml load netCDF/4.9.0
# ml load GEOS/3.11.1
module load Anaconda3
source activate PCV310

~/.conda/envs/PCV310/bin/python s2_save_seasonal_data.py
