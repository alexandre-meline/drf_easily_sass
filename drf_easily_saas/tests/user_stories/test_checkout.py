from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Django
from django.contrib.auth.models import User

# Drf Easily Saas
from drf_easily_saas.settings import FRONTEND_URL
from drf_easily_saas.payment.manager import StripeManager



# -------------------------------------------- #
# User
# -------------------------------------------- #
# Create a user
user = User.objects.create_user(username='testuser', password='12345')

# -------------------------------------------- #

# -------------------------------------------- #
# Crea



# Remplacez 'chrome' par le navigateur de votre choix (ex: 'firefox')
# Assurez-vous d'avoir installé le pilote de navigateur correspondant
driver = webdriver.Chrome()

# Remplacez 'URL_DE_VOTRE_APPLICATION' par l'URL de votre application
driver.get('URL_DE_VOTRE_APPLICATION')

# Attendre que le formulaire soit chargé
WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'form-id')))

# Remplacer 'form-id' par l'ID réel de votre formulaire
form = driver.find_element(By.ID, 'form-id')

# Remplir le numéro de carte
card_number_input = form.find_element(By.NAME, 'card_number')
card_number_input.send_keys('4242424242424242')

# Remplir le mois et l'année d'expiration
expiration_month_input = form.find_element(By.NAME, 'expiration_month')
expiration_month_input.send_keys('12')

expiration_year_input = form.find_element(By.NAME, 'expiration_year')
expiration_year_input.send_keys('2025')

# Remplir le CVC
cvc_input = form.find_element(By.NAME, 'cvc')
cvc_input.send_keys('123')

# Remplir le nom et le prénom
name_input = form.find_element(By.NAME, 'name')
name_input.send_keys('John Doe')

# Cliquer sur le bouton d'envoi
submit_button = form.find_element(By.NAME, 'submit')
submit_button.click()

# Attendre que la page suivante soit chargée
WebDriverWait(driver, 10).until(EC.title_contains('Titre de la page suivante'))

# Fermer le navigateur
driver.quit()
