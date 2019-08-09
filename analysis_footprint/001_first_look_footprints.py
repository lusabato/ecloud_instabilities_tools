import pylab as pl
import numpy as np
import matplotlib.gridspec as gridspec
import matplotlib.ticker as mtick

import os,sys
BIN = os.path.expanduser("../tools/")
sys.path.append(BIN)
import myfilemanager as mfm
import mystyle as ms

from mpl_toolkits.axes_grid1 import make_axes_locatable

pl.close('all')


Q_x = .27
Q_y = .295

betax         = 92.7
betay         = 93.2
#~ betax_vect = [50, 100, 150, 200, 300, 400, 500, 600]
#~ betax_vect = [100]

#~ betay_vect = betax_vect

#~ fact_beam = 1.0e11


#~ Qx_min = Q_x - 5e-4
#~ Qy_min = Q_y - 5e-4

#~ Qx_max_cut = Q_x+0.03
#~ Qy_max_cut = Q_y+0.03

Qx_min = Q_x - Q_x * 0.03
Qy_min = Q_y - Q_y * 0.03

Qx_max_cut = Q_x + Q_x * 0.1
Qy_max_cut = Q_y + Q_x * 0.1




# scan parameters

# 1. Intensity
intensity_vect = [1.2e11, 2.3e11]

# 2. Chromaticity
Qp_x_vect = np.linspace(-2.5,20,10)
Qp_y_vect = np.linspace(-2.5,20,10)

Qp_tag_vect = []
for index_tag,Qp_x in enumerate(Qp_x_vect):
    
    if Qp_x < 0:
        Qp_tag_vect.append(('minus' + '%s')%(np.abs(Qp_x)))

    else:
        Qp_tag_vect.append(Qp_x) 


folder_plot = 'footprint'
if not os.path.exists(folder_plot):
    os.makedirs(folder_plot)


ms.mystyle_arial(18)
i_fig = 0
#~ for betax, betay in zip(betax_vect, betay_vect):
    
    #~ for fraction_device_quad in fraction_device_quad_vec:

# 1. Intensity
for intensity in intensity_vect:

    # 2. Chromaticity
    for Qp_x,Qp_y,Qp_tag in zip(Qp_x_vect,Qp_y_vect,Qp_tag_vect):
             
        sim_ident = '../simulations_PyPARIS/Inj_ArcQuad_T0_x_slices_750_seg_8_MPslice_5e3_eMPs_250e3_length_7_VRF_4MV_intensity_%.1fe11ppb_Qp_xy_%s'%(intensity/1e11,Qp_tag)           
        filename_footprint = 'footprint.h5'
        print sim_ident
        
        try:                                               
            ob = mfm.object_with_arrays_and_scalar_from_h5(sim_ident + '/' + filename_footprint)
            
            Jy = (ob.y_init**2 + (ob.yp_init*betay)**2)/(2*betay)
            Jx = (ob.x_init**2 + (ob.xp_init*betax)**2)/(2*betax)
            
            #~ fig = pl.figure(i_fig, figsize=(11,8))
            #~ fig.patch.set_facecolor('w')
            #~ gs1 = gridspec.GridSpec(1, 1)
            #~ gs2 = gridspec.GridSpec(2, 1)
            fig = pl.figure(i_fig, figsize=(13,10))
            fig.patch.set_facecolor('w')
            gs1 = gridspec.GridSpec(1, 1)
            gs2 = gridspec.GridSpec(1, 2)
            

            sp1 = fig.add_subplot(gs1[0])
            s1 = sp1.scatter(np.abs(ob.qx_i), np.abs(ob.qy_i), c =ob.z_init*1e2, marker='.', edgecolors='none', vmin=-32, vmax=32)
            sp1.plot([Q_x], [Q_y], '*k', markersize=10)
            sp1.set_xlabel('Q$_x$')
            sp1.set_ylabel('Q$_y$')
            sp1.set_xlim([Qx_min, Qx_max_cut])
            sp1.set_ylim([Qy_min, Qy_max_cut])

            #~ sp1.set_xlim([0.2695, 0.300])
            #~ sp1.set_ylim([0.2945, 0.325])
            
        
            sp1.set_aspect(aspect=1, adjustable='box')
            ax = pl.gca()
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.02)
            clb1 = pl.colorbar(s1, cax=cax) 
            ax.yaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
            ax.xaxis.set_major_formatter(mtick.FormatStrFormatter('%.3f'))
            ax.yaxis.set_major_locator(mtick.MaxNLocator(nbins=5))
            ax.xaxis.set_major_locator(mtick.MaxNLocator(nbins=5))
            sp1.grid('on')


            # Vert. detuning plot
            #=====================
        
            sp2 = fig.add_subplot(gs2[1])#, sharex=sp3) 
            s2 = sp2.scatter(ob.z_init*1e2,np.abs(ob.qy_i)-Q_y, c =Jy, marker='.', edgecolors='none', vmin=0, vmax=8e-9)
            sp2.set_xlim(-30, 30)
            
            #~ sp2.set_ylim(-0.001, 0.003)
            sp2.set_ylim(-0.01, 3e-2)
            
            sp2.set_xlabel('z [cm]')
            sp2.set_ylabel('$\Delta$Qy', labelpad=5)
            ms.sciy()
            ax = pl.gca()
            ax.set_aspect(aspect='auto', adjustable='box')
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.02)
            clb2 = pl.colorbar(s2, cax=cax)
            sp2.grid('on')
            
            
            # Hor. detuning plot
            #=====================


            sp5 = fig.add_subplot(gs2[0])#, sharex=sp3) 
            s5 = sp5.scatter(ob.z_init*1e2,np.abs(ob.qx_i)-Q_x, c =Jx, marker='.', edgecolors='none', vmin=0, vmax=8e-9)
            sp5.set_xlim(-30, 30)
            
            #~ sp5.set_ylim(-0.001, 0.003)
            sp5.set_ylim(-0.01, 3e-2)
            
            sp5.set_xlabel('z [cm]')
            sp5.set_ylabel('$\Delta$Qx', labelpad=5)
            ax = pl.gca()
            ms.sciy()
            ax.set_aspect(aspect='auto', adjustable='box')
            divider = make_axes_locatable(ax)
            cax = divider.append_axes("right", size="5%", pad=0.02)
            clb5 = pl.colorbar(s5, cax=cax)
            sp5.grid('on')
            
            clb1.set_label('z [cm]', labelpad=5)
            clb2.set_label('J$_y$ [a.u.]', labelpad=5) #clb2.set_label('J$_y$ [a.u.]', labelpad=5)
            clb5.set_label('J$_x$ [a.u.]', labelpad=5) #clb2.set_label('J$_y$ [a.u.]', labelpad=5)
                                        
            i_fig = i_fig+1
            #~ gs1.tight_layout(fig, rect=[0, 0, 0.38, 0.96], pad=1.08, h_pad=1.5) #left,bottom,right,top
            #~ gs2.tight_layout(fig, rect=[0.41, 0.02, 1, 0.96], pad=1.08, h_pad=.5)
            gs1.tight_layout(fig, rect=[0.25, 0.51, 0.75, 1.], pad=1.08, h_pad=1.5) #left,bottom,right,top
            gs2.tight_layout(fig, rect=[0., 0., 1, 0.49], pad=1.08, h_pad=.5)
            
            #pl.suptitle('LHC_Quad_sey1.30_nseg%d'%n_segments)
            fname = sim_ident.split('/')[-1]+'_fp.png'
            
            pl.savefig(folder_plot + '/' +fname, dpi=300, bbox_inches='tight')                
            #~ pl.savefig(folder_plot + '/LHC_fp_nseg%d.eps'%n_segments, format='eps', dpi=1000, bbox_inches='tight')

            #pl.show()
        except IOError as goterror:
            print 'Skipped. Got:',  goterror
                        
