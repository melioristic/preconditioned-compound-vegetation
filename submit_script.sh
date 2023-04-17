#!/bin/bash

#SBATCH --job-name=sem_7
#SBATCH --time=0-01:30:00
#SBATCH --mem-per-cpu=4G
#SBATCH --cpus-per-task=4

# output files
#SBATCH -o sem_7.out
#SBATCH -e sem_7.err

ml purge
ml load GCC/10.2.0  OpenMPI/4.0.5
ml load netCDF/4.7.4
ml load GEOS/3.9.1
module load Anaconda3
source activate pcv

python s3_sem.py 13
