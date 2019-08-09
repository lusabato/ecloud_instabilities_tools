import numpy as np
import scipy.io as sio
import os
import pylab as pl


pl.close('all')
folder_work = 'computational_time/'

# Import the dictionary elements
dic = sio.loadmat(folder_work + 'computational_time.mat')
computational_time_seconds = np.squeeze(dic['computational_time_seconds'])
N_turns_done = np.squeeze(dic['N_turns_done'])
time_per_turn_seconds = computational_time_seconds/N_turns_done


# Scan Parameters
betax_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
betay_vect = [50., 100., 150., 200., 300., 400., 500., 600.]
fraction_device_quad_vect = [0.07, 0.16, 0.26]
n_slices_vect = np.array([250., 500., 750., 1000.])

# Simulation Parameters
n_segments = 16
PyPICmode_tag = 'Tblocked'
eMPs = 500000
macroparticles_per_slice = 5000.



# 1. Calculate the total computational time needed for this study
computational_time_total_days = (computational_time_seconds.sum()/(60*60*24))
writing_lines =['The total computational time is:\n', '%.1f days (using 16 cores)\n'%computational_time_total_days]



# 2. Report of the simulations
writing_lines = writing_lines + ['\n\n\n\n\nReport of the simulations\n']
sim_folder = '../simulations_PyPARIS/'
# variables needed for the check of the emittance growth
sim_died_emittance_growth = 0

# variables needed for the check of beam losses
sim_died_beam_losses = 0

# variables needed for the check of number of the turns
turns_goal = 20000                  # change it you need more turns
sim_died_beam_turns = 0
findln_opic_first_turn_part = 'first_turn_part ='
findln_opic_turn = 'Turn '

time_prediction_days = np.zeros((len(n_slices_vect),len(betax_vect),len(fraction_device_quad_vect)))
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):

    for jj, betax, betay in zip(range(len(betax_vect)), betax_vect, betay_vect):

        for ii, n_slices in enumerate(n_slices_vect):
        
            folder_curr_sim = sim_folder + 'transverse_grid_%s_betaxy_%.0fm_length%.2f_slices_%d'%(PyPICmode_tag, betax,fraction_device_quad,n_slices)                       
            writing_lines = writing_lines + ['\n\n%s\n'%folder_curr_sim]
            writing_lines = writing_lines + ['%1.f s/Turn.\n'%time_per_turn_seconds[ii,jj,kk]]

    # 2.1 check if the simulation died for emittance growth     
            file_opic = folder_curr_sim + '/opic.txt'
            emittance_growth_text = os.system('grep "Stop simulation due to emittance growth." %s'%file_opic)
            if emittance_growth_text == 512:
                print 'ERROR, No such file or directory: ' + folder
        
            if emittance_growth_text == 0:
                print folder_curr_sim + '\n'
                writing_lines = writing_lines + ['Stop simulation due to emittance growth.\n']              
                sim_died_emittance_growth = sim_died_emittance_growth + 1

            if emittance_growth_text == 256:        #simulation didn't die for emittance growth
    
    # 2.2 check if the simulation died for beam losses
                losses = os.system('grep "Stop simulation due to beam losses." %s'%file_opic)
                if losses == 512:
                    print 'ERROR, No such file or directory: ' + folder
        
                if losses == 0:
                    print folder_curr_sim + '\n'
                    writing_lines = writing_lines + ['Stop simulation due to losses.\n']
                    sim_died_beam_losses = sim_died_beam_losses + 1

                if losses == 256:       #simulation didn't die for beam losses
                
    # 2.3 check if the simulation died because reach the number of turns
                    with open(file_opic, 'r') as fid:
                        lines_opic = fid.readlines()
                                        
                    pos_opic_first_turn_part = None
                    pos_opic_turn = None
                    for ii_opic, line in enumerate(lines_opic):
                        if findln_opic_first_turn_part in line:
                            pos_opic_first_turn_part = ii_opic
                            
                    for ii_opic, line in enumerate(lines_opic):
                        if findln_opic_turn in line:
                            pos_opic_turn = ii_opic                         
                
                    if (pos_opic_first_turn_part is not None) and (pos_opic_turn is not None):
                        
                        first_turn_part = int((lines_opic[pos_opic_first_turn_part].split('= ')[1]).split('\n')[0])
                        turns = int((lines_opic[pos_opic_turn].split(',')[0]).split(' ')[1])
                        total_turns = first_turn_part + turns + 1
                        
                        if total_turns > turns_goal:
                            print '\n' + 'Stop simulation: reached the number of turns.\n' + folder_curr_sim + '\n'
                            writing_lines = writing_lines + ['Stop simulation: reached the number of turns.\n']                 
                            sim_died_beam_turns = sim_died_beam_turns + 1
                        
                        else:
                            writing_lines = writing_lines + ['Simulation not finished. %d turns done.\n'%total_turns]
                            turns_left = turns_goal - total_turns
                            time_prediction_days[ii,jj,kk] = (turns_left * time_per_turn_seconds[ii,jj,kk])/(60*60*24)
                            writing_lines = writing_lines + ['%1.f days are needed to complete %d turns.\n'%(time_prediction_days[ii,jj,kk], turns_goal)]
                    
                    else:
                        writing_lines = writing_lines + ['Simulation not started.\n']





# 3. Summary
simulations_total = len(fraction_device_quad_vect)*len(betax_vect)*len(n_slices_vect)
writing_lines = writing_lines + ['\n\n\n\n\nThe simulations are: %d.\n'%simulations_total]
simulations_finished = sim_died_emittance_growth + sim_died_beam_losses + sim_died_beam_turns
writing_lines = writing_lines + ['The finished simulations are: %d.\n'%simulations_finished]
writing_lines = writing_lines + ['The slowest simulation needs %.1f days to reach %d turns.\n'%(time_prediction_days.max(),turns_goal)]
writing_lines = writing_lines + ['The fastest simulation needs %.1f days to reach %d turns.\n'%((np.extract(time_prediction_days>0,time_prediction_days)).min(),turns_goal)]

time_per_turn_average_seconds = np.mean(time_per_turn_seconds)
writing_lines = writing_lines + ['The average time per turn is: %.1f s.\n'%(time_per_turn_average_seconds)]

with open(folder_work + 'computational_time.txt', 'w') as fid:
    fid.writelines(writing_lines)





# 4. Plots
computational_time_seconds_nslices = np.zeros(len(n_slices_vect))
N_turns_done_nslices = np.zeros(len(n_slices_vect))
for kk, fraction_device_quad in enumerate(fraction_device_quad_vect):

    for jj, betax, betay in zip(range(len(betax_vect)), betax_vect, betay_vect):

        for ii, n_slices in enumerate(n_slices_vect):

            computational_time_seconds_nslices[ii] = computational_time_seconds_nslices[ii] + computational_time_seconds[ii,jj,kk]
            N_turns_done_nslices[ii] = N_turns_done_nslices[ii] + N_turns_done[ii,jj,kk]

time_per_turn_seconds_nslice = computational_time_seconds_nslices/N_turns_done_nslices

# Figure parameters
fig_index = 0
fig_size = (12,8)
axis_font = {'fontname':'Arial', 'size':'24'}
axis_font_title = {'fontname':'Arial', 'size':'20'}
labelsize_choice = 24
labelsize_legend = 24
line_width = 3.5

fig_index = fig_index + 1
fig = pl.figure(fig_index,figsize=fig_size)
pl.plot(n_slices_vect,time_per_turn_seconds_nslice, 'o-', linewidth=line_width)
pl.ylim(bottom=0)
pl.xlabel('Slices', **axis_font)
pl.ylabel('Computational Time [s/Turn]', **axis_font)
pl.title('ArcQuad  %s  Segments = %d  MPs/Slice = %d  e$^-$ MPs = %d'%(PyPICmode_tag,n_segments,macroparticles_per_slice,eMPs), **axis_font_title)
pl.tick_params(labelsize=labelsize_choice)
pl.grid(linestyle='dashed')
pl.savefig(folder_work + 'computational_time_nSlices.png', dpi=300)


pl.show()




