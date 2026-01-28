# Avature ATS Scraper - Project Guide & Instructions

## Project Overview

**Goal:** Build a scraper to extract as many valid job postings as possible from as many Avature-hosted career sites as possible.

**Time Constraint:** Maximum 9 hours

**Primary Metric:** Total number of unique jobs scraped

**Current Status:** Site analysis complete - confirmed all Avature sites use server-side rendered HTML with consistent formatting. Job listings show 12 jobs per page, full descriptions only available on detail pages.

---

## Working Instructions for AI Assistant

### Communication Guidelines:

- **Explain reasoning** behind all decisions instead of asking questions
- **No code** should be written or shown unless explicitly requested
- **One step at a time** - don't move to next sub-task until given permission
- **Use best practices** for all technical decisions
- **Search web** (December 2025 and newer) for current, reliable information when needed
- **Natural tone** - communicate like a human, not robotic

### When I Need Something:

- I will ask questions if I need clarification
- I will explicitly request code when ready
- I will tell you when to proceed to next task

---

## Complete Task List (In Order)

### **Phase 1: Single-Site Prototype (2 hours)**

#### Task 1.1: Set Up Development Environment

- Choose and install necessary Python libraries
- Set up project structure (folders, files)
- Initialize version control

#### Task 1.2: Build Basic Job List Extractor (Bloomberg Only)

- Fetch HTML from Bloomberg careers page
- Parse total job count from results text
- Extract job cards from first page only
- Extract: title, location, detail page URL

#### Task 1.3: Implement Pagination Logic

- Calculate total number of pages from job count
- Generate pagination URLs with correct offsets
- Test fetching multiple pages
- Verify all pages load correctly

#### Task 1.4: Add Job Detail Page Scraping

- Visit individual job detail pages
- Extract full job description
- Extract any additional metadata (date posted, etc.)
- Test with 2-3 complete jobs end-to-end

#### Task 1.5: Validate Prototype

- Run scraper on first 2-3 pages of Bloomberg
- Verify data quality and completeness
- Check for any missing or malformed data

---

### **Phase 2: Scale to Multiple URLs (3 hours)**

#### Task 2.1: Download and Prepare URL List

- Download starter pack from Google Drive
- Parse/clean the URL list
- Validate URL formats
- Count total URLs in starter pack

#### Task 2.2: Generalize Scraper for Any Avature Site

- Refactor code to accept any domain
- Extract domain-agnostic selectors
- Make scraper work with `{company}.avature.net` pattern

#### Task 2.3: Implement Error Handling

- Add try/catch for network failures
- Handle missing data fields gracefully
- Add timeout handling for slow sites
- Log errors without crashing entire scrape

#### Task 2.4: Add Progress Tracking and Logging

- Show which site is currently being scraped
- Track success/failure counts
- Log summary statistics
- Save progress periodically

#### Task 2.5: Test on Sample of Starter Pack

- Run on 5-10 diverse sites from starter pack
- Identify and fix any issues
- Verify data consistency across different sites

#### Task 2.6: Full Starter Pack Scrape

- Run scraper on all starter pack URLs
- Monitor for errors and edge cases
- Collect initial dataset

---

### **Phase 3: URL Discovery & Expansion (2 hours)**

#### Task 3.1: Google Search Discovery

- Use Google dork: `site:avature.net/careers`
- Use Google dork: `inurl:avature.net/careers`
- Extract unique domains from results
- Add to URL list

#### Task 3.2: Certificate Transparency Discovery

- Query crt.sh for `%.avature.net` certificates
- Filter for career-related subdomains
- Validate discovered URLs
- Add new URLs to list

#### Task 3.3: Pattern-Based Discovery (Optional, if time allows)

- Analyze common company naming patterns
- Test variations of known companies
- Add confirmed working URLs

#### Task 3.4: Deduplicate and Validate Expanded List

- Remove duplicate URLs
- Remove dead/non-working URLs
- Count total unique domains discovered

---

### **Phase 4: Final Scrape & Delivery (2 hours)**

#### Task 4.1: Run Full Scrape on Expanded URL List

- Execute scraper on all discovered URLs
- Monitor progress and errors
- Ensure completion

#### Task 4.2: Data Cleaning and Deduplication

- Remove duplicate jobs (same job on multiple sites)
- Validate data completeness
- Clean any malformed text/HTML
- Calculate final statistics

#### Task 4.3: Format Output Files

- Save jobs data in JSON format
- Create input URL list file
- Generate summary statistics
- Verify file formats

#### Task 4.4: Documentation

- Write README explaining approach
- Document time spent on each phase
- Explain technical decisions made
- Note any limitations or edge cases

#### Task 4.5: Final Review and Submission Prep

- Review all deliverables
- Test that code runs from scratch
- Organize repository structure
- Prepare for submission

---

## Technical Approach & Reasoning

### **Technology Stack**

**HTTP Client: `requests`**

- Industry standard, simple API
- Handles headers/cookies automatically
- Sufficient for server-side rendered content

**HTML Parser: `BeautifulSoup4` with `lxml`**

- Most intuitive API for HTML navigation
- Fast lxml parser handles malformed HTML
- Good balance of speed and ease of use

**Data Storage: JSON**

- Easy to read and debug
- Preserves nested structures
- Can convert to other formats if needed

---

### **Scraping Strategy**

**Step 1: Pagination Discovery**

- Fetch main search page
- Extract total job count using regex: `r'(\d+)\s+results'`
- Calculate pages: `math.ceil(total_jobs / 12)`
- Generate URLs: `SearchJobs/?jobRecordsPerPage=12&jobOffset={n*12}`

**Step 2: Job List Extraction**

- Select all: `article.article--result`
- Extract title from: `h3 > a`
- Extract URL from: `h3 > a['href']`
- Extract location from: `span.list-item-location`

**Step 3: Detail Page Scraping**

- Visit each detail URL
- Extract description from main content area
- Extract additional metadata if available
- Handle missing fields gracefully

---

### **Performance Optimization**

**Concurrent Requests:**

- Use ThreadPoolExecutor with 10 workers
- Parallelizes I/O-bound network requests
- 10x faster than sequential scraping

**Rate Limiting:**

- Add 0.5 second delay between requests to same domain
- Prevents overwhelming servers
- Avoids IP bans

---

### **Error Handling**

**Network Errors:**

- Set 10-second timeout on all requests
- Catch and log exceptions
- Continue to next site on failure

**Parsing Errors:**

- Use try/except for all data extraction
- Default to null/empty for missing fields
- Don't crash on malformed HTML

---

### **Data Quality**

**Deduplication Strategy:**

- Use job detail URL as unique identifier
- Track in set() to prevent duplicates
- More reliable than title matching

**Output Format:**

```json
{
  "scrape_date": "2026-01-28",
  "total_jobs": 15234,
  "total_sites": 87,
  "jobs": [
    {
      "job_id": "unique_id",
      "title": "Job Title",
      "description": "Full description...",
      "apply_url": "https://...",
      "location": "City, State, Country",
      "company_domain": "bloomberg",
      "date_posted": null,
      "metadata": {}
    }
  ]
}
```

---

## Project Deliverables

1. **Code** - Complete Python scraper
2. **Input File** - List of all Avature URLs discovered and used
3. **Output File** - JSON file with all scraped jobs
4. **README** - Documentation of approach and reasoning

---

## Time Tracking

- Phase 1: **\_** hours
- Phase 2: **\_** hours
- Phase 3: **\_** hours
- Phase 4: **\_** hours
- **Total: **\_** hours** (Target: ≤9 hours)

---

## Notes & Discoveries

- Confirmed: All Avature sites use same HTML structure
- Confirmed: 12 jobs per page across all sites
- Confirmed: Full descriptions only on detail pages
- Total count appears in format: "X-Y of Z results"

---

_Last Updated: January 28, 2026_
