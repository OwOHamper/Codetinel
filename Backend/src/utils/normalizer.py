import uuid
def normalize_csv(csv_data):
        return {
        str(uuid.uuid4()): {key.strip().replace(' ', '_'): value for key, value in item.items()} for item in csv_data 
        }
    
    
