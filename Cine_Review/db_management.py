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

def mod_filme(cursor,conection_db, id_filme, opcao_mod, nova_class,type_mod):
    
    try:

        if type_mod == 1: #Modificar todo o filme
            nome = input("Ingressa o novo nome:")
            print("Nova calificaçao: ", nova_class)
            sinopse = input("Ingressa a nova sinpse:")

            query = "UPDATE filme SET titulo = %s, classificacao_indicativa = %s, sinopse = %s WHERE id = %s"
            cursor.execute(query,(nome, nova_class, sinopse, id_filme))

        else: #modificar uma parte do filme
            if opcao_mod == "classificaçao":
                print("classificaçao :)")
                query = "UPDATE filme SET classificacao_indicativa = %s WHERE id = %s"
                cursor.execute(query,(nova_class,id_filme))
                print("Classificaçao modificada")
            else:
                print(f"Ingresa a nova informaçao para @ {opcao_mod}")
                modificacao = input(f"Novo/a {opcao_mod}: ")

                query = f"UPDATE filme SET {opcao_mod} = %s WHERE id = %s"
                cursor.execute(query,(modificacao,id_filme))
            
    
        conection_db.commit()
        print("Modificaçao feita con susesso!!!")

    except Exception as error:
        
        conection_db.rollback()
        print("error ao modificar o filme",error)

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
            print("ERROR:", error)
            return []


    try:    
        cursor.execute(query)
        return cursor.fetchall()
    except mysql.connector.Error as error:
        print("ERROR:", error)
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
        print(f"\nERROR:{error}")
        return error
    

def Extrair_categoria(cursor):
    try:
        cursor.execute("SELECT id,genero FROM categoria")
        return cursor.fetchall()
    except Exception as error:
        print(f"\nERROR:{error}")
        return error
    
def Extrair_avaliacoes(cursor,id_filme): #avaleaçao = id, id usuario, nota, comentario <- orden de retorno
    try:
        cursor.execute('''
                       SELECT avaliacao.id_usuario, usuario.nome as nome ,avaliacao.nota, avaliacao.comentario FROM avaliacao
                       
                       JOIN usuario
                       ON avaliacao.id_usuario = usuario.id

                       LEFT JOIN filme
                       ON avaliacao.id_filme = filme.id 

                       WHERE filme.id = %s

                       ORDER BY filme.id 
                       ''', (id_filme,))

        return cursor.fetchall()
    except Exception as error:
        print("ERROR: ",error)
        return []
    
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
    except mysql.connector.Error as error:
        if error == 1062:
            print("ESTE FILME JA FOI AGREGADO NA CATEGORIA ESCOLHIDA")
        
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
        query = "UPDATE avaliacao SET nota = %(nota)s, comentario = %(comentario)s WHERE id_usuario = %(id_usuario)s AND id_filme = %(id_filme)s"
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
        conection_db.rollback()
        return error
    

#cria um film_cat e o agrega na basse de dados
def create_film_cat(cursor, conection_db, id_filme,id_categoria):

    try:
        query = "INSERT INTO film_cat (id_filme,id_categoria) VALUES (%s,%s)"
        cursor.execute(query,(id_filme,id_categoria))
        conection_db.commit()
        print("------- Filme agregado nesta categoria ----------")
        print("voltando ao menu")
        return True
    
    except Exception as error:
        print("Error ao agrgar o filme", error)
        conection_db.rollback()
        return error

def eliminar_filme(cursor, conetion_db, id_filme):
    try:
        cursor.execute("DELETE FROM avaliacao WHERE id_filme = %s",(id_filme,))
        cursor.execute("DELETE FROM film_cat WHERE id_filme = %s",(id_filme,))
        cursor.execute("DELETE FROM  filme WHERE id = %s",(id_filme,))

        conetion_db.commit()

        print("Filme eliminado da base de dados")
    except Exception as error:
        print(f"Error {error}")

