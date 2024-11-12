#!/usr/bin/env python3

import typing
from dataclasses import dataclass
from arcaflow_plugin_sdk import plugin, schema, validation,annotations

validation_warning = (
    " NOTE: Input not validated by the plugin --"
    " Any errors are likely to be produced at the end of the plugin run and"
    " may result in workflow failures."
)

class TestArguments(str, enum.Enum):
    FUNC = "func"
    STRESS = "stress"
    PERF = "perf"
    ALL = "all"
    LIST = "list"
    CLEAN = "clean"
    TEST_NAME = "test_name"

class TestsList(str,enum.Enum):
    PI-TESTS = "pi-tests"
    PI_PERF  = "pi_perf"
    PRIO-WAKE  = "prio-wake"
    SCHED_JITTER  = "sched_jitter"
    GTOD_LATENCY  = "gtod_latency"
    PERIODIC_CPU_LOAD  = "periodic_cpu_load"
    PTHREAD_KILL_LATENCY  = "pthread_kill_latency"
    SCHED_LATENCY  = "sched_latency"
    MATRIX_MULT  = "matrix_mult"
    THREAD_CLOCK  = "thread_clock"
    PRIO-PREEMPT  = "prio-preempt"
    RT-MIGRATE  = "rt-migrate"
    ASYNC_HANDLER  = "async_handler"
    LATENCY  = "latency"

testslist_schemas = {}

@dataclass
class LtpGlobalParams:
    test_argument: typing.Annotated[
        TestArguments,
        schema.name("Test Argument"),
        schema.description("Operation to be performed; options are run a test(s), list of tests and clean logs"),
    ]
    loop: typing.Annotated[
        int,
        schema.name("Loops"),
        schema.description(
            "Number of iterations"
        ),
    ] = 1

@dataclass
class LatencyStats:
    """
    This is the latency output data structure for tests measuring latencies
    """
    min_latency: typing.Annotated[
        float,
        schema.name("minumum latency"),
        schema.description("Minimum latency"),
    ] = None
    max_latency: typing.Annotated[
        float,
        schema.name("maximum latency"),
        schema.description("Maximum latency"),
    ] = None    
    avg_latency: typing.Annotated[
        float,
        schema.name("average latency"),
        schema.description("Average latency"),
    ] = None    
    std_dev: typing.Annotated[
        typing.Optional(float),
        schema.name("standard deviation"),
        schema.description("Standard deviation, optional value"),    
    ] = None   

@dataclass
class AsyncHandlerC100Output:
    """
    This is the output data structure for the Asynchronous event handler test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    latencyStats: typing.Annotated[
        LatencyStats,
        schema.name("latency statistics"),
        schema.description("Latencies and std deviation, measured in us"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Latency criteria to determine pass/fail"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail, depending if average latency is < 100 us"),
    ] = None    
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 

testslist_schemas[TestList.ASYNC_HANDLER] = plugin.build_object_schema(AsyncHandlerC100Output)

@dataclass
class AsyncHandlerJkC100Output:
    """
    This is the output data structure for the Asynchronous event handler in a real-time JVM test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    delta: typing.Annotated[
        float,
        schema.name("delta latency"),
        schema.description("Delta latency of an async event server thread, measured in us"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Latency criteria to determine pass/fail"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail, depending if average latency is < 100 us"),
    ] = None    
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.ASYNC_HANDLER] = plugin.build_object_schema(AsyncHandlerJkC100Output)

@dataclass
class GtodLatencyOutput:
    """
    This is the output data structure for the get-time-of-the-day latency test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    latencyStats: typing.Annotated[
        LatencyStats,
        schema.name("latency statistics"),
        schema.description("Latencies and std deviation, measured in ns"),
    ] = None
    quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values"),
        schema.description("List of latency percentiles"),
    ] = None
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.GTOD_LATENCY] = plugin.build_object_schema(GtodLatencyOutput)

@dataclass
class MatrixMultC0_75Output:
    """
    This is the output data structure for the Matrix multiplication test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    matrix_dim: typing.Annotated[
        str,
        schema.name("matrix dimentions"),
        schema.description("Matrix dimentions, default 100x100"),
    ] = None
    num_cpus: typing.Annotated[
        int,
        schema.name("number of CPUs"),
        schema.description("Number of CPUs"),
    ] = None
    seq_oper_latencies: typing.Annotated[
        LatencyStats,
        schema.name("sequential operations"),
        schema.description("Sequential matrix multiplication routines latencies and std dev"),
    ] = None
    par_oper_latencies: typing.Annotated[
        LatencyStats,
        schema.name("parallel operations"),
        schema.description("Parallel matrix multiplication routines latencies and std dev"),
    ] = None
    conc_multi_latencies: typing.Annotated[
        LatencyStats,
        schema.name("concurrent multipliers"),
        schema.description("Concurrent multipliers latencies"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Latency criteria to determine pass/fail"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail, depending on average latency < 100 us"),
    ] = None    
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.MATRIX_MULT] = plugin.build_object_schema(MatrixMultC0_75Output)

@dataclass
class PeriodicCpuLoadOutput:
    """
    This is the output data structure for the periodic cpu load test.
    """
   test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    thread_groupA: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("thread group A"),
        schema.description("Thread information for group A"),
    ] = None
    thread_groupB: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("thread group B"),
        schema.description("Thread information for group B"),
    ] = None
    thread_groupC: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("thread group C"),
        schema.description("Thread information for group C"),
    ] = None        
    threads_completed: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("threads list"),
        schema.description("List of threads from all groups that completed"),
    ] = None
    groupA stats: typing.Annotated[
        LatencyStats,
        schema.name("thread group A stats"),
        schema.description("Thread group A latency and std dev statistics"),
    ] = None
    groupA_quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values group A"),
        schema.description("Group A list of latency percentiles"),
    ] = None
    groupB stats: typing.Annotated[
        LatencyStats,
        schema.name("thread group B stats"),
        schema.description("Thread group B latency and std dev statistics"),
    ] = None
    groupB_quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values group B"),
        schema.description("Group B list of latency percentiles"),
    ] = None    
    groupC stats: typing.Annotated[
        LatencyStats,
        schema.name("thread group C stats"),
        schema.description("Thread group C latency and std dev statistics"),
    ] = None
    groupC_quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values group C"),
        schema.description("Group C list of latency percentiles"),
    ] = None    
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PERIODIC_CPU_LOAD] = plugin.build_object_schema(PeriodicCpuLoadOutput)

@dataclass
class PeriodicCpuLoadSingleOutput:
    """
    This is the output data structure for the periodic cpu load single test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    priority: typing.Annotated[
        int,
        schema.name("thread priority"),
        schema.description("Thread priority"),
    ] = None
    period: typing.Annotated[
        int,
        schema.name("thread period"),
        schema.description("Thread period time in ms"),
    ] = None
    logs: typing.Annotated[
        str,
        schema.name("logs name"),
        schema.description("Logs names"),
    ] = None
    num_worker_threads: typing.Annotated[
        str,
        schema.name("number of worker threads"),
        schema.description("Total number of worker threads, by default, is equal to number of CPUS"),
    ] = None
    latencyStats: typing.Annotated[
        LatencyStats,
        schema.name("latency stats"),
        schema.description("Latency and std dev statistics in us"),
    ] = None
    quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values"),
        schema.description("List of latency percentiles"),
    ] = None  
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Latency criteria to determine pass/fail"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None           
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PERIODIC_CPU_LOAD] = plugin.build_object_schema(PeriodicCpuLoadSingleOutput)

 @dataclass
class PiPerfC200Output:
    """
    This is the output data structure for the pi performance test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    busy_threads_list: typing.Annotated[
        typing.List[typing.Dict[str, str]],
        schema.name("list of busy threads"),
        schema.description("List of busy threads status"),
    ] = None
    min_delay: typing.Annotated[
        float,
        schema.name("min delay"),
        schema.description("Minimum delay taken for high prio thread to get the lock, measured in us"),
    ] = None
    max_delay: typing.Annotated[
        float,
        schema.name("max delay"),
        schema.description("Maximum delay taken for high prio thread to get the lock, measured in us"),
    ] = None
    avg_delay: typing.Annotated[
        float,
        schema.name("avg delay"),
        schema.description("Average delay taken for high prio thread to get the lock, measured in us"),
    ] = None
    std_dev: typing.Annotated[
        float,
        schema.name("std deviation"),
        schema.description("Standard deviation, measured in us"),
    ] = None
    quantiles_99_0: typing.Annotated[
        float,
        schema.name("Quantiles 99pct"),
        schema.description("Quantiles, 99.0%"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Lock wait time criteria to determine pass/fail. High prio thread < low prio thread"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None    
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI_PERF] = plugin.build_object_schema(PiPerfC200Output)

@dataclass
class PrioPreemptC1Output:
    """
    This is the output data structure for the priority preemption test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    worker_threads: typing.Annotated[
        int,
        schema.name("worker threads"),
        schema.description("Number of worker threads. "),
    ] = None
    busy_threads: typing.Annotated[
        int,
        schema.name("busy threads"),
        schema.description("Number of busy threads.By default, the number of threads is equal to number of CPUs"),
    ] = None
    busy_threads_list: typing.Annotated[
        typing.List[typing.Dict[str, str]],
        schema.name("list of busy threads"),
        schema.description("List of busy threads status"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Threads preempted criteria to determine pass/fail"),
    ] = None    
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail, depending of threads preempted within one loop(s)"),
    ] = None
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PRIO-PREEMPT] = plugin.build_object_schema(PrioPreemptC1Output)

 @dataclass
class PrioWakeOutput:   
   """
    This is the output data structure for the prio-wake test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    worker_thread: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("worker thread"),
        schema.description("Worker threads. By default, the number of threads is equal to number of CPUs"),
    ] = None
    thread_time: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("thread time"),
        schema.description("Time the thread starts or wakes up"),
    ] = None
    thread_name: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("thread name"),
        schema.description("Thread id"),
    ] = None
    thread_prio: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("thread priority"),
        schema.description("Thread priority, each worker thread is created with increasing FIFO priorities"),
    ] = None
     thread_status: typing.Annotated[
        typing.List[typing.Dict[str, str]],
        schema.name("thread status"),
        schema.description("Thread status, possible values are started or awake"),
    ] = None
    num_worker_threads: typing.Annotated[
        str,
        schema.name("number of worker threads"),
        schema.description("Total number of worker threads, by default, is equal to number of CPUS"),
    ] = None
    threads_order: typing.Annotated[
        typing.List[typing.Dict[str, str]],
        schema.name("thread wake up order"),
        schema.description("List of threads that woke up in incorrect order"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail, depending if threads woke up in correct order or not"),
    ] = None
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PRIO-WAKE] = plugin.build_object_schema(PrioWakeOutput)

 @dataclass
class PthreadCondManyOutput:
  """
    This is the output data structure for the pthread_cond_many test.
    """
    num_threads: typing.Annotated[
        int,
        schema.name("number of threads"),
        schema.description("Number of threads running together"),
    ] = None
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    num_proc: typing.Annotated[
        int,
        schema.name("number of processes"),
        schema.description("Number of processes running together"),
    ] = None
testslist_schemas[TestList.LATENCY] = plugin.build_object_schema(PthreadCondManyOutput)

@dataclass
class PthreadKillLatencyC20Output:
    """
    This is the output data structure for the kill latency test.
    """
   test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations"),
    ] = None
    latencyStats: typing.Annotated[
        LatencyStats,
        schema.name("latency stats"),
        schema.description("Latency and std dev statistics in us"),
    ] = None
    quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values"),
        schema.description("List of latency percentiles"),
    ] = None  
    failures: typing.Annotated[
        int,
        schema.name("number of failures"),
        schema.description("Number of failures"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Minimum latency criteria to determine pass/fail, the default is < 20"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None           
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PTHREAD_KILL_LATENCY] = plugin.build_object_schema(PthreadKillLatencyC20Output)

 @dataclass
class RtMigrageOutput:
    """
    This is the output data structure for the success case.
    """

    message: str
testslist_schemas[TestList.RT-MIGRATE] = plugin.build_object_schema(RtMigrageOutput)

@dataclass
class SbrkMutexOutput:
    """
    This is the output data structure for the sbrk_mutex test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    mutexes: typing.Annotated[
        int,
        schema.name("number of mutexes"),
        schema.description("Number of mutexes allocated "),
    ] = None
    mutexes_info: typing.Annotated[
        str,
        schema.name("mutexes info"),
        schema.description("Information about the mutexes status"),
    ] = None
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(SbrkMutexOutput)

@dataclass
class SchedJitterOutput:
    """
    This is the output data structure for the scheduling jitter
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    jitter_deltas: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("list of deltas"),
        schema.description("List of scheduling jitter deltas"),
    ] = None
    max_jitter: typing.Annotated[
        float,
        schema.name("maximum delta"),
        schema.description("Maximum jitter delta, measured in us"),
    ] = None
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.SCHED_JITTER] = plugin.build_object_schema(SchedJitterOutput)

@dataclass
class SchedLatencyD1T5C100Output:
    """
    This is the output data structure for the scheduling latency.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    num_iter: typing.Annotated[
        int,
        schema.name("number of iterations"),
        schema.description("Number of iterations with a period of 5 ms"),
    ] = None
    periodic_load_dur: typing.Annotated[
        int,
        schema.name("periodic duration"),
        schema.description("Periodic load duration in ms"),
    ] = None
    latencyStats: typing.Annotated[
        LatencyStats,
        schema.name("latency stats"),
        schema.description("Latency and std dev statistics in us"),
    ] = None
    quantiles: typing.Annotated[
        typing.List[typing.Dict[str, int]],
        schema.name("quantiles values"),
        schema.description("List of latency percentiles"),
    ] = None  
    failed_iter: typing.Annotated[
        int,
        schema.name("failed iterations"),
        schema.description("Number of failed iterations"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Latency criteria to determine pass/fail, default of < 100 us"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None           
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.SCHED_LATENCY] = plugin.build_object_schema(SchedLatencyD1T5C100Output)

@dataclass
class Tc2C0_5Output:
    """
    This is the output data structure for the clock_gettime.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    sleeper_threads: typing.Annotated[
        int,
        schema.name("sleeper threads"),
        schema.description("Number of sleeper threads created"),
    ] = None
    worker_threads: typing.Annotated[
        int,
        schema.name("worker threads"),
        schema.description("Number of worker threads created"),
    ] = None    
    worker_threads_time: typing.Annotated[
        float,
        schema.name("worker threads time"),
        schema.description("Sum time of worker threads, in sec"),
    ] = None
    sleeper_threads_time: typing.Annotated[
        float,
        schema.name("sleeper threads time"),
        schema.description("Sum time of sleeper threads, in sec"),
    ] = None
    delta_time: typing.Annotated[
        float,
        schema.name("delta time"),
        schema.description("Delta of worker and sleeper times, in sec"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Delta criteria to determine pass/fail"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None   
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.THREAD_CLOCK] = plugin.build_object_schema(Tc2C0_5Output)

@dataclass
class TestPi0Output:
    """
    This is the output data structure for the testpi-0 test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    libc_version: typing.Annotated[
        str,
        schema.name("libc version"),
        schema.description("LIBC_VERSION, to verify if priority inheritance feature is present in kernel "),
    ] = None
    libpthread_version: typing.Annotated[
        str,
        schema.name("libpthread version"),
        schema.description("LIBPTHREAD_VERSION, to verify if priority inheritance feature is present in kernel "),
    ] = None
    prio_inheritance: typing.Annotated[
        str,
        schema.name("prio-inheritance info"),
        schema.description("Information about weather priority inheritance feature is present in kernel"),
    ] = None
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(TestPi0Output)

@dataclass
class TestPi1Output:
    """
    This is the output data structure for the testpi-1 test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    threads_list: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("threads list"),
        schema.description("List of threads created with different priorities and other information"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Low Priority Thread should Preempt Higher Priority Noise Thread"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None              
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(TestPi1Output)

@dataclass
class TestPi2Output:
    """
    This is the output data structure for the testpi-2 test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    threads_list: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("threads list"),
        schema.description("List of threads created with different priorities and other information"),
    ] = None
    criteria: typing.Annotated[
        str,
        schema.name("criteria for pass/fail"),
        schema.description("Low Priority Thread and High Priority Thread should prempt each other multiple times"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None              
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(TestPi2Output)

@dataclass
class TestPi4Output:
    """
    This is the output data structure for the testpi-4 test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    threads_list: typing.Annotated[
        typing.List[typing.Dict[str, typing.Any]],
        schema.name("threads list"),
        schema.description("List of threads created with different priorities and other information"),
    ] = None
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail. No criteria output set for this test"),
    ] = None              
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(TestPi4Output)

@dataclass
class TestPi5Output:
    """
    This is the output data structure for the testpi-5 test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(TestPi5Output)

@dataclass
class TestPi6Output:
    """
    This is the output data structure for the testpi-6 test.
    """
    test_start_date: typing.Annotated[
        str,
        schema.name("Test start date and time"),
        schema.description("Date and time test started"),
    ] = None 
    test_result: typing.Annotated[
        str,
        schema.name("test result"),
        schema.description("Test result, pass or fail"),
    ] = None       
    test_end_date: typing.Annotated[
        str,
        schema.name("Test end date and time"),
        schema.description("Date and time test ended"),
    ] = None 
testslist_schemas[TestList.PI-TESTS] = plugin.build_object_schema(TestPi6Output)

@dataclass
class TestResults:
    test_config: typing.Annotated[
        TestArguments,
        schema.name("Test arguments"),
        schema.description("The LTP realtime tests parameters"),
    ]
    pi-tests_output: typing.Annotated[
        typing.Optional[SbrkMutexOutput],
        schema.name("SbrkMutexOutput Output"),
        schema.description("SbrkMutexOutput output object"),
    ] = None
    pi_perf_output: typing.Annotated[
        typing.Optional[PiPerfC200Output],
        schema.name("PiPerfC200Output Output"),
        schema.description("PiPerfC200Output output object"),
    ] = None
    prio-wake_output: typing.Annotated[
        typing.Optional[PrioWakeOutput],
        schema.name("PrioWakeOutput Output"),
        schema.description("PrioWakeOutput output object"),
    ] = None
    sched_jitter_output: typing.Annotated[
        typing.Optional[SchedJitterOutput],
        schema.name("SchedJitterOutput Output"),
        schema.description("SchedJitterOutput output object"),
    ] = None
    gtod_latency_output: typing.Annotated[
        typing.Optional[GtodLatencyOutput],
        schema.name("GtodLatencyOutput Output"),
        schema.description(" output object"),
    ] = None
    periodic_cpu_load: typing.Annotated[
        typing.Optional[PeriodicCpuLoadOutput],
        schema.name("PeriodicCpuLoadOutput Output"),
        schema.description("PeriodicCpuLoadOutput output object"),
    ] = None
    pthread_kill_latency_output: typing.Annotated[
        typing.Optional[PthreadKillLatencyC20Output],
        schema.name("PthreadKillLatencyC20Output Output"),
        schema.description("PthreadKillLatencyC20Output output object"),
    ] = None
    sched_latency_output: typing.Annotated[
        typing.Optional[SchedLatencyD1T5C100Output],
        schema.name("SchedLatencyD1T5C100Output Output"),
        schema.description("SchedLatencyD1T5C100Output output object"),
    ] = None
    matrix_mult_output: typing.Annotated[
        typing.Optional[MatrixMultC0_75Output],
        schema.name("MatrixMultC0_75Output Output"),
        schema.description(" output object"),
    ] = None
    thread_clock_output: typing.Annotated[
        typing.Optional[Tc2C0_5Output],
        schema.name("Tc2C0_5Output Output"),
        schema.description("Tc2C0_5Output output object"),
    ] = None
    prio-preempt_output: typing.Annotated[
        typing.Optional[PrioPreemptC1Output],
        schema.name("PrioPreemptC1Output Output"),
        schema.description("PrioPreemptC1Output output object"),
    ] = None
    rt-migrate_output: typing.Annotated[
        typing.Optional[RtMigrageOutput],
        schema.name("RtMigrageOutput Output"),
        schema.description("RtMigrageOutput output object"),
    ] = None
    async_handler_output: typing.Annotated[
        typing.Optional[AsyncHandlerC100Output],
        schema.name("AsyncHandlerC100Output Output"),
        schema.description(" output object"),
    ] = None
    latency_output: typing.Annotated[
        typing.Optional[PthreadCondManyOutput],
        schema.name("PthreadCondManyOutput Output"),
        schema.description("PthreadCondManyOutput output object"),
    ] = None

@dataclass
class TestError:
    error: str
