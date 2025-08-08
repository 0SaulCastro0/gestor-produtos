import json, sys, os
import subprocess
from time import sleep
from product import Product, ProductEncoder

class System:
    def __init__(self):
        self.products = []
        
        self.__main_dir = os.path.dirname(__file__)
        self.__data_dir = os.path.join(self.__main_dir, 'data')
        
        self.load_data()

    def clear_screen(self):
        """
        Limpa a tela no terminal com base no SO.
        
        Returns: 
            None
        """
        if os.name == 'nt': 
            subprocess.call('cls', shell=True)
        else: 
            subprocess.call('clear', shell=True)

    def show_header(self):
        """
        Exibe o cabeçalho do sistema.
        """
        print('Gestor de Produtos')
        print('='*30)
    
    def input_str(self, msg):
        """
        Solicita um texto ao usuário.

        Args:
            msg (str): Mensagem exibida ao usuário.
        """
        
        return input(msg)
    
    def input_int(self, msg):
        """
        Solicita e valida um número inteiro do usuário.

        Args:
            msg (str): Mensagem exibida ao usuário.

        Returns:
            int: Número digitado pelo usuário.
        """
        while True:
            try:
                return int(input(msg))
            except ValueError:
                print('\033[33mPor favor digite um número válido.\033[m')
                sleep(1)
    
    def input_float(self, msg):
        """
        Solicita e valida um número real do usuário.

        Args:
            msg (str): mensagem exibida para o usuário.

        Returns:
            float: Número digitado pelo usuário
        """
        while True:
            try:
                return float(input(msg))
            except ValueError:
                print('\033[33mPor favor digite um número válido.\033[m')
                sleep(1)
    
    def add_product(self):
        """
        Adiciona um novo produto a lista de produtos.
        
        Returns: 
            None
        """
        self.clear_screen()
        self.show_header()
        
        name = self.input_str('Informe o nome do produto: ')
        price = self.input_float('Informe o preço: ')
        quantity = self.input_int('Informe a quantidade: ')
        
        product = Product(name, price, quantity)
        self.products.append(product)
        
        print('\033[32mProduto adicionado com sucesso.\033[m')
        sleep(1)

    def list_products(self, clear_screen=True):
        """
        Exibe todos os produtos cadastrados, caso não tenha 
        produtos exibe uma mensagem de aviso.

        Args:
            clear_screen (bool, optional): Se True limpa a tela. Padrão para True.
        """
        if clear_screen: self.clear_screen()
        self.show_header()
        
        if len(self.products) > 0:
            print(f"{'ID':<5}{'Nome':<20}{'Preço':<12}{'Quantidade':<12}{'Valor Total':<15}")
            for index, product in enumerate(self.products):
                print(f'{index+1:<5}{product.name:<20}R$ {product.price:<12.2f}{product.quantity:<12}{product.value_total():<15.2f}')
            print(f'\033[32mTotal em estoque: R$ {sum(p.value_total() for p in self.products):.2f}\033[m')
        else:
            print('\033[33mNenhum produto cadastrado\033[m')
        
        print('='*60)

    def edit_product(self):
        """
        Edita propriedades do produto, caso não haja produtos mostra
        uma mensagem de aviso.
        
        Returns: 
            None
        """
        while True:
            self.list_products()
            print('\033[33mDigite 0 para voltar ao menu principal\033[m')
            try:
                product_id = int(input('Informe o ID do produto a ser editado: '))
                if product_id != 0:
                    try:
                        product = self.products[product_id-1]
                        
                        print(f'Editando produto: {product.name}')
                        print('O que deseja editar no produto?')
                        print('[1] - Nome')
                        print('[2] - Preço')
                        print('[3] - Quantidade')
                        
                        options_map = {
                            1: ('name', self.input_str, 'Digite o novo nome: '),
                            2: ('price', self.input_float, 'Digite o novo preço: '),
                            3: ('quantity', self.input_int, 'Digite a nova quantidade: ')
                        }
                        option = self.input_int('Digite o número da opção desejada: ')
                        
                        if option in options_map:
                            attr, func, prompt = options_map[option]
                            setattr(product, attr, func(prompt))
                            break
                        else:
                            print('\033[33mOpção inválida\033[m')
                    except IndexError:
                        print('\033[33mO produto não existe.\033[m')
                        sleep(1)
                else:
                    break
            except ValueError:
                    print('\033[33mPor favor digite um valor numerico.\033[m')
                    sleep(1)

    def remove_product(self):
        """
        Remove um produto da lista de produtos caso exista, caso não haja 
        produtos exibe uma mensagem de aviso.
        
        Returns: 
            None
        """
        while True:
            self.list_products()
            print('\033[33mDigite 0 para voltar ao menu principal\033[m')
            
            product_id = self.input_int('Informe o ID do produto a ser removido: ')
            if product_id != 0:
                try:
                    product = self.products[product_id-1]
                    self.products.remove(product)
                    break
                except IndexError:
                    print(f'\033[33mO produto de ID {product_id} não existe.\033[m')
            else:
                break

    def save_data(self):
        """
        Salva a lista de produtos em um arquivo json.
        
        Returns: 
            None
        """
        self.clear_screen()
        self.show_header()
        
        with open(os.path.join(self.__data_dir, 'products.json'), 'w', encoding='utf-8') as file:
            products_dicts = [product.__dict__ for product in self.products]
            json.dump(products_dicts, file, cls=ProductEncoder, indent=4, ensure_ascii=False)
                
        print('\033[32mAlterações salvas com sucesso.\033[m')
        sleep(1)

    def load_data(self):
        """
        Carrega os dados salvos no arquivo json.
        
        Returns: 
            None
        """
        os.makedirs(self.__data_dir, exist_ok=True)
        self.products.clear()
        
        try:
            with open(os.path.join(self.__data_dir, 'products.json'), 'r', encoding='utf-8') as file:
                json_file = json.load(file)
                
                for item in json_file:
                    product = Product(item['name'], item['price'], item['quantity'])
                    self.products.append(product)
        except FileNotFoundError:
            with open(os.path.join(self.__data_dir, 'products.json'), 'w') as file:
                json.dump([], file)

    def quit(self):
        self.clear_screen()
        self.show_header()
        
        print('Deseja salvar antes de sair?')
        print('[1] - Sim')
        print('[2] - Não')
        
        while True:
            option = self.input_int('Digite o número da opção desejada: ')
            
            if option == 1:
                self.save_data()
                sys.exit()
            elif option == 2:
                break
                sys.exit()
            else:
                print('\033[33mOpção inválida.\033[m')