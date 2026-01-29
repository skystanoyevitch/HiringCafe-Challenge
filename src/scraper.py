import requests
import re
import math
import json
from datetime import datetime

# 3rd Party Libs
from bs4 import BeautifulSoup


def fetch_page(url):
    """Fetch HTML content from a URL"""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    

def parse_total_jobs(html):
    """Extract total job count from results text"""
    find_html_pattern = re.search(r'(\d+)\s+results', html)
    if find_html_pattern:
        try:
            extract_group = find_html_pattern.group(1)
            number_to_int = int(extract_group)
            return number_to_int
        except ValueError:
             return 0    
    else:
            return 0
    

def extract_jobs(html):
    """Extract job listings from a page"""
    soup = BeautifulSoup(html, 'lxml')
    articles = soup.find_all('article', class_='article--result')
    jobs = []
    for article in articles:
        title_link = article.find('h3').find('a')
        title = title_link.text.strip()
        detail_url = title_link['href']
        location_element = article.find('span', class_='list-item-location')
        if location_element:
            location = location_element.text.strip()
        else:
            location = "Not Specified"
        job = {'title': title, 'detail_url': detail_url, 'location': location}
        jobs.append(job)
    return jobs


def scrape_job_description(detail_url, base_domain):
    """Fetch and extract job description from detail page"""
    # Check if detail_url is already a complete URL
    if detail_url.startswith('http'):
        full_url = detail_url
    else:
        full_url = f"{base_domain}{detail_url}"
    
    html = fetch_page(full_url)
    if html is None:
        return "Description unavailable - page failed to load"
    
    soup = BeautifulSoup(html, 'lxml')
    description_div = soup.find('div', class_='article__content__view__field__value')
    
    if description_div:
        description = description_div.get_text(separator='\n', strip=True)
        return description
    else:
        description_div = soup.find('div', class_='article__content__view__field')
        if description_div:
            description = description_div.get_text(separator='\n', strip=True)
            return description
        
        return "Description not found on page"


def scrape_single_site(base_domain):
    """
    Scrape all jobs from a single Avature site.
    
    Args:
        base_domain: Full domain URL like 'https://bloomberg.avature.net' or 'https://bloomberg.avature.net/careers'
    
    Returns:
        List of job dictionaries with all data, or empty list on failure
    """
    # Extract domain name for display
    domain_name = base_domain.replace('https://', '').replace('http://', '')
    
    # Normalize URL: remove trailing slash and /careers if present
    base_clean = base_domain.rstrip('/')
    if base_clean.endswith('/careers'):
        base_clean = base_clean[:-8]  # Remove '/careers'
    
    # Build search URL
    search_url = f"{base_clean}/careers/SearchJobs"
    
    print("=" * 60)
    print(f"Scraping {domain_name}")
    print("=" * 60)
    
    # Step 1: Fetch first page and get total count
    print("\n[1/3] Fetching job count...")
    html = fetch_page(search_url)
    if html is None:
        print(f"✗ Error: Could not fetch careers page for {domain_name}")
        return []
    
    total_jobs = parse_total_jobs(html)
    if total_jobs == 0:
        print(f"No jobs found on {domain_name}")
        return []
    
    total_pages = math.ceil(total_jobs / 12)
    print(f"Found {total_jobs} total jobs across {total_pages} pages")
    
    # Step 2: Scrape all job listings (titles, URLs, locations)
    print(f"\n[2/3] Scraping job listings...")
    all_jobs = []
    
    for page in range(total_pages):
        if page == 0:
            page_html = html
        else:
            page_offset = page * 12
            page_html = fetch_page(f"{search_url}?jobRecordsPerPage=12&jobOffset={page_offset}")
            if page_html is None:
                print(f"  ⚠️  Warning: Failed to fetch page {page + 1}, skipping...")
                continue
        
        page_jobs = extract_jobs(page_html)
        all_jobs.extend(page_jobs)
        
        # Progress update every 10 pages
        if (page + 1) % 10 == 0 or page == total_pages - 1:
            print(f"  Progress: {page + 1}/{total_pages} pages ({len(all_jobs)} jobs collected)")
    
    print(f"✓ Collected {len(all_jobs)} job listings")
    
    # Step 3: Fetch descriptions for each job
    print(f"\n[3/3] Fetching job descriptions...")
    if len(all_jobs) > 50:
        print("This will take a few minutes...")
    
    for idx, job in enumerate(all_jobs):
        description = scrape_job_description(job['detail_url'], base_domain)
        job['description'] = description
        job['company_domain'] = domain_name
        
        # Progress update every 50 jobs
        if (idx + 1) % 50 == 0:
            percentage = ((idx + 1) / len(all_jobs)) * 100
            print(f"  Progress: {idx + 1}/{len(all_jobs)} ({percentage:.1f}%) descriptions fetched")
    
    print(f"✓ Fetched {len(all_jobs)} job descriptions")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"COMPLETE: {domain_name}")
    print("=" * 60)
    print(f"Total jobs scraped: {len(all_jobs)}")
    successful = sum(1 for j in all_jobs if 'Description unavailable' not in j.get('description', ''))
    print(f"Jobs with descriptions: {successful}")
    
    return all_jobs


def main():
    """Scrape multiple Avature sites and save to JSON"""
    print("=" * 70)
    print("AVATURE MULTI-SITE SCRAPER - PHASE 2")
    print("=" * 70)
    
    # Read URLs from cleaned list
    url_file = "data/avature_urls_clean.txt"
    output_file = "data/all_jobs.json"
    
    print(f"\nReading URLs from {url_file}...")
    with open(url_file, 'r') as f:
        all_urls = [line.strip() for line in f if line.strip()]
    
    print(f"Found {len(all_urls)} sites to scrape")
    
    # For testing, scrape first 5 sites only
    # Remove this limit for full scrape
    test_mode = False  # Changed to False for full scrape
    if test_mode:
        print("\n⚠️  TEST MODE: Scraping first 5 sites only")
        print("To scrape all sites, set test_mode = False in main()")
        all_urls = all_urls[:5]
    else:
        print(f"\n🚀 FULL SCRAPE MODE: Scraping all {len(all_urls)} sites")
        print("This will take several hours. Progress is saved after each site.")
    
    # Track statistics
    all_jobs = []
    successful_sites = 0
    failed_sites = 0
    
    # Scrape each site
    start_time = datetime.now()
    
    for idx, url in enumerate(all_urls, 1):
        print(f"\n{'='*70}")
        print(f"Site {idx}/{len(all_urls)}")
        print(f"{'='*70}")
        
        try:
            jobs = scrape_single_site(url)
            
            if jobs:
                all_jobs.extend(jobs)
                successful_sites += 1
                print(f"✓ Successfully scraped {len(jobs)} jobs")
            else:
                failed_sites += 1
                print(f"✗ No jobs found or site failed")
                
        except Exception as e:
            failed_sites += 1
            print(f"✗ Error scraping site: {e}")
            continue
        
        # Save progress after each site
        save_jobs_to_json(all_jobs, output_file)
        
        # Show running totals
        print(f"\nRunning totals: {len(all_jobs)} jobs from {successful_sites} sites")
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).total_seconds() / 60
    
    print("\n" + "=" * 70)
    print("SCRAPING COMPLETE")
    print("=" * 70)
    print(f"Total sites attempted: {len(all_urls)}")
    print(f"Successful sites: {successful_sites}")
    print(f"Failed sites: {failed_sites}")
    print(f"Total jobs scraped: {len(all_jobs)}")
    print(f"Time taken: {duration:.1f} minutes")
    print(f"Output saved to: {output_file}")
    
    # Show sample jobs from different companies
    if all_jobs:
        unique_companies = list(set(j['company_domain'] for j in all_jobs))[:3]
        print(f"\n📋 Sample jobs from {len(unique_companies)} companies:")
        for company in unique_companies:
            company_jobs = [j for j in all_jobs if j['company_domain'] == company]
            if company_jobs:
                sample = company_jobs[0]
                print(f"\n  {company}:")
                print(f"    • {sample['title']}")
                print(f"    • {sample['location']}")


def save_jobs_to_json(jobs, output_file):
    """Save jobs list to JSON file"""
    output_data = {
        "scrape_date": datetime.now().isoformat(),
        "total_jobs": len(jobs),
        "total_companies": len(set(j['company_domain'] for j in jobs)),
        "jobs": jobs
    }
    
    with open(output_file, 'w') as f:
        json.dump(output_data, f, indent=2)


if __name__ == "__main__":
    main()
