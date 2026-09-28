from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def init_driver():
    """Abre el navegador Chrome y lo maximiza."""
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    driver = webdriver.Chrome(options=options)
    return driver

def esperar_elemento(driver, by, locator, timeout=10):
    """Espera explícita de hasta 10 segundos hasta que el elemento esté visible."""
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located((by, locator)))

def login_saucedemo(driver, username="standard_user", password="secret_sauce"):
    """Navega a saucedemo.com y realiza el login completando credenciales."""
    driver.get("https://www.saucedemo.com/")
    
    # Ingresar usuario
    user_input = esperar_elemento(driver, By.ID, "user-name")
    user_input.clear()
    user_input.send_keys(username)
    
    # Ingresar contraseña
    pass_input = driver.find_element(By.ID, "password")
    pass_input.clear()
    pass_input.send_keys(password)
    
    # Clic en login
    driver.find_element(By.ID, "login-button").click()
    
    # Validar redirección a inventario
    WebDriverWait(driver, 10).until(EC.url_contains("/inventory.html"))