#!/bin/bash

#SBATCH --job-name=sem_nhem
#SBATCH --time=0-02:30:00
#SBATCH --mem-per-cpu=8G


# output files
#SBATCH -o sem_2.out
#SBATCH -e sem_2.err

ml load GCC/10.2.0  OpenMPI/4.0.5
ml load netCDF/4.7.4
module load Anaconda3
conda init bash
source activate pcv

python s3_sem.py

