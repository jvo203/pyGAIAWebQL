def execute_gaia(params, sessionid):    
    """thread worker function"""    
    print('Session ID: ', sessionid, '-->', params)
    
    if 'xmin' in params:
        print(params['xmin'])
