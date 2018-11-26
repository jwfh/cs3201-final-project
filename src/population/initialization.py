

def init_file(location: str):
    
    f = open(location, "r")
    
    file_str = f.readlines()
       
    a = []
 
    for line in file_str:
        a.append(line.strip(None).split()[1:])

    f.close()
    
    return a


