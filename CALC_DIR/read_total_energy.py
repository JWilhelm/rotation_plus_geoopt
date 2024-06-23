import os
import time
import numpy as np

###############################
#  THIS NEEDS TO BE MODIFIED  #
###############################

delta_angle          = 5                                                # rotation angle in degree

################################

n_angles = 360//delta_angle

print ("Start single-point DFT calculations for " + str(n_angles) + " configurations")

for angle_index in range(n_angles):

    angle = angle_index * delta_angle

    if angle_index < 10:
        index_string = "00"+str(angle_index)
    elif angle_index < 100:
        index_string = "0"+str(angle_index)
    else:
        index_string = str(angle_index)

    dir_name = index_string + "_angle_" + str(angle)

    os.chdir( dir_name )

    print(angle)

    os.system("grep -e 'Total energy     '  aims.out | tail -n 1  ")

    os.chdir("..")
