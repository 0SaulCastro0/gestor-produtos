from system import System
from time import sleep

if __name__ == '__main__':
    system = System()

    while True:
        system.clear_screen()
        print('Gestor de Produtos')
        print('='*30)
        print('[1] - Adicionar Produto')
        print('[2] - Remover Produto')
        print('[3] - Lista Todos os Produtos')
        print('[4] - Editar Produto')
        print('[5] - Salvar Alterações')
        print('[6] - Sair')
        print('='*30)
        
        option = system.input_int('Digite o número da opção desejada: ')
        match option:
            case 1:
                system.add_product()
            case 2:
                system.remove_product()
            case 3:
                system.list_products()
                input('Pressione \033[34mENTER\033[m para continuar.')
            case 4:
                system.edit_product()
            case 5:
                system.save_data()
            case 6:
                system.quit()
            case _:
                print(f'\033[31mOpção {option} não existe.\033[m')
                sleep(1.5)