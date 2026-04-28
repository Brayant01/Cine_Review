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

    #print("id:",id_user," senha:",senha_db," user type:",user_type," nome:", nome)
    print("id: senha:",senha_db)

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


#------------------- agregar dados no banco de dados -------------------#

#Cria um filme agregando ele na base de dados se nao entao devolve um error
def create_filme(cursor, conection_db, classificacao_indicativa):
    
    titulo = str(input("\nIngrea o titulo do filme: ")).lower()
    ano_lancamento = str(input("\nIngresa o ano do lançamento: "))
    sinopse = str(input("\nIngresa uma sinpse: "))

    try:
        query = "INSERT INTO filme (titulo, ano_lancamente, sinopse, classificacao_indicativa) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (titulo,ano_lancamento,sinopse,classificacao_indicativa))
        conection_db.commit()
        print("-------------- Filme criado --------------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")
        return True
    except Exception as error:
        print("Error ao criar FILEM",error)
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

#Cria uma avaliaçao e agrega ela na base de dados

def create_avaliaçao(cursor, conection_db, avaliacao):

    try:
        query = "INCERT INTO avaliacao (id_usuario, id_filme,nota,comentario) VALUES %s,%s,%s,%s"

        cursor.execute(query
                       ,avaliacao["id_usuario"]
                       ,avaliacao["id_filme"]
                       ,avaliacao["nota"]
                       ,avaliacao["comentario"] )
        
        conection_db.commit()

        print("obrigado por avaliar este filme!!!")
        return True
    except Exception as error:
        print("Nao foi possivel fazer esta avaleaçao")
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

#cria uma avaliaçao pelo usuario e agrega ela na basse de dados
def create_avaliacao(cursor, conection_db, id_usuario, id_filme,nota,comentario):

    try:
        query = "INSERT INTO avaliacao (id_usuario, id_filme, nota, comentario) VALUES (%s,%s,%s,%s)"
        cursor.execute(query,id_usuario,id_filme,nota,comentario)
        conection_db.commit()
        print("------- avaliaçao agregada neste Filme ;) ----------")
        print("voltando ao menu")
        return True
    
    except Exception as error:
        print("Error ao agrgar esta avaliaçao", error)
        conection_db.rollback()
        return error