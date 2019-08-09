import numpy as np
import pylab as pl
import matplotlib.gridspec as gridspec
import glob

import os,sys
BIN = os.path.expanduser("../tools/")
sys.path.append(BIN)
import myfilemanager as mfm
import propsort as ps
import mystyle as ms

from scipy.constants import c as clight



pl.close('all')


# Scan Parameters
fraction_device_quad_vect = [0.07, 0.16, 0.26]
n_slices_vect = np.array([250., 500., 750., 1000.])
betax_vect = [50., 100., 150., 200., 300., 400., 500., 600.]


# Simulation Parameters
PyPICmode_tag = 'Tblocked'
macroparticles_per_slice = 5000.
n_segments = 16


# If you want to save the figures with all the scan parameters choose: savefigures = True
savefigures = True
#~ # Comment this part if you want to save the plots. You can choose only some scan parameters
#~ savefigures = False
#~ fraction_device_quad_vect = [0.26]
#~ n_slices_vect = np.array([1000])
#~ betax_vect = [150.]

betay_vect = betax_vect 
folder_plot = 'plots_extended/'
if not os.path.exists(folder_plot) and savefigures:
    os.makedirs(folder_plot)
    

# If you want to save the plots with the centroid choose: charge_weight_centroid_plots_flag = True
# with this option the script is slow
charge_weight_centroid_plots_flag = True

figNumber = 0
for betax, betay in zip(betax_vect, betay_vect):
    
    for fraction_device_quad in fraction_device_quad_vect:
        figNumber = figNumber + 1
        
        # Figure settings
        fig = pl.figure(figNumber, figsize=(14,16))
        fig.patch.set_facecolor('w')
        gs1 = gridspec.GridSpec(4, 2)

        sp1 = fig.add_subplot(gs1[0])
        sp2 = fig.add_subplot(gs1[1], sharex=sp1, sharey=sp1 )
        sp3 = fig.add_subplot(gs1[2], sharex=sp1)
        sp4 = fig.add_subplot(gs1[3], sharex=sp1, sharey=sp3)
        sp5 = fig.add_subplot(gs1[4], sharex=sp1) 
        sp6 = fig.add_subplot(gs1[5], sharex=sp1, sharey=sp5)
        sp7 = fig.add_subplot(gs1[6], sharex=sp1)
        sp8 = fig.add_subplot(gs1[7], sharex=sp1)

        colorcurr = pl.cm.rainbow(np.linspace(0, 1, len(n_slices_vect)))

        jj=0    
        for n_slices in n_slices_vect:          
            epsn_x_from_bunch_monitor = []
            epsn_y_from_bunch_monitor = []          
            sigma_z_from_bunch_monitor = []
            mean_x_from_bunch_monitor = []
            mean_y_from_bunch_monitor = []          
            N_mp_from_bunch_monitor = []
            
            folder_curr_sim = '../simulations_PyPARIS/transverse_grid_%s_betaxy_%.0fm_length%.2f_slices_%d'%(PyPICmode_tag, betax,fraction_device_quad,n_slices)                        
            sim_curr_list = ps.sort_properly(glob.glob(folder_curr_sim+'/bunch_evolution_*.h5'))

            if charge_weight_centroid_plots_flag:
                mean_x_from_slice_monitor = []
                mean_y_from_slice_monitor = []
                N_mp_from_slice_monitor = []
                sim_curr_list_slice_ev = ps.sort_properly(glob.glob(folder_curr_sim+'/slice_evolution_*.h5'))
                        
            print sim_curr_list[0]
            
            try:                
                ob = mfm.monitorh5list_to_obj(sim_curr_list)
                epsn_x_from_bunch_monitor.append(ob.epsn_x)
                epsn_y_from_bunch_monitor.append(ob.epsn_y)
                mean_x_from_bunch_monitor.append(ob.mean_x)
                mean_y_from_bunch_monitor.append(ob.mean_y)
                sigma_z_from_bunch_monitor.append(ob.sigma_z)               
                N_mp_from_bunch_monitor.append(ob.macroparticlenumber)
                                
                # Compute the rms of the bunch centroid position weighted on the particle number per slice
                if charge_weight_centroid_plots_flag:                   
                    ob_slice = mfm.monitorh5list_to_obj(sim_curr_list_slice_ev, key='Slices', flag_transpose=True)
                    w_slices = ob_slice.n_macroparticles_per_slice
                    rms_x = np.sqrt(np.mean((ob_slice.mean_x * w_slices)**2, axis=0))
                    rms_y = np.sqrt(np.mean((ob_slice.mean_y * w_slices)**2, axis=0))               
                    mean_x_from_slice_monitor.append(rms_x)
                    mean_y_from_slice_monitor.append(rms_y)
                    N_mp_from_slice_monitor.append(np.sum(ob_slice.n_macroparticles_per_slice, axis=0))


            except IOError as goterror:
                print 'Skipped. Got:',  goterror
                
                epsn_x_from_bunch_monitor.append(-1) 
                epsn_y_from_bunch_monitor.append(-1)                
                mean_x_from_bunch_monitor.append(-1)
                mean_y_from_bunch_monitor.append(-1)                
                sigma_z_from_bunch_monitor.append(-1)               
                N_mp_from_bunch_monitor.append(-1)

                if charge_weight_centroid_plots_flag:   
                    mean_x_from_slice_monitor.append(-1)
                    mean_y_from_slice_monitor.append(-1)
                    N_mp_from_slice_monitor.append(-1)
                    
            epsn_x_from_bunch_monitor = np.squeeze(np.array(epsn_x_from_bunch_monitor))
            epsn_y_from_bunch_monitor = np.squeeze(np.array(epsn_y_from_bunch_monitor))
            mean_x_from_bunch_monitor = np.squeeze(np.array(mean_x_from_bunch_monitor))
            mean_y_from_bunch_monitor = np.squeeze(np.array(mean_y_from_bunch_monitor))
            sigma_z_from_bunch_monitor = np.squeeze(np.array(sigma_z_from_bunch_monitor))       
            N_mp_from_bunch_monitor = np.squeeze(np.array(N_mp_from_bunch_monitor))         
            mask_from_bunch = N_mp_from_bunch_monitor>0.
            
            if charge_weight_centroid_plots_flag:   
                mean_x_from_slice_monitor = np.squeeze(np.array(mean_x_from_slice_monitor))
                mean_y_from_slice_monitor = np.squeeze(np.array(mean_y_from_slice_monitor))         
                N_mp_from_slice_monitor = np.squeeze(np.array(N_mp_from_slice_monitor))         
                mask_from_slice = N_mp_from_slice_monitor>0.            
            
            
            # check the successful sims 
            if epsn_x_from_bunch_monitor.size == 1:

                print 'ERROR, SIMULATION FAILED. length_%.2f_betaxy_%.0fm_nslices_%.0f_denSlice_%d'%(fraction_device_quad,betax,n_slices,density_macroparticles_per_slice)
            
            else:

                # Moving average filter applied to the rms signal
                if charge_weight_centroid_plots_flag:
                    from scipy import signal
                    n_turns_win = 20
                    sig_x = mean_x_from_slice_monitor#[mask_from_slice]
                    sig_y = mean_y_from_slice_monitor#[mask_from_slice]
                    win = signal.boxcar(n_turns_win)
                    filtered_x = signal.convolve(sig_x, win, mode='same') / np.sum(win)
                    filtered_y = signal.convolve(sig_y, win, mode='same') / np.sum(win)


                # Plot              
                tt = np.arange(0,ob.mean_x.shape[0],1)
                tt_from_slice = np.arange(0,ob_slice.mean_x.shape[1],1)

                sp1.plot(tt[mask_from_bunch], mean_x_from_bunch_monitor[mask_from_bunch]*1e3, color = colorcurr[jj])
                sp2.plot(tt[mask_from_bunch], mean_y_from_bunch_monitor[mask_from_bunch]*1e3, color = colorcurr[jj], 
                        label='%d '%(n_slices))

                if charge_weight_centroid_plots_flag:               
                    sp3.plot(tt_from_slice[mask_from_slice], filtered_x[mask_from_slice], color = colorcurr[jj])
                    sp4.plot(tt_from_slice[mask_from_slice], filtered_y[mask_from_slice], color = colorcurr[jj])
                
                sp5.plot(tt[mask_from_bunch], epsn_x_from_bunch_monitor[mask_from_bunch]*1e6, color = colorcurr[jj])
                #sp4.set_ylim(2.9,3.5)
               
                sp6.plot(tt[mask_from_bunch], epsn_y_from_bunch_monitor[mask_from_bunch]*1e6, color = colorcurr[jj]) 
                
                sp7.plot(tt[mask_from_bunch], N_mp_from_bunch_monitor[mask_from_bunch], color = colorcurr[jj])
                sp8.plot(tt[mask_from_bunch], sigma_z_from_bunch_monitor[mask_from_bunch]*4/clight*1e9, color = colorcurr[jj])



                legend = sp2.legend(bbox_to_anchor=(1.05, 1.03),  
                            loc='upper left', 
                            title='Slices', 
                            prop={'size':14}, ncol=1, 
                            borderpad=0.5, columnspacing=0.9, handlelength=0.16)
                
                
                
                legend.get_title().set_fontsize('16')
                jj=jj+1

                
        # Set limits
        sp1.set_ylim(-0.06, 0.06) 
        sp3.set_ylim(0., 0.35) 
        sp5.set_ylim(2.9, 3.4)          
        
        for sp in [sp1, sp2]:
            sp.set_ylim(-.3, .3)

        for sp in [sp3, sp4]:
            sp.set_ylim(0, 1.)    
            
        for sp in [sp5, sp6]:
            sp.set_ylim(2.,4.) 
        

        # Set the label 
        sp1.set_ylabel('Horizontal centroid position [mm]')
        sp2.set_ylabel('Vertical centroid position [mm]')
        sp3.set_ylabel('Charge weighted\nhorizontal centroid rms [a.u]')
        sp4.set_ylabel('Charge weighted\nvertical centroid rms [a.u]')
        sp5.set_ylabel('Normalized emittance x [um]')
        sp6.set_ylabel('Normalized emittance y [um]')
        sp7.set_ylabel('Number of macroparticles')
        sp8.set_ylabel('Bunch length (4$\sigma$) [ns]')


        #sp1.set_xlim(0, 1.0)
        for sp in [sp1, sp2, sp3, sp4, sp5, sp6, sp7, sp8]:
            sp.set_xlabel('Turns')
            sp.ticklabel_format(useOffset=False)
            sp.grid('on')
            ms.sciy()
            #~ sp.set_xlim(0, 20000)
        
        ms.mystyle_arial(14)  
        gs1.tight_layout(fig, rect=[0.02, 0, 0.86, .95], w_pad=.2, h_pad=1.5)
        #~ title = fig.suptitle(os.getcwd().split('/')[-2])
        title = fig.suptitle('ArcQuad:   Segments = %d   MPs/Slice = %d   Length: %.2f   Beta_xy: %.0f m'%(n_segments,macroparticles_per_slice,fraction_device_quad,betax))
        #~ pl.title('ArcQuad Drift    Length = %.2f'%(fraction_device_quad))
        if savefigures:
            fig.savefig(folder_plot + 'scanSlice_length%.2f_betaxy%.0f.png'%(fraction_device_quad,betax), dpi=300, 
                bbox_inches='tight', bbox_extra_artists=[legend, title])

pl.show()

