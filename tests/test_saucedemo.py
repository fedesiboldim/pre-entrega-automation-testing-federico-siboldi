import pytest
from selenium.webdriver.common.by import By
from utils.helpers import init_driver, login_saucedemo, esperar_elemento

@pytest.fixture
def driver():
    """Fixture de Pytest: abre Chrome antes de cada test y lo cierra al finalizar."""
    driver = init_driver()
    yield driver
    driver.quit()

def test_login_exitoso(driver):
    """Caso 1: Verifica login válido y redirección a la página de inventario."""
    login_saucedemo(driver)
    assert "/inventory.html" in driver.current_url
    titulo = esperar_elemento(driver, By.CSS_SELECTOR, "span.title")
    assert titulo.text.lower() == "products"

def test_catalogo_productos(driver):
    """Caso 2: Verifica catalogo, elementos de interfaz y lista nombres/precios."""
    login_saucedemo(driver)
    
    # 1. Validar título visible
    titulo = esperar_elemento(driver, By.CSS_SELECTOR, "span.title")
    assert titulo.is_displayed()
    
    # 2. Comprobar existencia y listar nombres y precios
    productos = driver.find_elements(By.CLASS_NAME, "inventory_item")
    assert len(productos) > 0, "No se encontraron productos en el inventario."
    
    for item in productos:
        nombre = item.find_element(By.CLASS_NAME, "inventory_item_name").text
        precio = item.find_element(By.CLASS_NAME, "inventory_item_price").text
        assert nombre != "", "El producto no tiene nombre"
        assert "$" in precio, "El precio no tiene formato valido"
        print(f"Producto: {nombre} | Precio: {precio}")

    # 3. Validar menú y selector de filtros
    menu_btn = driver.find_element(By.ID, "react-burger-menu-btn")
    filtro = driver.find_element(By.CLASS_NAME, "product_sort_container")
    assert menu_btn.is_displayed()
    assert filtro.is_displayed()

def test_interaccion_carrito(driver):
    """Caso 3: Añade producto al carrito, valida badge y confirma presencia en el carrito."""
    login_saucedemo(driver)
    
    # Clic en agregar producto
    btn_agregar = esperar_elemento(driver, By.ID, "add-to-cart-sauce-labs-backpack")
    btn_agregar.click()
    
    # Validar incremento del contador en el carrito
    badge = esperar_elemento(driver, By.CLASS_NAME, "shopping_cart_badge")
    assert badge.text == "1"
    
    # Navegar al carrito
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    
    # Validar que el producto aparezca listado
    item = esperar_elemento(driver, By.CLASS_NAME, "inventory_item_name")
    assert item.text == "Sauce Labs Backpack"