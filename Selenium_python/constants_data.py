from selenium.webdriver.common.by import By

CONFIG = {
    'base_url': 'https://www.saucedemo.com/',
    'window_size': (1920, 1080),
}


LOCATORS = {
    'login_page': {
        'username': [(By.ID, 'user-name'), 'Username'],
        'password': [(By.ID, 'password'), 'Password'],
        'login_button':[ (By.ID, 'login-button'), 'Login'],
        'error_text': [(By.XPATH, "//h3[@data-test='error']"), 'Error'],
        'error_close_button': [(By.XPATH, "//button[@class='error-button']"), 'Error Close Button'],
    },
    'products_page': {
        'title': (By.CLASS_NAME, 'title')
    }
}


TEST_CASES = [
    {
        'name': 'Wrong_data',
        'login': 'wrong_user',
        'password': 'wrong_password',
        'expected_success': False,
        'expected_error': 'Epic sadface: Username and password do not match any user in this service'
    },
    {
        'name': 'Empty_user',
        'login': '',
        'password': 'secret_sauce',
        'expected_success': False,
        'expected_error': 'Epic sadface: Username is required'
    },
    {
        'name': 'Empty_Password',
        'login': 'standard_user',
        'password': '',
        'expected_success': False,
        'expected_error': 'Epic sadface: Password is required'
    }
]