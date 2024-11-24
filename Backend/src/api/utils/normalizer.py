import uuid
def normalize_csv(csv_data):
        output = {
            (uid := str(uuid.uuid4())): {
                **{key.replace(' ', '_').lower(): value for key, value in item.items()},
                "id": uid,
                "status": "not_started"
            } for item in csv_data
        }
            
        

        # Define severity order
        severity_order = {'critical': 4, 'high': 3, 'medium': 2, 'low': 1, 'unknown': 0}
        
        # Sort by severity using custom order
        sorted_output = dict(sorted(
            output.items(),
            key=lambda x: severity_order.get(x[1].get('severity', '').lower(), -1),
            reverse=True
        ))
        # for i in sorted_output:
        #     print(sorted_output[i]["details"])
        
        return sorted_output
    
    
