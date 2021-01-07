import pymongo
from pymongo import MongoClient

class Products:
    def __init__(self):
        self.client = MongoClient()
        self.db = self.client.CarbonLab
        self.Products = self.db.products
        self.Cart = self.db.cart
        self.Users = self.db.users

    def newProduct(self, data):
        inserted = self.Products.insert({'product':data.product,
                                         'product_number': data.number,
                                         'image': data.imageUrl,   
                                         'description':data.description,
                                         'price':data.price})

    def get_products(self):
        all_products = self.Products.find()
        new_products =[]

        for product in all_products:
            new_products.append(product)

        return new_products

    def del_product(self, id):
        delete = self.Products.delete_one({'product_number': str(id)})

    def add_to_cart(self, id, data):
        choose_product = self.Products.find_one({'product_number': str(id)})
        ifexist = self.Cart.find_one({'product_number': str(id), 'customer': data})
        if ifexist:
            print('this is good')
            ifexist['order_count'] = int(ifexist['order_count']) + 1
            order_price = int(ifexist['order_count']) * int(ifexist['product_price'])
            update = self.Cart.update_one({'product_number': str(id), 'customer': data}, {'$set':{'order_count': ifexist['order_count'], 'order_price':order_price}})
        else:
            addProductToCart = self.Cart.insert({'customer': data,
                                                'product_number': choose_product['product_number'],
                                                'product_name': choose_product['product'],
                                                'order_count': '1',
                                                'product_price': choose_product['price'],
                                                'order_price': choose_product['price']
                                                })

    def customer_cart(self, data):
        cart = self.Cart.find({'customer': data})
        customerCart = []
        order_value = 0
        n = 1
        for item in cart:
            item['number'] = n
            order_value += int(item['order_price'])
            customerCart.append(item)
            n += 1

        self.Users.update_one({'email': data}, {'$set':{'order_value': order_value}})
        return customerCart, order_value

    def calculation(self, data):
        found_product = self.Cart.find_one({'product_number': data.id})
        order_price = int(data.count) * int(found_product['product_price'])
        update_cart = self.Cart.update_one({'product_number': data.id}, {"$set": { "order_count": data.count, 'order_price': order_price}} )
