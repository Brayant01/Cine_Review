import mysql.connector

conexion_a_base_de_dados = mysql.connector.connect(
    host = "localhost",
    user = "root",
    password = "1234",
    database = ""
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
            input("presiona cualquier tecla para continuar\n")
        else:
            return valor

#cria um usuario e agrega el na base de datos si nao existe a tabla crea uma de uma vez e agrega o usuario
def criar_usuario(cursor, admin = 0):
    nome  = str(input("\nIngresa teu Nome: "))
    senha = str(input("\nIngresa tua Senha: "))
    email = str(input("\nIngresa teu Email: "))

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
def normal_user_login(senha,email):

    query = "SELCT senha FROM usuario WHERE email = %s"
    cursor.execute(query,(email))

    resultado_busqueda = cursor.fetchone()

    if resultado_busqueda: #volta 1 de perfeito cara foi validado
        if resultado_busqueda[0] == senha:
            return 1
        else: #volta 2 de senha invalida
            print("contraseña incorrecta")
            return 2
    else: #Volta 3 do usuario nao existe :C
        print("El usuario no existe")
        return 3
            
    
#---------------------------!!!!so pode o administrador!!!!---------------------------#

#verificar se pode se crear a base de dados se no proba ver que bases de datos tem no sistema.
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

#valida el login do administrador pasando um de 3 valores
def login_admin(senha, email):
    query = "SELECT admin FROM usuario WHERE email = %s"
    cursor.execute(query,(email))

    resultado_busqueda = cursor.fetchone()

    if resultado_busqueda == 1:
        query = "SELECT senha FROM usuario WHERE email = %s"
        cursor.execute(query,(email))

        resultado_busqueda = cursor.fetchone()

        if resultado_busqueda:
            if resultado_busqueda[0] == senha:
                return 1
            else:
                print("contraseña incorrecta")
                return 2
        else:
            print("El usuario nao existe")
            return 3
    else:
        print("nao tem permisos como administrador")
        input()
        return 3       

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
    
    while True:
        opcion = input_validation(3,"ingresa uma das siguientes opçoens"
                                 "\nVer filme    - 1"
                                 "\nfazer login      - 2" 
                                 "\ncriar uma conta - 3")

        if opcion   == 1: 
            print("opcaon em desenvolvimento")
            break
        elif opcion == 2: 
            print("opcaon em desenvolvimento")
            break
        elif opcion == 3:
            print("Escolha uma das siguientes opcoes:\n")
            print("Administrador  - 1")
            print("Usuario normal - 2")

            x = int(input("opçao: "))

            if x == 1:
                print("Para criar uma conta de administrador ingresas as siguientes informacoes:")
                acceso = input("Acceso admins: ")
                senha  = input("Senhas admins: ")

                if acceso == "root" and senha == "123":
                    criar_usuario(cursor,1)
                
            else:
                print("ingresa as siguientes informacoes")
                criar_usuario(cursor,0)
            


            break

    print("Voltando ao inicio")
