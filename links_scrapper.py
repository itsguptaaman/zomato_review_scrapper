
import time
import json

from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.edge.options import Options
from selenium.webdriver.common.by import By


# Set up Edge options
options = Options()

# options.add_argument("--headless")  # Run in headless mode
options.add_argument("--disable-gpu")  # Disable GPU acceleration (sometimes necessary for headless)

# Specify the path to msedgedriver.exe
service = Service("msedgedriver.exe")

# Initialize the WebDriver with options and service
driver = webdriver.Edge(service=service, options=options)



def get_count():
    # Locate the parent div with the specified class names
    parent_div = driver.find_element(By.ID, "root")

    # Locate all inner divs with the class names sc-1mo3ldo-0 sc-hDgvsY aecIx within the parent div
    inner_divs = parent_div.find_elements(By.CSS_SELECTOR, "div.sc-1mo3ldo-0.sc-hDgvsY.aecIx")

    # Get the count of inner divs
    inner_div_count = len(inner_divs)

    # Print the count
    print(f"Number of inner divs: {inner_div_count}")

    return inner_div_count


def get_data():
    # Locate the parent div with the specified class names
    parent_div = driver.find_element(By.ID, "root")

    # Locate all inner divs with the class names sc-1mo3ldo-0 sc-hDgvsY aecIx within the parent div
    inner_divs = parent_div.find_elements(By.CSS_SELECTOR, "div.sc-1mo3ldo-0.sc-hDgvsY.aecIx")

    # Iterate through each inner div to find all <a> tags
    all_links = []
    for div in inner_divs:
        a_tags = div.find_elements(By.TAG_NAME, "a")
        for a in a_tags:
            href = a.get_attribute("href")
            # Replace /info with /reviews
            if "/info" in href:
                href = href.replace("/info", "/reviews")
            if href not in all_links:
                all_links.append(href)
                print(f"Found modified link: {href}")

    return all_links


def scroll_once(scroll_step=300, scroll_pause_time=1):
    # Scroll down by a fixed step
    driver.execute_script(f"window.scrollBy(0, {scroll_step});")

    # Wait for new content to load
    time.sleep(scroll_pause_time)


def main():
    # Navigate to the URL
    driver.get("https://www.zomato.com/pune/")
    time.sleep(5)
    scroll_once(scroll_step=1000)
    
    # Initial count
    init_count = get_count()
    consecutive_no_change = 0
    max_consecutive_no_change = 10  # Number of times count should not change before exiting
    
    while consecutive_no_change < max_consecutive_no_change:
        scroll_once(500)
        new_count = get_count()
        
        if new_count == init_count:
            consecutive_no_change += 1
            scroll_once(300)
        else:
            consecutive_no_change = 0  # Reset counter if count changes
        
        init_count = new_count  # Update init_count for the next iteration
        
        # Optional: print status for debugging
        print(f"Current count: {init_count}, Consecutive no change: {consecutive_no_change}")
    
    # Call get_data() after the loop exits
    all_links = get_data()
    data = {"links": all_links}
    with open('links.json', 'w') as fp:
        json.dump(data, fp)        
    # Close the browser
    driver.quit()


if __name__ == "__main__":
    main()
