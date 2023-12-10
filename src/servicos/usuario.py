import json

def criarUsuario(conexaoMongo):
    colecaoUsuario = conexaoMongo.Usuario
    
    while True:
        email = str(input("Email: "))
        usuarioEscolhido = colecaoUsuario.find_one({"email": email})
        if usuarioEscolhido != None:
            print("\nUsuário já cadastrado!")
            print("Digite outro email!\n")
        else:
            nome = str(input("Nome: "))
            cpf = str(input("CPF: "))                       
        senha = str(input("Senha: "))
        telefone = str(input("Número telefone: "))
        listaEndereco = []
        listaCompra = []
        listaFavorito = []
        key = "S"
        while key == "S":
            cep = str(input("CEP: "))
            ruaAvenida = str(input("Nome da rua ou avenida: "))
            numeroEndereco = str(input("Número endereço: "))
            bairro = str(input("Bairro: "))
            cidade = str(input("Cidade: "))
            estado = str(input("Estado(Sigla): "))
            endereco = {
                "cep": cep,
                "rua_avenida": ruaAvenida,
                "numero": numeroEndereco,
                "bairro": bairro,
                "cidade": cidade,
                "estado": estado,            
                }
            listaEndereco.append(endereco)
            key = input("Deseja cadastrar um novo endereço(S/N)? ")        
        usuario = {
            "nome": nome,
            "cpf": cpf,
            "email": email,
            "senha": senha,
            "telefone": telefone,
            "lista_endereco": listaEndereco,
            "lista_compra": listaCompra,
            "lista_favorito": listaFavorito
        }
        colecaoUsuario.insert_one(usuario)
        print(f'\nUsuário {nome} inserido com sucesso!\n')
    
def entrarUsuario(conexaoRedis, conexaoMongo):
    usuarioEscolhido = consultaUsuarioMongo(conexaoMongo)

    listaCompra = []
    listaFavorito = []
    if usuarioEscolhido != None:
        email = usuarioEscolhido['email']
        senha = usuarioEscolhido['senha']
        comparaSenha = str(input("Senha: "))
        if senha == comparaSenha:
            print("Usuário logado com sucesso!")
            for compra in usuarioEscolhido['lista_compra']:
                listaCompra.append(compra)
            for favorito in usuarioEscolhido['lista_favorito']:
                listaFavorito.append(favorito)
            objetoValorUsuarioRedis = {
                "listaCompra": listaCompra,
                "listaFavorito": listaFavorito
            }
            jsonObjetoValorUsuarioRedis = json.dumps(objetoValorUsuarioRedis)
            conexaoRedis.setex(f"usuario-{email}", 300, jsonObjetoValorUsuarioRedis)
            return usuarioEscolhido
    else:
        print("Nenhum usuário encontrado!") 

def consultaUsuarioMongo(conexaoMongo):
    colecaoUsuario = conexaoMongo.Usuario
    while True:
        email = str(input("Email do usuário: "))
        usuarioEscolhido = colecaoUsuario.find_one({"email": email})
        if usuarioEscolhido == None:
            print("Nenhum usuário encontrado")
            email = None
        else:
            break
    return usuarioEscolhido

def consultaUsuarioRedis(colecaoRedis):
    while True:
        email = str(input("Email do usuário: "))
        usuarioEscolhido = colecaoRedis.get(f"usuario-{email}")
        if usuarioEscolhido == None:
            print("Nenhum usuário encontrado")
            email = None
        else:
            break
    return usuarioEscolhido

def consultarTempoUsuario(conexaoRedis, email):
    tempoVidaUsuario = conexaoRedis.ttl(f"usuario-{email}")
    if tempoVidaUsuario == -2:
        print("Sessão expirada!")
        return False
    elif tempoVidaUsuario == -1:
        print("Sessão expirada!")
        conexaoRedis.delete(f"usuario-{email}")
        return False
    else:
        return True

def vinculaCompraUsuarioMongo(listaProduto, data_entrega, valorCompra, email, conexaoMongo):
    colecaoUsuario = conexaoMongo.Usuario

    usuarioEscolhido = colecaoUsuario.find_one({"email": email})
    compra = {
        "lista_produto": listaProduto,
        "data_entrega": data_entrega,
        "valor_total_compra": valorCompra
    }
    atualizacao = {
        "$push": {
            "lista_compra": compra
        }
    }   
    colecaoUsuario.update_one(usuarioEscolhido, atualizacao)
    return [usuarioEscolhido["nome"], usuarioEscolhido["email"]]

def vinculaCompraUsuarioRedis(listaProduto, data_entrega, valorCompra, email, conexaoRedis):    
    usuarioEscolhidoRedis = conexaoRedis.get(f"usuario-{email}")
    if usuarioEscolhidoRedis != None:
        objetoUsuarioRedis = json.loads(usuarioEscolhidoRedis)
        novaCompra = {
            "lista_produto": listaProduto,
            "data_entrega": data_entrega,
            "valor_total_compra": valorCompra
        }
        objetoUsuarioRedis['listaCompra'].append(novaCompra)
        jsonUsuarioRedis = json.dumps(objetoUsuarioRedis)
        tempoDeVida = conexaoRedis.ttl(f"usuario-{email}")
        conexaoRedis.set(f"usuario-{email}", jsonUsuarioRedis)
        conexaoRedis.expire(f"usuario-{email}", tempoDeVida)