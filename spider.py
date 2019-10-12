import requests
from requests.exceptions import RequestException
import re
import json
from selenium import webdriver
from hashlib import md5

def get_page_index(name,page):
    try:
        data = {
            "page": page,
            "per_page": 50,
            "pro_first": "1",
            "query": name,
            "sorting": "likes"
        }
        header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        proxies = {
            "http":"http://127.0.0.1:1087",
            "https": "https://127.0.0.1:1087"
        }
        url = "https://www.artstation.com/api/v2/search/projects.json"
        response = requests.get(url=url,headers=header,proxies=proxies,data=data)
        print(response.status_code)
        print(response.text)
        return response.text
    except RequestException as e:
        print(e)

def parse_vaule(vaule):
    try:
        listVaule = json.loads(vaule)
        items = listVaule["data"]
        for item  in items:
            yield {
                "title":item["title"],
                "url":item["url"]
            }
    except:
        pass


def parse_page_img(html):
    pattern = re.compile('<div class="artwork-image".*?<img.*?ng-src=.*?src="(.*?)">.*?',re.S)
    return re.findall(pattern,html)


def get_page_imege(browser,url):
    try:
        header = {
            "user-agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/77.0.3865.90 Safari/537.36"
        }
        proxies = {
            "http":"http://127.0.0.1:1087",
            "https": "https://127.0.0.1:1087"
        }
        browser.get(url)
        imgURL = parse_page_img(browser.page_source)
        # print("parse URL:{}".format(imgURL))
        for i in range(len(imgURL)):
            response = requests.get(url=imgURL[i],headers=header,proxies=proxies)
            File_path = "{}.jpg".format(md5(response.content).hexdigest())
            with open(File_path.encode('utf-8'),"wb") as f:
                print("Now Saving image:{}-{}".format(i+1,len(imgURL)))
                f.write(response.content)
                f.close()
    except RequestException as e:
        print(e)



if __name__ == "__main__":

    browser = webdriver.Chrome()
    for i in range(10):
        vaule = get_page_index("cyberpunk",i)
        for item in parse_vaule(vaule):
            print(item)
            get_page_imege(browser,item["url"])
            # time.sleep(1)