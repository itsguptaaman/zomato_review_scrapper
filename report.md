# **Project Report: Zomato Review Link Scraper**

## **1. Introduction**
This project aims to build a web scraper that automates the extraction of restaurant review links from Zomato’s Pune page. The scraping is performed using the Selenium WebDriver, which interacts with the web browser to navigate, scroll, and extract data from dynamically loaded content.

## **2. Tools and Technologies Used**
- **Python:** The primary programming language used to write the scripts.
- **Selenium:** A web automation tool used for navigating web pages and extracting data.
- **Edge WebDriver:** The browser automation driver used to control the Edge browser.
- **JSON:** Used to store the extracted links.

## **3. Scraping Strategy**

### **Website Structure and HTML Parsing**
The Zomato Pune page contains a list of restaurants, each represented by a `div` element with specific class names. Within these `div` elements, there are anchor (`<a>`) tags that link to the restaurant's details page. The goal is to modify these links to point to the restaurant's review page.

- **Identifying Elements:**
  The scraper identifies the parent `div` element by its `id` attribute (`root`). Within this parent `div`, the specific `div` elements containing restaurant information are identified using their CSS classes (`sc-1mo3ldo-0 sc-hDgvsY aecIx`).

- **HTML Parsing:**
  The `find_elements` method of Selenium is used to locate all `div` elements matching the specified class names. The `get_data` function iterates through each `div`, extracting the `href` attribute from all `a` tags found.

### **Handling Dynamic Content (JavaScript-Rendered Pages)**
The Zomato page dynamically loads more content as the user scrolls down. To handle this, the scraper simulates user scrolling using JavaScript execution through the `scroll_once` function. This function scrolls the page by a fixed pixel value and pauses to allow new content to load.

- **Scrolling Mechanism:**
  The page is scrolled in increments until the scraper detects that no new content is loaded. This is managed by comparing the count of restaurant `div` elements before and after each scroll.

### **Dealing with Pagination**
Zomato does not use traditional pagination (with numbered pages) but instead loads more content dynamically as the user scrolls. The scraper mimics this infinite scroll behavior to continuously load and extract data until no new content is detected.

### **Managing Request Headers and Sessions**
Selenium automates a real web browser, so it inherently manages cookies, sessions, and request headers as a real user would. This makes it particularly effective for scraping sites like Zomato that rely heavily on JavaScript and dynamic content.

### **Handling Potential Anti-Scraping Mechanisms**
Zomato may implement anti-scraping mechanisms, such as bot detection algorithms. The following strategies are employed to mitigate these:

- **Human-like Behavior:**
  The scraper uses realistic scroll intervals and pauses (`time.sleep()`) to mimic human interaction with the page. This reduces the likelihood of being flagged as a bot.
  
- **Headless Mode (Optional):**
  Although currently disabled in the script, running the browser in headless mode could reduce the load on the system and decrease the chances of detection. However, headless mode can sometimes trigger bot detection, so it is not used by default.

## **4. Implementation Details**

### **Code Snippets and Explanation**

**1. Scroll Mechanism:**
```python
def scroll_once(scroll_step=300, scroll_pause_time=1):
    # Scroll down by a fixed step
    driver.execute_script(f"window.scrollBy(0, {scroll_step});")
    # Wait for new content to load
    time.sleep(scroll_pause_time)

```
- Explanation: This function scrolls the web page by the specified scroll_step and then pauses to allow any new content to load.

** 2. Counting and Extracting Links:**
```
def get_count():
    parent_div = driver.find_element(By.ID, "root")
    inner_divs = parent_div.find_elements(By.CSS_SELECTOR, "div.sc-1mo3ldo-0.sc-hDgvsY.aecIx")
    inner_div_count = len(inner_divs)
    print(f"Number of inner divs: {inner_div_count}")
    return inner_div_count

def get_data():
    parent_div = driver.find_element(By.ID, "root")
    inner_divs = parent_div.find_elements(By.CSS_SELECTOR, "div.sc-1mo3ldo-0.sc-hDgvsY.aecIx")
    all_links = []
    for div in inner_divs:
        a_tags = div.find_elements(By.TAG_NAME, "a")
        for a in a_tags:
            href = a.get_attribute("href")
            if "/info" in href:
                href = href.replace("/info", "/reviews")
            if href not in all_links:
                all_links.append(href)
                print(f"Found modified link: {href}")
    return all_links
```
- Explanation: get_count() returns the count of restaurant div elements, and get_data() iterates through these elements to extract and modify links.

**Challenges and Solutions**
- Dynamic Content Loading: The infinite scroll mechanism on Zomato's page was challenging, but it was effectively managed by implementing a scroll loop that stops when no new content is loaded.

- Potential Blocking: Anti-scraping mechanisms could block access if the scraping activity appears suspicious. This was addressed by simulating human-like behavior with appropriate pauses and realistic interaction patterns.


## Conclusion
- This project successfully demonstrates the extraction of dynamically loaded content from a website using Selenium. The scraper efficiently handles infinite scrolling, dynamic content, and link extraction, storing the results in a structured JSON format.