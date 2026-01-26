import os
import time
import pandas as pd
from playwright.sync_api import sync_playwright


all_jobs = []

keyword = 'front end developer'
location = 'Bengaluru, Karnataka'
radius = 100
sort = 'date'
days = '1'
BASE_URL = f'https://in.indeed.com/jobs?q={keyword}&l={location}&radius={radius}&sort={sort}&fromage={days}&vjk=d60fe123ae2331d7'


with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)  # keep False for debugging
    page = browser.new_page()
    page.goto(BASE_URL, timeout=60000)

    while True:
        print("🔍 Scraping current page...")

        page.wait_for_selector("div.job_seen_beacon", timeout=10000)

        job_cards = page.query_selector_all("div.job_seen_beacon")

        for job in job_cards:
            title = job.query_selector("h2.jobTitle span")
            company = job.query_selector('span[data-testid="company-name"]')
            location = job.query_selector("div[data-testid='text-location']")
            link = job.query_selector("h2.jobTitle a")

            all_jobs.append({
                "Title": title.inner_text() if title else "",
                "Company": company.inner_text() if company else "",
                "Location": location.inner_text() if location else "",
                "Link": "https://in.indeed.com" + link.get_attribute("href") if link else ""
            })

        # Locate Next button
        next_button = page.query_selector('[data-testid="pagination-page-next"]')

        # Stop if button not found or disabled
        if not next_button or next_button.get_attribute("aria-disabled") == "true":
            print("🚫 No more pages. Pagination ended.")
            break

        print("➡️ Moving to next page...")
        next_button.click()
        time.sleep(2)

    browser.close()

# Save to Excel
# df = pd.DataFrame(all_jobs)
# df.to_excel("indeed_jobs.xlsx", index=False)

# print(f"✅ Scraped {len(df)} jobs and saved to indeed_jobs.xlsx")

# Save to CSV
df = pd.DataFrame(all_jobs)
df.to_csv("indeed_job_titles.csv", index=False, encoding="utf-8")

print(f"✅ Exported {len(df)} jobs to indeed_job_titles.csv")


