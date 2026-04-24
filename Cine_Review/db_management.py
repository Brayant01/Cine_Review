import mysql.connector

def conect_data_base():
    return  mysql.connector.connect(
        host = "localhost",
        user = "root",
        password = "1234",
        database = "cine_review"
    )

#------------------ Funcoes que mexen no banco de dados -----------------------

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
        return False

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
        return False

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
        return False
    

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
        return False

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
        conection_db()
        return False