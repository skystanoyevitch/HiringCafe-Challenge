import requests

# Test if Google discovery domains are valid or not
def get_valid_domains():
    with open('data/domain_discovery.txt', 'r') as f:
        read_domains = f.readlines()
        valid_domains = []
        invalid_domains = []
        for domain in read_domains:
            get_domains = domain.strip()

            if not get_domains:
                continue
            url = f"https://{get_domains}/careers/SearchJobs"

            try:
                response = requests.head(url, timeout=5)
                if response.status_code == 200:
                    print(f'Valid Domain: {get_domains}')
                    valid_domains.append(get_domains)
                else:
                    print(f'Invalid Domain: {get_domains} - Status: {response.status_code}')
                    invalid_domains.append(get_domains)
            except requests.RequestException as e:
                print(f'Error: {get_domains} - {e}')
                invalid_domains.append(get_domains)
    with open('data/discover_valid_domains.txt', 'w') as f:
        for domain in valid_domains:
            f.write(domain + '\n')
    print(f"\n✓ Found {len(valid_domains)} valid domains")
    print(f"✗ Found {len(invalid_domains)} invalid domains")


if __name__ == "__main__":
    get_valid_domains()

