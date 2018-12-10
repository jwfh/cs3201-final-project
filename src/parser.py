#!/usr/bin/env python3

import re 

logpaths = [
    '../logs/medium-set-en2048ece03.engr.mun.ca-10-2.txt',
    '../logs/medium-set-en2048ece04.engr.mun.ca-10-1.txt',
    '../logs/medium-set-en2048ece05.engr.mun.ca-10-2.txt',
    '../logs/medium-set-en2048ece07.engr.mun.ca-10-2.txt',
    '../logs/medium-set-en2048ece12.engr.mun.ca-10-1.txt',
    '../logs/tiny-set-devastator.cs.mun.ca-10-2.txt',
    '../logs/tiny-set-laserbeak.cs.mun.ca-10-2.txt',
    '../logs/tiny-set-overkill.cs.mun.ca-10-2.txt',
    '../logs/tiny-set-pounce.cs.mun.ca-10-2.txt',
    '../logs/tiny-set-starscream.cs.mun.ca-10-2.txt'
]

for logpath in logpaths:
    with open(logpath, 'r') as logfile:
        f_index = 1
        init_file = open(logpath.replace('/logs/', '/logs/out/').replace('.txt', '-init_file-out.txt'), 'w')   
        gen_file = open(logpath.replace('/logs/', '/logs/out/').replace('.txt', '-gen_all-out.txt'), 'w')  
        cands_file = open(logpath.replace('/logs/', '/logs/out/').replace('.txt', '-pick_cands-out.txt'), 'w') 
        fitness_file = open(logpath.replace('/logs/', '/logs/out/').replace('.txt', '-fitnesses-out.txt'), 'w') 
        last_gen_file = open(logpath.replace('/logs/', '/logs/out/').replace('.txt', '-last_gen-out.txt'), 'w')

        line = logfile.readline()
        while "init_file" not in line:
            line = logfile.readline()     
        init_time = line.split()[3]
        init_file.write(str(f_index) + ' ' + init_time + "\n")
        while "gen_all" not in line:
            line = logfile.readline()     
        gen_time = line.split()[3]
        gen_file.write(str(f_index) + ' ' + gen_time + "\n")

        while line.strip():
            trial_file = open(logpath.replace('/logs/', '/logs/out/').replace('.txt', '-log-' + str(f_index) + '.txt'), 'w')
            while "pick_cands" not in line:
                line = logfile.readline()     
            cand_time = line.split()[3]
            cands_file.write(str(f_index) + ' ' + cand_time + "\n")
            line = logfile.readline()
            while "Last geration with improvement" not in line:
                try:
                    if line:
                        linedata = line.split()
                        gen = linedata[4]
                        fitness = linedata[7]
                        timedata = re.split(r'[\[\]]', linedata[2])
                        time = timedata[2]
                        trial_file.write(gen + ' ' + fitness + ' ' + time + "\n")
                except Exception as e:
                    print(line, str(e))
                line = logfile.readline().strip()
            gen = line.split()[4]
            last_gen_file.write(str(f_index) + " " + gen + "\n")
            while "Best fitness" not in line:
                line = logfile.readline()
            f = line.split()[2]
            fitness_file.write(str(f_index) + " " + f + "\n")
            trial_file.close()

            while "pick_cands" not in line:
                line = logfile.readline()
                if not line:
                    break
        
            f_index += 1
        init_file.close()
        gen_file.close()
        cands_file.close()
        fitness_file.close()
        last_gen_file.close()
