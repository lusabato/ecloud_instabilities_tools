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
turns_goal = 20000

folder_plot = 'plots_summary/'
if not os.path.exists(folder_plot):
	os.makedirs(folder_plot)

# import the dictionary elements
dic = sio.loadmat('tt_complete.mat')

n_slices_vect = np.squeeze(dic['n_slices_vect'])
n_segments = np.squeeze(dic['n_segments'])
macroparticles_per_slice = np.squeeze(dic['macroparticles_per_slice'])
eMPs = np.squeeze(dic['eMPs'])
PyPICmode_tag = np.squeeze(dic['PyPICmode_tag'])

betax_vect = np.squeeze(dic['betax_vect'])
betay_vect = np.squeeze(dic['betax_vect'])
fraction_device_quad_vect = np.squeeze(dic['fraction_device_quad_vect'])

tt_first = np.squeeze(dic['tt_first'])
tt_last = np.squeeze(dic['tt_last'])
tt_difference = tt_last - tt_first


# figure Parameters	
fig_index = 0
fig_size = (12,8)
# colorcurr1 = pl.cm.rainbow(np.linspace(0, 1, len(fraction_device_quad_vect)-1))
colorcurr6 =  ['darkorange','coral','orangered','red','firebrick','darkred','lightblue','lightskyblue','cyan','blue','mediumblue','darkblue','lightgray','silver','darkgray','slategray','dimgray','black']
colorcurr5 =  ['coral','orangered','red','firebrick','darkred','lightblue','lightskyblue','blue','mediumblue','darkblue','lightgray','silver','darkgray','dimgray','black']
colorcurr4 =  ['coral','orangered','red','darkred','lightblue','lightskyblue','blue','darkblue','lightgray','darkgray','dimgray','black']
colorcurr3 =  ['orangered','red','darkred','lightskyblue','blue','darkblue','darkgray','dimgray','black']
colorcurr1 =  ['red','blue','black']

axis_font = {'fontname':'Arial', 'size':'24'}
axis_font_title = {'fontname':'Arial', 'size':'20'}
labelsize_choice = 24
labelsize_legend = 24
line_width = 3.5
line_width_stop = 2*line_width





# plot blow-up time versus beta (varying fraction of device and number of slices)
fig_index = fig_index + 1
fig = pl.figure(fig_index,figsize=fig_size)
index_color = 0
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
    for ii, n_slices in enumerate(n_slices_vect):	
		pl.semilogy(betax_vect,tt_first[ii,:,kk], 'o-', linewidth=line_width, color = colorcurr3[index_color], label='%.2f, slices = %d'%(fraction_device_quad,n_slices))
		index_color = index_color + 1
            
legend1 = pl.legend(loc='best')
legend1.get_title().set_fontsize('14')
pl.ylim(0, turns_goal*1.1)
pl.plot(betax_vect, turns_goal*np.ones(len(betax_vect)), '--', linewidth=line_width_stop, color = 'darkgreen')
pl.xlabel('Beta [m]', **axis_font)
pl.ylabel('Blow-up Time [Turns]', **axis_font)
pl.title('Quad  %s  Segments = %d   MPs/Slice = %de3  e$^-$ MPs = %de5'%(PyPICmode_tag,n_segments,macroparticles_per_slice/1e3,eMPs/1e5), **axis_font_title)
pl.tick_params(labelsize=labelsize_choice)
pl.grid(linestyle='dashed')
pl.savefig(folder_plot + 'blowupTimevsBeta_nSlices.png', dpi=300)


index_color = 0
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
	fig_index = fig_index + 1
	fig = pl.figure(fig_index,figsize=fig_size)
	for ii, n_slices in enumerate(n_slices_vect):	
		pl.semilogy(betax_vect,tt_first[ii,:,kk], 'o-', linewidth=line_width, color = colorcurr4[index_color], label='%d'%n_slices)
		index_color = index_color + 1
	
	legend1 = pl.legend(loc='best',title='Slices',prop={'size': labelsize_legend})
	legend1.get_title().set_fontsize('%d'%labelsize_legend)
	pl.ylim(0, turns_goal*1.1)
	pl.plot(betax_vect, turns_goal*np.ones(len(betax_vect)), '--', linewidth=line_width_stop, color = 'darkgreen')
	pl.xlabel('Beta [m]', **axis_font)
	pl.ylabel('Blow-up Time [Turns]', **axis_font)
	pl.title('ArcQuad  %s  Segments = %d  MPs/Slice = %de3  e$^-$ MPs = %de5  Length = %.2f'%(PyPICmode_tag,n_segments,macroparticles_per_slice/1e3,eMPs/1e5,fraction_device_quad), **axis_font_title)
	pl.tick_params(labelsize=labelsize_choice)
	pl.grid(linestyle='dashed')
	pl.savefig(folder_plot + 'blowupTimevsBeta_nSlices_length%.2f.png'%fraction_device_quad, dpi=300)        





#~ # plot growth rate versus beta (varying fraction of device and number of slices)	
#~ fig_index = fig_index + 1
#~ fig = pl.figure(fig_index,figsize=fig_size)
#~ index_color = 0
#~ for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
	#~ for ii, n_slices in enumerate(n_slices_vect[1:4]):	
		#~ pl.semilogy(betax_vect,1/(tt_first[ii+1,:,kk]), 'o-', linewidth=line_width, color = colorcurr3[index_color], label='%.2f, slices = %d'%(fraction_device_quad,n_slices))
		#~ index_color = index_color + 1
            
#~ pl.xlabel('Beta [m]', **axis_font)
#~ pl.ylabel('Growth rate', **axis_font)
#~ pl.title('ArcQuad    Segments = %d   Density Slice = %d'%(n_segments,density_macroparticles_per_slice), **axis_font_title)
#~ pl.tick_params(labelsize=labelsize_choice)
#~ pl.grid()
#~ pl.savefig(folder_plot + 'GrowthRatevsBeta_nSlices.png', dpi=300)


#~ index_color = 0
#~ for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
	#~ fig_index = fig_index + 1
	#~ fig = pl.figure(fig_index,figsize=fig_size)
	#~ for ii, n_slices in enumerate(n_slices_vect):	
		#~ pl.semilogy(betax_vect,1/(tt_first[ii,:,kk]), 'o-', linewidth=line_width, color = colorcurr4[index_color], label='slices = %d'%n_slices)
		#~ index_color = index_color + 1
            
	#~ pl.xlabel('Beta [m]', **axis_font)
	#~ pl.ylabel('Growth rate', **axis_font)
	#~ pl.title('ArcQuad    Segments = %d   Density Slice = %d   Length = %.2f'%(n_segments,density_macroparticles_per_slice,fraction_device_quad), **axis_font_title)
	#~ pl.tick_params(labelsize=labelsize_choice)
	#~ pl.grid()
	#~ pl.savefig(folder_plot + 'GrowthRatevsBeta_nSlices_length%.2f.png'%fraction_device_quad, dpi=300)





# plot blow-up time from 12% to 24% in turns versus beta (varying fraction of device and number of slices)
fig_index = fig_index + 1
fig = pl.figure(fig_index,figsize=fig_size)
index_color = 0
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
    for ii, n_slices in enumerate(n_slices_vect):	
		pl.semilogy(betax_vect,tt_difference[ii,:,kk], 'o-', linewidth=line_width, color = colorcurr3[index_color], label='%.2f, slices = %d'%(fraction_device_quad,n_slices))
		index_color = index_color + 1
            
legend1 = pl.legend(loc='best')
legend1.get_title().set_fontsize('14')
pl.xlabel('Beta [m]', **axis_font)
pl.ylabel('Blow-up Time 12 - 24% [Turns]', **axis_font)
pl.title('Quad  %s  Segments = %d   MPs/Slice = %de3  e$^-$ MPs = %de5'%(PyPICmode_tag,n_segments,macroparticles_per_slice/1e3,eMPs/1e5), **axis_font_title)
pl.tick_params(labelsize=labelsize_choice)
pl.grid(linestyle='dashed')
pl.savefig(folder_plot + 'blowup_time12to24vsBeta_nSlices.png', dpi=300)


index_color = 0
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
	fig_index = fig_index + 1
	fig = pl.figure(fig_index,figsize=fig_size)
	for ii, n_slices in enumerate(n_slices_vect):	
		pl.semilogy(betax_vect,tt_difference[ii,:,kk], 'o-', linewidth=line_width, color = colorcurr4[index_color], label='%d'%n_slices)
		index_color = index_color + 1
	
	legend1 = pl.legend(loc='best',title='Slices',prop={'size': labelsize_legend})
	legend1.get_title().set_fontsize('%d'%labelsize_legend)
	pl.xlabel('Beta [m]', **axis_font)
	pl.ylabel('Blow-up Time 12 - 24% [Turns]', **axis_font)
	pl.title('Quad  %s  Segments = %d  MPs/Slice = %de3  e$^-$ MPs = %de5  Length = %.2f'%(PyPICmode_tag,n_segments,macroparticles_per_slice/1e3,eMPs/1e5,fraction_device_quad), **axis_font_title)
	pl.tick_params(labelsize=labelsize_choice)
	pl.grid(linestyle='dashed')
	pl.savefig(folder_plot + 'blowup_time12to24vsBeta_nSlices_length%.2f.png'%fraction_device_quad, dpi=300)  





#~ # try the plot blow-up time versus beta*length for slices = 750
#~ fig_index = fig_index + 1
#~ fig = pl.figure(fig_index,figsize=fig_size)
#~ index_color = 0
#~ for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):	
	#~ pl.semilogy(betax_vect*fraction_device_quad,tt_first[3,:,kk], 'o-', linewidth=line_width, color = colorcurr1[index_color], label='%.2f'%(fraction_device_quad))
	#~ index_color = index_color + 1
            
#~ legend1 = pl.legend(loc='best',title='Length',prop={'size': labelsize_legend})
#~ legend1.get_title().set_fontsize('%d'%labelsize_legend)
#~ pl.xlabel('Beta x Length [m]', **axis_font)
#~ pl.ylabel('Blow-up Time [Turns]', **axis_font)
#~ pl.title('ArcQuad    Slices = 750   Segments = %d   Density Slice = %d'%(n_segments,density_macroparticles_per_slice), **axis_font_title)
#~ pl.tick_params(labelsize=labelsize_choice)
#~ pl.grid(linestyle='dashed')
#~ pl.savefig(folder_plot + 'blowupTimevsBetaTimesLength_nSlices.png', dpi=300)








pl.show()




