
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
        
        menu.menu_ver_filme() # <--- esta funçao nao esta funcionando so para o codigo no ficar mostrando erro

        '''
            Esta parte do codigo precisa ser feita
            mostrar o top 5 de filmes
            o usuario debe poder ver os filmes por categoria 
            ou busacar o filme pelo nome.

            o usuario pode seleccionar um filme e ver as informaçoes do mesmo
            a seleçao pode ser feita por indices

            exenplo:

            o usuario olha a siguiente lista de filmes e con o numero digitado ver as informaçoes do filme

            1- Nitgmare in the elm street
            2- tranformer
            3- dragon ball broly

            as informaçoes que o usuario vair ver sao as siguientes:

            nome, classificaçao, descripçao, nota.

            esta parte do codigo é so para usuarios nao logados entao nao debe trocar nada do banco

        '''
    
    elif opcao==2: #login
        repetir = True

        while repetir == True:

            print("\nPara logar ingresa as siguiente informaçoes")
            email = input("Email: ").strip().lower()
            senha = input("Senha : ")

            user_logado = db_management.login_user

            if user_logado["type_user"] == 1:
                print("menu para admin")
                mensagem = menu.menu_user_option(user_logado["type_user"],user_logado["nome"])

                """
                    nesta parte do codigo temos que fazer a funcionadidades para o admin
                    o administrador debe ter as siguiente 3 opçoes (a funçao menu.menu_user_option() ja imprime as 3 opçoes na tela)
                    falta a logica, a funçao do menu so imprime na tela pode usar a funçao menu.nput_validation(numero de opçoes, mensajem a mostrar na tela)
                    para validar o inputo do usuario e assim ele pode seleccionar uma das opçoes sem erros

                    as opçoes do administrador:

                    1- criar filme
                    2- modificar filme
                    3- criar categoria"
                    4- voltar

                    todas as funçoes desta parte do codigo ja foram criadas é so implementar

                    o usuario pode nao querer mais continuar con estas opçao entao ele tem que voltar para o menu principal
                """
            
            if user_logado["type_user"] == 2:
                print("menu usuario normal")
                menu.menu_user_option(user_logado["type_user"],user_logado["nome"])
            
                """as opçoes do usuario normal:

                    1- ver filmes -> esta opçao tem que cumplir con o da primera opçao do primer menu
                    2- avaliar filmes
                    4- voltar

                    todas as funçoes desta parte do codigo ja foram criadas é so implementar

                    o usuario pode nao querer mais continuar con estas opçao entao ele tem que voltar para o menu principal
                """

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


