# %%
from typing import List , Dict
import re, sys, json, yaml, csv, os, fnmatch

regex_stats = re.compile(r'(\w+):\s+(.+)')
regex_loop = re.compile(r'^\s+Running\s+(\d+)\s+runs')
regex_quantil = re.compile(r'(\d+\.\d+%)\s+([><]\s+\d+)')
regex_new_test = re.compile(r'--- Running testcase')
regex_date = re.compile(r'/\w+\s+\w+\s+\d+\s+\d{2}:\d{2}:\d{2}\s+\w+\s+\d{4}/gm')
regex_deltas = re.compile(r'delta:\s+(\d+)\s+ns')
regex_multi_words = re.compile(r'(\w+(?:(?:\s*\w+)+)):\s+(.*)')
regex_busy_threads = re.compile(r'^Busy\s+Thread\s+(\d+\(\d+\)):\s+(\w+)')
regex_iterations = re.compile(r'Running\s+(\d+)\s+iterations')
regex_threads = re.compile(r'(\d+)\s+(sleeper|worker)\s+threads\s+created')
#regex_threads_prio = re.compile(r'(Noise|Thread)\s+\w?\s?(\d+)\s+(sleeper|worker)\s+threads\s+created')
#regex_per_cpu = re.compile(r'\w+:')\s+
regex_task = re.compile(r'\s+Task\s+(\d+)\s+\(prio\s+(\d+)\)\s+\(pid\s+(\d+)\):')
regex_thread_info = re.compile(r'(\d+):\s+(\d+\s+us):\s+RealtimeThread-(\d+)\s+pri\s+(\d+)\s+(\w+)')
regex_single_word = re.compile(r'\s*(\w+):\s+(\w+)')
regex_multi_words2 = re.compile(r'([\w\s]+):\s+(.*)')
regex_thread_status = re.compile(r'Busy\s+(\d+)\s+(\w+)')
regex_stats2 = re.compile(r'([\w\s]+)=\s+(.+)')


def parser_pthread_kill_latency(log_file : str) :
    ltp_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                ltp_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                ltp_dict[loop_no] = {}
            elif row := regex_stats.match(line):
                # Stats rows
                ltp_dict[loop_no][row.group(1)] = row.group(2)
            elif quantiles := regex_quantil.match(line):
                # Quantiles rows
                ltp_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            sys.stdout.write(line)
        if 'loops' not in ltp_dict:
        # Log files don't show numberof loops
            ltp_dict['loops'] = loop_no
    return (ltp_dict)

# %%
def parser_sched_latency(log_file : str) :
    sl_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                sl_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                sl_dict[loop_no] = {}
            elif iter := regex_iterations.match(line):
                sl_dict['iterations'] = iter.group(1)
            elif row := regex_stats.match(line):
                # Stats rows
                sl_dict[loop_no][row.group(1)] = row.group(2)
            elif quantiles := regex_quantil.match(line):
                # Quantiles rows
                sl_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            sys.stdout.write(line)
        if 'loops' not in sl_dict:
        # Log files don't show numberof loops
            sl_dict['loops'] = loop_no
    return (sl_dict)

# %%
def parser_sched_jitter(log_file : str) :
    sj_dict = {}
    loop_no = 0
    deltas = 1
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                sj_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                deltas = 1
                sj_dict[loop_no] = {}
                sj_dict[loop_no]['deltas'] = {}
            elif row := regex_deltas.match(line):
                # Deltas rows
                sj_dict[loop_no]['deltas'][deltas] = row.group(1)
                deltas +=1
            elif max_jitter := regex_stats.match(line):
                # Get max jitter
                sj_dict[loop_no][max_jitter.group(1)] = max_jitter.group(2)
            sys.stdout.write(line)
        if 'loops' not in sj_dict:
        # Log files don't show numberof loops
            sj_dict['loops'] = loop_no
    return (sj_dict)

# %%
def parser_prio_preempt(log_file : str) :
    pp_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                pp_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                pp_dict[loop_no] = {}
                pp_dict[loop_no]['threads'] = {}
            elif threads := regex_busy_threads.match(line):
                pp_dict[loop_no]['threads'][threads.group(1)] = threads.group(2)
            elif row := regex_multi_words2.match(line):
                # Threads info
                pp_dict[loop_no][row.group(1)] = row.group(2)
                #print('key :', row.group(1))
                #print('value:', row.group(2))
            sys.stdout.write(line)
        if 'loops' not in pp_dict:
        # Log files don't show numberof loops
            pp_dict['loops'] = loop_no
    return (pp_dict)

# %%
def parser_async_handler(log_file : str) :
    ah_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                ah_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                ah_dict[loop_no] = {}
            elif iter := regex_iterations.match(line):
                ah_dict['iterations'] = iter.group(1)
            elif row := regex_stats.match(line):
                # Stats rows
                ah_dict[loop_no][row.group(1)] = row.group(2)
            sys.stdout.write(line)
        if 'loops' not in ah_dict:
        # Log files don't show numberof loops
            ah_dict['loops'] = loop_no
    return (ah_dict)

# %%
def parser_async_handler_jk(log_file : str) :
    ahj_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                ahj_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                ahj_dict[loop_no] = {}
            elif row := regex_stats.match(line):
                # Stats rows
                ahj_dict[loop_no][row.group(1)] = row.group(2)
            elif delta := re.match(r'delta\s+=\s+(\d+\s+us)',line):
                ahj_dict[loop_no]['delta'] = delta.group(1)
            sys.stdout.write(line)
        if 'loops' not in ahj_dict:
        # Log files don't show numberof loops
            ahj_dict['loops'] = loop_no
    return (ahj_dict)



# %%
def parser_tc_2(log_file : str) :
    tc_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                tc_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                tc_dict[loop_no] = {}
            elif threads := regex_threads.match(line):
                tc_dict[loop_no][threads.group(2)] = threads.group(1)
            elif row := regex_stats.match(line):
                # Stats rows
                tc_dict[loop_no][row.group(1)] = row.group(2)
            sys.stdout.write(line)
        if 'loops' not in tc_dict:
        # Log files don't show numberof loops
            tc_dict['loops'] = loop_no
    return (tc_dict)

# %%
def parser_rt_migrate(log_file : str) :
    rt_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if re.match("^\|",line):
                pass
            elif loops := regex_loop.match(line):
                # Get number of loops
                rt_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                rt_dict[loop_no] = {}
                rt_dict[loop_no]['tasks'] = {}
            elif iters := re.match('Iter:\s+(.*)',line):
                # Iter entries
                rt_dict[loop_no]['iter'] = {}
                rt_dict[loop_no]['cpus'] = iters.group(1)
                for i in range(50):
                    rt_dict[loop_no]['iter'][i] = {}
                    for j in range(4):
                        line = next(fptr)
                        sys.stdout.write(line)
                        if row := regex_stats.match(line.strip()):
                            rt_dict[loop_no]['iter'][i][row.group(1)] = row.group(2) 
            elif tasks := regex_task.match(line):
                # Tasks block, read next 4 lines
                rt_dict[loop_no]['tasks'][tasks.group(1)] = {}
                rt_dict[loop_no]['tasks'][tasks.group(1)]['prio'] = tasks.group(2)
                rt_dict[loop_no]['tasks'][tasks.group(1)]['pid'] = tasks.group(3) 
                for i in range(4):
                    sys.stdout.write(line)
                    line = next(fptr)
                    row = regex_stats.match(line.strip())
                    rt_dict[loop_no]['tasks'][tasks.group(1)][row.group(1)] = row.group(2) 
            elif results := regex_single_word.match(line):
                rt_dict[loop_no][results.group(1)] = results.group(2)
            sys.stdout.write(line)
        if 'loops' not in rt_dict:
        # Log files don't show numberof loops
            rt_dict['loops'] = loop_no
    return (rt_dict)

# %%
def parser_prio_wake(log_file : str) :
    pw_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                pw_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                pw_dict[loop_no] = {}
                pw_dict[loop_no]['threads'] = {}
            elif threads := regex_thread_info.match(line):
                pw_dict[loop_no]['threads'][threads.group(1)] = {}
                pw_dict[loop_no]['threads'][threads.group(1)]['time'] = threads.group(2)
                pw_dict[loop_no]['threads'][threads.group(1)]['id'] = threads.group(3)
                pw_dict[loop_no]['threads'][threads.group(1)]['priority'] = threads.group(4)
                pw_dict[loop_no]['threads'][threads.group(1)]['status'] = threads.group(5)
            elif row := regex_multi_words2.match(line):
                 # Threads info -- need to optimize this regex
                 pw_dict[loop_no][row.group(1)] = row.group(2)
            sys.stdout.write(line)
        if 'loops' not in pw_dict:
        # Log files don't show numberof loops
            pw_dict['loops'] = loop_no
    return (pw_dict)

# %%
def parser_matrix_multi(log_file : str) :
    mm_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                mm_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                mm_dict[loop_no] = {}
            elif iter := regex_iterations.match(line):
                mm_dict[loop_no]['iterations'] = iter.group(1)  
            elif ops := re.match('Running\s+(\w+)\s+operations',line):
                # Operations info
                    mm_dict[loop_no][ops.group(1)] = {}
                    for i in range(4):
                        line = next(fptr)
                        sys.stdout.write(line)
                        if stats := regex_stats.match(line):
                            mm_dict[loop_no][ops.group(1)][stats.group(1)] = stats.group(2) 
            elif ops := re.match('Concurrent Multipliers:',line):
                # Grab stats under this title
                    mm_dict[loop_no]['Concurrent_multipliers'] = {}
                    for i in range(3):
                        line = next(fptr)
                        sys.stdout.write(line)
                        if stats := regex_stats.match(line):
                            mm_dict[loop_no]['Concurrent_multipliers'][stats.group(1)] = stats.group(2)   
            elif row := regex_multi_words2.match(line):
                #print("processing multi words",line)
                #print("key is",row.group(1))
                mm_dict[loop_no][row.group(1)] = row.group(2)            
            elif quantiles := regex_quantil.match(line):
                # Quantiles rows
                mm_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            sys.stdout.write(line)
        if 'loops' not in mm_dict:
        # Log files don't show numberof loops
            mm_dict['loops'] = loop_no
    return (mm_dict)

# %%
def parser_cpu_load(log_file : str) :
    cl_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                cl_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                cl_dict[loop_no] = {}
            elif iter := regex_iterations.match(line):
                cl_dict[loop_no]['iterations'] = iter.group(1)
            elif row := regex_stats.match(line.strip()):
                # Stats rows
                cl_dict[loop_no][row.group(1)] = row.group(2)
            elif quantiles := regex_quantil.match(line):
                # Quantiles rows
                cl_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            sys.stdout.write(line)
        if 'loops' not in cl_dict:
        # Log files don't show numberof loops
            cl_dict['loops'] = loop_no
    return (cl_dict)

# %%
def parser_pi_perf(log_file : str) :
    pp_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                pp_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                pp_dict[loop_no] = {}
                pp_dict[loop_no]['threads'] = {}
            elif threads := regex_thread_status.match(line):
                pp_dict[loop_no]['threads'][threads.group(1)] = threads.group(2)
            elif row := regex_stats2.match(line):
                # Threads info
                pp_dict[loop_no][row.group(1)] = row.group(2)
            elif quantiles := regex_quantil.match(line):
                # Quantiles rows
                pp_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            elif mrow := regex_multi_words2.match(line):
                pp_dict[loop_no][mrow.group(1)] = mrow.group(2)   
            sys.stdout.write(line)
        if 'loops' not in pp_dict:
        # Log files don't show numberof loops
            pp_dict['loops'] = loop_no
    return (pp_dict)

# %%
def parser_test_pi_0(log_file : str) :
    # Should parse each pi test
    pi_dict = {}
    loop_no = 0
    # Grab pi test to parse
    test = re.match(r"\w+-(\d+).log",log_file)                
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                pi_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                pi_dict[loop_no] = {}
            elif re.match(r"LIBC_VERSION:\s+\(*+)",line):
                pi_dict['LIBC_VERSION'] = re.match(r"LIBC_VERSION:\s+\(*+)",line)
            elif re.match(r"LIBPTHREAD_VERSION:\s+\(*+)",line):
                pi_dict['LIBPTHREAD_VERSION'] = re.match(r"LIBPTHREAD_VERSION:\s+\(*+)",line)    
            elif row := regex_stats.match(line):
                # Stats rows
                pi_dict[loop_no][row.group(1)] = row.group(2)
            sys.stdout.write(line)
        if 'loops' not in pi_dict:
        # Log files don't show numberof loops
            pi_dict['loops'] = loop_no
    return (pi_dict)

# %%
def parser_test_pi_1(log_file : str) :
    # Should parse each pi test
    pi_dict = {}
    loop_no = 0
    # Grab pi test to parse
    test = re.match(r"\w+-(\d+).log",log_file)                
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.match(line):
                # Get number of loops
                pi_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.match(line):
                # New test, need to increase loop count
                loop_no +=1
                pi_dict[loop_no] = {}
            elif threads := regex_threads.match(line):  
                # Expand thread info, add prio
                pi_dict[loop_no][threads.group(2)] = threads.group(1)
            elif row := regex_stats.match(line):
                # Stats rows
                pi_dict[loop_no][row.group(1)] = row.group(2)
            sys.stdout.write(line)
        if 'loops' not in pi_dict:
        # Log files don't show numberof loops
            pi_dict['loops'] = loop_no
    return (pi_dict)

# %%
def dict_to_csv(log_dict : dict) :
    print("Code to create csv files")

 
# %%
if __name__ == "__main__" :
  log_dir = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111124"
  print(" working on dir", log_dir)
  log_dict = {}
  for f in os.listdir(log_dir):
    log_file = os.path.join(log_dir, f)
    if os.path.isfile(log_file) and log_file.endswith(".log"):
      print(log_file)
      if fnmatch.fnmatch(log_file, '*pthread_kill_latency_c20*'):
        print("Processing pthread_kill_latency_c20")
        log_dict = parser_pthread_kill_latency(log_file)
      elif fnmatch.fnmatch(log_file, '*sched_latency-d1-t5-c100*'):
        print("Processing sched_latency-d1-t5-c100")
        log_dict = parser_sched_latency(log_file)
      elif fnmatch.fnmatch(log_file, '*sched_jitter*'):
        print("Processing sched_jitter")
        log_dict = parser_sched_jitter(log_file)
      elif fnmatch.fnmatch(log_file, '*prio-preempt-c1*'):
        print("Processing prio-preempt")
        log_dict = parser_prio_preempt(log_file)
      elif fnmatch.fnmatch(log_file, '*async_handler-c100*'):
        print("Processing async_handler-c100")
        log_dict = parser_async_handler(log_file)   
      elif fnmatch.fnmatch(log_file, '*async_handler_jk-c100*'):
        print("Processing async_handler_jk-c100")
        log_dict = parser_async_handler_jk(log_file)   
      elif fnmatch.fnmatch(log_file, '*tc-2-c0.5*'):
        print("Processing tc-2-c0.5")
        log_dict = parser_tc_2(log_file)      
      elif fnmatch.fnmatch(log_file, '*rt-migrate*'):
        print("Processing rt-migrate")
        log_dict = parser_rt_migrate(log_file)      
      elif fnmatch.fnmatch(log_file, '*prio-wake*'):
        print("Processing prio-wake")
        log_dict = parser_prio_wake(log_file)  
      elif fnmatch.fnmatch(log_file, '*gtod_latency*'):
        print("Processing gtod_latency")
        log_dict = parser_pthread_kill_latency(log_file)  
      elif fnmatch.fnmatch(log_file, '*matrix_mult-c0.75*'):
        print("Processing matrix_mult-c0.75")
        log_dict = parser_matrix_multi(log_file)  
      elif fnmatch.fnmatch(log_file, '*periodic_cpu_load_single*'):
        print("Processing periodic_cpu_load_single")
        log_dict = parser_cpu_load(log_file)    
      elif fnmatch.fnmatch(log_file, '*pi_perf-c200*'):
        print("Processing pi_perf-c200")
        log_dict = parser_pi_perf(log_file)    
      # elif fnmatch.fnmatch(log_file, '*testpi*'):
      #   print("Processing testpi tests")
      #   test = re.match(r"\w+-(\d+).log",log_file)                
      #   log_dict = parser_testpi_(log_file)      
      else:
        print("We have other file:", log_file)
      print(log_dict)
      print(yaml.dump(log_dict, default_flow_style=False))
     # dict_to_csv(log_dict)
      log_dict.clear()

 



