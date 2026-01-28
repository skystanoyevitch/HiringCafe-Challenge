from urllib.parse import urlparse
from collections import Counter

from urllib.parse import urlparse


def extract_unique_domains(input_file):
    domains = set()
    
    with open(input_file, 'r') as f:
        for line in f:
            url = line.strip()
            if url:
                parsed = urlparse(url)
                domain = parsed.netloc
                if 'avature.net' in domain:
                    domains.add(domain)
    
    return domains


def build_careers_urls(domains):
    careers_urls = []
    
    for domain in domains:
        url = f"https://{domain}/careers"
        careers_urls.append(url)
    
    return careers_urls


def save_urls(urls, output_file):
    with open(output_file, 'w') as f:
        for url in urls:
            f.write(url + '\n')
    
    print(f"Saved {len(urls)} URLs to {output_file}")


def main():
    input_file = "data/avature_urls_starter_pack.txt"
    output_file = "data/avature_urls_clean.txt"
    
    print("Extracting unique domains...")
    domains = extract_unique_domains(input_file)
    print(f"Found {len(domains)} unique domains")
    
    print("Building careers URLs...")
    careers_urls = build_careers_urls(domains)
    
    print("Saving cleaned URLs...")
    save_urls(careers_urls, output_file)
    
    print("\nDone!")


if __name__ == "__main__":
    main()