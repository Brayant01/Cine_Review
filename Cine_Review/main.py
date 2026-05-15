
import db_management
import menu

#variavel global para clasificaçao indicativa
classi_indicativa= {
    1 : "L",
    2 : "10",
    3 : "12",
    4 : "14",
    5 : "16",
    6 : "18"
}

options_mod_films={
    1: "Titulo",
    2: "classificacao_indicativa",
    3: "sinopse"
}

avaliacao= {
    "id_usuario": "NULL",
    "id_filme": "NULL",
    "nota": "NULL",
    "comentario": "NULL"
}

conection_db = db_management.conect_data_base()
cursor = conection_db.cursor()

#---------------- MAIN PROGRAM :) ----------------#

while True:

    opcao = menu.main_menu()

    if opcao==1:# ver fimes
        while True:
            
            opcao = menu.input_validation(31,"1 - Ver todos os Filme\n2 - Ver o TOP 5 *o*\n3 - Voltar")

            if opcao == 1:
                filmes_db = db_management.Extrair_filmes(cursor,1)
                print("filmes:",filmes_db)
                menu.ver_filmes(filmes_db)
                opcao = menu.input_validation(2,"Deseja ver mais de um dos filmes?\n1 - SIM\n2 - NAO")
            elif opcao == 2:
                filmes_db = db_management.Extrair_filmes(cursor,2)
                menu.ver_filmes(filmes_db)
                opcao = menu.input_validation(2,"Deseja ver mais de um dos filmes?\n1 - SIM\n2 - NAO")
            else:
                print("voltando aou menu principal")
                break
        
            if opcao == 1:
                filme = menu.select_filme(filmes_db)
                menu.ver_filme(filme)
                input("precione qualquer tecla para voltar ao menu")
            else:
                print("Voltando")
                break

    
    elif opcao==2: #login

        while True:  # bucle usado para manter o suario na parte de ingresar as informaçoes
            print("\nPara logar ingresa as siguiente informaçoes")
            email = input("Email: ").strip().lower()
            senha = input("Senha : ")

            user_logado = db_management.login_user(cursor,email,senha) #chama a funçao e guarda um dicionario con dados para verificar que o login foi certo ou nao

            if user_logado["status"] == "no_user": # se o usuario nao existe entao validar se o suario quer tentar novamente 
                print("O usuario nao foi encontrado ou nao existe")
                if menu.input_validation(2,"dejesa tentar novamente?\n1 - sim\n2 - não")== 2: break
            
            elif user_logado["status"] == "senha_err": # se a senha esta errada entao validar se o suario quer tentar novamente 
                print("Senha incorrecta")
                if menu.input_validation(2,"dejesa tentar novamente?\n1 - sim\n2 - não")== 2: break
            
            else:
                break


        if user_logado["type_user"] == 1: #Menu de admin
            

            while True:
                while True:
                    mensagem = menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
                    opcao = menu.input_validation(3,mensagem)

                    break

                if opcao == 1: #criar filme
                    while True:
                        mensagem = f'''Para criar um filme seleciona uma das siguientes opçoes\n1 - [L]  para todu publico\n2 - [10] para maiores de 10\n3 - [12] para maiores de 12\n4 - [14] para maiores de 14\n5 - [16] para maiores de 16\n6 - [18] Maior de idade2'''
                        opcao = menu.input_validation(6,mensagem)
                    
                        db_management.create_filme(cursor,conection_db,classi_indicativa[opcao])

                        opcao = menu.input_validation(2,"Deseja criar outro filme?")

                        if opcao== 2:
                            print("Voltando ")
                            break


                elif opcao == 2: #modificar filme
                    filmes_db = db_management.Extrair_filmes(cursor,2)

                    print("Escolha uma das siguientes opçoes:")

                    opçao = menu.input_validation(2,"1 - Modificar Tudo \n2 - Modificar uma das informaçoes")
                    menu.ver_filmes(filmes_db)

                    if opcao == 2:
                        filme = menu.select_filme(filmes_db)
                        id_filme = filme[0]
                        opcao = menu.menu_mod_filme()
                        db_management.mod_filme(cursor,conection_db,id_filme,opcao,2)

                    else:
                        filme = menu.select_filme(filmes_db)
                        id_filme = filme[0]
                        db_management.mod_filme(cursor,conection_db,id_filme,0)
            
                elif opcao == 3: #criar categoria
                    db_management.create_categoria(cursor, conection_db)
                else:
                    break

            
        if user_logado["type_user"] == 0: #menu user
            while True:
                print("menu usuario normal")
                opcao = menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
            
                if opcao == 1: #VER TODOS OS FILMES
                    while True:
                        filmes_db = db_management.Extrair_filmes(cursor,1)
                        menu.ver_filmes(filmes_db)

                        print("deseja ver mais de um dos filmes?")

                        opcao = menu.input_validation(2,"1 - sim \n2- nao (voltar)")

                        if opcao == 1:
                            filme = menu.select_filme(filmes_db) # orden de filme = id, titulo, nota, classificacao, sinopse
                            menu.ver_filme(filme)
                            opcao = menu.input_validation(2,"Deseja avaliar este filme?:\n1 - sim\n2 - voltar aos filmes\n3 - voltar ao menu")

                            avaliacao["id_filme"] = filme[0]
                            avaliacao["id_usuario"]= user_logado["id"]

                            if opcao == 1:

                                if not db_management.avaliacao_exist(cursor,user_logado["id"],filme[0]):
                                    print("ingresa as siguientes informaçoes:")

                                    avaliacao["nota"] = menu.input_validation(10,"Como foi o filme para você de 1 ao 10? 1 É Ruim :c e É 10 - Perfeitooo!!!)")
                                    avaliacao["comentario"] = input("Comentario: ")
                                    print("fuera: ",avaliacao)

                                    db_management.create_avaliacao(cursor,conection_db,avaliacao)
                                else:
                                    print("ingresa as siguientes informaçoes:")
                                    
                                    avaliacao["nota"] = menu.input_validation(10,"Como foi o filme para você de 1 ao 10? 1 É Ruim :c e É 10 - Perfeitooo!!!\nNota:)")
                                    avaliacao["comentario"] = input("Comentario: ")
                                    print("fuera: ",avaliacao)

                                    db_management.update_avaliacao(cursor,conection_db,avaliacao)
                        
                            elif opcao == 3:
                                break
                        
                            print("voltanto aos filmes")
                        else:
                            break
                        

                elif opcao == 2: #BUSCAR FILMES

                    buscar = input("Ingresa o nome do filme:")

                    filmes_db = db_management.buscar_filme(cursor,buscar)
                    menu.ver_filmes(filmes_db)

                    print("deseja ver mais de um dos filmes?")

                    opcao = menu.input_validation(2,"1 - sim 2- nao (voltar)")

                    if opcao == 1: 
                        filme = menu.select_filme(filmes_db) 
                        menu.ver_filme(filme)
                        id_filme = filme[0]
                        
                        opcao = menu.input_validation(2,"Deseja avaliar este filme?:\n1 - sim\n2 - voltar aos filmes\n3 - voltar ao menu")
                        
                        if opcao == 1:
                            
                            avaliacao["id_filme"] = id_filme
                            avaliacao["id_usuario"]= user_logado["id"]

                            if db_management.avaliacao_exist(cursor) == False:
                                print("ingresa as siguientes informaçoes:")

                                avaliacao["nota"] = menu.input_validation(10,"Como foi o filme para você de 1 ao 10? \n1 É Ruim :c e É 10 - Perfeitooo!!!)")
                                avaliacao["comentario"] = input("Comentario: ")

                                db_management.create_avaliacao(cursor,conection_db,avaliacao)
                            else:
                                print("ingresa as siguientes informaçoes:")
                                avaliacao["nota"] = menu.input_validation(10,"Como foi o filme para você de 1 ao 10? \n1 É Ruim :c e É 10 - Perfeitooo!!!)")
                                avaliacao["comentario"] = input("Comentario: ")

                                db_management.update_avaliacao(cursor,conection_db,avaliacao)
                        
                        elif opcao == 3:
                            break
                        
                        print("voltanto aos filmes")
                    else:
                        break
                elif opcao == 3: #VER TOP FIVE 
                    
                    filmes_db = db_management.Extrair_filmes(cursor)
                    menu.ver_filmes(filmes_db)
                    opcao = menu.input_validation(2,"Deseja ver mais de um dos filmes?")

                    if opcao == 1:
                        filme = menu.select_filme(filmes_db)
                        menu.ver_filme(filme)

                    else:
                        print("Voltando")
                        break

                    opcao = menu.input_validation(2,"Deseja avaliar este filme?:\n1 - sim\n2 - voltar aos filmes\n3 - voltar ao menu")
                
                    if opcao == 1:
                        avaliacao["id_filme"] = id_filme
                        avaliacao["id_usuario"]= user_logado["id"]

                        if db_management.avaliacao_exist(cursor) == False:
                            print("ingresa as siguientes informaçoes:")

                            avaliacao["nota"] = menu.input_validation(10,"Como foi o filme para você de 1 ao 10? 1 É Ruim :c e É 10 - Perfeitooo!!!\nNota:)")
                            avaliacao["comentario"] = input("Comentario: ")

                            db_management.create_avaliacao(cursor,conection_db,avaliacao)
                        else:
                            print("ingresa as siguientes informaçoes:")
                            avaliacao["nota"] = menu.input_validation(10,"Como foi o filme para você de 1 ao 10? 1 É Ruim :c e É 10 - Perfeitooo!!!\nNota:)")
                            avaliacao["comentario"] = input("Comentario: ")

                            db_management.update_avaliacao(cursor,conection_db,avaliacao)
                else:
                    print("VOLTE PRONTOOOOOO!!!!")
                    break

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


