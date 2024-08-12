import hashlib
import json
import traceback
import time
import random
import requests
from bs4 import BeautifulSoup 

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en;q=0.9,en-US;q=0.8',
    'cache-control': 'max-age=0',
    'dnt': '1',
    'priority': 'u=0, i',
    'referer': 'https://www.zomato.com/',
    'sec-ch-ua': '"Not/A)Brand";v="8", "Chromium";v="126", "Microsoft Edge";v="126"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36 Edg/126.0.0.0',
}


BASE_URL = "https://www.zomato.com/"


def create_session(retry=5):
    global session  # Declare 'session' as global to modify it
    try:
        # Check if 'session' exists in globals and is an instance of requests.Session
        if 'session' in globals():
            session.close()  # Close the existing session to destroy it
            print("Existing session destroyed.")
        
        # Create a new session
        session = requests.Session()
        res = session.get(BASE_URL, headers=headers, verify=False)
        if res.status_code != 200 and retry > 0:
            create_session(retry=retry-1)
        else:
            print("New session created.")
    except Exception as e:
        print(f"An error occurred: {e}")
        traceback.print_exc()

def md5_of_dict(data):
  # Sort keys to ensure consistent hashing
  sorted_data = dict(sorted(data.items()))

  # Convert dictionary to JSON string
  json_data = json.dumps(sorted_data).encode('utf-8')

  # Calculate MD5 hash
  md5_hash = hashlib.md5(json_data).hexdigest()

  return md5_hash


def read_links(file_path="links.json"):
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(e)
        traceback.print_exc()


def get_review(url, retry=3):
    try:
        time.sleep(random.randint(1, 4))
        response = session.get(url, headers=headers)
        if response.status_code != 200 and retry > 0:
            create_session()
            get_review(url, retry=retry-1)

        elif response.status_code == 200:
            return response
        
        else:
            return None
    except Exception as e:
        print(e)
        traceback.print_exc()

def export_data(dictionary, file_path="reviews.json"):
    with open(file_path, 'a') as json_file:
        json.dump(dictionary, json_file, indent=4)

        

def main():
    try:
        data = read_links()
        for link in data["links"]:
            create_session()
            previous_md5 = None
            full_data = []
            for page_no in range(1, 100000):
                print(f">>>>>>On page number {page_no}<<<<<<<<<<")
                url = link + f"?page={page_no}&amp;sort=dd&amp;filter=reviews-dd"
                response = get_review(url)
                if response:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    data_list = soup.find_all("script")
                    data = eval(data_list[1].text)
                    current_md5 = md5_of_dict(data)
                    
                    if previous_md5 == current_md5:
                        break
                    
                    previous_md5 = current_md5
                    full_data.append({"pageno_"+ str(page_no): data})
                    
                else:
                    continue
            
            export_data({"link": link, "data": full_data})
            # break
        

    except Exception as e:
        print(e)
        traceback.print_exc()


if __name__ == "__main__":
    main()



