def alterarQuantidadeProdutoVendedor(quantidadeProduto, produto, conexaoMongo):
    colecaoVendedor = conexaoMongo.Vendedor

    email = produto["vendedor"]["email"]
    filtro = {
        "email": email, "lista_produto.descricao": produto["descricao"]
    }   
    atualizacaoListaProduto = {
        "$set": {
            "lista_produto.$.quantidade": quantidadeProduto
        }
    }
    colecaoVendedor.update_one(filtro, atualizacaoListaProduto)