# classes (propriedade / exclusivade)

# Nome do Produto: Campo para armazenar o nome do produto.
# Código do Produto: Um código único para identificar o produto.
# Categoria: Categorias como "eletrônicos", "vestuário", etc.
# Quantidade em Estoque: Campo para armazenar a quantidade disponível no estoque.
# Preço: Preço de venda do produto.
# Descrição: Detalhes adicionais sobre o produto.
# Fornecedor: Informações sobre o fornecedor do produto.

class Produto:
    
    def __init__(self, nome:str, codigo:int, categoria:str, quantidade:int, preco:float, descriçao:str, fornecedor:str):
        self.nome = nome
        self.codigo = codigo
        self.categoria = categoria
        self.quantidade = quantidade
        self.preco = preco
        self.descriçao = descriçao
        self.fornecedor = fornecedor

    def info(self):
        print(f'nome:{self.nome}\ncodigo: {self.codigo}\ncategoria: {self.categoria}\nquantidade: {self.quantidade}\npreço: {self.preco}\ndescriçao: {self.descriçao}\nfornecedor: {self.fornecedor}')



class Estoque:
    
    def __init__(self):
        self.produtos = {}

    def exibir_estoque(self):
        if not self.produtos:
            print("O estoque está vazio.")
            return
        
        print("\n===== ESTOQUE =====")
        for produto in self.produtos.values():
                print(f"Nome: {produto.nome}")
                print(f"Código: {produto.codigo}")
                print(f"Categoria: {produto.categoria}")
                print(f"Quantidade: {produto.quantidade}")
                print(f"Preço: R$ {produto.preco}")
                print(f"Fornecedor: {produto.fornecedor}")
                print("---------------------------")

    def cadastrar_produto(self, produto):
        self.produtos[produto.codigo] = produto
        print("Produto Cadastrado com Sucesso")

    def adicionar_estoque(self, codigo, quantidade):
        if codigo in self.produtos:
            self.produtos[codigo].quantidade += quantidade
            print("Estoque atualizado")
        else:
            print("produto não encontrado")

    def remover_estoque(self , codigo, quantidade):
        if codigo in self.produtos:
            produto = self.produtos[codigo]

            if produto.quantidade >= quantidade:
                produto.quantidade -= quantidade
                print("Produto removido do estoque.")

            else:
                print("Estoque insuficiente")

        else:
            print("Produto não encontrado")


    def atualizar_estoque(self , codigo, nova_quantidade):
        if codigo in self.produtos:
            self.produtos[codigo].quantidade = nova_quantidade
            print("Quantidade atualiazada")
        else:
            print("Produto não encontrado")

    def alerta_estoque_baixo(self, limite):
        print("Produtos com estoque baixo:")
        for produto in self.produtos.values():
            if produto.quantidade <= limite:
                print(f"{produto.nome} - Quantidade: {produto.quantidade}")

        
estoque = Estoque()

produto_1 = Produto("PS5" , 1 , "eletronico" , 2 , 3500.45, "video game playstation 5 da sony", "sony")

estoque.cadastrar_produto(produto_1)

estoque.exibir_estoque()
