

class Administration():
    '''
    This class is used for administration purposes.
    E.g. Authentication. 
    '''
    def __init__(self):
        self.__allow = False

    def __init__(self, user, passw):
        self.user = user
        self.passw = passw
        self.__allow = True
    
    def __repr__():
        return f'<User: {self.username}>'
    
    def __str__():
        if self.__allow:
            return "User: "+ self.user +" connected successfully."
        else:
            return "User not allowed to be connected."
    
    def isConnected():
        return self.__allow
