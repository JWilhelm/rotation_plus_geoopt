import os
import time
import numpy as np

###############################
#  THIS NEEDS TO BE MODIFIED  #
###############################

delta_angle          = 5                                                # rotation angle in degree
directory_for_calcs  = "CALC_DIR"
geometry_file_bottom = "00_create_geometry/geometry_only_bottom.in"
geometry_file_top    = "00_create_geometry/geometry_only_top.xyz"
geometry_file_top_2  = "00_create_geometry/geometry_only_2_rotation_molecules.in"

################################

def rotate_and_write_geometry(angle, geometry_file_top, geometry_file_top_2, geometry_file_bottom):

    geofile_final      = "geometry.in"

    top_geometry       = open(geometry_file_top, 'r')
    top_geometry_lines = top_geometry.readlines()
    
    for index, line in enumerate(top_geometry_lines):
    
        line_array = line.split()
    
        if index == 0:
            vec_atom_0 = np.array([ float(line_array[1]), float(line_array[2]), float(line_array[3]) ])

        if index == 1:
            vec_atom_1 = np.array([ float(line_array[1]), float(line_array[2]), float(line_array[3]) ])

    vec_rot = (vec_atom_1 - vec_atom_0) / np.linalg.norm(vec_atom_1 - vec_atom_0)

    os.system( "cat " + geometry_file_bottom + " >> " + geofile_final )
    os.system( "cat " + geometry_file_top_2  + " >> " + geofile_final )

    for index, line in enumerate(top_geometry_lines):

        if index > 1:

            line_array = line.split()

            vec_atom_index = np.array([ float(line_array[1]), float(line_array[2]), float(line_array[3]) ])

            vec_d_atom_0_atom_index = vec_atom_index - vec_atom_0

            vec_d_normal = vec_d_atom_0_atom_index - np.dot(vec_rot, vec_d_atom_0_atom_index) * vec_rot

            vec_d_ortho = np.cross(vec_d_normal, vec_rot)

            vec_d_rot = np.cos( angle * np.pi / 180. ) * vec_d_normal + np.sin( angle * np.pi / 180. ) * vec_d_ortho

            vec_atom_index_new = vec_atom_index - vec_d_normal + vec_d_rot

            os.system( "echo 'atom " + str(vec_atom_index_new[0]) + " " + str(vec_atom_index_new[1]) + " "+ str(vec_atom_index_new[2]) + " " + line_array[0] + " ' >> "   + geofile_final )
            os.system( "echo 'constrain_relaxation .true.' >> "   + geofile_final )


    top_geometry.close()

n_angles = 360//delta_angle

print ("Start DFT geoopt for " + str(n_angles) + " configurations")

os.mkdir(directory_for_calcs)
os.chdir(directory_for_calcs)

for angle_index in range(n_angles):

    angle = angle_index * delta_angle

    if angle_index < 10:
        index_string = "00"+str(angle_index)
    elif angle_index < 100:
        index_string = "0"+str(angle_index)
    else:
        index_string = str(angle_index)

    dir_name = index_string + "_angle_" + str(angle)

    os.mkdir( dir_name )

    os.chdir( dir_name )

    rotate_and_write_geometry(angle, "../../"+geometry_file_top, "../../"+geometry_file_top_2, "../../"+geometry_file_bottom)

    os.system("cp ../../run_supermuc.sh .")

    os.system("cp ../../control.in .")

    os.system("sbatch run_supermuc.sh")

#    while not os.path.exists("aims.out"):
#        time.sleep(1)

    os.chdir("..")
