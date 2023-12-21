#!/bin/bash

#SBATCH --job-name=log
#SBATCH --time=0-02:30:00
#SBATCH --mem-per-cpu=4G
#SBATCH --cpus-per-task=1

# output files
#SBATCH -o log.out
#SBATCH -e log.err

ml purge
# ml load GCC/12.2.0  OpenMPI/4.1.4
# ml load netCDF/4.9.0
# ml load GEOS/3.11.1
module load Anaconda3
source activate PCV310

~/.conda/envs/PCV310/bin/python s8_weather_xtreme.py
