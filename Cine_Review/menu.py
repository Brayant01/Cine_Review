#validador de opcao com bucle infinito
def input_validation(valor_max, mensagem):

   while True: 
        print(mensagem)
        
        try :
            opcao = int(input("\nopcao: "))
            
            if  opcao > valor_max or opcao < 1:
                print("\n" + "=" * 60)
                print("\n❌ Opção inválida!")
                print("Por favor, escolha um valor válido do menu.\n")

                input("Pressione ENTER para continuar...")

                print("\n" + "=" * 60 +"\n")
            else:
                return opcao
        
        except ValueError:
            print("\n" + "=" * 60)
            print("\n⚠️  !Entrada inválida!")
            print("Digite apenas números válidos.\n")

            input("Pressione ENTER para continuar...")

            print("\n" + "=" * 60 +"\n")

#----------------- Opçoes do menu principal -----------------
def option_validation(aux):
    
    if aux == 1:
        mensagem= (    
            "\n============================================================\n"
            "\n               🎬 Deseja ver filme?\n"
            "[1] Ver todos os Filme\n"
            "[2] Ver o TOP 5 *o*\n"
            "[3] Ver por categoria\n"
            "[4] Voltar\n"
            "\n============================================================"
        )
        opcao = 4
    elif aux == 2:
        mensagem= (
        "\n============================================================\n"
        "\n               🎬 Deseja ver detalhes de um filme?\n"
        "[1] Sim\n"
        "[2] Não\n"
        "\n============================================================"
        )
        opcao = 2
    elif aux == 3:
        mensagem= (
        "============================================================\n"
        "\n               🔄 Deseja tentar novamente?\n"
        "[1] Sim\n"
        "[2] Não\n"
        "\n============================================================\n"
        )
        opcao = 2
    elif aux  == 4:
        mensagem = (
            "\n============================================================\n"
            "                CLASSIFICAÇÃO INDICATIVA"
            "\n============================================================\n"

            "\nEscolha a classificação do filme:\n"

            "[1] L   - Livre para todos os públicos\n"
            "[2] 10  - Maiores de 10 anos\n"
            "[3] 12  - Maiores de 12 anos\n"
            "[4] 14  - Maiores de 14 anos\n"
            "[5] 16  - Maiores de 16 anos\n"
            "[6] 18  - Maiores de idade\n"

            "\n============================================================\n"
        )
        opcao = 6
    elif aux == 5:
        mensagem= (
        "\n============================================================\n"
        "\n               🎬 Deseja agregar outro filme?\n"
        "[1] Sim\n"
        "[2] Não\n"
        "\n============================================================"
        )

        opcao = 2
    elif aux == 6:
        mensagem= (
        "\n============================================================\n"
        "\n          ⚙️ Escolha uma das siguientes opçoes:?\n"
        "[1] Modificar Tudo\n"
        "[2] Modificar uma das informaçoes\n"
        "\n============================================================"
        )
        opcao = 2
    else:
        print("")
    
    return input_validation(opcao,mensagem)

def ver_filmes(filmes_db): 
    #filmes_db = id, titulo, nota, classificacao, ano_lancamento
    print("=" *60, "\n"," "*20 + "LISTA DE FILMES\n", "="*60)

    for i, filme in enumerate(filmes_db,start=1):
        id, titulo, nota, classificacao, ano,*_ = filme
        
        if not nota:
            texto_nota = f"😔 Sem avaleaçao"
        else:
            texto_nota = f"⭐ {nota:.1f} / 10"

        print(
            f"{i:<2}. "
            f"{titulo:<25} | "
            f"{classificacao:<2} | "
            f"{ano:<2} | "
            f"{texto_nota}"
            )
    print("\n","="*60 + "\n")
            
def ver_categorias(categorias):
    print("=" *60, "\n"," "*20 + "LISTA DE CATEGORIAS\n", "="*60)

    for i, categoria in enumerate(categorias,start=1):
        id, genero = categoria

        print(f"{i:<2} {genero}")
    
    print("\n","="*60+"\n")


def select_filme(filmes_db):#filmes_db = id, titulo, nota, classificacao, ano_lancamento
    selection = input_validation(len(filmes_db),"=============== ⬆️ Escolha uma dos filmes ⬆️ ===============")
    
    return filmes_db[selection-1]

def select_categoria(categorias_db):#filmes_db = id, titulo, nota, classificacao, ano_lancamento
    selection = input_validation(len(categorias_db),"============ ⬆️ Escolha uma das categorias ⬆️ ============")
    
    return categorias_db[selection-1]

def ver_filme(filme):# orden de filme = id, titulo, nota, classificacao, sinopse
    id, titulo,nota, classificacao, ano, sinopse = filme
    
    print("=" * 60)
    print(f"🎬 {titulo}")
    print("=" * 60)

    print(f"\n📌 Classificação: {classificacao}")

    if nota is None:
        print("😔 Nota média: Sem avaliações")
    else:
        print(f"⭐ Nota média: {nota:.1f}")

    print(f"📅 Ano: {ano}")

    print(f"\n📝 Sinopse:\n{sinopse}")

    print("\n" + "=" * 60 + "\n")


def menu_mod_filme():
    
    mensagem = (
        "============================================================\n"
        "                      MODIFICAR FILME\n"
        "============================================================\n"

        "Escolha uma informação para modificar:\n"

        "[1] Nome\n"
        "[2] Classificação\n"
        "[3] Sinopse\n"
        "============================================================\n")

    return input_validation(3, mensagem)


def menu_user_option(type_user,nome):
    
    # Se o usario for admin entao tem essas opçoes
    if(type_user == 1):

        mensagem=(
            "============================================================\n"
            "                   OPÇOES DE ADministrador\n"
            "============================================================\n"

            f"Benvido {nome} escolhe uma das opçoes:\n"
            "[1] Criar filme \n"
            "[2] Modificar/Eliminar filme\n"
            "[3] Criar categoria\n"
            "[4] Agregar Filmes em categoria\n"
            "[5] Sair\n"
            "============================================================\n"
        )

        return input_validation(4,mensagem)
        #print("2- modificar login??")
    
    else:
        #se o usuario nao for admin entao tem essas opçoes
    
        mensagem=(
            "============================================================\n"
            "                       OPÇOES DE USUARIO\n"
            "============================================================\n"

            f"Benvido {nome} escolhe uma das opçoes:\n"
            "[1] Ver todos os filmes\n"
            "[2] Buscar filme\n"
            "[3] ver top 5 *o*\n"
            "[4] Sair\n"
            "============================================================\n"
        )
        return input_validation(4,mensagem)
        
#---------------------------------------------------------------------------
def menu_criar_conta():
    mensagem =(
    f"\n============================================================\n"
    "                         CRIAR CONTA\n"
    "============================================================\n\n"

    "Escolha o tipo de conta:\n\n"
    "[1] Administrador\n"
    "[2] Usuário normal\n"
    "============================================================"
    )
    return input_validation(2,mensagem)



#------------------ MENU PRINCIPAL ------------------
def main_menu():
    
    mensagem = (
    "\n"
    "============================================================\n"
    "                    🎬 CINE REVIEW 🎬\n"
    "============================================================\n\n"
    "Escolha uma das opções abaixo:\n\n"
    "[1] Ver filmes\n"
    "[2] Fazer login\n"
    "[3] Criar uma conta\n"
    "[4] Sair\n"
    "============================================================"
    )

    opcaon = input_validation(4,mensagem)    
    return opcaon