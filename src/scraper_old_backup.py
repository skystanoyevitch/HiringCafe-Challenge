
import requests
import re
import math


# 3rd Party Libs
from bs4 import BeautifulSoup



def fetch_page(url):
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        print(f"Error fetching {url}: {e}")
        return None
    

def parse_total_jobs(html):
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
    # Check if detail_url is already a complete URL
    if detail_url.startswith('http'):
        full_url = detail_url  # Already complete
    else:
        full_url = f"{base_domain}{detail_url}"  # Relative path, prepend domain
    
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
     print("=" * 60)
     print("PHASE 1: Scraping Bloomberg job listings")
     print("=" * 60)
     
     # Step 1: Fetch first page and get total count
     print("\n[1/3] Fetching job count...")
     html = fetch_page(base_domain)
     if html is None:
         print("Error: Could not fetch Bloomberg careers page")
         return
     
     total_jobs = parse_total_jobs(html)
     total_pages = math.ceil(total_jobs / 12)
     print(f"Found {total_jobs} total jobs across {total_pages} pages")
     
     # Step 2: Scrape all job listings (titles, URLs, locations)
     print(f"\n[2/3] Scraping job listings from all pages...")
     all_jobs = []
     
     for page in range(total_pages):
         if page == 0:
             page_html = html
         else:
             page_offset = page * 12
             page_html = fetch_page(f"{base_domain}/?jobRecordsPerPage=12&jobOffset={page_offset}")
             if page_html is None:
                 print(f"  ⚠️  Warning: Failed to fetch page {page + 1}, skipping...")
                 continue
         
         page_jobs = extract_jobs(page_html)
         all_jobs.extend(page_jobs)
         
         # Progress update every 10 pages
         if (page + 1) % 10 == 0 or page == total_pages - 1:
             print(f"  Progress: {page + 1}/{total_pages} pages ({len(all_jobs)} jobs collected)")
     
     print(f"\n✓ Collected {len(all_jobs)} job listings")
     

def main():

     # Step 3: Fetch descriptions for each job
     print(f"\n[3/3] Fetching job descriptions...")
     print("This will take a few minutes...")
     
     for idx, job in enumerate(all_jobs):
         # Fetch the description
         description = scrape_job_description(job['detail_url'], base_domain)
         job['description'] = description
         
         # Progress update every 50 jobs
         if (idx + 1) % 50 == 0:
             percentage = ((idx + 1) / len(all_jobs)) * 100
             print(f"  Progress: {idx + 1}/{len(all_jobs)} ({percentage:.1f}%) descriptions fetched")
     
     print(f"\n✓ Fetched {len(all_jobs)} job descriptions")
     
     # Final summary
     print("\n" + "=" * 60)
     print("SCRAPING COMPLETE")
     print("=" * 60)
     print(f"Total jobs scraped: {len(all_jobs)}")
     print(f"Jobs with descriptions: {sum(1 for j in all_jobs if 'Description unavailable' not in j.get('description', ''))}")
     
     # Sample output - show first job
     if all_jobs:
         print("\n📋 Sample job:")
         sample = all_jobs[0]
         print(f"  Title: {sample['title']}")
         print(f"  Location: {sample['location']}")
         print(f"  Description preview: {sample['description'][:200]}...")




if __name__ == "__main__":
    main()