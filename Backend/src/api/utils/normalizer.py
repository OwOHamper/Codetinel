import uuid


def get_file(file_context):
    if not file_context:
        return ""
        
    if isinstance(file_context, dict):
        # If it's already a dictionary, just get the file path
        file_path = file_context.get('file')
        start_line = file_context.get('start_line')
    else:
        try:
            # Try to evaluate the string as a Python dict
            # This handles the Ruby-style hash syntax
            file_context = file_context.replace('=>', ':')
            file_context_dict = eval(file_context)
            
            file_path = file_context_dict.get('file')
            start_line = file_context_dict.get('start_line')
            
        except Exception as e:
            print(f"Error parsing file context: {str(e)}")
            return ""

    if file_path and start_line:
        if 'end_line' in file_context_dict:
            end_line = file_context_dict['end_line']
            return f"{file_path}:{start_line}-{end_line}"
    
    return file_path if file_path else ""

def normalize_csv(csv_data):
        output = {
            (uid := str(uuid.uuid4())): {
                **{key.replace(' ', '_').lower(): value for key, value in item.items()},
                "id": uid,
                "status": "not_started",
                "file_key": get_file(item.get("Location"))
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
    
    
