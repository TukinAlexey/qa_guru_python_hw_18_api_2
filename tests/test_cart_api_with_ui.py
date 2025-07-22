import json

import requests

from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have, be

import allure

LOGIN = "example4705@example.com"
PASSWORD = "123456"
URL = "https://demowebshop.tricentis.com/"


@allure.title("Добавление товара в корзину")
def test_add_product_in_cart():
    with step("Авторизация через API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with step("Получаем cookie через API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step('Добавить товар в корзину через API'):
        response = requests.post(
            url=URL + 'addproducttocart/details/31/1',
            data={f"addtocart_31.EnteredQuantity": str(1)},
            cookies={'NOPCOMMERCE.AUTH': cookie}
        )
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")
        assert response.status_code == 200

    with step("Открываем корзину с добавленным товаром"):
        browser.open('https://demowebshop.tricentis.com/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('https://demowebshop.tricentis.com/cart')

    with step("Проверяем что товар в корзине"):
        browser.element('.product-name').should(have.exact_text('14.1-inch Laptop'))
        browser.element('[value="1"][type="text"]').should(be.visible)

    with step('Очистка корзины'):
        browser.element('.qty-input').clear()
        browser.element('.qty-input').set_value('0').press_enter()


@allure.title("Добавление нескольких единиц одного товара в корзину")
def test_add_some_product_in_cart():
    with step("Авторизация через API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with step("Получаем cookie через API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step('Добавляем несколько единиц одного товара в корзину'):
        response = requests.post(
            url=URL + 'addproducttocart/details/31/1',
            data={f"addtocart_31.EnteredQuantity": str(5)},
            cookies={'NOPCOMMERCE.AUTH': cookie}
        )
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")
        assert response.status_code == 200

    with step("Открываем корзину с добавленными товарами"):
        browser.open('https://demowebshop.tricentis.com/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('https://demowebshop.tricentis.com/cart')

    with step("Проверяем что необходимое количество единиц товара в корзине"):
        browser.element('.product-name').should(have.exact_text('14.1-inch Laptop'))
        browser.element('[value="5"][type="text"]').should(be.visible)

    with step('Очистка корзины'):
        browser.element('.qty-input').clear()
        browser.element('.qty-input').set_value('0').press_enter()


@allure.title("При выполнении запроса на добавление продукта в корзину с EnteredQuantity = 0 корзина пустая")
def test_empty_cart():
    with step("Авторизация через API"):
        result = requests.post(
            url=URL + "/login",
            data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
            allow_redirects=False
        )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with step("Получаем cookie через API"):
        cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step('Отправляем запрос на добавление товаров в корзину с EnteredQuantity = 0'):
        response = requests.post(
            url=URL + 'addproducttocart/details/31/1',
            data={f"addtocart_31.EnteredQuantity": str(0)},
            cookies={'NOPCOMMERCE.AUTH': cookie}
        )
        allure.attach(body=json.dumps(response.json(), indent=4, ensure_ascii=True), name="Response",
                      attachment_type=AttachmentType.JSON, extension="json")
        assert response.status_code == 200

    with step("Открываем корзину"):
        browser.open('https://demowebshop.tricentis.com/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('https://demowebshop.tricentis.com/cart')

    with step('Проверяем что корзина пустая'):
        browser.element('[class="order-summary-content"]').should(have.exact_text('Your Shopping Cart is empty!'))
