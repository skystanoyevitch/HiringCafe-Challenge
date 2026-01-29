import json

def parse_json(input_file):
    unique_domains = set() 
    
    with open(input_file, 'r') as f:
        data = json.load(f)  
    
    for cert in data:  
        name_value = cert.get('name_value', '')  
        
        if not name_value: 
            continue
            
        domains = name_value.split('\n') 
        
        for domain in domains: 
            domain = domain.strip() 
            
            if filter_domain(domain):  
                unique_domains.add(domain) 
    
    return unique_domains  


def filter_domain(domain):
    """Check if domain should be kept or filtered out"""
    
    if not domain:  
        return False
    
    if domain.startswith('*'):  
        return False
    
    skip_patterns = ['sandbox', 'test', 'staging', 'internal', 'mail.', 
                     'smtp', 'analytics', 'clientcertificate', 'pentest',
                     'uat', 'qa', 'dev']
    
    for pattern in skip_patterns:
        if pattern in domain.lower():  
            return False
    
    if 'avature.net' not in domain:  
        return False
    
    return True 


def main():
    input_file = 'data/crt_domain_results.json'
    
    print("Parsing CT logs...")
    domains = parse_json(input_file)
    
    print(f"Found {len(domains)} unique production domains")
    
    output_file = 'data/ct_discovered_domains.txt'
    with open(output_file, 'w') as f:
        for domain in sorted(domains):  
            f.write(domain + '\n')
    
    print(f"Saved to {output_file}")


if __name__ == "__main__":
    main()