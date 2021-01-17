
import datetime
import os
import sys

import selenium
from playsound import playsound
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

myDict = {}

#lista słówek do tłuumaczenia
words = ['sleep', 'cat', 'dog', 'run', "Santa Claus", 'nice']

#ścieżka folderu, do którego ma być zapisany pilik tekstowy z tłumaczeniem
outDir = 'C:/Users/Ola/Desktop'

def OpenDriver(url):
    global driver
    try:
        ChromeDriverPath = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
        driver = selenium.webdriver.Chrome(ChromeDriverPath)
        driver.implicitly_wait(5)
        driver.maximize_window()
        driver.get(url)
    except Exception as e:
        print("OpenDriver problem\n" + str(e))
        exit()


def TranslateWord(searchWord):
    global driver
    global myDict

    PrivacyButtonXpath = '//button[@mode="primary"]'
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, PrivacyButtonXpath))).click()
    except Exception as e:
        pass

    try:
        dropDownXpath = '//div[@class="btn-group direction"]/button[@class="btn btn-large dropdown-toggle"]'
        driver.find_element(By.XPATH, dropDownXpath).click()
        EnglishToPolishXpath = '//a[@class="uni"]/i[@class="icon-long-arrow-right"]'
        driver.find_element(By.XPATH, EnglishToPolishXpath).click()
    except:
        pass



    searchInputId = "q"
    try:
        searchInput = WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, searchInputId)))
        searchInput.clear()
        searchInput.send_keys(searchWord)
        searchInput.send_keys(Keys.ENTER)
    except Exception as e:
        print("searchInput problem\n" + str(e))
        exit()
    try:
        noWordXpath = '//strong[contains(text(), "Widzisz podobne wyniki:")]'
        element = driver.find_element(By.XPATH, noWordXpath)
        print(searchWord + " - nie ma takiego słowa")
    except:
        polishTranslationXpath = '//dl[@class="dl-horizontal kne first"]/dd[@class="dd-inner"]/div'
        try:
            polishTranslation = WebDriverWait(driver, 3).until(
                EC.presence_of_element_located((By.XPATH, polishTranslationXpath))).text
            if len(polishTranslation) > 0:
                print(searchWord + ' - ', polishTranslation)
                myDict.update({searchWord: polishTranslation})
        except Exception as e:
            print("wywaliło sie na %s z powodu:\n%s" % (searchWord, str(e)))
         

def CloseDriver():
    global driver
    try:
        driver.quit()
    except Exception as e:
        print('CloseDriver problem\n' + str(e))


def PrintDictionary():
    global myDict
    try:
        myDictToString = ''
        for k, v in myDict.items():
            myDictToString = myDictToString + k + ' - ' + v + '\n'
        #print(myDictToString)
        return myDictToString

    except Exception as e:
        print('PrintDictionary\n' + str(e))
        return ''


def dicToFile(outPath):
    if os.path.isdir(outPath):
        try:
            now = datetime.datetime.now()
            currTime = now.strftime('%Y-%m-%d__%H-%M-%S')
            fileName = "translation_" + currTime + '.txt'
            outputFile = outPath + '/' + fileName
            file = open(outputFile, 'w', encoding='utf-8')
            fileText = str(PrintDictionary())
            file.write(fileText)
            file.close()
        except Exception as e:
            print('dicToFile problem\n' + str(e))
            exc_type, exc_obj, exc_tb = sys.exc_info()
            errMsg = '''
            dicToFile(

            Error msg: %s
            Error line no: %s
            Error type: %s
                        ''' % (str(e), exc_tb.tb_lineno, exc_type)
            print(errMsg)

    else:
        print("wrong output path")



ponsUrl='https://pl.pons.com/t%C5%82umaczenie/angielski-polski'
soundPath = 'sounds/win-level-51754.mp3'


start = datetime.datetime.now()
startTime = start.strftime("%H:%M:%S")
print("\n\npoczątek %s\n\n\n" % (startTime))
OpenDriver(ponsUrl)

for word in words:
    word = word.strip()
    TranslateWord(word)
CloseDriver()

dicToFile(outDir)
end = datetime.datetime.now()
endTime = end.strftime("%H:%M:%S")
print("\n\nkoniec %s\n" % (endTime))
duration = end - start
duration = str(duration).split('.')[0]
print("czas trwania", duration)
playsound(soundPath)
