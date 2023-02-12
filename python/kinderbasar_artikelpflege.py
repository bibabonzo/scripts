from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import csv
import time
import sys
import getopt

USERNAME = ""
PASSWORD = ""
DATASOURCE_PATH = ""

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
driver = webdriver.Chrome(executable_path="/Users/joachim/chromedriver", chrome_options=chrome_options)
driver.maximize_window()

def readArgs(argv):
  global USERNAME
  global PASSWORD
  global DATASOURCE_PATH

  opts, args = getopt.getopt(argv,"hu:p:f:",["username=","password=","file="])
  
  for opt, arg in opts:
    if opt == '-h':
      print ('test.py -u <username> -p <password> -f <file>')
      sys.exit()
    elif opt in ("-u", "--username"):
      USERNAME = arg
    elif opt in ("-p", "--password"):
      PASSWORD = arg
    elif opt in ("-f", "--file"):
      DATASOURCE_PATH = arg

def login(url, driver):
  driver.get(url)
  driver.find_element(By.ID, "username").send_keys(USERNAME)
  driver.find_element(By.ID, "password").send_keys(PASSWORD)
  driver.find_element(By.CLASS_NAME, "btn-primary").click()

def createNewArticle(size, color, description, price):
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Größe")))
  driver.find_element(By.ID, "Größe").send_keys(size)
  driver.find_element(By.ID, "Farbe").send_keys(color)
  driver.find_element(By.ID, "Beschreibung").send_keys(description)
  driver.find_element(By.ID, "price").send_keys(price)
  WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.ID, "article_submit")))
  driver.find_element(By.ID, "article_submit").click()

if __name__ == "__main__":
  # Kommandozeilen-Argumente einlesen
  readArgs(sys.argv[1:])

  # Einloggen
  login("https://www.easybasar.de/einloggen", driver)

  # Skript pausieren bis Artikeleingabemaske geladen ist
  driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
  WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "Größe")))

  # Artikel erfassen
  with open(DATASOURCE_PATH, 'r') as file:
      csvreader = csv.reader(file, delimiter=';')
      header = next(csvreader)
      for row in csvreader:
        createNewArticle(row[1], row[2], row[0], row[3])
        time.sleep(5)