import json
import servicos.produto as produto


def criarFavorito(usuarioEscolhidoMongo, conexaoRedis, conexaoMongo):
    colecaoUsuario = conexaoMongo.Usuario

    usuarioEscolhidoRedis = conexaoRedis.get(f"usuario-{usuarioEscolhidoMongo['email']}")
    if usuarioEscolhidoRedis != None:
        objetoUsuarioRedis = json.loads(usuarioEscolhidoRedis)
        produtoEscolhido = produto.consultaProduto(conexaoMongo)
        produtoObjeto = {
            "descricao": produtoEscolhido["descricao"],
            "preco": produtoEscolhido["preco"],
            "vendedor": produtoEscolhido["vendedor"]        
        }
        consultaFavorito = usuarioEscolhidoMongo["lista_favorito"]
        if produtoObjeto in consultaFavorito:
            print("Produto já está entre os favoritos!")
        else:
            atualizacao = {
                "$push": {
                    "lista_favorito": produtoObjeto 
                }
            }
            objetoUsuarioRedis['listaFavorito'].append(produtoObjeto)
            jsonUsuarioRedis = json.dumps(objetoUsuarioRedis)
            colecaoUsuario.update_one(usuarioEscolhidoMongo, atualizacao)
            tempoDeVida = conexaoRedis.ttl(f"usuario-{usuarioEscolhidoMongo['email']}")
            conexaoRedis.set(f"usuario-{usuarioEscolhidoMongo['email']}", jsonUsuarioRedis)
            conexaoRedis.expire(f"usuario-{usuarioEscolhidoMongo['email']}", tempoDeVida)
            print(f'\nO produto {produtoEscolhido["descricao"]} está entre seus favoritos!\n')

def listarFavorito(usuarioEscolhidoMongo, conexaoRedis):
    usuarioEscolhidoRedis = conexaoRedis.get(f"usuario-{usuarioEscolhidoMongo['email']}")
    if usuarioEscolhidoRedis != None:
        objetoUsuarioRedis = json.loads(usuarioEscolhidoRedis)
        print("\nProdutos")
        for favorito in objetoUsuarioRedis['listaFavorito']:
            print(f"Descrição: {favorito['descricao']}")
            print(f"Preço: R${favorito['preco']}")
            print("\n---------------------------------------\n")

def deletarFavorito(usuarioEscolhidoMongo, conexaoRedis, conexaoMongo): 
    colecaoUsuario = conexaoMongo.Usuario

    usuarioEscolhidoRedis = conexaoRedis.get(f"usuario-{usuarioEscolhidoMongo['email']}")
    if usuarioEscolhidoRedis != None:
        objetoUsuarioRedis = json.loads(usuarioEscolhidoRedis)   
        produtoEscolhido = produto.consultaProduto(conexaoMongo)
        produtoObjeto = {
            "descricao": produtoEscolhido["descricao"],
            "preco": produtoEscolhido["preco"],
            "vendedor": produtoEscolhido["vendedor"]
        }
        atualizacaoListaFavorito = {
            "$pull": {
                "lista_favorito": produtoObjeto
            }
        }
        for produtoEscolhido in objetoUsuarioRedis['listaFavorito']:
            if produtoEscolhido["descricao"] == produtoObjeto['descricao']:
                objetoUsuarioRedis['listaFavorito'].remove(produtoEscolhido)            
                colecaoUsuario.update_one(usuarioEscolhidoMongo, atualizacaoListaFavorito)
                jsonUsuarioRedis = json.dumps(objetoUsuarioRedis)
                tempoDeVida = conexaoRedis.ttl(f"usuario-{usuarioEscolhidoMongo['email']}")
                conexaoRedis.set(f"usuario-{usuarioEscolhidoMongo['email']}", jsonUsuarioRedis)
                conexaoRedis.expire(f"usuario-{usuarioEscolhidoMongo['email']}", tempoDeVida)
                print(f'\nO produto {produtoObjeto["descricao"]} deixou da sua lista de favoritos!\n')
                break
            else:
                print(f"Não existe nenhum produto com essa descrição nos seus favoritos!")
