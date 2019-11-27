def execute_gaia(params):    
    """thread worker function"""    
    print('Worker:', params)
    
    if 'xmin' in params:
        print(params['xmin'])
