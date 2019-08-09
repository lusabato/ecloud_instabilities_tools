import numpy as np

import glob
import os
import time
import datetime



sim_folder = '../simulations_PyPARIS/'
list_folders_all = glob.glob(sim_folder + '*')


now = time.strftime("%d/%m/%Y %H:%M:%S")
now_year = int((now.split('/')[2]).split(' ')[0])
now_month = int(now.split('/')[1])
now_day = int(now.split('/')[0])
now_hour = int(((now.split('/')[2]).split(' ')[1]).split(':')[0])
now_minute = int(now.split(':')[1])
now_second = int(now.split(':')[2])
now_date = datetime.datetime(now_year, now_month, now_day, now_hour, now_minute, now_second)

today = '%d_%d_%d'%(now_year,now_month,now_day)
folder_work = 'report_%s/'%today
if not os.path.exists(folder_work):
    os.makedirs(folder_work)
writing_lines =['Restart Simulation Report   %s\n'%today]


# parameters needed for the check of the emittance growth
sim_died_emittance_growth = 0
epsn = 2.5e-6
epsn_max_growth_fraction = 0.5
epsn_max = (epsn)*(1 + epsn_max_growth_fraction)


# parameters needed for the check of beam losses
sim_died_beam_losses = 0


# parameters needed for the check of number of the turns
turns_goal = 20000                  # change it you need more turns
sim_died_beam_turns = 0
findln_opic = 'last_turn_part ='


# parameters needed for the check if the simulation is running
sim_running = 0
findln_pyparislog = 'Turn '

check_is_running_mode = 'auto'
minimum_number_of_turns_for_std = 10   # (at least 2) minimum number of turns in order to calculate the standard deviation of time per turn
# 1. if the number of turns is larger than 'minimum_number_of_turns_for_std'
# the turn time, after that the simulation is considered died, is calculated as:
# average + 'number_std_to_calculate_minutes' * standard_deviation
number_std_to_calculate_minutes = 10
# 2. if the number of turns is smaller than 'minimum_number_of_turns_for_std'
# the turn time, after that the simulation is considered died, is calculated as:
# average * 'times_average_to_calculate_minutes'
times_average_to_calculate_minutes = 3
# parameters needed to evaluate minutes_queue 
N_turns_per_job = 128
findln_pyparislog_start_sim = 'Starting simulation on '

#~ # Uncomment this part if you want to insert the time after that the simulation is considered died
#~ check_is_running_mode = 'manual'
#~ minutes_sim_considered_died = 1    # turn time (in minutes) after that the simulation is considered died
#~ minutes_queue = 0                  # queue time (in minutes)



list_folders_resubmit = []
for folder in list_folders_all:

    writing_lines = writing_lines + ['\n\n%s\n'%folder]

# 1. check if the simulation died for emittance growth      
    file_opic = folder + '/opic.txt'
    emittance_growth_text = os.system('grep "Stop simulation due to emittance growth." %s'%file_opic)
    if emittance_growth_text == 512:
        print 'ERROR, No such file or directory: ' + folder
        
    if emittance_growth_text == 0:
        print folder + '\n'
        writing_lines = writing_lines + ['Stop simulation due to emittance growth. \n']
        sim_died_emittance_growth = sim_died_emittance_growth + 1

    if emittance_growth_text == 256:        #simulation didn't die for emittance growth

    
# 2. check if the simulation died for beam losses
        losses = os.system('grep "Stop simulation due to beam losses." %s'%file_opic)
        if losses == 512:
            print 'ERROR, No such file or directory: ' + folder
        
        if losses == 0:
            print folder + '\n'
            writing_lines = writing_lines + ['Stop simulation due to losses.\n']
            sim_died_beam_losses = sim_died_beam_losses + 1

        if losses == 256:       #simulation didn't die for beam losses
        
        
# 3. check if the simulation died because reach the number of turns
            with open(file_opic, 'r') as fid:
                lines_opic = fid.readlines()
                
            found_opic = False
            pos_opic = None
            for ii_opic, line in enumerate(lines_opic):
                if findln_opic in line:
                    pos_opic = ii_opic
                    found_opic = True
                
            if found_opic:
                turns = int((lines_opic[pos_opic].split('= ')[1]).split('\n')[0])
                
                if turns > turns_goal:
                    print '\n' + 'Simulation reached the number of turns\n' + folder + '\n'
                    writing_lines = writing_lines + ['Simulation reached the number of turns.\n']
                    sim_died_beam_turns = sim_died_beam_turns + 1
        
                else:       #simulation didn't reach the number of turns

    
# 4. check if the simulation is running                     
                    file_pyparislog = folder + '/pyparislog.txt'
                    with open(file_pyparislog, 'r') as fid:
                        lines_pyparislog = fid.readlines()

                    found_pyparislog = False
                    last_pos_pyparislog = None
                    for ii_pyparislog, line in enumerate(lines_pyparislog):
                        if findln_pyparislog in line:
                            last_pos_pyparislog = ii_pyparislog
                            found_pyparislog = True
                    
                    if not found_pyparislog:    # The simulation ran 0 turns
                        print '\n' + 'Simulation ran 0 turns. Simulation needs to be resubmitted \n' + folder + '\n'
                        writing_lines = writing_lines + ['Simulation ran 0 turns. Simulation needs to be resubmitted.\n']
                        list_folders_resubmit.append(folder)
                    
                    else:    # The simulation ran at least 1 turn
                        
                        last_job_last_turn = int((lines_pyparislog[last_pos_pyparislog].split('Turn ')[1]).split(',')[0])
                        
                        last_Turn = (lines_pyparislog[last_pos_pyparislog].split(', ')[2]).split('\n')[0]
                        last_Turn_day = int((last_Turn.split('/')[2]).split(' ')[0])
                        last_Turn_month = int(last_Turn.split('/')[1])
                        last_Turn_year = int(last_Turn.split('/')[0])
                        last_Turn_hour = int(((last_Turn.split('/')[2]).split(' ')[1]).split(':')[0])
                        last_Turn_minute = int(last_Turn.split(':')[1])
                        last_Turn_second = int(last_Turn.split(':')[2])
                        last_Turn_date = datetime.datetime(last_Turn_day, last_Turn_month, last_Turn_year, last_Turn_hour, last_Turn_minute, last_Turn_second)

                        diff_date = now_date - last_Turn_date
                        diff_minutes = diff_date.days * 24 * 60 + diff_date.seconds / 60
                    
                        if check_is_running_mode == 'auto':
                            # Evaluation of the average of the time per turn
                            time_per_turn_seconds = []
                            for ii_pyparislog, line in enumerate(lines_pyparislog):
                                if findln_pyparislog in line:                         
                                    this_turn_time = int((line.split(',')[1]).split(' ')[1])
                                    time_per_turn_seconds.append(this_turn_time)
                                    
                            time_per_turn_average_seconds = np.mean(time_per_turn_seconds)
                            time_per_turn_std_seconds = np.std(time_per_turn_seconds)
                            # Evaluation of turn time (in minutes) after that the simulation is considered died
                            if len(time_per_turn_seconds) > minimum_number_of_turns_for_std:

                                minutes_sim_considered_died = (time_per_turn_average_seconds + number_std_to_calculate_minutes * time_per_turn_std_seconds) / 60

                            else:    # few turns in order to calculate the standard deviation

                                minutes_sim_considered_died = (times_average_to_calculate_minutes * time_per_turn_average_seconds) / 60
                    
                            # Evaluation of queue time (in minutes)
                            if last_job_last_turn == N_turns_per_job - 1:    # The job is finished and the queue time should be estimated
                                
                                for ii_pyparislog, line in enumerate(lines_pyparislog):
                                    if findln_pyparislog_start_sim in line:
                                        last_pos_start_sim_pyparislog = ii_pyparislog
                                
                                start_sim = lines_pyparislog[last_pos_start_sim_pyparislog].split(' on ')[1]
                                start_sim_day = int((start_sim.split('/')[2]).split(' ')[0])
                                start_sim_month = int(start_sim.split('/')[1])
                                start_sim_year = int(start_sim.split('/')[0])
                                start_sim_hour = int(((start_sim.split('/')[2]).split(' ')[1]).split(':')[0])
                                start_sim_minute = int(start_sim.split(':')[1])
                                start_sim_second = int(start_sim.split(':')[2])
                                start_sim_date = datetime.datetime(start_sim_day, start_sim_month, start_sim_year, start_sim_hour, start_sim_minute, start_sim_second)
                        
                                for ii_pyparislog, line in enumerate(lines_pyparislog[0:last_pos_start_sim_pyparislog]):
                                    if findln_pyparislog in line:
                                        previous_job_last_turn_pos_pyparislog = ii_pyparislog
                                        
                                previous_job_last_turn = (lines_pyparislog[previous_job_last_turn_pos_pyparislog].split(', ')[2]).split('\n')[0]
                                previous_job_last_turn_day = int((previous_job_last_turn.split('/')[2]).split(' ')[0])
                                previous_job_last_turn_month = int(previous_job_last_turn.split('/')[1])
                                previous_job_last_turn_year = int(previous_job_last_turn.split('/')[0])
                                previous_job_last_turn_hour = int(((previous_job_last_turn.split('/')[2]).split(' ')[1]).split(':')[0])
                                previous_job_last_turn_minute = int(previous_job_last_turn.split(':')[1])
                                previous_job_last_turn_second = int(previous_job_last_turn.split(':')[2])
                                previous_job_last_turn_date = datetime.datetime(previous_job_last_turn_day, previous_job_last_turn_month, previous_job_last_turn_year, previous_job_last_turn_hour, previous_job_last_turn_minute, previous_job_last_turn_second)
                        
                                diff_date_queue = start_sim_date - previous_job_last_turn_date
                                minutes_queue = diff_date_queue.days * 24 * 60 + diff_date_queue.seconds / 60
                    
                        if last_job_last_turn == N_turns_per_job - 1:    # The job is finished and there is also the queue time to take into account
                            time_out = minutes_sim_considered_died + minutes_queue
                        else:
                            time_out = minutes_sim_considered_died
                    
                        if diff_minutes < time_out:       # simulation is running
                            print '\n' + 'Simulation is running \n' + folder + '\n'
                            writing_lines = writing_lines + ['Simulation is running.\n']
                            sim_running = sim_running + 1
                    
                        else:                                               # simulation isn't running
                            print '\n' + 'Simulation needs to be resubmitted \n' + folder + '\n'
                            writing_lines = writing_lines + ['Simulation needs to be resubmitted.\n']
                            list_folders_resubmit.append(folder)

                
#summary
print '\nAll the simulations are: %d\n\n'%(len(list_folders_all))
writing_lines = writing_lines + ['\nAll the simulations are: %d\n'%(len(list_folders_all))]

print 'The simulations died for emittance growth are: %d'%sim_died_emittance_growth
print 'The simulations died for beam losses are: %d'%sim_died_beam_losses
print 'The simulations that reached the number of turns are: %d'%sim_died_beam_turns
print 'The simulations that are running are: %d'%sim_running
print 'The simulations that need to be resubmitted are: %d'%(len(list_folders_resubmit))
writing_lines = writing_lines + ['The simulations died for emittance growth are: %d\n'%sim_died_emittance_growth]
writing_lines = writing_lines + ['The simulations died for beam losses are: %d\n'%sim_died_beam_losses]
writing_lines = writing_lines + ['The simulations that reached the number of turns are: %d\n'%sim_died_beam_turns]
writing_lines = writing_lines + ['The simulations that are running are: %d\n'%sim_running]
writing_lines = writing_lines + ['The simulations that need to be resubmitted are: %d\n'%(len(list_folders_resubmit))]


with open(folder_work + 'restart_simulations_report_%s.txt'%(today), 'w') as fid:
    fid.writelines(writing_lines)


#resubmit simulations
for folder in list_folders_resubmit:
   print folder
   os.chdir(folder)
   print os.system('pwd')

   os.system('cp ../../restart_simulations/super_reset_last_part.py ./')
   os.system('python super_reset_last_part.py')
   os.system('sh launch_this')

   os.chdir('../../restart_simulations/')



