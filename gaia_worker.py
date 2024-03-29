import multiprocessing
import csv
import psycopg2

import math
import astropy.coordinates as coord
import astropy.units as u


def execute_gaia(params, datasetid):
    """thread worker function"""
    print('Session ID: ', datasetid, '-->', params)

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
        reader = multiprocessing.Process(target=process_queue, args=(res,))
        reader.start()

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

        res.put('DONE')
        reader.join()

    print("execute_gaia::" + str(datasetid) + " finished.")


def search_gaia_db(params, pid, step, entries, queue):
    #print("search_gaia_db process id", pid)

    for index in range(pid, len(entries), step):
        entry = entries[index]

        try:
            conn = psycopg2.connect(user=entry[3],
                                    password=entry[3]+"!",
                                    host=entry[4],
                                    port=entry[5],
                                    database="gaiadr2")

            cursor = conn.cursor()
            #print("PostgreSQL connection successful.")

            sql = "select count(*) from " + \
                entry[0] + "." + entry[1] + \
                " where parallax > 0 and ra is not null and dec is not null and phot_g_mean_mag is not null and bp_rp is not null and pmra is not null and pmdec is not null and radial_velocity is not null"
            sql2 = "select ra,dec,phot_g_mean_mag,bp_rp,parallax,pmra,pmdec,radial_velocity from " + \
                entry[0] + "." + entry[1] + \
                " where parallax > 0 and ra is not null and dec is not null and phot_g_mean_mag is not null and bp_rp is not null and pmra is not null and pmdec is not null and radial_velocity is not null"

            # where
            if 'where' in params:
                where = params['where']
                if where:
                    sql += " and " + where[0]
                    sql2 += " and " + where[0]

            # parallax_over_error
            if 'parallax_over_error' in params:
                parallax = params['parallax_over_error']
                if parallax:
                    sql += " and parallax_over_error > " + parallax[0]
                    sql2 += " and parallax_over_error > " + parallax[0]

            # finish the sql
            sql += ";"
            sql2 += ";"
            #sql += " limit 1;"
            #sql2 += " limit 1;"

            # print(sql)
            cursor.execute(sql)
            no_records = cursor.fetchone()[0]
            #print("SQL(" + sql + ") - " + str(no_records) + "\n")

            cursor.execute(sql2)
            records = cursor.fetchall()
            for row in records:
                # print(record)
                valid = True
                try:
                    ra = float(row[0])
                    dec = float(row[1])
                    phot_g_mean_mag = float(row[2])
                    bp_rp = float(row[3])
                    parallax = float(row[4])
                    pmra = float(row[5])
                    pmdec = float(row[6])
                    radial_velocity = float(row[7])
                except ValueError:
                    valid = False

                if valid:
                    M_G = phot_g_mean_mag + 5.0 + \
                        5.0 * math.log10(parallax / 1000.0)
                    distance = 1000.0 / parallax  # distance[parsec, pc]

                    orig = coord.ICRS(ra=ra*u.degree, dec=dec*u.degree,
                                      distance=(distance*u.mas).to(u.pc,
                                                                   u.parallax()),
                                      pm_ra_cosdec=pmra*u.mas/u.yr,
                                      pm_dec=pmdec*u.mas/u.yr,
                                      radial_velocity=radial_velocity*u.km/u.s)

                    gc = orig.transform_to(coord.Galactocentric)

                    X = gc.x.value  # [pc]
                    Y = gc.y.value  # [pc]
                    Z = gc.z.value  # [pc]

                    Vx = gc.v_x.value  # [km/s]
                    Vy = gc.v_y.value  # [km/s]
                    Vz = gc.v_z.value  # [km/s]

                    gc.representation_type = 'cylindrical'

                    R = gc.rho.value  # [pc]
                    Phi = gc.phi.value  # [deg]

                    # a final user validation
                    try:
                        if 'xmin' in params:
                            xmin = params['xmin']
                            if xmin:
                                if X < 1000 * float(xmin[0]):
                                    valid = False

                        if 'xmax' in params:
                            xmax = params['xmax']
                            if xmax:
                                if X > 1000 * float(xmax[0]):
                                    valid = False

                        if 'ymin' in params:
                            ymin = params['ymin']
                            if ymin:
                                if Y < 1000 * float(ymin[0]):
                                    valid = False

                        if 'ymax' in params:
                            ymax = params['ymax']
                            if ymax:
                                if Y > 1000 * float(ymax[0]):
                                    valid = False

                        if 'zmin' in params:
                            zmin = params['zmin']
                            if zmin:
                                if Z < 1000 * float(zmin[0]):
                                    valid = False

                        if 'zmax' in params:
                            zmax = params['zmax']
                            if zmax:
                                if Z > 1000 * float(zmax[0]):
                                    valid = False

                        if 'rmin' in params:
                            rmin = params['rmin']
                            if rmin:
                                if R < 1000 * float(rmin[0]):
                                    valid = False

                        if 'rmax' in params:
                            rmax = params['rmax']
                            if rmax:
                                if R > 1000 * float(rmax[0]):
                                    valid = False

                        if 'phimin' in params:
                            phimin = params['phimin']
                            if phimin:
                                if Phi < 1000 * float(phimin[0]):
                                    valid = False

                        if 'phimax' in params:
                            phimax = params['phimax']
                            if phimax:
                                if Phi > 1000 * float(phimax[0]):
                                    valid = False

                        if 'mgmin' in params:
                            mgmin = params['mgmin']
                            if mgmin:
                                if M_G < 1000 * float(mgmin[0]):
                                    valid = False

                        if 'mgmax' in params:
                            mgmax = params['mgmax']
                            if mgmax:
                                if M_G > 1000 * float(mgmax[0]):
                                    valid = False

                    except ValueError:
                        valid = False

                    if valid:
                        queue.put((bp_rp, M_G, X, Y, Z, Vx, Vy, Vz, R, Phi))

        except (Exception, psycopg2.Error) as error:
            print("Error while connecting to PostgreSQL", error)
        finally:
            # closing database connection.
            if(conn):
                cursor.close()
                conn.close()
                #print("PostgreSQL connection is closed.")

        #print("pid:", pid, "index:", index, "done;\n")


def process_queue(queue):
    # Read from the queue; this will be spawned as a separate Process
    while True:
        msg = queue.get()         # Read from the queue and do nothing
        if (msg == 'DONE'):
            break
        else:
            print("queue -", msg)
