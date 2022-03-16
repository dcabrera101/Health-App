import json

def ingest_data(file):
    # open file
    try:
        data = json.load(file)
    except:
        return False, 'IS NOT JSON'
    
    # check required data fields
    if type(data.get('Patient ID',False)) != int:
        return False, 'Missing/Invalid Required Field'
    
    # validate readings
    fields = list(data.keys())
    if len(fields) > 7:
        return False, "Unexpected Field(s)"
    fields.remove("Patient ID")
    for field in fields:
        print(field)
        if field == 'Temperature':
            temp = data.get(field,False)
            if temp:
                if type(temp) != float:
                    return False, 'Invalid Reading(s)'
        elif field == 'Blood Pressure':
            bp = data.get(field)
            try:
                if len(bp) != 2: 
                    return False, "Invalid Reading(s)"
                for p in bp:
                    if type(p) != int:
                        return False, 'Invalid Reading(s)'
            except:
                return False, 'Invalid Reading(s)'
        elif field == 'Pulse':
            pulse = data.get(field,False)
            if pulse:
                if type(pulse) != int:
                    return False, 'Invalid Reading(s)'
        elif field == 'Oximeter':
            oxi = data.get(field,False)
            if oxi:
                if type(pulse) != int:
                    return False,'Invalid Reading(s)'
        elif field == 'Weight':
            weight = data.get(field,False)
            if weight:
                if type(weight) != float:
                    return False,'Invalid Reading(s)'
        elif field == "Glucometer":
            gluco = data.get(field,False)
            if gluco:
                if type(gluco) != int:
                    return False,'Invalid Reading(s)'
        else:
            return False, "Unexpected Field(s)"
    
    return True, None
    
    
    

