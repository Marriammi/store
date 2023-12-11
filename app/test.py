import unittest
import requests

class ApiTest(unittest.TestCase):
    API_URL = "http://127.0.0.1:5000"

    Register_URL = "{}/register".format(API_URL)
    Login_URL = "{}/login".format(API_URL)
    Logout_URL = "{}/logout".format(API_URL)
    GetUserId_URL = "{}/get_user_id".format(API_URL)
    GetUserInfo_URL = "{}/get_user_info".format(API_URL)
    ChangeUsername_URL = "{}/change_username".format(API_URL)
    ChangeEmail_URL = "{}/change_email".format(API_URL)
    DeleteAccount_URL = "{}/delete_account".format(API_URL)

    PlaceOrder_URL = "{}/place_order".format(API_URL)
    GetProducts_URL = "{}/get_products".format(API_URL)
    GetUserOrders_URL = "{}/get_user_orders".format(API_URL)
    DeleteOrder_URL = "{}/delete_order".format(API_URL)
    Products_URL = "{}/get_products".format(API_URL)

    def test_1_unauthorized_access(self):
        # Make a request to the start page without logging in
        response = requests.get('http://127.0.0.1:5000/start-page', allow_redirects=False)

        # Check if the status code is 401 (Unauthorized)
        self.assertEqual(response.status_code, 401)

        # Check if the 'Location' header is not present in the response
        self.assertNotIn('Location', response.headers)


    def test_2_register_user(self):
        # Припустимі дані для реєстрації
        data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        # Виклик API для реєстрації
        r = requests.post(ApiTest.Register_URL, json=data)

        # Перевірка відповіді сервера
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['message'], 'Registration successful')


    def test_3_register_duplicate_user(self):
        duplicate_data = {
            'username': 'testuser',
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        duplicate_response = requests.post(ApiTest.Register_URL, json=duplicate_data)

        # Перевірка відповіді сервера на спробу створення дубліката користувача
        self.assertEqual(duplicate_response.status_code, 400)
        self.assertEqual(duplicate_response.json()['error'], 'Username or email already exists')


    def test_4_login_logout_user(self):
        # Логін нового користувача
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Виклик API для логауту
        logout_response = requests.post(ApiTest.Logout_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на логаут
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json()['message'], 'You have been logged out successfully.')


    def test_5_get_all_products(self):
        r = requests.get(ApiTest.Products_URL)
        self.assertEqual(r.status_code, 200)
        self.assertEqual(len(r.json()), 8)


    def test_6_place_order_successful(self):
        # Логін нового користувача
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Припустимі дані для замовлення
        order_data = {
            'product_id': 1,  # Замініть на реальний ID продукту
            'units': 1
        }

        # Виклик API для розміщення замовлення після логіну
        place_order_response = requests.post(ApiTest.PlaceOrder_URL, json=order_data, cookies=login_response.cookies)

        # Перевірка відповіді сервера на успішне розміщення замовлення
        self.assertEqual(place_order_response.status_code, 201)
        self.assertEqual(place_order_response.json()['message'], 'Order placed successfully')

        # Виклик API для логауту
        logout_response = requests.post(ApiTest.Logout_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на логаут
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json()['message'], 'You have been logged out successfully.')


    def test_7_get_user_orders(self):
        # Логін нового користувача
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Assuming the user has placed orders
        response = requests.get(ApiTest.GetUserOrders_URL, cookies=login_response.cookies)
        self.assertEqual(response.status_code, 200)
        self.assertIn('orders', response.json())


    def test_8_place_order_insufficient_stock(self):
        # Логін нового користувача
        login_data = {
            'email': 'testuser@example.com',
            'password': 'testpassword'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Припустимі дані для замовлення
        order_data = {
            'product_id': 1,
            'units': 100
        }

        # Виклик API для розміщення замовлення з недостатнім запасом
        place_order_response = requests.post(ApiTest.PlaceOrder_URL, json=order_data, cookies=login_response.cookies)

        # Перевірка відповіді сервера на помилку недостатнього запасу
        self.assertEqual(place_order_response.status_code, 400)
        self.assertEqual(place_order_response.json()['error'], 'Not enough stock available')

        # Виклик API для логауту
        logout_response = requests.post(ApiTest.Logout_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на логаут
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.json()['message'], 'You have been logged out successfully.')

        # Виклик API для видалення облікового запису
        delete_account_response = requests.post(ApiTest.DeleteAccount_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на видалення облікового запису
        self.assertEqual(delete_account_response.status_code, 200)
        self.assertEqual(delete_account_response.json()['message'], 'Account deleted successfully')


    def test_9_change_username_authenticated(self):
        # Припустимі дані для реєстрації
        data = {
            'username': 'testuser1',
            'email': 'testuser1@example.com',
            'password': 'test1password'
        }

        # Виклик API для реєстрації
        r = requests.post(ApiTest.Register_URL, json=data)

        # Перевірка відповіді сервера
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['message'], 'Registration successful')

        # Логін нового користувача
        login_data = {
            'email': 'testuser1@example.com',
            'password': 'test1password'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Attempt to change username with authentication
        response = requests.post(ApiTest.ChangeUsername_URL, json={'newUsername': 'new_test_user'},
                                 cookies=login_response.cookies)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Username changed successfully')

        # Виклик API для видалення облікового запису
        delete_account_response = requests.post(ApiTest.DeleteAccount_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на видалення облікового запису
        self.assertEqual(delete_account_response.status_code, 200)
        self.assertEqual(delete_account_response.json()['message'], 'Account deleted successfully')


    def test_10_change_email_authenticated(self):
        # Припустимі дані для реєстрації
        data = {
            'username': 'test2',
            'email': 'test2@example.com',
            'password': 'test2'
        }

        # Виклик API для реєстрації
        r = requests.post(ApiTest.Register_URL, json=data)

        # Перевірка відповіді сервера
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['message'], 'Registration successful')

        # Логін нового користувача
        login_data = {
            'email': 'test2@example.com',
            'password': 'test2'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Attempt to change email without authentication
        response = requests.post(ApiTest.ChangeEmail_URL, json={'newEmail': 'new_test@example.com'},
                                 cookies=login_response.cookies)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Email changed successfully')

        # Виклик API для видалення облікового запису
        delete_account_response = requests.post(ApiTest.DeleteAccount_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на видалення облікового запису
        self.assertEqual(delete_account_response.status_code, 200)
        self.assertEqual(delete_account_response.json()['message'], 'Account deleted successfully')


    def test_11_delete_account(self):
        # Припустимі дані для реєстрації
        data = {
            'username': 'test',
            'email': 'test@example.com',
            'password': 'test'
        }

        # Виклик API для реєстрації
        r = requests.post(ApiTest.Register_URL, json=data)

        # Перевірка відповіді сервера
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()['message'], 'Registration successful')

        # Логін нового користувача
        login_data = {
            'email': 'test@example.com',
            'password': 'test'
        }

        login_response = requests.post(ApiTest.Login_URL, json=login_data)
        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_response.json()['message'], 'Login successful')

        # Виклик API для видалення облікового запису
        delete_account_response = requests.post(ApiTest.DeleteAccount_URL, cookies=login_response.cookies)

        # Перевірка відповіді сервера на видалення облікового запису
        self.assertEqual(delete_account_response.status_code, 200)
        self.assertEqual(delete_account_response.json()['message'], 'Account deleted successfully')



if __name__ == '__main__':
    unittest.main()
