import web
import os
from Models import RegisterModel, LoginModel, Posts, Contact
from Models import Products as PM

web.config.debug = False

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/deleteproduct/(.+)', 'DeleteProduct',
    '/deletepost/(.+)', 'DeletePost',
    '/add-to-cart/(.+)', 'addToCart',
    '/controlpanel', 'ControlPanel',
    '/posts/(.+)', 'BlogPost',
    '/blog', 'Blog',
    '/cart', 'Cart',
    '/logout', 'Logout',
    '/profile', 'Profile',
    '/update-profile', 'UpdateProfile',
    '/checklogin', 'CheckLogin',
    '/products', 'Products',
    '/contact-us', 'ContactUs',
    '/submitposts', 'SubmitPosts',
    '/submitnewproduct', 'SubmitProduct',
    '/postregisteration', 'PostRegisteration',
    '/submit-comment', 'SubmitComment',
    '/contact-request', 'ContactReq',
    '/price-calculation', 'PriceCalculation'
)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer = {'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", 
                            globals = {'session': session_data, 'current_user': session_data["user"]})
post_number = 1


class Home:
    def GET(self):
        ifactive = True
        post_model = Posts.Posts()
        posts = post_model.get_latest_posts()
        return render.Home(posts, ifactive)


class DeletePost:
    def GET(self, id):
        post_model = Posts.Posts()
        delete_post = post_model.del_post(id)
        raise web.seeother('/controlpanel')


class DeleteProduct:
    def GET(self, id):
        product_model = PM.Products()
        delete_product = product_model.del_product(id)
        raise web.seeother('/controlpanel')
        

class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


class Blog:
    def GET(self):
        post_model = Posts.Posts()
        posts = post_model.get_posts()
        return render.Blog(posts)


class BlogPost:
    def GET(self, id):
        post_model = Posts.Posts()
        found_post = post_model.find_post(id)
        return render.Post(found_post)


class CheckLogin:
    def POST(self):
        data = web.input()

        login_model = LoginModel.LoginModel()
        isCorrect = login_model.check_user(data)
        if isCorrect:
            session_data["user"] = isCorrect
            return isCorrect
        else:
            return "error"


class Profile:
    def GET(self):
        return render.Profile()


class UpdateProfile:
    def POST(self):
        data = web.input()
        data.email = session_data['user']['email']
        login_model = LoginModel.LoginModel()
        update = login_model.updateProfile(data)
        return "success"


class Cart:
    def GET(self):
        product_model = PM.Products()
        customer = session_data['user']['email']
        cart_and_totalvalue = product_model.customer_cart(customer)
        cart = cart_and_totalvalue[0]
        total_order_price = cart_and_totalvalue[1] 
        return render.Cart(cart, total_order_price)


class Products:
    def GET(self):
        product_model = PM.Products()
        products = product_model.get_products()
        return render.Products(products)


class addToCart:
    def GET(self, id):
        product_model = PM.Products()
        customer = session_data['user']['email']
        print(customer)
        cartItem = product_model.add_to_cart(id, customer)
        raise web.seeother('/products') 
        

class SubmitPosts:
    def POST(self):
        global post_number
        data = web.input(image={})
        file_dir = os.getcwd() + "/static/uploads/"

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        if "image" in data:
            filepath = data.image.filename.replace("\\", "/")
            filename = filepath.split("/")[-1]
            f = open(file_dir + "/" + filename, 'wb')
            f.write(data.image.file.read())
            f.close()
            data.imageUrl = "/static/uploads/" + filename

        post_model = Posts.Posts() 
        all_posts = post_model.get_posts()
        post_number = len(all_posts) + 1
        data.number = str(post_number)
        post_number += 1
        post = post_model.insert_posts(data)
        return "success" 


class SubmitProduct:
    def POST(self):
        data = web.input(image={})
        file_dir = os.getcwd() + "/static/uploads/"

        if not os.path.exists(file_dir):
            os.mkdir(file_dir)

        if "image" in data:
            filepath = data.image.filename.replace("\\", "/")
            filename = filepath.split("/")[-1]
            f = open(file_dir + "/" + filename, 'wb')
            f.write(data.image.file.read())
            f.close()
            data.imageUrl = "/static/uploads/" + filename

        product_model = PM.Products()
        all_products = product_model.get_products()
        product_number = len(all_products) + 1
        data.number = str(product_number)
        new_product = product_model.newProduct(data)

        return "success"


class ContactReq:
    def POST(self):
        data = web.input()
        contact_model = Contact.Contact()
        contact_us = contact_model.contactRequest(data)

        return "success"


class ContactUs:
    def GET(self):
        return render.ContactUs()


class PostRegisteration:
    def POST(self):
        data = web.input()

        reg_model = RegisterModel.RegisterModel()
        user_exists = reg_model.check_if_user_exists(data)
        if user_exists:
            return "error"
        else:
            reg_model.insert_users(data)
            return data.name


class Logout:
    def GET(self):
        session["user"] = None
        session_data["user"] = None

        session.kill()
        return 'success'


class ControlPanel:
    def GET (self):
        post_model = Posts.Posts()
        product_model = PM.Products()
        posts = post_model.get_posts()
        products = product_model.get_products()
        return render.ControlPanel(posts, products)

class SubmitComment:
    def POST(self):
        data = web.input()
        if session_data['user']:
            data.username = session_data['user']['name']
            post_model = Posts.Posts()
            added_comment = post_model.add_comment(data)
            if added_comment:
                return "success"
            else:
                return "fatal error"
        else:
            return "error"


class PriceCalculation:
    def POST(self):
        data = web.input()
        print(data)
        product_model = PM.Products()
        cal = product_model.calculation(data)


if __name__ == "__main__":
    app.run()
