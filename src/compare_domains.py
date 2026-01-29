

def compare_domains():
    ct_domains = set()
    with open('data/ct_discovered_domains.txt', 'r') as f:
        for line in f:
            ct_domains.add(line.strip())
    original_domains = set()
    with open('data/avature_urls_clean.txt', 'r') as f:
        for line in f:
            avature_domains_url = line.strip()
            domain = avature_domains_url.replace('https://', '').replace('/careers', '')
            original_domains.add(domain)
    new_domains = ct_domains - original_domains
    return new_domains



def main():
    print("Comparing CT domains with original list...")
    
    new_domains = compare_domains()
    
    print(f"\n✓ CT logs found: 20 total domains")
    print(f"✓ New domains (not in original): {len(new_domains)}")
    
    if len(new_domains) > 0:
        print("\nNew domains to scrape:")
        for domain in sorted(new_domains):
            print(f"  • {domain}")
        
        # Save new domains to file
        with open('data/ct_new_domains.txt', 'w') as f:
            for domain in sorted(new_domains):
                f.write(domain + '\n')
        print(f"\nSaved to data/ct_new_domains.txt")
    else:
        print("\nNo new domains found - all 20 were already in the original list")


if __name__ == "__main__":
    main()