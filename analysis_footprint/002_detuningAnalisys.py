import pylab as pl
import myfilemanager as mfm
import numpy as np
import mystyle as ms
import matplotlib.gridspec as gridspec
import os
from mpl_toolkits.axes_grid1 import make_axes_locatable
import matplotlib.ticker as mtick



pl.close('all')

#~ Q_x = .31
#~ Q_y = .32

Q_x = .27
Q_y = .295

fact_beam = 1.0e11	

#~ init_unif_edens_dip_vec = np.linspace(1e11,1e12,10)
#~ fraction_device_dip = 0.65	
fraction_device_quad_vect = np.linspace(0.07, 1.00, 11)[0:3]
betax_vect = [50, 100, 150, 200, 300, 400, 500, 600]
betay_vect = [50, 100, 150, 200, 300, 400, 500, 600]

enable_arc_dip = False
enable_arc_quad = True
onoff = {False: 'OFF', True: 'ON'}

folder_plot = 'footprint_analysis_detuning/'
if not os.path.exists(folder_plot):
	os.makedirs(folder_plot)


#~ Define the matrix of the average and standard deviation of the horizontal and vertical tune 
#~ versus length or fraction device (the rows of the matrix) and the beta (the columns of the matrix) 
DeltaQx_average = np.zeros((len(fraction_device_quad_vect),len(betax_vect)))
DeltaQy_average = np.zeros((len(fraction_device_quad_vect),len(betax_vect)))

DeltaQx_std = np.zeros((len(fraction_device_quad_vect),len(betax_vect)))
DeltaQy_std = np.zeros((len(fraction_device_quad_vect),len(betax_vect)))

for ii,fraction_device_quad in enumerate(fraction_device_quad_vect):
    
    for jj,betax in enumerate(betax_vect):     
		
		sim_ident = '../simulations/%.1fe11ppb_ecdip%s_ecquad%s_%.3ffracQuad_%dbetaxy'%(fact_beam/1e11,
								onoff[enable_arc_dip], onoff[enable_arc_quad], fraction_device_quad, betax)
		filename_footprint = 'footprint.h5'

		ob = mfm.object_with_arrays_and_scalar_from_h5(sim_ident + '/' + filename_footprint)


		
		DeltaQx_vec = np.abs(ob.qx_i) - Q_x
		DeltaQy_vec = np.abs(ob.qy_i) - Q_y


		
		DeltaQx_average[ii,jj] = np.mean(DeltaQx_vec)
		DeltaQy_average[ii,jj] = np.mean(DeltaQy_vec)
		
		DeltaQx_std[ii,jj] = np.std(DeltaQx_vec)
		DeltaQy_std[ii,jj] = np.std(DeltaQy_vec)



	
	
folder_plot_average = folder_plot + 'average/'
if not os.path.exists(folder_plot_average):
	os.makedirs(folder_plot_average)
#~ plot horizontal and vertical tune average versus beta, for fixed device length
for ii,fraction_device_quad in enumerate(fraction_device_quad_vect):
	fig = pl.figure(ii)
	
	#~ colorcurr = pl.cm.rainbow(np.linspace(0, 1, len(init_unif_edens_dip_vec)))
	axis_font = {'fontname':'Arial', 'size':'18'}

	pl.plot(betax_vect, DeltaQx_average[ii,:]*1e3, 'o-', color = 'blue', label='Horizontal')
	pl.plot(betax_vect, DeltaQy_average[ii,:]*1e3, 'o-', color = 'red', label='Vertical')
	#~ legend2 = pl.legend(loc='best',title='Beta [m]')
	legend = pl.legend(loc='best')
	legend.get_title().set_fontsize('14')
	pl.xlabel('Beta$_{x,y}$ [m]', **axis_font)
	pl.ylabel('<$\Delta$Q> [$\cdot$ 10$^{-3}$]', **axis_font)
	pl.ylim((0., 30.))
	pl.title('Fraction Quadrupole = %.3f'%(fraction_device_quad), **axis_font)
	pl.tick_params(labelsize=16)
	pl.grid()
	pl.gcf().subplots_adjust(bottom=0.15)
	pl.savefig(folder_plot_average + 'Quadrupole_DeltaQaverageVSbeta_%.3ffracQuad.png'%(fraction_device_quad), dpi=300)


#~ plot horizontal and vertical tune average versus fixed device length, for fixed beta
ii = len(fraction_device_quad_vect)
for jj,betax in enumerate(betax_vect):
	fig = pl.figure(ii+jj)
	
	#~ colorcurr = pl.cm.rainbow(np.linspace(0, 1, len(init_unif_edens_dip_vec)))
	axis_font = {'fontname':'Arial', 'size':'18'}

	pl.plot(fraction_device_quad_vect*100, DeltaQx_average[:,jj]*1e3, 'o-', color = 'blue', label='Horizontal')
	pl.plot(fraction_device_quad_vect*100, DeltaQy_average[:,jj]*1e3, 'o-', color = 'red', label='Vertical')
	#~ legend2 = pl.legend(loc='best',title='Beta [m]')
	legend = pl.legend(loc='best')
	legend.get_title().set_fontsize('14')
	pl.xlabel('Fraction Device Length [%]', **axis_font)
	#~ pl.ylabel('<Q> [$\cdot$ 10$^{-4}$]', **axis_font)
	pl.ylabel('<$\Delta$Q> [$\cdot$ 10$^{-3}$]', **axis_font)
	pl.ylim((0., 30.))
	pl.title('Quadrupole     Beta$_{x,y} = %.0f$'%(betax), **axis_font)
	pl.tick_params(labelsize=16)
	pl.grid()
	pl.gcf().subplots_adjust(bottom=0.15)
	pl.savefig(folder_plot_average + 'Quadrupole_DeltaQaveragevsLength_%.0fBeta.png'%(betax), dpi=300)





folder_plot_std = folder_plot + 'std/'
if not os.path.exists(folder_plot_std):
	os.makedirs(folder_plot_std)
#~ plot horizontal and vertical tune standard deviation versus beta, for fixed device length
jj = len(fraction_device_quad_vect) + len(betax_vect)
for ii,fraction_device_quad in enumerate(fraction_device_quad_vect):
	fig = pl.figure(jj+ii)

	axis_font = {'fontname':'Arial', 'size':'18'}
	pl.plot(betax_vect,DeltaQx_std[ii,:]*1e3, 'o-', color = 'blue', label='Horizontal')
	pl.plot(betax_vect,DeltaQy_std[ii,:]*1e3, 'o-', color = 'red', label='Vertical')
	legend = pl.legend(loc='best')
	legend.get_title().set_fontsize('14')
	pl.xlabel('Beta$_{x,y}$ [m]', **axis_font)
	pl.ylabel('$\sqrt{<(\Delta Q - <\Delta Q>)^2>}$ [$\cdot$ $10^{-3}$]', **axis_font)
	pl.ylim((0., 8.))
	pl.title('Fraction Quadrupole = %.3f'%(fraction_device_quad), **axis_font)
	pl.tick_params(labelsize=16)
	pl.grid()
	pl.gcf().subplots_adjust(bottom=0.15)
	pl.savefig(folder_plot_std + 'Quadrupole_DeltaQstdVSBeta_%.3ffracQuad.png'%(fraction_device_quad), dpi=300)


#~ plot horizontal and vertical tune standard deviation versus device length, for fixed beta
ii = 2*len(fraction_device_quad_vect) + len(betax_vect)
for jj,betax in enumerate(betax_vect):
	fig = pl.figure(ii+jj)

	axis_font = {'fontname':'Arial', 'size':'18'}
	pl.plot(fraction_device_quad_vect*100,DeltaQx_std[:,jj]*1e3, 'o-', color = 'blue', label='Horizontal')
	pl.plot(fraction_device_quad_vect*100,DeltaQy_std[:,jj]*1e3, 'o-', color = 'red', label='Vertical')
	legend = pl.legend(loc='best')
	legend.get_title().set_fontsize('14')
	pl.xlabel('Fraction Device Length [%]', **axis_font)
	pl.ylabel('$\sqrt{<(\Delta Q - <\Delta Q>)^2>}$ [$\cdot$ $10^{-3}$]', **axis_font)
	pl.ylim((0., 8.))
	pl.title('Quadrupole     Beta$_{x,y} = %.0f$'%(betax), **axis_font)
	pl.tick_params(labelsize=16)
	pl.grid()
	pl.gcf().subplots_adjust(bottom=0.15)
	pl.savefig(folder_plot_std + 'Quadrupole_DeltaQstdVSLength_%.0fBeta.png'%(betax), dpi=300)



#~ pl.show()














