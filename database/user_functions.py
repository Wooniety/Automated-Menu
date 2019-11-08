class Shopping_Cart:
    def __init__(self):
        self.name = ""
        self.cart = {}
    
    def add_to_cart(self, item){
        if item in self.cart:
            self.cart[item] = self.cart[item]+1
        else:
            self.cart[item] = 1
    
    def remove_from_cart(self, item):
        if item in self.cart:
            if self.cart[item] == 1:
                del self.cart[item]
            else:
                self.cart[item] -= 1
    
    def view_cart(self):
        for item in sorted(self.cart):
            print(f"{item}: {self.cart[item]}")