import os,sys
import time
import datetime

BIN = os.path.expanduser("../../PyPARIS_sim_class/")
sys.path.append(BIN)
import Save_Load_Status as SLS


now = time.strftime("%d/%m/%Y %H:%M:%S")
now_year = int((now.split('/')[2]).split(' ')[0])
now_month = int(now.split('/')[1])
now_day = int(now.split('/')[0])
now_hour = int(((now.split('/')[2]).split(' ')[1]).split(':')[0])
now_minute = int(now.split(':')[1])
now_second = int(now.split(':')[2])
now_date = datetime.datetime(now_year, now_month, now_day, now_hour, now_minute, now_second)

today = '%d_%d_%d'%(now_year,now_month,now_day)
folder_work = '../../restart_simulations/report_%s/'%today
writing_lines =['\n\n\n']

folder_curr_sim = os.getcwd().split('/')[-1]


SimSt = SLS.SimulationStatus()
SimSt.load_from_file()

if not SimSt.present_part_done:
    part_finished = SimSt.present_simulation_part-1
    sim_status_file_is_already_ok = False
else:
    part_finished = SimSt.present_simulation_part   
    sim_status_file_is_already_ok = True



if part_finished==-1:
    print 'First part not finished. I restart from scratch!'
    writing_lines = writing_lines + ['First part not finished. I restart from scratch!\n']
    os.remove('simulation_status.sta')
else:
   if not os.path.isfile('bunch_status_part%02d.h5'%part_finished):
        raise ValueError('There seems to be a status incositency.\nSimulation CANNOT be restarted!')
        writing_lines = writing_lines + ['There seems to be a status incositency.\nSimulation CANNOT be restarted!\n']

   
   if not sim_status_file_is_already_ok:
        print 'I try to restart your simulation...'
        writing_lines = writing_lines + ['I try to restart your simulation...\n']
        SimSt.N_turns_per_run =  SimSt.last_turn_part - SimSt.first_turn_part + 1
        SimSt.present_simulation_part = part_finished
        SimSt.first_turn_part -= SimSt.N_turns_per_run
        SimSt.last_turn_part -= SimSt.N_turns_per_run
        SimSt.present_part_done = True
        SimSt.present_part_running = False

        SimSt.dump_to_file()

        print 'Restored status:\n\n'
        writing_lines = writing_lines + ['Restored status:\n\n\n']
        SimSt.print_from_file()
        print '\n\n'
        writing_lines = writing_lines + ['\n\n\n']
   else:
        print 'Your simulation can be restarted without action!'
        writing_lines = writing_lines + ['Your simulation can be restarted without action!\n']


if os.path.exists(folder_work):
    with open(folder_work + 'reset_last_part_%s.txt'%(folder_curr_sim), 'w') as fid:
        fid.writelines(writing_lines)
