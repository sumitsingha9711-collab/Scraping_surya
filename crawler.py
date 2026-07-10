from selenium import webdriver
from selenium.webdriver.common.by import By

driver = webdriver.Chrome()

unique_links = set()

# -------- Home Page --------
driver.get("https://www.suryasangam.com")

for link in driver.find_elements(By.TAG_NAME, "a"):
    url = link.get_attribute("href")

    if url:
        unique_links.add(url)

# -------- Product Listing Page --------
driver.switch_to.new_window()

driver.get("https://www.suryasangam.com/productlistning?page=1")

for link in driver.find_elements(By.TAG_NAME, "a"):
    url = link.get_attribute("href")

    if url:
        unique_links.add(url)

driver.quit()

# Save only unique URLs
with open("data/urls.csv", "w", encoding="utf-8") as f:
    for url in sorted(unique_links):
        f.write(url + "\n")

print(f"Saved {len(unique_links)} unique URLs.")