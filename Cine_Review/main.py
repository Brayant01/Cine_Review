
import db_management
import menu

#variavel global para clasificaçao indicativa
classificacao_indicativa= {
    1 : "L",
    2 : "10",
    3 : "12",
    4 : "14",
    5 : "16",
    6 : "18"
}

conection_db = db_management.conect_data_base()
cursor = conection_db.cursor()

#---------------- MAIN PROGRAM :) ----------------#

while True:
    
    opcao = menu.main_menu()

    if opcao==1:# ver fimes
        menu.menu_ver_filme()
    
    elif opcao==2: #login
        repetir = True

        while repetir == True:

            print("\nPara logar ingresa as siguiente informaçoes")
            email = input("Email: ").strip().lower()
            senha = input("Senha : ")

            user_logado = db_management.login_user

            if user_logado["type_user"] == 1:
                print("menu para admin")
                menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
            
            if user_logado["type_user"] == 2:
                print("menu usuario normal")
                menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
            

    elif opcao==3: #criar conta
        while True:
            if menu.menu_criar_conta() == 1:
                if db_management.val_create_admin() == False:
                    if menu.input_validation(2,"Deseja tentar novamente?\nSim --> 1\nNão --> 2")==2:
                        repetir = False
                        print("vontando ao menu inicial")
                else:
                    db_management.create_usuario(cursor,conection_db,1)
                    break
            else:
                db_management.create_usuario(cursor,conection_db,0)
                break

              
    else:
        print("Obridado por usar nosso serviço ate mais!!!!")
        break


