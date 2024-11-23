import uuid
def normalize_csv(csv_data):
        output = {
        str(uuid.uuid4()): {key.strip().replace(' ', '_'): value for key, value in item.items()} for item in csv_data
        }
        for i in output:
            output[i]["Status"] = "not_started"
        
        return output
    
    
