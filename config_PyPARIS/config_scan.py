import os,sys
BIN = os.path.expanduser("../tools/")
sys.path.append(BIN)
import replaceline as rl


# PyFriend folder
rel_pyfriends = '../../'
abs_pyfriends =  os.path.abspath(rel_pyfriends)


tag_prefix = 'QMPsl_'

# Scan parameters
betax_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
betay_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
fraction_device_quad_vect = [0.07, 0.16, 0.26]
macroparticles_per_slice_vect = [2500, 5000, 10000]

n_cores = 16
ask_for_n_times = 1

parallel_mode = 'multiproc'
cluster = 'cnaf_acc'

if cluster == 'lxplus':
    cluster_specific = {}
    cluster_specific['queue'] = 'spacecharge'
    cluster_specific['setup_env_source'] = 'setup_env_lxplus; export LD_LIBRARY_PATH=/afs/cern.ch/sw/lcg/contrib/gcc/4.8.1/x86_64-slc6-gcc48-opt/lib64; source /afs/cern.ch/work/l/lusabato/sim_workspace_PyPARIS/virtualenvs/py2.7/bin/activate'
    #~ cluster_specific['setup_env_source'] = 'setup_env_lxplus'
    cluster_specific['mpiex'] = 'to_be_installed'
elif cluster == 'cnaf':
    cluster_specific = {}
    cluster_specific['queue'] = 'hpc_56inf'
    cluster_specific['setup_env_source'] = 'setup_env_cnaf'
    cluster_specific['mpiex'] = 'mpiexec'
elif cluster == 'cnaf_acc':
    cluster_specific = {}
    cluster_specific['queue'] = 'hpc_acc'
    cluster_specific['setup_env_source'] = 'setup_env_cnaf'
    cluster_specific['mpiex'] = 'mpiexec'

exec_string = {}
exec_string['multiproc'] = 'python ../../../PyPARIS/multiprocexec.py -n %d'
exec_string['mpi'] = cluster_specific['mpiex'] + ' -n %d ../../../PyPARIS/withmpi.py'
#~ exec_string['multiproc'] = 'python /afs/cern.ch/work/l/lusabato/sim_workspace_PyPARIS/PyPARIS/multiprocexec.py -n %d'
#~ exec_string['mpi'] = cluster_specific['mpiex'] + ' -n %d /afs/cern.ch/work/l/lusabato/sim_workspace_PyPARIS/PyPARIS/withmpi.py'

current_dir = os.getcwd()
study_folder =  current_dir.split('/config')[0]
scan_folder = study_folder+'/simulations_PyPARIS'
os.mkdir(scan_folder)

launch_file_lines = []
launch_file_lines +=['#!/bin/bash\n']

prog_num = 0
for fraction_device_quad in fraction_device_quad_vect:

	for macroparticles_per_slice in macroparticles_per_slice_vect:
		
		for betax, betay in zip(betax_vect, betay_vect):
							
				prog_num +=1
				current_sim_ident= 'ArcQuad_T0_x_slices_750_segments_16_length_%02d_MPslice_%05d_betaxy_%03dm'%(fraction_device_quad*100,macroparticles_per_slice,betax)                       
				sim_tag = tag_prefix+'%04d'%prog_num

				print sim_tag, current_sim_ident
				current_sim_folder = scan_folder+'/'+current_sim_ident
				os.mkdir(current_sim_folder)
				os.system('cp -r sim_prototype/* %s'%current_sim_folder)								
				
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'fraction_device_quad = ', 
									newline = 'fraction_device_quad = %.2f'%fraction_device_quad)				
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'macroparticles_per_slice = ', 
									newline = 'macroparticles_per_slice = %d'%macroparticles_per_slice)	
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'beta_x = ', 
									newline = 'beta_x = %d'%betax)									
				rl.replaceline_and_save(fname = current_sim_folder+'/Simulation_parameters.py',
									findln = 'beta_y = ', 
									newline = 'beta_y = %d'%betay)	
													
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = 'export STUDYPATH=',
					 newline = 'export STUDYPATH=%s\n'%study_folder)					
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = 'export PYFRIENDSPATH=',
					 newline = 'export PYFRIENDSPATH=%s\n'%abs_pyfriends)					
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = '#BSUB -J',
					 newline = '#BSUB -J %s\n'%sim_tag)						 
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = '#BSUB -n',
					 newline = '#BSUB -n %d\n'%(n_cores*ask_for_n_times))	
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
						 findln = '#BSUB -R',
						 newline = '#BSUB -R span[ptile=%d]\n'%(n_cores*ask_for_n_times))						 
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = '#BSUB -q',
					 newline = '#BSUB -q %s\n'%cluster_specific['queue'])	   						 
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
					 findln = 'CURRDIR=',
					 newline = 'CURRDIR=%s\n'%current_sim_folder)				  			  
				rl.replaceline_and_save(fname = current_sim_folder+'/job.cmd',
						 findln = 'stdbuf -oL ',
						 newline = 'stdbuf -oL '+ exec_string[parallel_mode]%n_cores+\
						 ' sim_class=PyPARIS_sim_class.Simulation.Simulation >> opic.txt 2>> epic.txt\n')
				
				launch_file_lines += ['cd ' + current_sim_folder+'\n',
							'bsub < job.cmd\n',
							'cd ..\n']

				with open(current_sim_folder+'/launch_this', 'w') as fid:
					fid.writelines(['#!/bin/bash\n','bsub < job.cmd\n'])

				with open(current_sim_folder+'/opic.txt', 'w') as fid:
					fid.writelines([''])

				with open(current_sim_folder+'/epic.txt', 'w') as fid:
					fid.writelines([''])

with open(study_folder+'/run_PyPARIS', 'w') as fid:
	fid.writelines(launch_file_lines)
os.chmod(study_folder+'/run_PyPARIS',0755)

import htcondor_config as htcc
htcc.htcondor_config(scan_folder, time_requirement_days=2., runfilename='../run_PyPARIS_htcondor', 
                    n_cores=n_cores, job_filename = 'job.cmd', htcondor_subfile='htcondor_PyPARIS.sub',
                    listfolderfile = 'list_sim_folders_PyPARIS.txt')




