driver.switch_to.new_window()

for i in range(1, 75):
    driver.get(f"https://www.suryasangam.com/productlistning?page={i}")
    
    all_links = driver.find_elements(By.TAG_NAME, "a")
    count = len(all_links)

    with open("data/urls.csv", 'w', encoding="utf-8") as f: 
        f.write(f"The number of links in store page {i} is {count} \n")

    for link in all_links:
        url = link.get_attribute("href")
        name = link.get_attribute("text")
        
        with open("data/urls.csv", 'a', encoding="utf-8") as f:
            f.write(f"{name} => {url}\n")
