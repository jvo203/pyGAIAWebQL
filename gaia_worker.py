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

        for pid in range(num_procs):
            search = multiprocessing.Process(
                target=search_gaia_db, args=(params, pid, num_procs, entries))
            search.start()

        # process the results from the shared queue


def search_gaia_db(params, pid, step, entries):
    print("search_gaia_db process id", pid)

    for index in range(pid, len(entries), step):
        entry = entries[index]
        conn_str = "dbname=gaiadr2 host=" + \
            entry[4] + " port=" + entry[5] + " user=" + \
            entry[3] + " password=" + entry[3] + "!"

        print("pid:", pid, "index:", index, conn_str)
