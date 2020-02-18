class EList:
    def __init__(self):
        self.e = {}
        self.length = 0
    
    def print_e(self):
        for key, entry in self.e.items():
            print('{:20}{:>20}'.format(key, entry))
    
    def check_token(self, token):
        return token in self.e
    
    def get_e(self, token):
        return self.e[token]
    
    def add_e(self, token):
        if not self.check_token(token):
            self.length += 1
            self.e[token] = 'e' * self.length
    
    def get_e_define(self, token):
        return "#define {} {}".format(self.get_e(token), token)