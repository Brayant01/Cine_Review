
import db_management
import menu

conection_db = db_management.conect_data_base()
cursor = conection_db.cursor()

#valida o login do usuario pasando um de 3 valores

def login_user(email, senha_input):
    
    query = "SELECT id, senha, type_user FROM usuario WHERE email = %s"  #Verifica o valor senha e admin na db de usuario
    
    cursor.execute(query,(email,))
    resultado = cursor.fetchone()

    if not resultado: #se nao tem usuario devolve 0 e uma mensagem
        print("O usuario nao existe voltando ao inicio")
        return 3 # 2 = erro ao fazer login se esse valor é retornado entao validar input do usuario
    
    #pasa a senha_db o resuldado da consulta com o valor da senha na base de dados e o valor admin
    id_user,senha_db, user_type, nome = resultado 

    if senha_db[0] != senha_input:
        print("Senha incorrecta")
        return 2 # 2 = erro de senha se esse valor é retornado entao validar input do usuario

    if type_user[0] == 1: #se for admin = 1 entao devolve 2 (usuario admin)
        print("O usuario é admin")
        return user_type,id_user,nome
    else:                          #se nao entao devolve 1 (usuario normal)
        print("Usuario nao admin")
        return user_type,id_user,nome


#---------------- MAIN PROGRAM :) ----------------#

while True:
    
    opcao = menu.main_menu()

    if opcao==1:
        menu.menu_ver_filme
    
    elif opcao==2:
        repetir = True

        while repetir == True:

            print("Para logar ingresa as siguiente informaçoes")
            email = input("Email: ").strip().lower()
            senha = input("Senha : ")

            user_type,id_user,nome = login_user(email,senha)

            if user_type == 2:
                if menu.input_validation(2,"Deseja tentar novamente?\nSim --> 1\nNão --> 2") == 2:
                    repetir = False
                    print("vontando ao menu inicial")
                    break
            
            if  user_type == 3:

                if menu.input_validation(2,"Deseja tentar novamente?\nSim --> 1\nNão --> 2") == 2:
                    repetir = False
                    print("vontando ao menu inicial")
                    break

            if user_type == 1:

               opcao = menu.input_validation(3,menu.menu_user_option(user_type,nome))
               
               if opcao == 1:
                   #criar Filme
                   mensagem = "Para criar um filme precisa escolher uma opçao de classificacao indicativa" \
                              "1- L  para toda a famila" \
                              "2- 10 mais de 10 anos " \
                              "3- 12 mais de 10 anos" \
                              "4- 14 mais de 10 anos" \
                              "5- 16 mais de 10 anos" \
                              "6- 18 so para maiores de idade"
                   
                   auxiliar = menu.input_validation(6,mensagem)

                   if auxiliar == 1: classificacao_indicativa = "L"
                   if auxiliar == 2: classificacao_indicativa = 10
                   if auxiliar == 3: classificacao_indicativa = 12
                   if auxiliar == 4: classificacao_indicativa = 14
                   if auxiliar == 5: classificacao_indicativa = 16
                   if auxiliar == 6: classificacao_indicativa = 18
                                      
                   db_management.create_filme(cursor,conection_db,classificacao_indicativa)
               elif opcao == 2:
                   #Modificar Filme
                   print("opçao en desenvolvimento")
               elif opcao == 3:
                   #criar Categoria
                   db_management.create_categoria()
        
        type_user,id_user = login_user(email,senha)

            

    elif opcao==3:
        menu.menu_criar_conta()
    else:
        print("Obridado por usar nosso serviço ate mais!!!!")
        break

    break

