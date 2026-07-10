import csv
import json
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import WebDriverException

# Read URLs
all_links = set()

with open("data/urls.csv", "r", encoding="utf-8") as f:
    reader = csv.reader(f)

    for row in reader:
        if row and row[0]:
            all_links.add(row[0].strip())

all_links = sorted(all_links)

print(f"Found {len(all_links)} unique URLs.")
# Chrome options
options = Options()
# Uncomment the next line to run Chrome in headless mode
# options.add_argument("--headless=new")

driver = webdriver.Chrome(options=options)
driver.implicitly_wait(5)

all_pages = []
all_forms = []

for url in all_links:
    try:
        driver.get(url)

        soup = BeautifulSoup(driver.page_source, "html.parser")

        # --------------------
        # Page Information
        # --------------------

        title = soup.title.get_text(strip=True) if soup.title else ""

        h1_tags = [
            h1.get_text(strip=True)
            for h1 in soup.find_all("h1")
        ]

        h2_tags = [
            h2.get_text(strip=True)
            for h2 in soup.find_all("h2")
        ]

        paragraphs = []

        for p in soup.find_all("p"):
            text = p.get_text(" ", strip=True)
            if text:
                paragraphs.append(text)

        images = []

        for img in soup.find_all("img"):
            src = img.get("src")
            if src:
                images.append(urljoin(url, src))

        page_data = {
            "url": url,
            "title": title,
            "h1_tags": h1_tags,
            "h2_tags": h2_tags,
            "paragraphs": paragraphs,
            "images": images,
        }

        all_pages.append(page_data)

        # --------------------
        # Form Information
        # --------------------

        for form in soup.find_all("form"):

            form_data = {
                "page_url": url,
                "action": urljoin(url, form.get("action", "")),
                "method": form.get("method", "GET").upper(),
                "id": form.get("id"),
                "name": form.get("name"),
                "fields": []
            }

            # Inputs
            for inp in form.find_all("input"):
                form_data["fields"].append({
                    "tag": "input",
                    "type": inp.get("type", "text"),
                    "name": inp.get("name"),
                    "id": inp.get("id"),
                    "placeholder": inp.get("placeholder"),
                    "value": inp.get("value"),
                    "required": inp.has_attr("required")
                })

            # Textareas
            for textarea in form.find_all("textarea"):
                form_data["fields"].append({
                    "tag": "textarea",
                    "name": textarea.get("name"),
                    "id": textarea.get("id"),
                    "placeholder": textarea.get("placeholder"),
                    "required": textarea.has_attr("required")
                })

            # Selects
            for select in form.find_all("select"):

                options = [
                    option.get_text(strip=True)
                    for option in select.find_all("option")
                ]

                form_data["fields"].append({
                    "tag": "select",
                    "name": select.get("name"),
                    "id": select.get("id"),
                    "options": options,
                    "required": select.has_attr("required")
                })

            # Buttons
            for button in form.find_all("button"):
                form_data["fields"].append({
                    "tag": "button",
                    "type": button.get("type", "submit"),
                    "text": button.get_text(strip=True)
                })

            all_forms.append(form_data)

        print(f"✓ Scraped: {url}")

    except WebDriverException as e:
        print(f"Selenium Error: {url}")
        print(e)

    except Exception as e:
        print(f"Failed: {url}")
        print(e)

driver.quit()

# --------------------
# Save Pages
# --------------------

with open("data/pages.json", "w", encoding="utf-8") as f:
    json.dump(
        all_pages,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Saved {len(all_pages)} pages to data/pages.json")

# --------------------
# Save Forms
# --------------------

with open("data/forms.json", "w", encoding="utf-8") as f:
    json.dump(
        all_forms,
        f,
        indent=4,
        ensure_ascii=False
    )

print(f"Saved {len(all_forms)} forms to data/forms.json")