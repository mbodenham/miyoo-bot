import json

from playwright.sync_api import Playwright, sync_playwright, expect
import time

class Miyoo():
    def __init__(self):
        self.url = 'https://www.aliexpress.us/item/1005003611677275.html'
        self.colors = ['RetroGrey', 'Transparent Black', 'Transparent Blue', 'White']

        print('Miyoo Mini Bot')

        self.select_color()
        self.open()
        self.load()
        self.login()

    def open(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.firefox.launch(headless=False)
        self.context = self.browser.new_context()
        self.page = self.context.new_page()

    def close(self):
        self.context.close()
        self.browser.close()
        self.playwright.stop()

    def load(self):
        self.page.goto(self.url)
        self.page.wait_for_load_state('networkidle')

    def reload(self):
        self.page.reload()
        self.page.wait_for_load_state('networkidle')

    def login(self):
        self.page.get_by_role("link", name="Account").click()
        self.page.get_by_role("link", name="Sign in").click()
        self.page.locator("input[name=\"fm-login-id\"]").click()
        input('Login then press any key')

    def buy_now(self):
        self.page.get_by_role("button", name="Buy Now").click()
        self.page.wait_for_load_state('networkidle')

    def select_color(self):
        for i, color in enumerate(self.colors):
            print(f'  {i+1}. {color}')
        i = int(input('Select a color:')) - 1

        self.color = self.colors[i]
        print(f'{self.color} selected')

    def check_available(self):
        return self.page.locator(".customs-message-wrap").count() == 0

    def check_total_stock(self):
        txt = self.page.locator(".product-quantity-tip").inner_text()
        return int(''.join(i for i in txt if i.isdigit()))

    def check_stock(self):
        total_stock = self.check_total_stock()

        self.page.get_by_role("img", name=self.color).click()
        time.sleep(1)
        txt = self.page.locator(".product-quantity-tip").inner_text()
        stock = int(''.join(i for i in txt if i.isdigit()))

        if stock == total_stock:
            stock = 0
        else:
            print(f'{stock} {self.color} in stock')

        return stock > 0

    def checkout(self):
        self.page.locator('button:has-text("Pay Now"), button:has-text("Place Order")').click()
        self.page.wait_for_load_state('networkidle')


miyoo = Miyoo()

while True:
    if miyoo.check_available() and miyoo.check_stock():
        break
    time.sleep(5)
    miyoo.reload()

try:
    miyoo.buy_now()
except:
    print('Failed buy now')
    input('Press any key to close')
    miyoo.close()
    exit()


try:
    miyoo.checkout()
except:
    print('Failed checkout')
    input('Press any key to close')
    miyoo.close()
    exit()


print('Purchase Complete')
miyoo.close()
