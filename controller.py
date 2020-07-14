import web
from Models import RegisterModel, LoginModel

web.config.debug = False

urls = (
    '/', 'Home',
    '/register', 'Register',
    '/login', 'Login',
    '/logout', 'Logout',
    '/checklogin', 'CheckLogin',
    '/products', 'Products',
    '/contact-us', 'ContactUs',
    '/postregisteration', 'PostRegisteration'
)


app = web.application(urls, globals())
session = web.session.Session(app, web.session.DiskStore("sessions"), initializer = {'user': None})
session_data = session._initializer

render = web.template.render("Views/Templates", base="MainLayout", 
                            globals = {'session': session_data, 'current_user': session_data["user"]})


class Home:
    def GET(self):
        return render.Home()


class Register:
    def GET(self):
        return render.Register()


class Login:
    def GET(self):
        return render.Login()


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


class Products:
    def GET(self):
        return render.Products()


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


if __name__ == "__main__":
    app.run()
