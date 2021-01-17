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


#lista śłowek do przetłumaczenia
words = ['fallen', 'hund', 'holen', 'katze', 'ticket', 'klein']


# ścieżka folderu, w krótym ma być zapisany plik tekstowy z tłumaczeniem
outDir = 'C:/Users/Ola/Desktop'


myDict = {}


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
    PrivacyButtonXpath = '//button[@class="sc-bwzfXH eoPHLu"]'
    try:
        WebDriverWait(driver, 2).until(EC.element_to_be_clickable((By.XPATH, PrivacyButtonXpath))).click()
    except Exception as e:
        pass


    try:
        # german to polish
        try:
            dropDownXpath = '//div[@class="btn-group direction"]/button[@class="btn btn-large dropdown-toggle"]'
            driver.find_element(By.XPATH, dropDownXpath).click()
            germanToPolishXpath = '//a[@class="uni"]/i[@class="icon-long-arrow-right"]'
            # germanToPolishClass = 'icon-long-arrow-right'
            driver.find_element(By.XPATH, germanToPolishXpath).click()
        except:
            pass
        searchInputId = "q"
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
        polishTranslation = WebDriverWait(driver, 3).until(
            EC.presence_of_element_located((By.XPATH, polishTranslationXpath))).text
        if len(polishTranslation) > 0:
            try:
                partOfSpeechXpath = '//span[@class="wordclass"]'
                partOfSpeechClass = "wordclass"
                partOfSpeechAndArticleXpath = '//div[@class="rom first"]//./h2'
                partOfSpeechAndArticle = WebDriverWait(driver, 3).until(EC.presence_of_element_located
                                                                        ((By.XPATH, partOfSpeechAndArticleXpath))).text
                partOfSpeechAndArticle = partOfSpeechAndArticle.split("]")[-1].strip()
                # print('partOfSpeechAndArticle',partOfSpeechAndArticle)
                NounStr = 'RZ.'
                if NounStr in partOfSpeechAndArticle:
                    article = partOfSpeechAndArticle.split('. ')[1]
                 
                    finalArticle = ''
                    if article == 'r.m.':
                        finalArticle = "der"
                    elif article == 'r.ż.':
                        finalArticle = "die"
                    elif article == 'r.n.':
                        finalArticle = "das"
                    else:
                        finalArticle = ''
                    searchWord = finalArticle + " " + searchWord
                # print(searchWord + ' - ', polishTranslation)
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
        # print(myDictToString)
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
            Get book details

            Error msg: %s
            Error line no: %s
            Error type: %s
                        ''' % (str(e), exc_tb.tb_lineno, exc_type)
            print(errMsg)

    else:
        print("wrong output path")


# ponsUrl = 'https://pl.pons.com/t%C5%82umaczenie?q=&l=depl&in=de&lf=de&qnac='
ponsUrl = 'https://pl.pons.com/tłumaczenie/niemiecki-polski'
soundPath = 'sounds/win-level-51754.mp3'







start = datetime.datetime.now()
startTime = start.strftime("%H:%M:%S")
print("\n\npoczątek %s\n\n\n" % (startTime))
OpenDriver(ponsUrl)

for word in words:
    TranslateWord(word)
CloseDriver()
myStr = PrintDictionary()
print("\nsłownik\n\n"+ myStr)

dicToFile(outDir)
end = datetime.datetime.now()
endTime = end.strftime("%H:%M:%S")
print("\n\nkoniec %s\n" % (endTime))
duration = end - start
duration = str(duration).split('.')[0]
print("czas trwania", duration)
playsound(soundPath)
