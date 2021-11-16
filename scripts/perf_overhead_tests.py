import subprocess
import json
import random
import os
import sys
import datetime

class PerfOverheadTests:

    def __init__(self, number):

        self.number_of_registers = number

        self.make_perf_bash_file()
        
        self.experiment_setup()

        self.run_experiment()

    def make_perf_bash_file(self):

        def perf_picker(value):

            #registers_list = ['-ecycles','-ebus-cycles', '-ebus_access', '-eL1-icache-load', '-emem_access',\
            #'-eLLC-loads', '-eLLC-stores', '-eLLC-load-misses', '-eLLC-store-misses', \
            #'-edTLB-loads', '-edTLB-load-misses', '-edTLB-store-misses', '-eiTLB-load-misses', '-er066', '-er067']
            #0x66 is mem access load, 0x67 is mem access store, see ARM72 programmers manual
            registers_list = ['-er013', '-er014', '-er015', '-er016', '-er017', '-er018', '-er019', '-er040', '-er041', '-er042', '-er043', '-er044', '-er046', '-er047', '-er048', '-er04c', '-er050', '-er051', '-er052', '-er053', '-er056', '-er057', '-er058', '-er060', '-er061', '-er063', '-er064', '-er066', '-er067']
            value=int(value)
            
            selected_registers = random.sample(registers_list, value)
            selected_registers = ' '.join([str(item) for item in selected_registers])
            print("these are the selected registers: \n")
            print(selected_registers)

            return selected_registers

        def command_setup(selected_registers):

            initial_command = '''\
            #! /bin/bash\nperf_5.10 stat '''

            bash_command = initial_command + selected_registers + " "

            return bash_command

        selected_registers = perf_picker(self.number_of_registers)

        bash_command = command_setup(selected_registers)

        path = r"/home/pi/multicore-test-harness/scripts/perf_scripts/test.sh"

        assert os.path.isfile(path)
        with open (path, 'w') as rsh:
            rsh.writelines(bash_command + '''"${@:1}"''')

    def experiment_setup(self):


        def filename():

            today = datetime.datetime.now()
            json_log_directory = "L1_events/"
            json_file = str(self.number_of_registers) + "-registers-" +str(today.day) + "-" +str(today.minute) +"-"+str(today.hour)+"-"+ str(today.month) + "-perfoverheadtest.json"  
            json_log = json_log_directory + json_file
            print(json_log)
            return json_log
        
        
        start_of_cmd = "sudo python3 run_experiments.py "

        perf_filepath = "exp_configs/eval_env/stress_all_pi.json "

        json_filename = filename()

        self.subprocess_command = start_of_cmd + perf_filepath + json_filename

    def run_experiment(self):

        subprocess.run(self.subprocess_command, shell=True)





if __name__ == "__main__":

    if len(sys.argv) != 2:

        print("usage: " + sys.argv[0] + "number of experiments\n")

        exit(1)

    counter = 0

    argv1 = int(sys.argv[1])

    while (counter < argv1):

        counter = counter + 1

        number = random.randrange(1,15)

        print(f"number is {number}\n")

        PerfOverheadTests(number)

        

        
