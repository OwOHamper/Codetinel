class DataNormalizer:
    @staticmethod
    def normalize_keys(data, id_counter=1):
        if isinstance(data, dict):
            normalized = {}
            id_mapping = {}
            
            for k, v in data.items():
                norm_key = k.lower().replace(' ', '_')
                if isinstance(v, (dict, list)):
                    normalized_v, sub_mapping = DataNormalizer.normalize_keys(v, id_counter)
                    normalized[norm_key] = normalized_v
                    id_mapping.update(sub_mapping)
                    id_counter = max(int(k) for k in sub_mapping.keys()) + 1 if sub_mapping else id_counter
                else:
                    normalized[norm_key] = v
                    id_mapping[str(id_counter)] = v  # Convert to string
                    id_counter += 1
                    
            if 'status' in normalized:
                normalized['status'] = 'undetected'
                
            return normalized, id_mapping
            
        elif isinstance(data, list):
            normalized = []
            id_mapping = {}
            
            for item in data:
                normalized_item, sub_mapping = DataNormalizer.normalize_keys(item, id_counter)
                normalized.append(normalized_item)
                id_mapping.update(sub_mapping)
                id_counter = max(int(k) for k in sub_mapping.keys()) + 1 if sub_mapping else id_counter
                
            return normalized, id_mapping
            
        return data, {str(id_counter): data}  # Convert to string