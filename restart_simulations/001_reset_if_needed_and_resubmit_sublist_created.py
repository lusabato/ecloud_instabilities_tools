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

# variables needed for the check of the emittance growth
sim_died_emittance_growth = 0
epsn = 2.5e-6
epsn_max_growth_fraction = 0.5
epsn_max = (epsn)*(1 + epsn_max_growth_fraction)

# variables needed for the check of beam losses
sim_died_beam_losses = 0

# variables needed for the check of number of the turns
turns_goal = 20000					# change it you need more turns
sim_died_beam_turns = 0
findln_opic = 'last_turn_part ='

# variables needed for the check if the simulation is running
hours_sim_considered_running = 1	# change it if you want a different time (in hours) after that the simulation is considered died
sim_running = 0
findln_pyparislog = 'Turn '


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

	if emittance_growth_text == 256:		#simulation didn't die for emittance growth

	
# 2. check if the simulation died for beam losses
		losses = os.system('grep "Stop simulation due to beam losses." %s'%file_opic)
		if losses == 512:
			print 'ERROR, No such file or directory: ' + folder
		
		if losses == 0:
			print folder + '\n'
			writing_lines = writing_lines + ['Stop simulation due to losses.\n']
			sim_died_beam_losses = sim_died_beam_losses + 1

		if losses == 256:		#simulation didn't die for beam losses
		
		
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
		
				else:		#simulation didn't reach the number of turns

	
# 4. check if the simulation is running						
					file_pyparislog = folder + '/pyparislog.txt'
					with open(file_pyparislog, 'r') as fid:
						lines_pyparislog = fid.readlines()
				
					found_pyparislog = False
					pos_pyparislog = None
					for ii_pyparislog, line in enumerate(lines_pyparislog):
						if findln_pyparislog in line:
							pos_pyparislog = ii_pyparislog
							found_pyparislog = True
					
					last_Turn = (lines_pyparislog[pos_pyparislog].split(', ')[2]).split('\n')[0]
					last_Turn_day = int((last_Turn.split('/')[2]).split(' ')[0])
					last_Turn_month = int(last_Turn.split('/')[1])
					last_Turn_year = int(last_Turn.split('/')[0])
					last_Turn_hour = int(((last_Turn.split('/')[2]).split(' ')[1]).split(':')[0])
					last_Turn_minute = int(last_Turn.split(':')[1])
					last_Turn_second = int(last_Turn.split(':')[2])
					last_Turn_date = datetime.datetime(last_Turn_day, last_Turn_month, last_Turn_year, last_Turn_hour, last_Turn_minute, last_Turn_second)

					diff_date = now_date - last_Turn_date
					diff_hours = diff_date.days * 24 + diff_date.seconds / 3600
					
					if diff_hours < hours_sim_considered_running:		#the simulation is running
						print '\n' + 'Simulation is running \n' + folder + '\n'
						writing_lines = writing_lines + ['Simulation is running.\n']
						sim_running = sim_running + 1
					
					else:												#simulation isn't running
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



