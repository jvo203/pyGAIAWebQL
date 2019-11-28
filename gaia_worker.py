import multiprocessing
import csv
import psycopg2


def execute_gaia(params, datasetid):
    """thread worker function"""
    print('Session ID: ', datasetid, '-->', params)

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
        res = multiprocessing.Queue()

        # pass the queue and params to #<num_procs> search workers (processes)
        jobs = []
        for pid in range(num_procs):
            search = multiprocessing.Process(
                target=search_gaia_db, args=(params, pid, num_procs, entries, res))
            jobs.append(search)
            search.start()

        # process the results from the shared queue

        # wait for all processes to end
        for job in jobs:
            job.join()

    print("execute_gaia::" + str(datasetid) + " finished.")

def search_gaia_db(params, pid, step, entries, queue):
    print("search_gaia_db process id", pid)

    for index in range(pid, len(entries), step):
        entry = entries[index]

        try:
            conn = psycopg2.connect(user=entry[3],
                                    password=entry[3]+"!",
                                    host=entry[4],
                                    port=entry[5],
                                    database="gaiadr2")

            cursor = conn.cursor()
            # Print PostgreSQL Connection properties
            #print(conn.get_dsn_parameters(), "\n")

            # Print PostgreSQL version
            #cursor.execute("SELECT version();")
            #record = cursor.fetchone()
            #print("You are connected to - ", record, "\n")
            print("PostgreSQL connection successful.")

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if(conn):
                cursor.close()
                conn.close()
                print("PostgreSQL connection is closed.")

        print("pid:", pid, "index:", index, "done;\n")


def writer(count, queue):
    # Write to the queue
    for ii in range(0, count):
        queue.put(ii)             # Write 'count' numbers into the queue
    queue.put('DONE')


def process_queue(queue):
    # Read from the queue; this will be spawned as a separate Process
    while True:
        msg = queue.get()         # Read from the queue and do nothing
        if (msg == 'DONE'):
            break
