#Импорт модуля time для работы с задержками
import time
# Импорт необходимых модулей Selenium для работы с Chrome
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.common.keys import Keys
# Импорт webdriver-manager для автоматической установки драйвера Chrome последней версии
from webdriver_manager.chrome import ChromeDriverManager
#Импорт констант с данными конфигурационных файлов, локаторов, параметров тестов
from constants_data import CONFIG, LOCATORS, TEST_CASES


def try_to_authorization(test_case, driver):
    # Заполнение поля логина
    fill_in_the_fields(
        driver,
        LOCATORS.get('login_page')['username'],
        test_case.get('login')
    )
    # Заполнение поля пароля
    fill_in_the_fields(
        driver,
        LOCATORS.get('login_page')['password'],
        test_case.get('password')
    )
    # Нажатие на клавишу Enter для авторизации

    driver.find_element(*LOCATORS.get('login_page')['login_button'][0]).send_keys(Keys.ENTER)
    # Вывод сообщения в консоль
    print(f"Клавиша ENTER нажата")
    time.sleep(1) # Задержка перед выполнением следующей команды

    # Проверка на появленние корректного сообщения об ошибке
    check_error_message(
        driver,
        LOCATORS.get('login_page')['error_text'],
        test_case.get('expected_error'),
        test_case.get('name')
    )
    # Проверка на возможность закрытия сообщения об ошибке
    try_to_close_error_button(
        driver,
        LOCATORS.get('login_page')['error_close_button'],
        LOCATORS.get('login_page')['error_text'],
        test_case.get('name')
    )


def fill_in_the_fields(driver, locator, field_value):
    # Установка значения в поле по локатору
    field = driver.find_element(*locator[0])
    # Выделяем всё поле
    field.send_keys(Keys.CONTROL + 'a')
    print(f"Выделяем поле {locator[1]}")
    #Удаляем содержимое поля
    field.send_keys(Keys.DELETE)
    print(f"Очищаем поле {locator[1]}")
    # Ввод значений в поле
    field.send_keys(field_value)
    # Вывод сообщения в консоль
    print(f"Поле \"{locator[1]}\" заполнено, данными: {field.get_attribute('value')}")
    time.sleep(1) # Задержка перед выполнением следующей команды


def check_error_message(driver, locator, expected_message, test_name):
    # Получение сообщения об ошибке
    current_message = get_error_message(driver, locator)
    # Проверка корректности полученной ошибки
    assert current_message == expected_message, \
        (f"Тест {test_name}! Некорректное сообщение об ошибке"
         f"\nполучено:{current_message}, ожидалось:{expected_message}")
    # Вывод сообщения в консоль
    print(f"Тест \"{test_name}\" на проверку корректности сообщения пройден")


def try_to_close_error_button(driver, locator_button, locator_message, test_name):
    # Нажатие на кнопку закрытия сообщения об ошибке
    driver.find_element(*locator_button[0]).click()
    print("Сообщение об ошибке закрыто")
    # Задержка
    time.sleep(1)
    # Проверка отсутсвия сообщения об ошибки после закрытия окна
    assert get_error_message(driver, locator_message) is None,\
        f"Тест {test_name}! Сообщения об ошибке не должно быть"
    # Вывод сообщения в консоль
    print(f"Тест \"{test_name}\" на проверку закрытия сообщения об ошибке пройден")


def get_error_message(driver, locator):
    # Попытка получения сообщения об ошибке
    try:
        return driver.find_element(*locator[0]).text
    except NoSuchElementException:
        return None


def main(): # Основная программа
    #Установка параметров (опций) работы с драйвером
    options = webdriver.ChromeOptions()
    # Не открывать браузер (режим headless)
    options.add_argument("--headless")
    # Получение web драйвера браузера Chrome
    driver = webdriver.Chrome(
        options=options,
        service=ChromeService(ChromeDriverManager().install())
    )

    # Переход на указанную страницу в браузере
    driver.get(CONFIG.get('base_url'))
    # Установка размера окна браузера в разрешение 1920x1080 (FHD)
    driver.set_window_size(*CONFIG.get('window_size'))
    print("Сайт открыт")

    for test_case in TEST_CASES:
        #Запуск теста из пула тест-кейсов
        try_to_authorization(test_case, driver)
        # Вывод сообщения в консоль
        print(f"\nТест {test_case.get('name')} пройден!\n")

    driver.quit() # Закрытие браузера
    print("Сайт закрыт")  # Вывод сообщения в консоль


if __name__ == '__main__':
    main()