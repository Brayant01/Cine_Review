'''
    As siguintes funçoes so imprimen na tela as opçoes e devolver valores
    O fluxo real do programa tem que ser no main.py
'''

#validador de opcao com bucle infinito
def input_validation(valor_max, mensagem):

   while True: 
        print(mensagem)
        
        try :
            opcao = int(input("opcao: "))
            
            if  opcao > valor_max or opcao < 1:
                print("\ningresa um valor correcto")
                input("presiona qualquer tecla para continuar\n")
            else:
                return opcao
        
        except ValueError:
            print("\nErro: debes ingresar um número válido")
            input("Pressiona qualquer tecla para continuar\n")

#----------------- Opçoes do menu principal -----------------
def menu_ver_filme():
    print("---------------------- VER FILMES ----------------------")
    print("opcaon em desenvolvimento")

def menu_user_option(type_user,nome):
    
    # Se o usario for admin entao tem essas opçoes
    if(type_user == 1):
        return "Benvido ",nome," escolhe uma das opçoes:\n 1- criar filme \n 2- modificar filme\n 3- criar categoria"
        
        #print("2- modificar login??")
    
    else:
        #se o usuario nao for admin entao tem essas opçoes

        return "Benvido ",nome," escolhe uma das opçoes:1- ver filmes\n2- avaliar filme" 
        
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