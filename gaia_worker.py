import multiprocessing
import csv


def execute_gaia(params, sessionid):
    """thread worker function"""
    print('Session ID: ', sessionid, '-->', params)

    if 'xmin' in params:
        print(params['xmin'])

    num_procs = multiprocessing.cpu_count()
    print("launching", num_procs, "parallel search_gaia_db processes...")

    with open('gaiadr2-table.dat') as csvfile:
        dbCSV = csv.reader(csvfile, delimiter='|')
        entries = []
        for entry in dbCSV:
            entries.append(entry)
        print("PostgreSQL cluster database #entries:", len(entries))

    # make a shared queue
    # pass the queue and params to #<num_procs> search workers (processes)
