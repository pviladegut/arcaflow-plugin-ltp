# %%
from typing import List , Dict
import re, sys, json, yaml

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
            elif row := regex_multi_words.match(line):
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
if __name__ == "__main__" :
  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111524/2024-11-15-pthread_kill_latency_c20.log"
  ltp_dict = parser_pthread_kill_latency(log_file)
  print(ltp_dict)
  print(yaml.dump(ltp_dict, default_flow_style=False))
  
  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111524/2024-11-15-sched_latency-d1-t5-c100.log"
  sl_dict = parser_sched_latency(log_file)
  print(sl_dict)
  print(yaml.dump(sl_dict, default_flow_style=False))

  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111524/2024-11-15-sched_jitter.log"
  sj_dict = parser_sched_jitter(log_file)
  print(sj_dict)
  print(yaml.dump(sj_dict, default_flow_style=False))

  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111124/localhost-aarch64-5.14.0-501.451.el9iv.aarch64+debug-2024-11-11-prio-preempt-c1.log"
  pp_dict = parser_prio_preempt(log_file)
  print(pp_dict)
  print(yaml.dump(pp_dict, default_flow_style=False))

  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111124/localhost-aarch64-5.14.0-501.451.el9iv.aarch64+debug-2024-11-11-async_handler-c100.log"
  ah_dict = parser_async_handler(log_file)
  print(ah_dict)
  print(yaml.dump(ah_dict, default_flow_style=False))

  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111124/localhost-aarch64-5.14.0-501.451.el9iv.aarch64+debug-2024-11-11-async_handler_jk-c100.log"
  ahj_dict = parser_async_handler_jk(log_file)
  print(ahj_dict)
  print(yaml.dump(ahj_dict, default_flow_style=False))

  log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111124/localhost-aarch64-5.14.0-501.451.el9iv.aarch64+debug-2024-11-11-tc-2-c0.5.log"
  tc_dict = parser_tc_2(log_file)
  print(tc_dict)
  print(yaml.dump(tc_dict, default_flow_style=False))



