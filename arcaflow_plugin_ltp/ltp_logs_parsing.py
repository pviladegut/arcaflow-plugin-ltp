# %%
from typing import List , Dict
import re, sys, json, yaml

regex_stats = re.compile(r'(\S+):\s+(.+)')
regex_loop = re.compile(r'^\s+Running\s+(\d+)\s+runs')
regex_quantil = re.compile(r'(\d+\.\d+%)\s+([><]\s+\d+)')
regex_new_test = re.compile(r'--- Running testcase')
regex_date = re.compile(r'/\w+\s+\w+\s+\d+\s+\d{2}:\d{2}:\d{2}\s+\w+\s+\d{4}/gm')
regex_deltas = re.compile(r'delta:\s+(\d+)\s+ns')
regex_multi_words = re.compile(r'^(\w+(?:(\s*\w+)+)):\s+(.*)')

def parser_pthread_kill_latency(log_file : str) :
    ltp_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.search(line):
                # Get number of loops
                ltp_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.search(line):
                # New test, need to increase loop count
                loop_no +=1
                ltp_dict[loop_no] = {}
            elif row := regex_stats.search(line):
                # Stats rows
                ltp_dict[loop_no][row.group(1)] = row.group(2)
            elif quantiles := regex_quantil.search(line):
                # Quantiles rows
                ltp_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            sys.stdout.write(line)
    return (ltp_dict)

# %%
def parser_sched_latency(log_file : str) :
    sl_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.search(line):
                # Get number of loops
                sl_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.search(line):
                # New test, need to increase loop count
                loop_no +=1
                sl_dict[loop_no] = {}
            elif row := regex_stats.search(line):
                # Stats rows
                sl_dict[loop_no][row.group(1)] = row.group(2)
            elif quantiles := regex_quantil.search(line):
                # Quantiles rows
                sl_dict[loop_no][quantiles.group(1)] = quantiles.group(2)
            sys.stdout.write(line)
    return (sl_dict)

# %%
def parser_sched_jitter(log_file : str) :
    sj_dict = {}
    loop_no = 0
    deltas = 1
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.search(line):
                # Get number of loops
                sj_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.search(line):
                # New test, need to increase loop count
                loop_no +=1
                deltas = 1
                sj_dict[loop_no] = {}
                sj_dict[loop_no]['deltas'] = {}
            elif row := regex_deltas.search(line):
                # Deltas rows
                sj_dict[loop_no]['deltas'][deltas] = row.group(1)
                deltas +=1
            elif max_jitter := regex_stats.search(line):
                # Get max jitter
                sj_dict[loop_no][max_jitter.group(1)] = max_jitter.group(2)
            sys.stdout.write(line)
    return (sj_dict)

# %%
def parser_prio_preempt(log_file : str) :
    pp_dict = {}
    loop_no = 0
    with open(log_file , "r") as fptr :
        # loop through each line
        for line in fptr:
            if loops := regex_loop.search(line):
                # Get number of loops
                pp_dict['loops'] = loops.group(1)
            elif new_test := regex_new_test.search(line):
                # New test, need to increase loop count
                loop_no +=1
                pp_dict[loop_no] = {}
            elif row := regex_multi_words.search(line):
                # Threads info
                pp_dict[loop_no][row.group(1)] = row.group(2)
            sys.stdout.write(line)
    return (pp_dict)

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





