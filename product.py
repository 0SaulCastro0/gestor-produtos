from json import JSONEncoder

class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        
        self.price = price
        if self.price < 0:
            raise ValueError('\033[33mPreço não pode ser negativo.\033[33m')
        
        self.quantity = quantity
        if self.quantity < 0:
            raise ValueError('\033[33mQuantidade não pode ser negativa.\033[33m')
    
    def value_total(self):
        return self.price * self.quantity
    
    def __str__(self):
        return f'Product(name={self.name!r}, price={self.price}, quanitity={self.quantity})'

class ProductEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Product):
            return {
                'name': obj.name,
                'price': obj.price,
                'quantity': obj.quantity
            }
            
        return super().default(obj)