from datetime import datetime
import json
import servicos.produto as produto
import servicos.vendedor as vendedor
import servicos.usuario as usuario


def criarCompra(conexaoRedis, conexaoMongo, email):
    colecaoCompra = conexaoMongo.Compra

    usuarioEscolhidoRedis = conexaoRedis.get(f"usuario-{email}")
    if usuarioEscolhidoRedis != None:
        dataCompra = datetime.now()
        dataCompraFormatada = dataCompra.strftime("%d/%m/%Y %H:%M")
        listaProduto = []
        valorTotalCompra = 0
        key = "S"
        while key == "S":        
            produtoEscolhido = produto.consultaProduto(conexaoMongo)
            if produtoEscolhido["quantidade"] != 0:
                quantidadeProdutoCompra = int(input(f"Unidades de produtos compradas(max = {produtoEscolhido['quantidade']}): "))        
                quantidadeProdutoCompraFinal = produto.diminuirQuantidadeProduto(quantidadeProdutoCompra, produtoEscolhido, conexaoMongo)
                vendedor.alterarQuantidadeProdutoVendedor(quantidadeProdutoCompraFinal[1], produtoEscolhido, conexaoMongo)
                produtoObjeto = {
                    "descricao": produtoEscolhido["descricao"],
                    "preco": produtoEscolhido["preco"],
                    "quantidade_produto_compra": quantidadeProdutoCompraFinal[0],
                    "vendedor": produtoEscolhido["vendedor"] 
                }
                listaProduto.append(produtoObjeto)    
                valorTotalCompra += produtoEscolhido["preco"] * quantidadeProdutoCompraFinal[0]    
            else:
                print(f"Produto {produtoEscolhido['descricao']} está em falta!")
            key = str(input("Deseja comprar um outro produto(S/N)? "))
        dataCompraEntrega = str(input("Data da entrega(dd/mm/AAAA): "))
        listaNomeEmailUsuario = usuario.vinculaCompraUsuarioMongo(listaProduto, dataCompraEntrega, valorTotalCompra, email, conexaoMongo) 
        usuario.vinculaCompraUsuarioRedis(listaProduto, dataCompraEntrega, valorTotalCompra, email, conexaoRedis)
        usuarioObjeto = {
            "nome": listaNomeEmailUsuario[0],
            "email": listaNomeEmailUsuario[1]
        }
        compra = {
            "usuario": usuarioObjeto,
            "lista_produto": listaProduto,
            "data_compra": dataCompraFormatada,
            "data_entrega_compra": dataCompraEntrega,
            "valor_total_compra": valorTotalCompra
        }
        colecaoCompra.insert_one(compra)
        print(f'\nCompra realizada com sucesso!\n')

def listarCompras(usuario):
    listaCompra = []
    for compra in usuario['lista_compra']:
      listaCompra.append(compra)
    indiceCompra = 1
    for compra in listaCompra:
        print(f"\n{indiceCompra}º Compra\n")
        print(f"Data entrega: {compra['data_entrega']}\n")
        print(f"Valor total da compra: R${compra['valor_total_compra']:.2f}")
        print("\nProdutos\n")
        for produto in compra['lista_produto']:
            print(f"Descrição: {produto['descricao']}")
            print(f"Preço: {produto['preco']:.2f}")
            print(f"Quantidade: {produto['quantidade_produto_compra']}")
            print("\n---------------------------------------\n")
    indiceCompra += 1