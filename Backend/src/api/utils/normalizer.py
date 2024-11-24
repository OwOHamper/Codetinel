import uuid


def get_file(file_context):
    print(file_context)
    if file_context and isinstance(file_context, str):
        # Parse the Ruby-style string format
        try:
            # Remove curly braces and split by commas
            content = file_context.strip('{}').split(',')
            file_context_dict = {}
            
            for item in content:
                key, value = item.split('=>')
                # Clean up the strings
                key = key.strip().strip('"')
                value = value.strip()
                # Convert numeric values
                if value.isdigit():
                    value = int(value)
                else:
                    value = value.strip('"')
                file_context_dict[key] = value

            file_path = file_context_dict.get('file')
            start_line = file_context_dict.get('start_line')
            
            if file_path and start_line:
            #     # If end_line exists, use middle line, otherwise use start_line
                if 'end_line' in file_context_dict:
                    end_line = file_context_dict['end_line']
                    return f"{file_path}:{start_line}-{end_line}"
            #         middle_line = start_line + ((end_line - start_line) // 2)
            #     else:
            #         middle_line = start_line
                    
            return f"{file_path}:{start_line}"
        except Exception as e:
            print(f"Error parsing file context: {str(e)}")
            return ""

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
    
    
