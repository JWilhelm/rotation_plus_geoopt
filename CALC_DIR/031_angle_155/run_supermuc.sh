#!/bin/bash
# Job Name and Files (also --job-name)
#SBATCH -J WWrot

#Output and error (also --output, --error):
#SBATCH -o ./%x.%j.out
#SBATCH -e ./%x.%j.err

#Initial working directory (also --chdir):
#SBATCH -D ./

# Change here the job size and time limit:
#SBATCH --time=00:20:00
#SBATCH --nodes=16
#SBATCH --ntasks-per-core=1
#SBATCH --ntasks-per-node=48
#SBATCH --partition=test
#SBATCH --no-requeue

#Setup of execution environment
#SBATCH --export=NONE
#SBATCH --get-user-env
#SBATCH --account=pn36zo

module load slurm_setup
module load intel/18.0
module load mpi.intel/2018
module load mkl/2018
export OMP_NUM_THREADS=1
exec="/dss/dsshome1/07/di76zil/09_FHI_aims_19_August_2021/aims.210807.scalapack.mpi.x"

name='aims.out'

mpiexec -n $SLURM_NTASKS $exec >& $name
