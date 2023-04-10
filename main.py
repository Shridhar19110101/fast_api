from selenium import webdriver 
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import time
from selenium.common.exceptions import TimeoutException
import json
from fastapi import FastAPI
import uvicorn
from selenium.webdriver.chrome.options import Options



app = FastAPI(timeout=600)

def pipeline(domain):
    chat_providers=[("js.driftt.com/","drift"),(".intercom.io/messenger/web/","intercom"),(".livechatinc.com/","LiveChat"),(".salesforceliveagent.com//chat/","Salesforce"),(".hubspot.com/livechat","hubspot"),(".hubspot.com/conversations-visitor/","hubspot"),
    (".zohocdn.com/salesiq/","zohodesk"),(".zohocdn.com/zohoim/imchat","zohodesk"),("ladesk.com/scripts/","liveagent"),("connect.podium.com/styles","podium"),(".widget.insent.ai","zoominfo"),(".terminus.services/","Terminus"),
    (".qualified.com/","Qualified"),(".tidiochat.com/","Tidio"),("static.zdassets.com/ekr/","Zendesk"),(".olark.com/","Olark"),(".liveperson.net/","LivePerson"),(".freshbots.ai/","Freshwork"),(".artibot.ai/","artibot"),(".groovehq.com/","Groove")]

    url=domain
    desired_capabilities = DesiredCapabilities.CHROME
    desired_capabilities["goog:loggingPrefs"] = {"performance": "ALL"}
    
    chrome_options = Options()
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--disable-dev-shm-usage')
#     driver = webdriver.Chrome(service=Service('/usr/bin/chromedriver'),options=chrome_options,desired_capabilities=desired_capabilities)
    
    driver =webdriver.Chrome(service=Service(ChromeDriverManager().install()),options=chrome_options,desired_capabilities=desired_capabilities)
    
    try:
        driver.get(url)
        driver.set_page_load_timeout(90)
        # Sleeps for 30 seconds
        time.sleep(30)
        # Gets all the logs from performance in Chrome
        logs = driver.get_log("performance")
        driver.quit()
    except TimeoutException:
        print("Page load Timeout Occured. Quiting !!!")
        logs = driver.get_log("performance")
        driver.quit()
    
    request_urls=[]
    for log in logs:
        try:
            log_message=json.loads(log["message"])["message"]
            if ("Network" in log_message["method"]):
                url=log_message["params"]["request"]["url"]
                request_urls.append(url)
        except:
            pass

    for url in request_urls:
        for provider in chat_providers:
            if (provider[0] in url):
                return "yes",provider[1]
    return "no",""


@app.get("/")
async def main(domain: str):
    return pipeline(domain)


@app.post("/")
async def root(domain: str):
    return await main(domain)


   # to run the app, run uvicorn main:app --reload
   # then, make a post request to http://localhost:8000/ with a body of {"domain": "getlyne.com"}
