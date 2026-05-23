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
    1: "classificacao_indicativa",
    2: "Titulo",
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
input()# ao iniciar o programa na terminal de vs ingresa-se de forma automatica a direçao do programa este input so esta para que nao seja mostrad ou ingresado no programa e mostre a mensajen de entrada invalida :c

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
                print("voltando ao menu principal")
                break
        
            if opcao == 1:
                filme = menu.select_filme(filmes_db)
                menu.ver_filme(filme)
                avaliacoes = db_management.Extrair_avaliacoes(cursor,filme[0])

                menu.ver_avaliacoes(avaliacoes)

            elif opcao == 2:
                print("\n🔄 Voltando...")
            else:
                print("\n🔄 Voltando ao menu ...")

    
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
                    while True:

                        opcao = menu.option_validation(6) #selecciona se vai modificar so uma das informaçoes ou tudo o filme
                        
                        if opcao == 3:# voltar pra o menu anterior
                            print("\n🔄  Voltando ao menu...\n")
                            break

                        while True:
                            filmes_db = db_management.Extrair_filmes(cursor,"todos")
                            menu.ver_filmes(filmes_db)
                            filme = menu.select_filme(filmes_db)

                            if opcao == 1: # vai modificar tudo o filme
                            
                                # para modificar tudo o filme tem que esolher primeiro tem que escolhe uma classificaçao
                                classi_indi = menu.option_validation(4)# escolhe uma classificaçao indicativa

                                db_management.mod_filme(cursor,conection_db, filme[0],"none",classi_indicativa[classi_indi],1)
                            elif opcao == 2: # vai modificar so uma das informaçoes
                        
                                mod_option = menu.menu_mod_filme()

                                #para modificar a classificaçao indicativa o usuario tera que escolher uma
                                if mod_option == 1:
                                    classi_indi = menu.option_validation(4)
                                    db_management.mod_filme(cursor, conection_db, filme[0], "classificaçao", classi_indicativa[classi_indi], "outra_mod")

                                    if menu.option_validation(5) == 2:
                                        break

                                else:
                                    db_management.mod_filme(cursor, conection_db, filme[0], options_mod_films[mod_option],"none", "outra_mod")

                                    if menu.option_validation(5) == 2:
                                        break
                                

                elif opcao == 3: #criar categoria
                    while True:
                        db_management.create_categoria(cursor, conection_db)

                        if menu.option_validation(3) == 2:
                            print("\n🔄  Voltando ao menu...\n")
                            break
                
                elif opcao == 4: # agregar um filme a uma categoria
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
                elif opcao == 5:
                    while True:
                        print("\n!!!ESTEJA SEGURO DE SEGUIR CON ESTA ACCÃO!!!\n")
                        filmes_db = db_management.Extrair_filmes(cursor, "todos")
                        menu.ver_filmes(filmes_db)
                        filme = menu.select_filme(filmes_db)

                        if menu.option_validation(7) == 1:
                            db_management.eliminar_filme(cursor, conection_db, filme[0])
                        
                        if menu.option_validation(5) == 2:
                            print("\n🔄  Voltando ao menu...\n")
                            break
                        
                else:
                    break
            
        if user_logado["type_user"] == 0: #menu user
            
            avaliacao["id_usuario"]= user_logado["id"]

            while True:
                opcao = menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
            
                if opcao == 1: #VER TODOS OS FILMES
                    while True:
                        filmes_db = db_management.Extrair_filmes(cursor,"todos")
                        menu.ver_filmes(filmes_db)

                        opcao = menu.option_validation(2)

                        if opcao == 1:
                            filme = menu.select_filme(filmes_db) # orden de filme = id, titulo, nota, classificacao, sinopse
                            menu.ver_filme(filme)
                            opcao = menu.input_validation(3,"[1] avaliar este filme\n[2] Ver comentarios\n[3] voltar aos filmes")

                            avaliacao["id_filme"] = filme[0]
                            
                            while True:
                                if opcao == 1: #avaliar o filme

                                    if not db_management.avaliacao_exist(cursor,user_logado["id"],filme[0]):
                                        print("\n🎬 AVALIAÇÃO DO FILME 🎬")
                                        print("Como foi o filme para você?")
                                        print("1 = Ruim :c | 10 = Perfeitooo!!! 🤩\n")

                                        avaliacao["nota"] = menu.input_validation(10,"Nota (1-10): ")
                                        avaliacao["comentario"] = input("Comentario: ")
                                        
                                        db_management.create_avaliacao(cursor,conection_db,avaliacao)
                                        print("Voltando aos filmes")
                                        break
                                    else:
                                        print("\n🎬 AVALIAÇÃO DO FILME 🎬")
                                        print("Como foi o filme para você?")
                                        print("1 = Ruim :c | 10 = Perfeitooo!!! 🤩\n")

                                        avaliacao["nota"] = menu.input_validation(10,"Nota (1-10): ")
                                        avaliacao["comentario"] = input("Comentario: ")
                                    
                                        db_management.update_avaliacao(cursor,conection_db,avaliacao)
                                        print("Voltando aos filmes")
                                        break
                                elif opcao == 2:
                                    avaliacoes = db_management.Extrair_avaliacoes(cursor,filme[0])
                                    menu.ver_avaliacoes(avaliacoes)

                                    if menu.input_validation(2,"Deseja avaliar este filme?: [1] SIM\n[2] NAO") == 1:
                                        opcao = 1 #Voltar directamente a avaliar o filme
                                    else:

                                        break

                                elif opcao == 3:
                                    break

                        else:
                            break
                        

                elif opcao == 2: #BUSCAR FILMES
                    while True:
                        
                        while True:
                            print("=" * 60)
                            print("\n         Bucar filme")
                            print("=" * 60)

                            buscar = input("Ingresa o nome do filme:")

                            filmes_db = db_management.buscar_filme(cursor,buscar)

                            if filmes_db:
                                menu.ver_filmes(filmes_db)
                                break
                            else:
                                print(f"Nao foi posivel encontrar o filme {buscar}")
                                
                        opcao = menu.option_validation(2)

                        if opcao == 1: # opçoes para o filme escolhido
                            filme = menu.select_filme(filmes_db) 
                            menu.ver_filme(filme)
                            id_filme = filme[0]
                            
                            while True:
    
                                opcao = menu.input_validation(3,"[1] avaliar este filme\n[2] Ver comentarios\n[3] voltar aos filmes")
                                
                                while True:
                                    if opcao == 1:# avaliado o filme seleccionado
                                        
                                        avaliacao["id_filme"] = id_filme

                                        if db_management.avaliacao_exist(cursor,user_logado["id"],filme[0]) == False:
                                            print("\n🎬 AVALIAÇÃO DO FILME 🎬")
                                            print("Como foi o filme para você?")
                                            print("1 = Ruim :c | 10 = Perfeitooo!!! 🤩\n")

                                            avaliacao["nota"] = menu.input_validation(10,"Nota (1-10): ")
                                            avaliacao["comentario"] = input("Comentario: ")

                                            db_management.create_avaliacao(cursor,conection_db,avaliacao)
                                            print("\n🔄  Voltando...\n")
                                            break
                                        else:
                                            print("\n🎬 AVALIAÇÃO DO FILME 🎬")
                                            print("Como foi o filme para você?")
                                            print("1 = Ruim :c | 10 = Perfeitooo!!! 🤩\n")

                                            avaliacao["nota"] = menu.input_validation(10,"Nota (1-10): ")
                                            avaliacao["comentario"] = input("Comentario: ")

                                            db_management.update_avaliacao(cursor,conection_db,avaliacao)

                                            print("\n🔄  Voltando...\n")
                                            break
                            
                                    elif opcao == 2:
                                        avaliacoes = db_management.Extrair_avaliacoes(cursor,filme[0])
                                        menu.ver_avaliacoes(avaliacoes)

                                        if menu.input_validation(2,"Deseja avaliar este filme?: [1] SIM\n[2] NAO") == 1:
                                            opcao = 1 #Voltar directamente a avaliar o filme
                                        else:

                                            break
                                         
                        else:
                            print("\n🔄  Voltando ao menu...\n")
                            break
                elif opcao == 3: #VER TOP FIVE 
                    while True:
                        filmes_db = db_management.Extrair_filmes(cursor,"top5")
                        menu.ver_filmes(filmes_db)
                        
                        opcao = menu.option_validation(2)

                        if opcao == 1:
                            filme = menu.select_filme(filmes_db)
                            id_filme = filme[0]
                            menu.ver_filme(filme)

                            opcao = menu.input_validation(3,"[1] avaliar este filme\n[2] Ver comentarios\n[3] voltar aos filmes")
                            
                            while True:
                                if opcao == 1:
                                    avaliacao["id_filme"] = id_filme

                                    if db_management.avaliacao_exist(cursor,user_logado["id"],filme[0],) == False:
                                        print("\n🎬 AVALIAÇÃO DO FILME 🎬")
                                        print("Como foi o filme para você?")
                                        print("1 = Ruim :c | 10 = Perfeitooo!!! 🤩\n")

                                        avaliacao["nota"] = menu.input_validation(10,"Nota (1-10): ")
                                        avaliacao["comentario"] = input("Comentario: ")

                                        db_management.create_avaliacao(cursor,conection_db,avaliacao)
                                        print("\n🔄  Voltando...\n")
                                        break
                                    else:
                                        print("\n🎬 AVALIAÇÃO DO FILME 🎬")
                                        print("Como foi o filme para você?")
                                        print("1 = Ruim :c | 10 = Perfeitooo!!! 🤩\n")

                                        avaliacao["nota"] = menu.input_validation(10,"Nota (1-10): ")
                                        avaliacao["comentario"] = input("Comentario: ")

                                        db_management.update_avaliacao(cursor,conection_db,avaliacao)
                                        print("\n🔄  Voltando...\n")
                                        break
                                elif opcao == 2:
                                    avaliacoes = db_management.Extrair_avaliacoes(cursor,filme[0])
                                    menu.ver_avaliacoes(avaliacoes)

                                    if menu.input_validation(2,"Deseja avaliar este filme?: [1] SIM\n[2] NAO") == 1:
                                        opcao = 1 #Voltar directamente a avaliar o filme
                                    else:
                                        print("\n🔄  Voltando...\n")
                                        break
                        else:
                            print("\n🔄 Voltando...")
                            break
                    
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


