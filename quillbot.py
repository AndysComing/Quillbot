import time
import io
import sys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from webdriver_manager.chrome import ChromeDriverManager
import requests
import json
import customtkinter as ck
from tkinter import *


networkScript = """
var performance = window.performance || window.webkitPerformance || {};
var network = performance.getEntries() || {};
return network;
"""

def init():
    global driver
    caps = DesiredCapabilities.CHROME
    caps['goog:loggingPrefs'] = {'performance': 'ALL'}
    driver = webdriver.Chrome(desired_capabilities=caps, service=Service(ChromeDriverManager().install()))

    driver.get("https://www.quill.org/session/new")

def getAnswer(id):
    response = requests.get(id)
    json = response.json()
    for element in json:
        if (element.get("optimal")) == True:
            return(element.get("text"))

def process_browser_log_entry(entry):
    response = json.loads(entry['message'])['message']
    return response

def glogin():
    global email
    global password
    global waittime
    global driver
    try:
        if waittime == "":
            waittime = 0.1
        else:
            waittime = float(waittime.get())
    except:
        waittime = 0.1
    email = email.get()
    password = password.get()
    window.destroy()
    init()
    if password != "" and email != "":
        step = 0
        while step == 0:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, "/html/body/div[3]/div/div/div/div/div[1]/form/button")))
                driver.find_element(By.XPATH, "/html/body/div[3]/div/div/div/div/div[1]/form/button").click()
                time.sleep(.5)
                step = step + 1
            except:
                pass
        while step == 1:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "identifier")))
                driver.find_element(By.NAME, "identifier").clear()
                driver.find_element(By.NAME, "identifier").send_keys(email)
                driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
                time.sleep(.5)
                step = step + 1
            except:
                pass
        while step == 2:
            try:
                WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.NAME, "password")))
                driver.find_element(By.NAME, "password").send_keys(password)
                time.sleep(.5)
                driver.find_element(By.XPATH,"/html/body/div[1]/div[1]/div[2]/div/div[2]/div/div/div[2]/div/div[2]/div/div[1]/div/div/button").click()
                step = step + 1
            except:
                pass


def elogin():
    global email
    global password
    global waittime
    global driver
    try:
        if waittime == "":
            waittime = 0.1
        else:
            waittime = float(waittime.get())
    except:
        waittime = 0.1
    email = email.get()
    password = password.get()
    window.destroy()
    init()
    if password != "" and email != "":
        try:
            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, '//*[@id="email-or-username"]')))
            driver.find_element(By.XPATH, '//*[@id="email-or-username"]').send_keys(email)
            driver.find_element(By.XPATH, '//*[@id="password"]').send_keys(password)
            driver.find_element(By.ID, "log-in").click()
        except:
            pass


ck.set_appearance_mode("system")

buffer = io.StringIO()
sys.stdout = buffer
sys.stderr = buffer

window = ck.CTk()
window.title("Quillbot V1")
window.geometry("250x200")

email = ck.CTkEntry(master=window,placeholder_text="Email")
email.place(relx=.5,rely=.2,anchor=CENTER)

password = ck.CTkEntry(master=window,placeholder_text="Password")
password.place(relx=.5,rely=.35,anchor=CENTER)

waittime = ck.CTkEntry(master=window,placeholder_text="Sec/Question")
waittime.place(relx=.5,rely=.5,anchor=CENTER)

glogin = ck.CTkButton(master=window, text="Login with gmail", command=glogin)
glogin.place(relx=.5,rely=.7,anchor=CENTER)

elogin = ck.CTkButton(master=window, text="Login with email", command=elogin)
elogin.place(relx=.5,rely=.85,anchor=CENTER)

window.mainloop()





def shortanswer():
    try:
        global waittime
        time.sleep(waittime)
        networkRequests = driver.execute_script(networkScript)
        time.sleep(1)
        response = [request['name'] for request in networkRequests if request['name'].split("/")[-1].startswith("response")]
        mcq = [request['name'] for request in networkRequests if request['name'].split("/")[-1].startswith("multiple_choice_options")]
        URLs = response + mcq
        text = getAnswer(str(URLs[-1]))
        first = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div[1]/div/div/div[1]/span[1]").text
        second = driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div[1]/div/div/div[1]/span[3]").text
        answer = text.replace(first, "")
        answer = answer.replace(second, "")
        driver.find_element(By.XPATH,'//*[@id="input0"]').clear()
        driver.find_element(By.XPATH, '//*[@id="input0"]').send_keys(answer)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div[2]/button").click()
        time.sleep(.25)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div[2]/button").click()

        print("Short Answer")

    except:
        print("error")

def longanswer():
    try:
        global waittime
        time.sleep(waittime)
        networkRequests = driver.execute_script(networkScript)
        time.sleep(1)
        response = [request['name'] for request in networkRequests if request['name'].split("/")[-1].startswith("response")]
        mcq = [request['name'] for request in networkRequests if request['name'].split("/")[-1].startswith("multiple_choice_options")]
        URLs = response + mcq
        text = getAnswer(str(URLs[-1]))
        answer = text
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div/div[2]/div[3]/div/div/div').clear()
        driver.find_element(By.XPATH,'/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div/div[2]/div[3]/div/div/div').send_keys(answer)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div/div[2]/div[4]/button").click()
        time.sleep(.25)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div/div[2]/div[4]/button").click()
        time.sleep(.25)
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div/div[2]/div[4]/button").click()
        print("Long Answer")
    except:
        print("error")


def check():
    try:
        driver.find_element(By.XPATH, "//a[text()='Resume']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//span[text()='Resume']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//span[text()='Begin']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//button[text()='Start activity']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//a[text()='Start']").click()
    except:
        pass
    try:
        driver.find_element(By.XPATH, "//a[text()='Back to your dashboard']").click()
    except:
        pass

while True:

    check()

    try:
        driver.find_element(By.XPATH,"/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div/div[1]")
        print("Found")
        try:
            driver.find_element(By.XPATH, "/html/body/div[1]/div/div/main/div[2]/div/section/div[2]/div/div[1]/div/div/div[1]/span[1]")
            shortanswer()
        except:
            longanswer()
    except:
        pass
    try:
        driver.current_url
        time.sleep(.25)
    except:
        print("exit")
        sys.exit()






















