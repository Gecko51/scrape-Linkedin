import time
from selenium import webdriver
from selenium.webdriver.common.by import By
import pandas as pd

LOGIN = 'votre_email@exemple.com'
PASSWORD = 'votre_mot_de_passe'

search_url = "https://www.linkedin.com/search/results/people/?eventAttending=[\"7379456428287217665\"]&origin=EVENT_PAGE_CANNED_SEARCH&page={page_num}"

options = webdriver.ChromeOptions()
# options.add_argument('--headless')  # décommente en prod sans navigateur

driver = webdriver.Chrome(options=options)

# 1. Connexion à LinkedIn
driver.get('https://www.linkedin.com/login')
time.sleep(2)
driver.find_element(By.ID, 'username').send_keys(LOGIN)
driver.find_element(By.ID, 'password').send_keys(PASSWORD)
driver.find_element(By.XPATH, '//button[@type="submit"]').click()
time.sleep(3)

results = []

for page in range(1, 32):  # Pages 1 à 31
    url = search_url.format(page_num=page)
    driver.get(url)
    time.sleep(4)
    profiles = driver.find_elements(By.CSS_SELECTOR, 'li.reusable-search__result-container')
    for prof in profiles:
        try:
            name = prof.find_element(By.CSS_SELECTOR, 'span.entity-result__title-text > a > span[aria-hidden]').text
        except:
            name = ''
        try:
            titre = prof.find_element(By.CSS_SELECTOR, 'div.entity-result__primary-subtitle').text
        except:
            titre = ''
        try:
            lieu = prof.find_element(By.CSS_SELECTOR, 'div.entity-result__secondary-subtitle').text
        except:
            lieu = ''
        try:
            lien = prof.find_element(By.CSS_SELECTOR, 'span.entity-result__title-text > a').get_attribute('href')
            # Nettoyage du lien ?miniProfileUrn...
            lien = lien.split('?')[0]
        except:
            lien = ''
        results.append({'Nom': name.strip(), 'Titre': titre.strip(), 'Lieu': lieu.strip(), 'Lien LinkedIn': lien.strip()})
    print(f"Page {page} OK")
    time.sleep(2)

driver.quit()
pd.DataFrame(results).to_csv('profils_linkedin.csv', sep=';', index=False)
print('CSV téléchargé : profils_linkedin.csv')
