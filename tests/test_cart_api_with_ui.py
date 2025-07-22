import requests

from allure_commons._allure import step
from allure_commons.types import AttachmentType
from selene import browser, have

import allure

LOGIN = "example4705@example.com"
PASSWORD = "123456"
WEB_URL = "https://demowebshop.tricentis.com/"
API_URL = "https://demowebshop.tricentis.com/"

@allure.title("Добавление товара в корзину авторизованным пользователем")
def test_add_product_through_api_authorized_user():
    with step("Авторизоваться через API"):
        result = requests.post(
        url=API_URL + "/login",
        data={"Email": LOGIN, "Password": PASSWORD, "RememberMe": False},
        allow_redirects=False
    )
        allure.attach(body=result.text, name="Response", attachment_type=AttachmentType.TEXT, extension="txt")
        allure.attach(body=str(result.cookies), name="Cookies", attachment_type=AttachmentType.TEXT, extension="txt")

    with step("Получить cookie через API"):
         cookie = result.cookies.get("NOPCOMMERCE.AUTH")

    with step('Добавить товар в корзину через API'):
        response = requests.post(
            url=WEB_URL + 'addproducttocart/details/31/1',
            data={f"addtocart_31.EnteredQuantity": str(1)},
            cookies={'NOPCOMMERCE.AUTH': cookie})

    with step("Проверка статус-кода после добавления товара"):
        assert response.status_code == 200

    with step("Переход в корзину через UI с авторизационным cookie"):
        browser.open('https://demowebshop.tricentis.com/')
        browser.driver.add_cookie({"name": "NOPCOMMERCE.AUTH", "value": cookie})
        browser.open('https://demowebshop.tricentis.com/cart')

    with step("Проверка добавления товара в корзину через UI"):
        browser.element('.product-name').should(have.exact_text('14.1-inch Laptop'))

    with step('Очистка корзины'):
        browser.element('.qty-input').clear()
        browser.element('.qty-input').set_value('0').press_enter()