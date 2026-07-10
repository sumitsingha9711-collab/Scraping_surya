import csv
import json
import os

# Create reports directory if it doesn't exist
os.makedirs("reports", exist_ok=True)

# -----------------------------
# Load URLs
# -----------------------------
with open("data/urls.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)
    total_urls = sum(1 for row in reader if row)

# -----------------------------
# Load Pages
# -----------------------------
with open("data/pages.json", "r", encoding="utf-8") as f:
    pages = json.load(f)

# -----------------------------
# Load Forms
# -----------------------------
with open("data/forms.json", "r", encoding="utf-8") as f:
    forms = json.load(f)

# -----------------------------
# Calculate Statistics
# -----------------------------
pages_scraped = len(pages)
forms_found = len(forms)

total_images = sum(len(page.get("images", [])) for page in pages)
total_h1 = sum(len(page.get("h1_tags", [])) for page in pages)
total_h2 = sum(len(page.get("h2_tags", [])) for page in pages)
total_paragraphs = sum(len(page.get("paragraphs", [])) for page in pages)

# Count downloaded images
if os.path.exists("images"):
    images_downloaded = len(
        [
            file
            for file in os.listdir("images")
            if os.path.isfile(os.path.join("images", file))
        ]
    )
else:
    images_downloaded = 0

# Average statistics
avg_images = (
    total_images / pages_scraped
    if pages_scraped else 0
)

avg_paragraphs = (
    total_paragraphs / pages_scraped
    if pages_scraped else 0
)

# -----------------------------
# Create Report
# -----------------------------
report = f"""
========================================
        WEBSITE SCRAPING REPORT
========================================

Total URLs Found        : {total_urls}
Pages Scraped           : {pages_scraped}

Forms Found             : {forms_found}

Images Referenced       : {total_images}
Images Downloaded       : {images_downloaded}

Total H1 Tags           : {total_h1}
Total H2 Tags           : {total_h2}

Total Paragraphs        : {total_paragraphs}

Average Images/Page     : {avg_images:.2f}
Average Paragraphs/Page : {avg_paragraphs:.2f}

========================================
"""

# Save report
with open("reports/summary.txt", "w", encoding="utf-8") as f:
    f.write(report)

print(report)
print("Report saved to reports/summary.txt")