# %%
from typing import List , Dict
import re , sys , json , yaml

regex_stats = re.compile(r'(\S+):\s+(.+)')
regex_loop = re.compile(r'^\s+Running\s+(\d+)\s+runs')
regex_quantil = re.compile(r'(\d+\.\d+%)\s+([><]\s+\d+)')
regex_new_test = re.compile(r'--- Running testcase')
regex_date = re.compile(r'\w+\s+\w+\s+\d+\s+\d{2}:\d{2}:\d{2}\s+\w+\s+\d{4}')

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

if __name__ == "__main__" :
    log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111524/2024-11-15-pthread_kill_latency_c20.log"
    ltp_dict = parser_pthread_kill_latency(log_file)
    # print(json.dumps(ltp_dict, indent=4, sort_keys=True))
    print(ltp_dict)
    print(yaml.dump(ltp_dict, default_flow_style=False))
    log_file = "/home/pviladeg/Documents/Projects/RHIVOS/LTP/realtime_tests/tests_111524/2024-11-15-sched_latency-d1-t5-c100.log"
    sl_dict = parser_sched_latency(log_file)
    print(sl_dict)
    print(yaml.dump(sl_dict, default_flow_style=False))



