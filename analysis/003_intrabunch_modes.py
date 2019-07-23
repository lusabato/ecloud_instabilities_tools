import scipy.io as sio
import glob
import numpy as np
import matplotlib.pyplot as plt
import math

import os,sys
BIN = os.path.expanduser("../tools/")
sys.path.append(BIN)
import myfilemanager as mfm
import mystyle as ms 
import propsort as ps

from functools import partial
from scipy.ndimage import gaussian_filter1d

from scipy.constants import c as clight


plt.close('all')


# Scan Parameters
fraction_device_quad_vect = [0.07, 0.16, 0.26]
n_slices_vect = np.array([250., 500., 750., 1000.])
betax_vect = [50, 100, 150, 200, 300, 400, 500, 600]

# Simulations Parameters
PyPICmode_tag = 'Tblocked'


# If you want to save the figures with all the scan parameters choose: savefigures = True and mode = 'auto'
savefigure = True
mode = 'auto'
#~ # Comment this part if you want to save the plots. You can choose only some scan parameters
#~ savefigure = False 
#~ fraction_device_quad_vect = [0.26]
#~ n_slices_vect = np.array([1000.,])
#~ betax_vect = [100]
#~ mode = 'manual'
#~ turn_obs = 350

betay_vect = betax_vect
folder_plot = 'intrabunch_modes/'
if not os.path.exists(folder_plot) and savefigure:
	os.makedirs(folder_plot)


# choice of the window of turns
# import the dictionary elements
dic = sio.loadmat('tt_complete.mat')
tt = np.squeeze(dic['tt_first'])

smooth = partial(gaussian_filter1d, sigma=2, mode='nearest')

n_turns_window = 20
n_sigmaz_sim = 10. #we are simulating 10 long sigmas
i_want_to_count_over = 4.
flag_weighted =  True


#Figure parameters
ii_fig = 0
tick_size = 20
axis_font = {'fontname':'Arial', 'size':'24'}
fig_size = (15, 5)
line_width = 3.5

ms.mystyle_arial(16)


# calculate intra-bunch modes
for fraction_device_quad in fraction_device_quad_vect:
        
        kk = np.argmin(np.abs(dic['fraction_device_quad_vect']-fraction_device_quad))
	for betax, betay in zip(betax_vect, betay_vect):
                jj = np.argmin(np.abs(dic['betax_vect']-betax))	
		subfolder_plot = folder_plot + 'betaxy_%d_length_%.2f/'%(betax,fraction_device_quad)
		if not os.path.exists(subfolder_plot) and savefigure:
			os.makedirs(subfolder_plot)
		
		for n_slices in n_slices_vect:
                        ii = np.argmin(np.abs(dic['n_slices_vect']-n_slices)) 
			if not math.isnan(tt[ii,jj,kk]):

                                if mode == 'auto':
                                    wind_center = int(tt[ii,jj,kk])
                                elif mode == 'manual':
                                    wind_center = turn_obs
                                else:
                                    raise ValueError("I don't understand!?")

				start = [wind_center + n_turns_window/2]
						
				if int(tt[ii,jj,kk]) - n_turns_window/2 < 0:
					window_min = 1
					window = [np.s_[1:s] for s in start]
				else:
					window_min = wind_center - n_turns_window/2
					window = [np.s_[s-n_turns_window:s] for s in start]
				
				window_max = wind_center + n_turns_window/2
				
				folder_curr_sim = '../simulations_PyPARIS/transverse_grid_%s_betaxy_%.0fm_length%.2f_slices_%d'%(PyPICmode_tag, betax,fraction_device_quad,n_slices)                       
														
				sim_curr_list = ps.sort_properly(glob.glob(folder_curr_sim+'/slice_evolution_*.h5'))

				
				print sim_curr_list[0]

				try:
					data = mfm.monitorh5list_to_obj(sim_curr_list, key='Slices', flag_transpose=True)

					if flag_weighted:
						bpm_x = data.mean_x * data.n_macroparticles_per_slice
						bpm_y = data.mean_y * data.n_macroparticles_per_slice
					else:
						bpm_x = data.mean_x 
						bpm_y = data.mean_y 

					xfft = np.fft.rfft(bpm_x, axis=0)
					yfft = np.fft.rfft(bpm_y, axis=0)
					xfft = np.abs(xfft)**2 #Power
					yfft = np.abs(yfft)**2 #Power


					for wd in window:
						print wd

						n_slices, n_turns = data.mean_z.shape
						zz = np.linspace(-2.5e-9*clight/2, 2.5e-9*clight/2, n_slices)
						xx, yy = bpm_x, bpm_y    

						# Setting to plot the fft
						xftt_to_plot = np.log10(xfft.T)
						yftt_to_plot = np.log10(yfft.T)
						minval_x = np.max([xftt_to_plot])-3
						minval_y = np.max([yftt_to_plot])-3
						xftt_to_plot[xftt_to_plot<minval_x] = minval_x
						yftt_to_plot[yftt_to_plot<minval_y] = minval_y
					
						YY_to_plot, XX_to_plot = xftt_to_plot.shape
						XX_to_plot = np.arange(XX_to_plot)
						YY_to_plot = np.arange(YY_to_plot)

						fig, ((ax1, ax2)) = plt.subplots(1, 2, figsize=fig_size)
						fig.patch.set_facecolor('w')
						fig.subplots_adjust(left=0.05, right=0.95, wspace=0.3)
					
						xmin, xmax = wd.start, wd.stop
						col = plt.cm.rainbow_r(np.linspace(0, 1, xmax-xmin))
						for i, t in enumerate(range(n_turns)[wd]):
							ax1.plot(zz, smooth(bpm_x[:, t]), c=col[i], linewidth=line_width)
							ax2.plot(zz, smooth(bpm_y[:, t]), c=col[i], linewidth=line_width)


					ax1.set_xlabel('z [m]')
					ax2.set_xlabel('z [m]')

					ax1.set_title('Turns %.0f - %.0f'%(window_min, window_max))
					ax2.set_title('Turns %.0f - %.0f'%(window_min, window_max))

					if flag_weighted:
						ax1.set_xlim(-2.5e-9*c/2, 2.5e-9*c/2)
						ax2.set_xlim(-2.5e-9*c/2, 2.5e-9*c/2)
						ax1.set_ylabel('Charge weighted\nhorizontal signal')
						ax2.set_ylabel('Charge weighted\nvertical signal')

					else:
						ax1.set_xlim(-0.30, 0.30)
						ax2.set_xlim(-0.30, 0.30)
						#~ ax1.set_ylim(-.0001,.0001)
						#~ ax2.set_ylim(-.0001,.0001)
						ax1.set_ylabel('Horizontal signal')
						ax2.set_ylabel('Vertical signal')

					title = fig.suptitle('Beta_xy = %.0f    Fraction Device = %.3f     Slices = %.0f\n'%(betax, fraction_device_quad, n_slices))

					if flag_weighted and savefigure:
						plt.savefig(subfolder_plot + 'charge_weighted_betaxy_%d_length_%.2f_slices_%.0f.png'%(betax, fraction_device_quad, n_slices), dpi=300, bbox_inches='tight')
				
				except IOError as goterror:
					print 'Skipped. Got:',  goterror
						
plt.show()

