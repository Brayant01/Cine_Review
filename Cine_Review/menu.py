'''
    As siguintes funçoes so imprimen na tela as opçoes e devolver valores
    O fluxo real do programa tem que ser no main.py
'''

#validador de opcao com bucle infinito
def input_validation(valor_max, mensagem):

   while True: 
        print(mensagem)
        
        try :
            opcao = int(input("\nopcao: "))
            
            if  opcao > valor_max or opcao < 1:
                print("\ningresa um valor correcto")
                input("presiona qualquer tecla para continuar\n")
            else:
                return opcao
        
        except ValueError:
            print("\nErro: debes ingresar um número válido")
            input("Pressiona qualquer tecla para continuar\n")

#----------------- Opçoes do menu principal -----------------
def ver_filmes(filmes_db,opcao): #filmes_db = id, titulo, nota, classificacao
    print("---------------------- VER FILMES ----------------------")

    if opcao == 1:
        for i, filme in enumerate(filmes_db,start=1):
            id, titulo, nota, classificacao, *_ = filme

            print(f"{i} - {titulo} ({classificacao}) nota:{nota}")
    else:
        for i, filme in enumerate(filmes_db,start=1):
            id, titulo, ano,sinopse = filme

            print(f"{titulo} ({classificacao}) ano:{ano} \nSinopse: {sinopse}")


def select_filme(filmes_db):# orden de filme = id, titulo, nota, classificacao, sinopse
    selection = input_validation(len(filmes_db),"Escolha um dos filmes")
    
    return filmes_db[selection-1]

def ver_filme(filme, opcao):# orden de filme = id, titulo, nota, classificacao, sinopse
    
    if opcao== 1:
        id, titulo,nota, classificacao, sinopse = filme
        print(f"{titulo} ({classificacao}) nota:{nota} \nSinopse: {sinopse}")
    else:#id, titulo, ano_lancamento, sinopse
        id, titulo, ano,sinopse = filme
        print(f"{titulo} ({classificacao}) ano:{ano} \nSinopse: {sinopse}")
    

def menu_mod_filme():
    print("Escolhe uma das das siguientes opçoes a modificar")

    print("1 - Nome\n2 - classificaçao\n3 - Sinopse")

    return input_validation(3, "Opçao: ")


def menu_user_option(type_user,nome):
    
    # Se o usario for admin entao tem essas opçoes
    if(type_user == 1):
        print("-------------------- OPÇOES DE ADMINISTRADOR --------------------")
        return f'''Benvido ",nome," escolhe uma das opçoes:\n1- criar filme \n2- modificar filme\n3- criar categoria\n4 - Sair'''
        
        #print("2- modificar login??")
    
    else:
        #se o usuario nao for admin entao tem essas opçoes
        print("-------------------- OPÇOES DE USUARIO --------------------")
        return f'''Benvido "{nome}" escolhe uma das opçoes:1- ver filmes\n2 - Buscar filme\n3 - Sair'''
        
        #print("3- modificar login??")

def menu_criar_conta():
    print("-------------------- CRIAR CONTA ----------------------")
    
    mensagem = "Escolha uma das siguientes opcoes:\n Administrador  - 1 \nUsuario normal - 2"

    return input_validation(2,mensagem)



#------------------ MENU PRINCIPAL ------------------
def main_menu():

    print("\nBem vido a ! Cine review ! seu programa de avaliaçoes de confiança")
    print("\nSeleciona uma das siguientes opçoes")
    
    opcaon = input_validation(3,"ingresa uma das siguientes opçoens"
                                "\nVer filme       - 1"
                                "\nfazer login     - 2" 
                                "\ncriar uma conta - 3")    
    return opcaon