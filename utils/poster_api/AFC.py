import requests


class PosterAPI:
    def __init__(self, api_key):
        self.base_url = 'https://joinposter.com'
        self.api_key = api_key

    def get_categories(self):
        url = self.base_url + '/api/' + 'menu.getCategories' + '?token=' + self.api_key
        response = requests.get(url).json()
        return response['response']

    def get_category(self, id):
        url = self.base_url + '/api/' + 'menu.getCategory' + '?token=' + self.api_key + '&category_id=' + str(id)
        response = requests.get(url).json()
        return response['response']

    def get_products(self, category_id=None):
        if category_id is None:
            url = self.base_url + '/api/' + 'menu.getProducts' + '?token=' + self.api_key
            response = requests.get(url).json()
            return response['response']
        else:
            url = self.base_url + '/api/' + 'menu.getProducts' + '?token=' + self.api_key + '&category_id=' + str(
                category_id)
            response = requests.get(url).json()
            return response['response']

    def get_product(self, product_id):
        url = self.base_url + '/api/' + 'menu.getProduct' + '?token=' + self.api_key + '&product_id=' + str(product_id)
        response = requests.get(url).json()
        return response['response']

    def create_delivery_order(self, phone, first_name, payment, products, service_type, client_address):
        incoming_order = {
            'spot_id': 1,
            'phone': phone,
            'name': first_name,
            'service_mode': service_type,
            'client_address': client_address,
            'payment': payment,
            'products': products
        }
        print(incoming_order)
        url = self.base_url + '/api/' + 'incomingOrders.createIncomingOrder' + '?token=' + self.api_key
        response = requests.post(url, json=incoming_order).json()
        return response['response']

    def create_takeout_order(self, phone, first_name, payment, products, service_type, client_address=None,
                             comment=None, delivery_time=None, ):
        incoming_order = {
            'spot_id': 1,
            'phone': phone,
            'name': first_name,
            'service_mode': service_type,
            'payment': payment,
            'products': products
        }
        print(incoming_order)
        url = self.base_url + '/api/' + 'incomingOrders.createIncomingOrder' + '?token=' + self.api_key
        response = requests.post(url, json=incoming_order).json()
        return response

    def get_order(self, incoming_order_id):
        url = self.base_url + '/api/' + 'incomingOrders.getIncomingOrder' + '?token=' + self.api_key + '&incoming_order_id=' + str(
            incoming_order_id)
        response = requests.get(url).json()
        return response['response']
