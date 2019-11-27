import multiprocessing


def execute_gaia(params, sessionid):
    """thread worker function"""
    print('Session ID: ', sessionid, '-->', params)

    if 'xmin' in params:
        print(params['xmin'])

    # make a shared queue
    # pass the queue and params to #<num_procs> search workers (processes)
