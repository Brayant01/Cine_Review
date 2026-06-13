import mysql.connector

def conect_data_base():
    return  mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1234",
        database = "cine_review"
    )

#------------------ Funcoes de verificaçoes -----------------------

#login do usuario valida o login do usuario pasando um dicionario
def login_user(cursor, email, senha_input):
    
    query = "SELECT id, nome, senha, type_user FROM usuario WHERE email = %s"  #Verifica o valor senha e admin na db de usuario
    
    cursor.execute(query,(email,))
    resultado = cursor.fetchone()

    if not resultado: #se nao tem usuario devolve 0 e uma mensagem
        print("O usuário não existe, voltando ao início...")
        return {"status":"no_user"} # 2 = erro ao fazer login se esse valor é retornado entao validar input do usuario
    
    #pasa a senha_db o resuldado da consulta com o valor da senha na base de dados e o valor admin
    id_user, nome, senha_db, type_user = resultado 

    if senha_db != senha_input:
        print("Senha incorreta.")
        return {"status": "senha_err"}

    
    print("O usuário foi logado.")
    return {"status":"ok", "id":id_user,"nome":nome, "type_user": type_user}


#valida se pode o nao criar uma conta de administrador
def val_create_admin():
    print("Para criar uma conta de administrador, preencha as seguintes informações: ")

    admin = input("Administrador: ").lower()
    senha = input("Senha: ")

    if admin != "root" or senha != "123":
        print("Credenciais incorretas.")
        return False
    
    return True

#------------------- modificar dados do banco de dados -------------------#

def mod_filme(cursor,conection_db, id_filme, opcao_mod, nova_class,type_mod):
    
    try:

        if type_mod == 1: #Modificar todo o filme
            nome = input("Digite o novo nome: ")
            print("Nova classificação: ", nova_class)
            sinopse = input("Digite a nova sinopse: ")

            query = "UPDATE filme SET titulo = %s, classificacao_indicativa = %s, sinopse = %s WHERE id = %s"
            cursor.execute(query,(nome, nova_class, sinopse, id_filme))

        else: #modificar uma parte do filme
            if opcao_mod == "Classificação":
                print("Classificação: ")
                query = "UPDATE filme SET classificacao_indicativa = %s WHERE id = %s"
                cursor.execute(query,(nova_class,id_filme))
                print("Classificação modificada.")
            else:
                print(f"Digite a nova informação para @{opcao_mod}")
                modificacao = input(f"Novo/a {opcao_mod}: ")

                query = f"UPDATE filme SET {opcao_mod} = %s WHERE id = %s"
                cursor.execute(query,(modificacao,id_filme))
            
    
        conection_db.commit()
        print("Modificação feita com sucesso!")

    except Exception as error:
        
        conection_db.rollback()
        print("Erro ao modificar o filme",error)

#------------------- ver dados do banco de dados -------------------#


def Extrair_filmes(cursor, opcao):
#filmes_db = id, titulo, nota, classificacao, ano_lancamento
    if opcao == "todos": # ver todos os filmes da base de dados
        query='''
            SELECT filme.id, filme.titulo, AVG(avaliacao.nota) AS nota, filme.classificacao_indicativa, filme.ano_lancamento, sinopse  FROM filme
            LEFT JOIN avaliacao
            ON filme.id = avaliacao.id_filme
            GROUP BY filme.id
            ORDER BY filme.titulo
        '''
    elif opcao == "top5": #ver o top 5 dos filmes
        query='''
            SELECT filme.id, filme.titulo, AVG(avaliacao.nota) AS nota, filme.classificacao_indicativa, filme.ano_lancamento, sinopse  FROM filme
            LEFT JOIN avaliacao
            ON filme.id = avaliacao.id_filme
            GROUP BY filme.id
            ORDER BY nota DESC
            LIMIT 5
        '''
    else: #ver filmes por categoria
        query = '''
            SELECT filme.id, filme.titulo, AVG(avaliacao.nota) AS nota, filme.classificacao_indicativa, filme.ano_lancamento, sinopse  FROM filme
            LEFT JOIN avaliacao
            ON filme.id = avaliacao.id_filme
            JOIN film_cat
            ON filme.id = film_cat.id_filme
            JOIN categoria
            ON categoria.id = film_cat.id_categoria
            WHERE categoria.genero = %s
            GROUP BY filme.id
            ORDER BY filme.titulo
        '''
        try:    
            cursor.execute(query,(opcao,))
            return cursor.fetchall() #trai todos os filmes
        except mysql.connector.Error as error:
            print("ERRO:", error)
            return []


    try:    
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        print("ERRO:", error)
        return []

def buscar_filme(cursor, nome_busca):
    try:
        nome = f"%{nome_busca}%"

        cursor.execute('''
                       SELECT filme.id, filme.titulo, avg(avaliacao.nota) as nota, filme.classificacao_indicativa, filme.ano_lancamento, filme.sinopse FROM filme 
                       
                       LEFT JOIN avaliacao
                       ON filme.id = avaliacao.id_filme

                       WHERE filme.titulo LIKE %s

                       GROUP BY filme.id
                       ''', (nome,))
        
        return cursor.fetchall()
    except Exception as error:
        print(f"\nERRO:{error}")
        return error
    

def Extrair_categoria(cursor):
    try:
        cursor.execute("SELECT id,genero FROM categoria")
        return cursor.fetchall()
    except Exception as error:
        print(f"\nERRO:{error}")
        return error
    
def Extrair_avaliacoes(cursor,id_filme): #avaliação = id, id usuario, nota, comentario <- orden de retorno
    try:
        cursor.execute('''
                       SELECT avaliacao.id_usuario, usuario.nome as nome ,avaliacao.nota, avaliacao.comentario, DATE_FORMAT(avaliacao.dia_avaliacao, '%d/%m/%Y %H:%i') FROM avaliacao
                       
                       JOIN usuario
                       ON avaliacao.id_usuario = usuario.id

                       LEFT JOIN filme
                       ON avaliacao.id_filme = filme.id 

                       WHERE filme.id = %s

                       ORDER BY filme.id 
                       ''', (id_filme,))

        return cursor.fetchall()
    except Exception as error:
        print("ERRO: ",error)
        return []
    
#------------------- agregar dados no banco de dados -------------------#

#Cria um filme agregando ele na base de dados se nao entao devolve um error
def create_filme(cursor, conection_db, classificacao_indicativa):
    
    titulo = str(input("Digite o título do filme: ")).lower()
    ano_lancamento = str(input("\nDigite o ano do lançamento: "))
    sinopse = str(input("\nDigite uma sinopse: "))

    try:
        query = "INSERT INTO filme (titulo, ano_lancamento, sinopse, classificacao_indicativa) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (titulo,ano_lancamento,sinopse,classificacao_indicativa))
        conection_db.commit()
        print("-------------- Filme criado --------------")
        print("Voltando ao menu inicial. Faça login com a opção 2.")
        return True
    except mysql.connector.Error as error:
        if error == 1062:
            print("ESTE FILME JÁ FOI ADICIONADO NA CATEGORIA ESCOLHIDA")
        
        conection_db.rollback()
        return error

#cria um usuario e agrega ele na base de datos se nao entao devolve um error
def create_usuario(cursor, conection_db, type_user = 0):
    nome  = str(input("\nDigite seu Nome: ")).lower()
    senha = str(input("\nDigite sua Senha: "))
    email = str(input("\nDigite seu Email: ")).lower()

    try:
        query = "INSERT INTO usuario (nome,senha,email,type_user) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (nome,senha,email,type_user))
        conection_db.commit()
        print("------- Usuário criado! ----------")
        print("Voltando ao menu inicial. Faça login com a opção 2.")
        return True
    except Exception as error:
        print("Erro ao criar usuário:", error)
        conection_db.rollback()
        return error

#fuçoes para as avaleacoes

def avaliacao_exist(cursor, id_user, id_filme):

    query = "SELECT id FROM avaliacao WHERE id_usuario = %s AND id_filme = %s"

    cursor.execute(query,(id_user,id_filme))
    
    resultado = cursor.fetchone()

    return resultado

def create_avaliacao(cursor, conection_db, avaliacao):

    try:
        query = '''INSERT INTO avaliacao (id_usuario, id_filme, nota, comentario) VALUES (%(id_usuario)s, %(id_filme)s, %(nota)s, %(comentario)s)'''
        cursor.execute(query, avaliacao)
        conection_db.commit()

        print("Obrigado por avaliar este filme!")
        return True
    except Exception as error:
        print("Não foi possível fazer esta avaliação")
        print("ERRO:",error)
        conection_db.rollback()
        return error 

def update_avaliacao(cursor, conection_db, nova_avaliacao):
    try:
        query = "UPDATE avaliacao SET nota = %(nota)s, comentario = %(comentario)s WHERE id_usuario = %(id_usuario)s AND id_filme = %(id_filme)s"
        cursor.execute(query, nova_avaliacao)
        
        conection_db.commit()

        print("SUA AVALIAÇÃO FOI ATUALIZADA!!!")
        return True
    except Exception as error:
        print("Não foi possível fazer esta avaliação")
        conection_db.rollback()
        print(error)
        
        return error 

#Cria uma categodia e agrega ela na base de dados
def create_categoria(cursor, conection_db):
    print("Digite o nome do gênero desta categoria")

    genero = input("Gênero:")

    try:
        query = "INSERT INTO categoria (genero) VALUES (%s)"
        cursor.execute(query, (genero,))
        conection_db.commit()    
        print("------- Categoria criada ----------")
        print("Voltando ao menu.")
        return True
    except Exception as error:
        conection_db.rollback()
        return error
    

#cria um film_cat e o agrega na basse de dados
def create_film_cat(cursor, conection_db, id_filme,id_categoria):

    try:
        query = "INSERT INTO film_cat (id_filme,id_categoria) VALUES (%s,%s)"
        cursor.execute(query,(id_filme,id_categoria))
        conection_db.commit()
        print("------- Filme adicionado nesta categoria ----------")
        print("Voltando ao menu.")
        return True
    
    except Exception as error:
        print("Erro ao adicionar o filme", error)
        conection_db.rollback()
        return error

def eliminar_filme(cursor, conetion_db, id_filme):
    try:
        cursor.execute("DELETE FROM avaliacao WHERE id_filme = %s",(id_filme,))
        cursor.execute("DELETE FROM film_cat WHERE id_filme = %s",(id_filme,))
        cursor.execute("DELETE FROM  filme WHERE id = %s",(id_filme,))

        conetion_db.commit()

        print("FILME APAGADO DA BASE DE DADOS!")
    except Exception as error:
        print(f"Erro {error}")

