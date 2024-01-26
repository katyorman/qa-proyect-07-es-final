import code
from telnetlib import EC
from typing import Tuple
import time

from selenium.common import NoSuchElementException, TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
import data
from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
import pytest
from selenium.common.exceptions import NoSuchElementException


# no modificar
def retrieve_phone_code(driver) -> str:
    """Este código devuelve un número de confirmación de teléfono y lo devuelve como un string.
    Utilízalo cuando la aplicación espere el código de confirmación para pasarlo a tus pruebas.
    El código de confirmación del teléfono solo se puede obtener después de haberlo solicitado en la aplicación."""

    import json
    import time
    from selenium.common import WebDriverException
    code = None
    for i in range(10):
        try:
            logs = [log["message"] for log in driver.get_log('performance') if log.get("message")
                    and 'api/v1/number?number' in log.get("message")]
            for log in reversed(logs):
                message_data = json.loads(log)["message"]
                body = driver.execute_cdp_cmd('Network.getResponseBody',
                                              {'requestId': message_data["params"]["requestId"]})
                code = ''.join([x for x in body['body'] if x.isdigit()])
        except WebDriverException:
            time.sleep(1)
            continue
        if not code:
            raise Exception("No se encontró el código de confirmación del teléfono.\n"
                            "Utiliza 'retrieve_phone_code' solo después de haber solicitado el código en tu aplicación.")
        return code

class UrbanRoutesPage:
    # Ruta
    from_field = (By.ID, 'from')
    to_field = (By.ID, 'to')
    # Click boton "Pedir Taxi"
    pedir_taxi_locator = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[1]/div[3]/div[1]/button')
    # Seleccionar la tarifa conford
    tarifa_conford = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[1]/div[5]')
    # Clic al campo numero de telefono
    campo_telefono = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[1]/div')
    # Ingresar numero de telefono
    numero_telefono = (By.ID, 'phone')
    #Boton siguiente al ingresar numero de telefono
    siguiente_telefono = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[1]/form/div[2]/button')
    # Clic campo code
    campo_code = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[1]/div[1]')
    # Agregar el code
    phone_code = (By.XPATH, '//*[@id="code"]')
    #Clic boton confirmar code
    confirmar_code = (By.XPATH, '//*[@id="root"]/div/div[1]/div[2]/div[2]/form/div[2]/button[1]')
    #Seleccionar Forma de pago
    seleccionar_forma_pago = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[2]')
    #Boton de agregar tarjeta
    boton_agregar_tarjeta = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/div[2]/div[3]')
    # Clic campo agregar tarjeta
    campo_tarjeta = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]')
    # Agregar numero de tarjeta
    agregar_numero_tarjeta = (By.XPATH, '//*[@id="number"]')
    # Clic campo agregar CVV
    campo_cvv = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[1]/div[2]/div[2]/div[2]')
    # Agregar numero de CVV
    agregar_numero_cvv = (By.XPATH, '//*[@id="code" and contains(@class, "card-input")]')
    # Click tab
    enfoque = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form')
    # Clic boton enlace
    boton_enlace = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form/div[3]/button[1]')
    # Cierre ventana de pago
    cierre_pago = (By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[1]/button')
    # Click campo para el mensaje al controlador
    campo_mensaje = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[3]/div')
    # Mensaje al controlador
    agregar_mensaje_conductor = (By.XPATH, '//*[@id="comment"]')
    # Mantas y pañuelos
    pedir_mantas = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[1]/div/div[2]/div/span')
    # Pedir 2 Helados
    pedir_helados = (By.XPATH, '//*[@id="root"]/div/div[3]/div[3]/div[2]/div[2]/div[4]/div[2]/div[3]/div/div[2]/div[1]/div/div[2]/div/div[3]')
    # Pedir Taxi
    pedir_taxi = (By.XPATH, '//*[@id="root"]/div/div[3]/div[4]/button')

    def __init__(self, driver):
        self.pedir_helado = None
        self.agregar_mensaje_conductor_field = None
        self.enfoque = None
        self.agregar_numero_cvv_field = None
        self.agregar_numero_tarjeta_field = None
        self.phone_number = None
        self.driver = driver

    def set_from(self, address_from):
        self.driver.find_element(*self.from_field).send_keys(address_from)

    def set_to(self, address_to):
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def get_from(self):
        return self.driver.find_element(*self.from_field).get_property('value')

    def get_to(self):
        return self.driver.find_element(*self.to_field).get_property('value')

    def set_route(self, address_from, address_to):
        self.driver.find_element(*self.from_field).send_keys(address_from)
        self.driver.find_element(*self.to_field).send_keys(address_to)

    def click_pedir_taxi_locator(self):
        self.driver.find_element(*self.pedir_taxi_locator).click()

    def click_tarifa_conford(self):
        self.driver.find_element(*self.tarifa_conford).click()

    def click_campo_telefono(self):
        self.driver.find_element(*self.campo_telefono).click()

    def get_phone_number(self):
        return self.driver.find_element(*self.phone_number).get_property('value')

    def set_phone_number(self, phone_number):
        data.phone_number = phone_number
        self.driver.find_element(*self.numero_telefono).send_keys(phone_number)

    def click_siguiente_telefono(self):
        self.driver.find_element(*self.siguiente_telefono).click()

    def click_campo_code(self):
        self.driver.find_element(*self.campo_code).click()

    def get_phone_code(self):
        return self.driver.find_element(*self.phone_code).get_property('value')

    def set_phone_code(self):
        phone_code = retrieve_phone_code(self.driver)
        self.driver.find_element(*self.phone_code).send_keys(str(phone_code))

    def click_confirmar_code(self):
        self.driver.find_element(*self.confirmar_code).click()

    def click_seleccionar_forma_pago(self):
        self.driver.find_element(*self.seleccionar_forma_pago).click()

    def click_boton_agregar_tarjeta(self):
        self.driver.find_element(*self.boton_agregar_tarjeta).click()

    def click_campo_tarjeta(self):
        self.driver.find_element(*self.campo_tarjeta).click()

    def set_agregar_numero_tarjeta(self, card_number):
        self.driver.find_element(*self.agregar_numero_tarjeta).send_keys(card_number)

    def get_agregar_numero_tarjeta(self):
        return self.driver.find_element(*self.agregar_numero_tarjeta_field).get_property('value')

    def click_campo_cvv(self):
        self.driver.find_element(*self.campo_cvv).click()

    def set_agregar_numero_cvv(self, card_code):
        self.driver.find_element(*self.agregar_numero_cvv).send_keys(card_code)

    def get_agregar_numero_cvv(self):
        return self.driver.find_element(*self.agregar_numero_cvv_field).get_property('value')

    def enfoque(self):
        self.driver.find_element(*self.enfoque).click()

    def click_boton_enlace(self):
        self.driver.find_element(*self.boton_enlace).click()

    def click_cierre_pago(self):
        self.driver.find_element(*self.cierre_pago).click()

    def click_campo_mensaje(self):
        self.driver.find_element(*self.campo_mensaje).click()

    def set_agregar_mensaje_conductor(self, message_for_driver):
        self.driver.find_element(*self.agregar_mensaje_conductor).send_keys(message_for_driver)

    def get_agregar_mensaje_conductor(self):
        return self.driver.find_element(*self.agregar_mensaje_conductor_field).get_property('value')

    def click_pedir_mantas(self):
        self.driver.find_element(*self.pedir_mantas).click()

    def click_pedir_helado(self):
        self.driver.find_element(*self.pedir_helado).click()

    def click_pedir_taxi(self):
        self.driver.find_element(*self.pedir_taxi).click()
class TestUrbanRoutes:
    driver = None

    @classmethod
    def setup_class(cls):  # Configuración inicial de la clase de prueba

        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_experimental_option("perfLoggingPrefs", {'enableNetwork': True, 'enablePage': True})
        chrome_options.set_capability("goog:loggingPrefs", {'performance': 'ALL'})
        cls.driver = webdriver.Chrome(options=chrome_options)
        cls.driver.maximize_window()
        cls.driver.get(data.urban_routes_url)
        cls.routes_page = UrbanRoutesPage(cls.driver)

    def test_set_route(self):
        routes_page = UrbanRoutesPage(self.driver)
        address_from = data.address_from
        address_to = data.address_to
        time.sleep(3)
        # Espera hasta que el campo "from" sea visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.from_field))
        # Espera hasta que el campo "from" sea visible
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.to_field))

        routes_page.set_route(address_from, address_to)

        assert routes_page.get_from() == address_from
        assert routes_page.get_to() == address_to

    def test_click_pedir_taxi_locator(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.pedir_taxi_locator))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.pedir_taxi_locator))
        time.sleep(3)
        self.driver.find_element(*routes_page.pedir_taxi_locator).click()

        assert self.driver.find_element(
            *routes_page.pedir_taxi_locator).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'Pedir Taxi'"

    def test_tarifa_conford(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.tarifa_conford))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.tarifa_conford))
        time.sleep(3)
        self.driver.find_element(*routes_page.tarifa_conford).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.tarifa_conford))

        assert self.driver.find_element(
            *routes_page.tarifa_conford).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'Conford'"

    def test_campo_telefono(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_telefono))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.campo_telefono))
        time.sleep(3)
        self.driver.find_element(*routes_page.campo_telefono).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_telefono))

        assert self.driver.find_element(
            *routes_page.campo_telefono).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'telefono'"

    def test_set_phone_number(self):
        # Establecer el número de teléfono
        phone_number = data.phone_number
        self.routes_page.set_phone_number(phone_number)
        time.sleep(3)
        # Verificar si el número de teléfono establecido es igual al número de teléfono recuperado
        assert data.phone_number == phone_number

    def test_click_siguiente_telefono(self):
        routes_page = UrbanRoutesPage(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.siguiente_telefono))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.siguiente_telefono))
            time.sleep(3)
            # Hacer clic en el botón "Siguiente"
            self.driver.find_element(*routes_page.siguiente_telefono).click()

            # Esperar a que el elemento esté visible después del clic
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.siguiente_telefono))

            # Verificar si el elemento es visible
            nuevo_elemento = self.driver.find_element(*routes_page.siguiente_telefono)
            assert nuevo_elemento.is_displayed(), "El elemento no está visible después de hacer clic en 'siguiente'"

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error durante la ejecución de la prueba: {e}")

    def test_click_campo_code(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_code))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.campo_code))
        time.sleep(3)
        self.driver.find_element(*routes_page.campo_code).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_code))

        assert self.driver.find_element(
            *routes_page.campo_code).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'campo code'"

    def test_phone_code(self):
        # Establecer el código
        self.routes_page.set_phone_code()
        time.sleep(3)
        # Obtener el código establecido
        phone_code = self.routes_page.get_phone_code()

        # Esperar hasta que el código sea visible (ajusta según sea necesario)
        WebDriverWait(self.driver, timeout=10).until(
            EC.text_to_be_present_in_element_value(self.routes_page.phone_code, phone_code)
        )

        # Obtener el código después de la espera
        code_after_wait = self.routes_page.get_phone_code()

        # Verificar si el código antes y después de la espera es el mismo
        assert phone_code == code_after_wait

    def test_confirmar_code(self):
        routes_page = UrbanRoutesPage(self.driver)

        try:
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.confirmar_code))
            WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.confirmar_code))
            time.sleep(3)
            # Hacer clic en el botón "Siguiente"
            self.driver.find_element(*routes_page.confirmar_code).click()

            # Esperar a que el elemento esté visible después del clic
            WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.confirmar_code))

            # Verificar si el elemento es visible
            nuevo_elemento = self.driver.find_element(*routes_page.confirmar_code)
            assert nuevo_elemento.is_displayed(), "El elemento no está visible después de hacer clic en 'siguiente'"

        except (NoSuchElementException, TimeoutException) as e:
            print(f"Error durante la ejecución de la prueba: {e}")

    def test_click_seleccionar_forma_pago(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.seleccionar_forma_pago))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.seleccionar_forma_pago))
        time.sleep(3)
        self.driver.find_element(*routes_page.seleccionar_forma_pago).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.seleccionar_forma_pago))

        assert self.driver.find_element(
            *routes_page.seleccionar_forma_pago).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'forma de pago'"
    def test_click_boton_agregar_tarjeta(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.boton_agregar_tarjeta))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.boton_agregar_tarjeta))
        time.sleep(3)
        # Guardar el estado de visibilidad antes de hacer clic
        is_boton_agregar_tarjeta_visible_before_click = self.driver.find_element(*routes_page.boton_agregar_tarjeta).is_displayed()
        # Hacer clic en 'agregar tarjeta'
        self.driver.find_element(*routes_page.boton_agregar_tarjeta).click()
        # Esperar a que el botón 'agregar tarjeta' ya no esté visible
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(routes_page.boton_agregar_tarjeta))
        # Verificar que el botón 'agregar tarjeta' estaba visible antes de hacer clic
        assert is_boton_agregar_tarjeta_visible_before_click, "El botón 'agregar tarjeta' no estaba visible antes de hacer clic"

    def test_campo_tarjeta(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_tarjeta))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.campo_tarjeta))
        time.sleep(3)
        self.driver.find_element(*routes_page.campo_tarjeta).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_tarjeta))

        assert self.driver.find_element(
            *routes_page.campo_tarjeta).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'tarjeta'"
    def test_set_agregar_numero_tarjeta(self):
        # Establecer el número de tarjeta
        agregar_numero_tarjeta = data.card_number
        self.routes_page.set_agregar_numero_tarjeta(agregar_numero_tarjeta)
        time.sleep(3)
        # Verificar si el número de tarjeta establecido es igual al número de tarjeta recuperado
        assert data.card_number == agregar_numero_tarjeta

    def test_campo_cvv(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_cvv))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.campo_cvv))
        time.sleep(3)
        self.driver.find_element(*routes_page.campo_cvv).click()

        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_cvv))

        assert self.driver.find_element(
            *routes_page.campo_cvv).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'CVV'"

    def test_set_agregar_numero_cvv(self):
        # Establecer el número de cvv
        agregar_numero_cvv = data.card_code
        self.routes_page.set_agregar_numero_cvv(agregar_numero_cvv)
        time.sleep(3)
        # Verificar si el número de cvv establecido es igual al número de cvv recuperado
        assert data.card_code == agregar_numero_cvv

    def test_click_enfoque(self):
        # Espera hasta que el elemento que quieres enfocar sea visible
        enfoque_elements = WebDriverWait(self.driver, 10).until(
            EC.presence_of_all_elements_located((By.XPATH, '//*[@id="root"]/div/div[2]/div[2]/div[2]/form'))
        )
        # Verifica si la lista de elementos no está vacía antes de continuar
        if enfoque_elements:
            enfoque = enfoque_elements[0]
            # Hacer clic en el elemento para asegurarse de que tenga el foco
            enfoque.click()
            # Simula la pulsación de la tecla Tab
            enfoque.send_keys(Keys.TAB)
            time.sleep(3)
        else:
            print("No se encontró el elemento o no fue visible.")
    def test_click_boton_enlace(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.boton_enlace))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.boton_enlace))
        time.sleep(3)
        # Guardar el estado de visibilidad antes de hacer clic
        is_boton_enlace_visible_before_click = self.driver.find_element(*routes_page.boton_enlace).is_displayed()
        # Hacer clic en 'boton enlace'
        self.driver.find_element(*routes_page.boton_enlace).click()
        # Esperar a que el botón 'boton enlace' ya no esté visible
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(routes_page.boton_enlace))
        # Verificar que el botón 'boton enlace' estaba visible antes de hacer clic
        assert is_boton_enlace_visible_before_click, "El botón 'Cerrar pago' no estaba visible antes de hacer clic"
    def test_click_cierre_pago(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.cierre_pago))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.cierre_pago))
        time.sleep(3)
        # Guardar el estado de visibilidad antes de hacer clic
        is_cierre_pago_visible_before_click = self.driver.find_element(*routes_page.cierre_pago).is_displayed()
        # Hacer clic en 'Cerrar pago'
        self.driver.find_element(*routes_page.cierre_pago).click()
        # Esperar a que el botón 'Cerrar pago' ya no esté visible
        WebDriverWait(self.driver, 10).until_not(EC.visibility_of_element_located(routes_page.cierre_pago))
        # Verificar que el botón 'Cerrar pago' estaba visible antes de hacer clic
        assert is_cierre_pago_visible_before_click, "El botón 'Cerrar pago' no estaba visible antes de hacer clic"

    def test_click_campo_mensaje(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.campo_mensaje))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.campo_mensaje))
        time.sleep(3)
        # Guardar el estado de visibilidad antes de hacer clic
        is_campo_mensaje_visible_before_click = self.driver.find_element(*routes_page.campo_mensaje).is_displayed()
        # Hacer clic en 'campo mensaje'
        self.driver.find_element(*routes_page.campo_mensaje).click()
        # Verificar que el botón 'campo mensaje' estaba visible antes de hacer clic
        assert is_campo_mensaje_visible_before_click, "El botón 'mensaje' no estaba visible antes de hacer clic"

    def test_set_mensaje_conductor(self):
        # Establecer el mensaje
        time.sleep(3)
        agregar_mensaje_conductor = data.message_for_driver
        self.routes_page.set_agregar_mensaje_conductor(agregar_mensaje_conductor)
        time.sleep(3)
        assert data.message_for_driver == agregar_mensaje_conductor

    def test_click_pedir_mantas(self):
        routes_page = UrbanRoutesPage(self.driver)

        # Espera hasta que el toggle button 'pedir_mantas' sea visible y clickeable
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.pedir_mantas))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.pedir_mantas))
        time.sleep(2)
        # Guardar el estado de visibilidad antes de hacer clic
        is_pedir_mantas_visible_before_click = self.driver.find_element(*routes_page.pedir_mantas).is_displayed()
        time.sleep(2)
        # Hacer clic en el toggle button 'pedir_mantas' para activarlo
        self.driver.find_element(*routes_page.pedir_mantas).click()

        # Verificar que el botón 'pedir_mantas' estaba visible antes de hacer clic
        assert is_pedir_mantas_visible_before_click, "El botón 'pedir_mantas' no estaba visible antes de hacer clic"

    def test_click_pedir_helados(self, cantidad=2):
        routes_page = UrbanRoutesPage(self.driver)
        time.sleep(2)
        # Espera hasta que el toggle button 'pedir_helados' sea visible y clickeable
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.pedir_helados))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.pedir_helados))

        for _ in range(cantidad):
            # Guardar el estado de visibilidad antes de hacer clic
            is_pedir_helados_visible_before_click = self.driver.find_element(*routes_page.pedir_helados).is_displayed()

            # Hacer clic en el toggle button 'pedir_helados' para activarlo
            self.driver.find_element(*routes_page.pedir_helados).click()
            time.sleep(3)
            # Verificar que el botón 'pedir_helados' estaba visible antes de hacer clic
            assert is_pedir_helados_visible_before_click, "El botón 'pedir_helados' no estaba visible antes de hacer clic"

    def test_click_pedir_taxi(self):
        routes_page = UrbanRoutesPage(self.driver)
        WebDriverWait(self.driver, 10).until(EC.visibility_of_element_located(routes_page.pedir_taxi))
        WebDriverWait(self.driver, 10).until(EC.element_to_be_clickable(routes_page.pedir_taxi))
        time.sleep(5)
        self.driver.find_element(*routes_page.pedir_taxi).click()

        assert self.driver.find_element(
            *routes_page.pedir_taxi).is_displayed(), "No se encontró el nuevo elemento después de hacer clic en 'Pedir Taxi'"
    @classmethod
    def teardown_class(cls):
        cls.driver.quit()
