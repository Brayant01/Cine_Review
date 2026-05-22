
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
            
            opcao = menu.option_validation(1)

            if opcao == 1: #ver todos os filmes
                
                filmes_db = db_management.Extrair_filmes(cursor,"todos")
                menu.ver_filmes(filmes_db)
                opcao = menu.option_validation(2)

            elif opcao == 2: #ver o top 5

                filmes_db = db_management.Extrair_filmes(cursor,"top5")
                menu.ver_filmes(filmes_db)
                opcao = menu.option_validation(2)

            elif opcao == 3: #ver por categoria
                
                categorias_db = db_management.Extrair_categoria(cursor)
                menu.ver_categorias(categorias_db)
                categoria = menu.select_categoria(categorias_db)

                filmes_db = db_management.Extrair_filmes(cursor,categoria[1])
                menu.ver_filmes(filmes_db)
                opcao = menu.option_validation(2)

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
            print("\n")
            print("="*60,"\nPara logar ingresa as siguiente informaçoes",)
            print("="*60,"\n")

            email = input("Email: ").strip().lower()
            senha = input("Senha : ")

            user_logado = db_management.login_user(cursor,email,senha) #chama a funçao e guarda um dicionario con dados para verificar que o login foi certo ou nao

            if user_logado["status"] == "no_user": # se o usuario nao existe entao validar se o suario quer tentar novamente 

                if menu.option_validation(3)== 2: 
                    user_logado["type_user"] = "none"
                    break
            
            elif user_logado["status"] == "senha_err": # se a senha esta errada entao validar se o suario quer tentar novamente 

                if menu.option_validation(3)== 2: 
                    user_logado["type_user"] = "none"
                    break
            else:
                break


        if user_logado["type_user"] == 1: #Menu de admin
            

            while True:
                
                opcao = menu.menu_user_option(user_logado["type_user"],user_logado["nome"])

                if opcao == 1: #criar filme
                    while True:
                        opcao = menu.option_validation(4)

                        db_management.create_filme(cursor,conection_db,classi_indicativa[opcao])

                        if menu.option_validation(5) != 1:
                            print("\n🔄  Voltando ao menu...\n")
                            break


                elif opcao == 2: #modificar filme
                    filmes_db = db_management.Extrair_filmes(cursor,"todos")

                    opcao = menu.option_validation(6)
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
                
                elif opcao == 4: # falta hacer la parte para "agregar" el filme en la categoria
                    categorias_db = db_management.Extrair_categoria(cursor)
                    menu.ver_categorias(categorias_db)
                    categoria = menu.select_categoria(categorias_db)

                    filmes_db = db_management.Extrair_filmes(cursor,"todos")
                    
                    while True:
                        menu.ver_filmes(filmes_db)
                        filme = menu.select_filme(filmes_db)
                        
                        if db_management.create_film_cat(cursor, conection_db, filme[0], categoria[0]) != True:
                            if menu.option_validation(3) == 2:
                                print("\n🔄  Voltando ao menu...\n")
                                break
                        else:
                            if menu.option_validation(5) != 1:
                                print("\n🔄  Voltando ao menu...\n")
                                break
                else:
                    break
            
        if user_logado["type_user"] == 0: #menu user
            while True:
                opcao = menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
            
                if opcao == 1: #VER TODOS OS FILMES
                    while True:
                        filmes_db = db_management.Extrair_filmes(cursor,"todos")
                        menu.ver_filmes(filmes_db)

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
                    
                    filmes_db = db_management.Extrair_filmes(cursor,"top5")
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
                    if menu.option_validation(3)==2:
                        print("vontando ao menu inicial")
                        break
                else:
                    db_management.create_usuario(cursor,conection_db,1)
                    break
            else:
                db_management.create_usuario(cursor,conection_db,0)
                break

              
    else:
        conection_db.close()
        print("Obridado por usar nosso serviço ate mais!!!!")
        break


