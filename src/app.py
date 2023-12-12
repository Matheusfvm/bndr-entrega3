from pymongo.server_api import ServerApi
from pymongo import MongoClient
import redis
import servicos.usuario as usuario
import servicos.compra as compra
import servicos.favorito as favorito

global db, conexaoRedis, usuarioLogado

usuarioLogado = None

uri = "mongodb+srv://entregaBranquinho:N4UNMCRomo4fJ3@cluster0.dodulda.mongodb.net/?retryWrites=true&w=majority"        
cliente = MongoClient(uri, server_api=ServerApi('1'))
db = cliente.mercado_livre


conexaoRedis = redis.Redis(
    host='redis-19604.c308.sa-east-1-1.ec2.cloud.redislabs.com',
    port=19604,
    password='1KgyiU6XWIk0AnY2tqEHHwfxFVE6VbKw'
    )


key = 0
sub = 0
while key != 'S':
    if usuarioLogado == None:
        print("\n1 - Entrar")
        print("2 - Cadastrar usuário")
        print("3 - Menu de Compra")
        print("4 - Menu de Favorito")
        key = input("\nDigite a opção desejada?(S para sair) ").upper()

        if key == '1':
            print("\n----ENTRAR----\n")
            usuarioLogado = usuario.entrarUsuario(conexaoRedis, db)
        
        elif key == '2':
            print("\n----CADASTRAR USUÁRIO----\n")
            usuario.criarUsuario(conexaoRedis, db)
        
        elif key == '3':
            print("\n-----------------")
            print("\nMenu de Compra\n")
            print("1 - Comprar um Produto")
            print("2 - Listar Compras")
            sub = input("\nDigite a opção desejada? (V para voltar) ")

            if sub == "1":
                print("\n----COMPRAR UM PRODUTO----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    compra.criarCompra(conexaoRedis, db, usuarioLogado['email'])
                else:
                    usuarioLogado = None

            if sub == "2":
                print("\n----LISTAR COMPRAS----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    compra.listarCompras(usuarioLogado) 
                else:
                    usuarioLogado = None

        elif key == '4':
            print("\n-----------------")
            print("\nMenu de favorito\n")
            print("1 - Favoritar um Produto")
            print("2 - Desfavoritar um Produto")
            print("3 - Listar Favoritos")        
            sub = input("\nDigite a opção desejada? (V para voltar) ")

            if sub == "1":
                print("\n----FAVORITAR PRODUTO----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    favorito.criarFavorito(usuarioLogado, conexaoRedis, db)
                else:
                    usuarioLogado = None


            if sub == "2":
                print("\n----DESFAVORITAR PRODUTO----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    favorito.deletarFavorito(usuarioLogado, conexaoRedis, db)
                else:
                    usuarioLogado = None
            
            if sub == "3":
                print("\n----LISTAR FAVORITOS----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    favorito.listarFavorito(usuarioLogado, conexaoRedis)
                else:
                    usuarioLogado = None

        elif key == "S":
            break
    else:
        print("\n1 - Encerrar sessão")
        print("2 - Menu de Compra")
        print("3 - Menu de Favorito")
        key = input("\nDigite a opção desejada?(S para sair) ").upper()

        if key == '1':
            print("\n----ENCERRAR SESSÃO----\n")
            usuarioLogado = None
        
        elif key == '2':
            print("\n-----------------")
            print("\nMenu de Compra\n")
            print("1 - Comprar um Produto")
            print("2 - Listar Compras")
            sub = input("\nDigite a opção desejada? (V para voltar) ")

            if sub == "1":
                print("\n----COMPRAR UM PRODUTO----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    compra.criarCompra(conexaoRedis, db, usuarioLogado['email'])
                else:
                    usuarioLogado = None

            if sub == "2":
                print("\n----LISTAR COMPRAS----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    compra.listarCompras(usuarioLogado) 
                else:
                    usuarioLogado = None

        elif key == '3':
            print("\n-----------------")
            print("\nMenu de favorito\n")
            print("1 - Favoritar um Produto")
            print("2 - Desfavoritar um Produto")
            print("3 - Listar Favoritos")        
            sub = input("\nDigite a opção desejada? (V para voltar) ")

            if sub == "1":
                print("\n----FAVORITAR PRODUTO----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    favorito.criarFavorito(usuarioLogado, conexaoRedis, db)
                else:
                    usuarioLogado = None


            if sub == "2":
                print("\n----DESFAVORITAR PRODUTO----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    favorito.deletarFavorito(usuarioLogado, conexaoRedis, db)
                else:
                    usuarioLogado = None
            
            if sub == "3":
                print("\n----LISTAR FAVORITOS----\n")
                tempoSessao = usuario.consultarTempoUsuario(conexaoRedis, usuarioLogado['email'])
                if tempoSessao == True:
                    favorito.listarFavorito(usuarioLogado, conexaoRedis)
                else:
                    usuarioLogado = None

        elif key == "S":
            break