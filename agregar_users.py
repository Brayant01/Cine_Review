import mysql.connector

conexion_a_base_de_dados = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = "prueba1"
)

cursor = conexion_a_base_de_dados.cursor()

#---------------- Funçoes do programa ;) ----------------#

#validador de opciones com bucle infinito
def input_validation(valor_max, mensagem):

   while True: 
        print(mensagem)
        valor = int(input("opcao: "))

    
        if  valor > valor_max or valor < 1:
            print("\ningresa um valor correcto")
            input("presiona qualquer tecla para continuar\n")
        else:
            return valor

def create_filme(cursor, classificacao_indicativa):
    
    titulo = str(input("\nIngrea o titulo do filme: ")).lower
    ano_lancamento = str(input("\nIngresa o ano do lançamento: ")).lower
    sinopse = str(input("\nIngresa uma sinpse: ")).lower

    try:
        query = "INSERT INTO filme (titulo, ano_lancamente, sinopse, classificacao_indicativa) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (titulo,ano_lancamento,sinopse,classificacao_indicativa))
        conexion_a_base_de_dados.commit()
        print("-------------- Filme criado --------------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")
    
    except:
        cursor.execute("create table filme("
                       "id int primary key auto_increment not null,"
                       "titulo varchar(255) not null,"
                       "ano_lancamento year not null,"
                       "sinopse text not null,"
                       "classificacao_indicativa enum('L', '10', '12', '14', '16', '18') not null);")
        
        query = "INSERT INTO filme (titulo, ano_lancamente, sinopse, classificacao_indicativa) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (titulo,ano_lancamento,sinopse,classificacao_indicativa))
        conexion_a_base_de_dados.commit()
        print("-------------- Filme criado --------------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")


#cria um usuario e agrega ele na base de datos, se nao existe a tabla crea uma de uma vez e agrega o usuario
def criar_usuario(cursor, admin = 0):
    nome  = str(input("\nIngresa teu Nome: ")).lower
    senha = str(input("\nIngresa tua Senha: ")).lower
    email = str(input("\nIngresa teu Email: ")).lower

    try:
        query = "INSERT INTO usuario (nome,senha,email,admin) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (nome,senha,email,admin))
        conexion_a_base_de_dados.commit()
        print("------- Usuario criado ----------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")

    except:
        cursor.execute("CREATE TABLE usuario("
                        "id int primary key auto_increment not null,"
                        "nome varchar(150) not null,"
                        "senha varchar(255) not null,"
                        "email varchar(255) not null unique,"
                        "admin tinyint(1) default 0);")
        
        query = "INSERT INTO usuario (nome,senha,email,admin) VALUES (%s,%s,%s,%s)"
        cursor.execute(query, (nome,senha,email,admin))
        conexion_a_base_de_dados.commit()
        print("------- Usuario criado ----------")
        print("voltando ao menu inicial favor de fazer login com a opçao 2")



#valida o login do usuario pasando um de 3 valores
def user_login(senha,email):
    
    query = "SELECT senha FROM usuario WHERE email = %s"
    cursor.execute(query,(email,))

    resultado_busqueda = cursor.fetchone()

    if resultado_busqueda: #verifica se tem ou nao um registro se nao devolve 0

        if resultado_busqueda[0] == senha: #Se tem um registro verifica o valor com a senha ingresada
            print("Bem vido")

            query = "SELECT admin FROM usuario WHERE email = %s" #verifica o valor de admin
            cursor.execute(query,(email,))

            resultado_busqueda = cursor.fetchone()

            if resultado_busqueda[0] == 1: #se for admin = 1 entao devolve 2 (usuario admin)
                print("O usuario é admin")
                return 2
            else:                          #se nao entao devolve 1 (usuario normal)
                print("Usuario nao admin")
                return 1
        else:                              # se a senha nao é igaul devolve 0 e uma mensagem
            print("senha incorrecta")
            return 0
    else:
        print("O usuario nao existe")
        return 0
        
            
    
#---------------------------!!!! FUNCOES PARA VER A BASE DE DADOS !!!!---------------------------#

#verificar se pode-se criar a base de dados se no proba ver que bases de datos tem no sistema.
def verificar_bd(cursor):
    try:
        cursor.execute("CREATE DATABASE IF NOT EXISTS prueba1;")
    except:
        print("No se pudo crear la base de datos")

        print("Deseas ver las basse de datos?")

        if input_validation(2) == 1: 
            print("Base de datos") 
        else: 
            return 2
     

# ver todas as bases de dados criadas
def ver_db(cursor):
    cursor.execute("SHOW DATABASES")
    print("Bases de dados actuales:")
    
    for i in cursor:
        print("\n",i)


#---------------- MAIN PROGRAM :) ----------------#
verificar_bd(cursor)

while True:
    print("\nBem vido a ! Cine review ! seu programa de avaliaçoes de confiança")
    print("\nSeleciona uma das siguientes opçoes")

    #----------- MENU PRINCIPAL -----------#

    
    opcion = input_validation(3,"ingresa uma das siguientes opçoens"
                             "\nVer filme       - 1"
                             "\nfazer login     - 2" 
                             "\ncriar uma conta - 3")
    
    if opcion   == 1:
        print("---------------------- VER FILMES ----------------------")
        print("opcaon em desenvolvimento")
        break

    elif opcion == 2: 
        print("---------------------- LOGIN ----------------------")
        email = input("EMAIL: ").lower
        senha = input("SENHA: ").lower

        '''
        Se o usario for admin entao tem essas opçoes

        1- criar filme
        2- modificar filme
        3- criar categoria
        3- modificar login??

        se o usuario nao for admin entao tem essas opçoes

        1- ver filmes
        2- avaliar filme (seleciona um e da uma nota e um comentario)
        3- modificar login??
        '''

        break
    elif opcion == 3:
        print("-------------------- CRIAR CONTA ----------------------")
        print("Escolha uma das siguientes opcoes:\n")
        print("Administrador  - 1")
        print("Usuario normal - 2")

        x = int(input("opçao: "))

        if x == 1:
            print("Para criar uma conta de administrador ingresas as siguientes informacoes:")
            acceso = input("Acceso admins: ").lower
            senha  = input("Senhas admins: ").lower

            if acceso == "root" and senha == "123":
                criar_usuario(cursor,1)
                
        else:
            print("ingresa as siguientes informacoes")
            criar_usuario(cursor,0)
            


    break

