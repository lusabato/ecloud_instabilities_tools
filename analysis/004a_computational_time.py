import numpy as np
import scipy.io as sio
import os


folder_work = 'computational_time/'
if not os.path.exists(folder_work):
	os.makedirs(folder_work)


# Scan Parameters
betax_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
betay_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
fraction_device_quad_vect = [0.07, 0.16, 0.26]
n_slices_vect = np.array([250., 500., 750., 1000.])

# Simulationd Parameters
n_segments = 16
PyPICmode_tag = 'Tblocked'
eMPs = 500000
macroparticles_per_slice = 5000.


computational_time_seconds = np.zeros((len(n_slices_vect),len(betax_vect),len(fraction_device_quad_vect)))
N_turns_done = np.zeros((len(n_slices_vect),len(betax_vect),len(fraction_device_quad_vect)))
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):

	for jj, betax, betay in zip(range(len(betax_vect)), betax_vect, betay_vect):

		for ii, n_slices in enumerate(n_slices_vect):
			
			folder_curr_sim = '../simulations_PyPARIS/transverse_grid_%s_betaxy_%.0fm_length%.2f_slices_%d'%(PyPICmode_tag, betax,fraction_device_quad,n_slices)                       
			file_pyparislog = folder_curr_sim + '/pyparislog.txt'
			with open(file_pyparislog, 'r') as fid:
				lines_pyparislog = fid.readlines()
			
			find_turn = False
			for ii_pyparislog, line in enumerate(lines_pyparislog):
				
				if 'Turn ' in line:							
					this_turn_time = int((line.split(',')[1]).split(' ')[1])
					N_turns_done[ii,jj,kk] = N_turns_done[ii,jj,kk] + 1
					computational_time_seconds[ii,jj,kk] = computational_time_seconds[ii,jj,kk] + this_turn_time
					find_turn = True					
			
			if not find_turn:
				N_turns_done[ii,jj,kk] = np.nan
				computational_time_seconds[ii,jj,kk] = np.nan
					
			
sio.savemat(folder_work + 'computational_time.mat',{'computational_time_seconds':computational_time_seconds,
										'N_turns_done':N_turns_done})
	
	




