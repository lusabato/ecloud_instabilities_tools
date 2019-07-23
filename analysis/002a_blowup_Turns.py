import numpy as np
import scipy.io as sio
import pylab as pl
import glob

import os,sys
BIN = os.path.expanduser("../tools/")
sys.path.append(BIN)
import propsort as ps
import myfilemanager as mfm
import mystyle as ms


pl.close('all')


# Scan Parameters
betax_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
betay_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
fraction_device_quad_vect = [0.07, 0.16, 0.26]
n_slices_vect = np.array([250., 500., 750., 1000.])
n_macroparticles_vect = density_macroparticles_per_slice*n_slices_vect

# Simulations Parameters
n_segments = 16
PyPICmode_tag = 'Tblocked'
eMPs = 500000
macroparticles_per_slice = 5000.


tt_first = np.zeros((len(n_slices_vect),len(betax_vect),len(fraction_device_quad_vect)))
tt_last = np.zeros((len(n_slices_vect),len(betax_vect),len(fraction_device_quad_vect)))
enx = 2.5e-6
threshold_first = 2.8e-6
enx_max_ratio = 0.24
threshold_last = enx * (1 + enx_max_ratio)
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):

	for jj, betax, betay in zip(range(len(betax_vect)), betax_vect, betay_vect):

		for ii, n_slices in enumerate(n_slices_vect):

			# create the arrays of horizontal and vertical emittances		
			epsn_x_from_bunch_monitor = []
			epsn_y_from_bunch_monitor = []
			
			folder_curr_sim = '../simulations_PyPARIS/transverse_grid_%s_betaxy_%.0fm_length%.2f_slices_%d'%(PyPICmode_tag, betax,fraction_device_quad,n_slices)			
			sim_curr_list = ps.sort_properly(glob.glob(folder_curr_sim+'/bunch_evolution_*.h5'))

			print sim_curr_list[0]


			try:
				ob = mfm.monitorh5list_to_obj(sim_curr_list)				
				epsn_x_from_bunch_monitor.append(ob.epsn_x)
				epsn_y_from_bunch_monitor.append(ob.epsn_y)
				epsn_x_from_bunch_monitor = np.squeeze(np.array(epsn_x_from_bunch_monitor))
				epsn_y_from_bunch_monitor = np.squeeze(np.array(epsn_y_from_bunch_monitor))

				tt = np.arange(0,ob.mean_x.shape[0],1)


		# evaluate the first point where the emittance (horizontal or vertical) is above the first threshold
				mask_above_x_first = epsn_x_from_bunch_monitor > threshold_first
				if any(mask_above_x_first==True):
					ix_first = np.min(np.where(mask_above_x_first)[0])
					
				mask_above_y_first = epsn_y_from_bunch_monitor > threshold_first
				if any(mask_above_y_first==True):
					iy_first = np.min(np.where(mask_above_y_first)[0])
				
				
				if not any(mask_above_x_first==True) and not any(mask_above_y_first==True):
					tt_first[ii,jj,kk] = np.nan
					
				elif any(mask_above_x_first==True) and not any(mask_above_y_first==True):
					tt_first[ii,jj,kk] = tt[ix_first]
				
				elif not any(mask_above_x_first==True) and any(mask_above_y_first==True):
					tt_first[ii,jj,kk] = tt[iy_first]
					
				elif any(mask_above_x_first==True) and any(mask_above_y_first==True):		
					i_first = np.min([ix_first,iy_first])		
					tt_first[ii,jj,kk] = tt[i_first]
			
			
		# evaluate the first point where the emittance (horizontal or vertical) is above the last threshold
				mask_above_x_last = epsn_x_from_bunch_monitor > threshold_last
				if any(mask_above_x_last==True):
					ix_last = np.min(np.where(mask_above_x_last)[0])
					
				mask_above_y_last = epsn_y_from_bunch_monitor > threshold_last
				if any(mask_above_y_last==True):
					iy_last = np.min(np.where(mask_above_y_last)[0])
				
				
				if not any(mask_above_x_last==True) and not any(mask_above_y_last==True):
					tt_last[ii,jj,kk] = np.nan
					
				elif any(mask_above_x_last==True) and not any(mask_above_y_last==True):
					tt_last[ii,jj,kk] = tt[ix_last]
				
				elif not any(mask_above_x_last==True) and any(mask_above_y_last==True):
					tt_last[ii,jj,kk] = tt[iy_last]
					
				elif any(mask_above_x_last==True) and any(mask_above_y_last==True):		
					i_last = np.min([ix_last,iy_last])		
					tt_last[ii,jj,kk] = tt[i_last]
			
			
			except IOError as goterror:
				print 'Skipped. Got:',  goterror
				tt_first[ii,jj,kk] = np.nan
				tt_last[ii,jj,kk] = np.nan


			
sio.savemat('tt_complete.mat',{'tt_first':tt_first, 'tt_last':tt_last, 'n_slices_vect':n_slices_vect, 'enx':enx, 'enx_max_ratio':enx_max_ratio,
							'macroparticles_per_slice':macroparticles_per_slice, 'n_segments':n_segments, 
							'eMPs':eMPs, 'PyPICmode_tag':PyPICmode_tag,
							'betax_vect':betax_vect, 'fraction_device_quad_vect':fraction_device_quad_vect})
	
	




