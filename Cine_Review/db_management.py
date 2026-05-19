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
        print("O usuario nao existe voltando ao inicio")
        return {"status":"no_user"} # 2 = erro ao fazer login se esse valor é retornado entao validar input do usuario
    
    #pasa a senha_db o resuldado da consulta com o valor da senha na base de dados e o valor admin
    id_user, nome, senha_db, type_user = resultado 

    if senha_db != senha_input:
        print("Senha incorrecta")
        return {"status": "senha_err"}

    
    print("O usuario foi logado")
    return {"status":"ok", "id":id_user,"nome":nome, "type_user": type_user}


#valida se pode o nao criar uma conta de administrador
def val_create_admin():
    print("para criar uma conta de administrador ingresa as siguietes informaçoes")

    admin = input("Administrador:").lower()
    senha = input("Senha: ")

    if admin != "root" or senha != "123":
        print("Credenciais incorrectas")
        return False
    
    return True

#------------------- modificar dados do banco de dados -------------------#

def mod_filme(cursor,conection_db, id_filme, opcao, type_mod):
    
    try:

        if type_mod == 2:
            print(f"Ingresa a nova informaçao para {opcao}")
            modificacao = input(f"Novo/a {opcao}: ")

            query = f"UPDATE filme {opcao} = %s WHERE id = %s"
            cursor.execute(query,modificacao,id_filme)
        else:
            nome = input("Ingressa o novo nome:")
            classificacao = input("Ingressa o novo nome:")
            sinopse = input("Ingressa o novo nome:")

            query = "UPDATE filme titulo = %s, cassificacao_indicativa = %s, sinopse = %s WHERE id = %s"
            cursor.execute(query,nome, classificacao, sinopse, id_filme)
    
        conection_db.commit()
        print("Modificaçao feita con susesso!!!")

    except Exception as error:
        
        conection_db.rollback()
        print("error ao modificar o filme",error)

#------------------- ver dados do banco de dados -------------------#


def Extrair_filmes(cursor, opcao):
#filmes_db = id, titulo, nota, classificacao, ano_lancamento
    if opcao == "todos":
        query='''
            SELECT filme.id, filme.titulo, AVG(avaliacao.nota) AS nota, filme.classificacao_indicativa, filme.ano_lancamento, sinopse  FROM filme
            LEFT JOIN avaliacao
            ON filme.id = avaliacao.id_filme
            GROUP BY filme.id
            ORDER BY filme.titulo
        '''
    elif opcao == "top5":
        query='''
            SELECT filme.id, filme.titulo, AVG(avaliacao.nota) AS nota, filme.classificacao_indicativa, filme.ano_lancamento, sinopse  FROM filme

            LEFT JOIN avaliacao
            ON filme.id = avaliacao.id_filme

            GROUP BY filme.id

            ORDER BY nota DESC
            LIMIT 5
        '''
    else:
        query = '''
            SELECT filme.id, filme.titulo, AVG(avaliacao.nota) AS nota, filme.classificacao_indicativa, filme.ano_lancamento, sinopse  FROM filme

            LEFT JOIN avaliacao
            ON filme.id = avaliacao.id_filme

            JOIN film_cat
            ON filme.id = film_cat.id_filme

            JOIN categoria
            ON categoria.id = film_cat.id_categoria

            where categoria.genero = %s

        '''
        try:    
            cursor.execute(query,(opcao,))
            return cursor.fetchall() #trai todos os filmes
        except mysql.connector.Error as error:
            print("ERROR:", error)
            return []


    try:    
        cursor.execute(query)
        return cursor.fetchall() #trai todos os filmes
    except mysql.connector.Error as error:
        print("ERROR:", error)
        return []

def buscar_filme(cursor, nome_busca):
    try:
        query = "SELECT id, titulo, classificacao_indicativa, ano_lancamento, sinopse FROM filme WHERE titulo LIKE %s"
        valor = f"%{nome_busca}%"

        cursor.execute(query, (valor,))
        return cursor.fetchall()
    except Exception as error:
        print(f"\nERROR:{error}")
        return error
    

def Extrair_categoria(cursor):
    try:
        query = "SELECT id,genero FROM categoria"
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as error:
        print(f"\nERROR:{error}")
        return error
    

#------------------- agregar dados no banco de dados -------------------#

#Cria um filme agregando ele na base de dados se nao entao devolve um error
def create_filme(cursor, conection_db, classificacao_indicativa):
    
    titulo = str(input("\nIngrea o titulo do filme: ")).lower()
    ano_lancamento = str(input("\nIngresa o ano do lançamento: "))
    sinopse = str(input("\nIngresa uma sinpse: "))

    try:
        query = "INSERT INTO filme (titulo, ano_lancamento, sinopse, classificacao_indicativa) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (titulo,ano_lancamento,sinopse,classificacao_indicativa))
        conection_db.commit()
        print("-------------- Filme criado --------------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")
        return True
    except Exception as error:
        print("Error ao criar FILME",error)
        conection_db.rollback()
        return error

#cria um usuario e agrega ele na base de datos se nao entao devolve um error
def create_usuario(cursor, conection_db, type_user = 0):
    nome  = str(input("\nIngresa teu Nome: ")).lower()
    senha = str(input("\nIngresa tua Senha: "))
    email = str(input("\nIngresa teu Email: ")).lower()

    try:
        query = "INSERT INTO usuario (nome,senha,email,type_user) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (nome,senha,email,type_user))
        conection_db.commit()
        print("------- Usuario criado ----------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")
        return True
    except Exception as error:
        print("Error ao criar usuario", error)
        conection_db.rollback()
        return error

#fuçoes para as avaleacoes

def avaliacao_exist(cursor, id_user, id_filme):

    query = "SELECT id FROM avaliacao WHERE id_usuario = %s AND id_filme = %s"

    cursor.execute(query,(id_user,id_filme))
    
    resultado = cursor.fetchone()
    print("aqui esta el peo:", resultado)

    return resultado

def create_avaliacao(cursor, conection_db, avaliacao):

    try:
        query = '''INSERT INTO avaliacao (id_usuario, id_filme, nota, comentario) VALUES (%(id_usuario)s, %(id_filme)s, %(nota)s, %(comentario)s)'''
        cursor.execute(query, avaliacao)
        conection_db.commit()

        print("obrigado por avaliar este filme!!!")
        return True
    except Exception as error:
        print("Nao foi possivel fazer esta avaleaçao")
        print("error:",error)
        conection_db.rollback()
        return error 

def update_avaliacao(cursor, conection_db, nova_avaliacao):
    try:
        query = "UPDATE avaliacao SET nota = %s, comentario = %s WHERE id_usuario = %s AND id_filme = %s"


        cursor.execute(query, nova_avaliacao)
        
        conection_db.commit()

        print("SUA AVALEAÇAO FOI ACTUALIZADA!!!")
        return True
    except Exception as error:
        print("Nao foi possivel fazer esta avaleaçao")
        conection_db.rollback()
        print(error)
        
        return error 

#Cria uma categodia e agrega ela na base de dados
def create_categoria(cursor, conection_db):
    print("ingresa o nome do genero desta categoria")

    genero = input("Genero:")

    try:
        query = "INSERT INTO categoria (genero) VALUES (%s)"
        cursor.execute(query,genero)
        conection_db.commit()    
        print("------- categoria criada ----------")
        print("voltando ao menu")
        return True
    except Exception as error:
        print("Error ao criar a categoria", error)
        conection_db.rollback()
        return error
    

#cria um film_cat e o agrega na basse de dados
def create_film_cat(cursor, conection_db, id_filme,id_categoria):

    try:
        query = "INSERT INTO film_cat (id_filme,id_categoria) VALUES (%s,%s)"
        cursor.execute(query,id_filme,id_categoria)
        conection_db.commit()
        print("------- Filme agregado nesta categoria ----------")
        print("voltando ao menu")
        return True
    
    except Exception as error:
        print("Error ao agrgar o filme", error)
        conection_db.rollback()
        return error

