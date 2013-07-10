from settings import c3_user

class C3():
    def __init__(self,params,engine):
        user = engine.find(id="username")
        user.clear()
        user.send_keys(c3_user["user"])
        password = engine.find(id="password")
        password.clear()
        password.send_keys(c3_user["password"])
        engine.find(name='Submit').click()

