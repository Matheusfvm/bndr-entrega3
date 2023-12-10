def consultaProduto(conexaoMongo):
    colecaoProduto = conexaoMongo.Produto
    while True:
        descricao = str(input("Descrição do produto: "))
        produtoEscolhido = colecaoProduto.find_one({"descricao": descricao})
        if produtoEscolhido == None:
            print("Nenhum produto encontrado")
            descricao = None            
        else:
            break
    return produtoEscolhido

def diminuirQuantidadeProduto(quantidadeCompra, produto, conexaoMongo):
    colecaoProduto = conexaoMongo.Produto
    produtoEscolhido = colecaoProduto.find_one({"descricao": produto["descricao"]})    
    quantidadeEstoque = produtoEscolhido["quantidade"]  
    resultado = quantidadeEstoque - quantidadeCompra
    while resultado < 0:
        print(f"Só existem {quantidadeEstoque} no estoque!")
        quantidadeCompra = int(input(f"Unidades de produtos compradas(max = {quantidadeEstoque}): "))
        resultado = quantidadeEstoque - quantidadeCompra
    atualizacao = {
        "$set": {
            "quantidade": resultado
        }
    }
    colecaoProduto.update_one(produto, atualizacao)
    return [quantidadeCompra, resultado]