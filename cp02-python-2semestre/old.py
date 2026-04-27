class Produto:
    contador_produtos = 0

    def __init__(self, nome: str, codigo: int, categoria: str, preco: float, descricao: str, fornecedor: str):
        try:
            if not isinstance(nome, str) or nome == "":
                raise ValueError("Nome inválido")

            if not isinstance(codigo, int):
                raise ValueError("Código deve ser inteiro")

            if not isinstance(categoria, str) or categoria == "":
                raise ValueError("Categoria inválida")

            if preco < 0:
                raise ValueError("Preço não pode ser negativo")

            if not isinstance(fornecedor, str) or fornecedor == "":
                raise ValueError("Fornecedor inválido")

            self.nome = nome
            self.codigo = codigo
            self.categoria = categoria
            self.preco = preco
            self.descricao = descricao
            self.fornecedor = fornecedor

            Produto.contador_produtos += 1

        except ValueError as e:
            print(f"Erro ao criar produto: {e}")
            raise


    def info(self):
        print(
            f"nome:{self.nome}\n"
            f"codigo: {self.codigo}\n"
            f"categoria: {self.categoria}\n"
            f"preço: {self.preco}\n"
            f"descricao: {self.descricao}\n"
            f"fornecedor: {self.fornecedor}"
        )


    @classmethod
    def contar_produtos(cls):
        return cls.contador_produtos


class Estoque:
    contador_estoques = 0

    def __init__(self):
        self.produtos = {}
        Estoque.contador_estoques += 1

    @classmethod
    def contar_estoque(cls):
        return cls.contador_estoques

    def exibir_estoque(self):
        try:

            if not self.produtos:
                print("O estoque está vazio.")
                return

            print("\n===== ESTOQUE =====")

            for item in self.produtos.values():

                produto = item["produto"]
                quantidade = item["quantidade"]

                print(f"Nome: {produto.nome}")
                print(f"Código: {produto.codigo}")
                print(f"Categoria: {produto.categoria}")
                print(f"Quantidade: {quantidade}")
                print(f"Preço: R$ {produto.preco}")
                print(f"Fornecedor: {produto.fornecedor}")
                print("---------------------------")

        except Exception as e:
            print(f"Erro ao exibir estoque: {e}")


    def cadastrar_produto(self, produto, quantidade_inicial=0):
        try:

            if produto.codigo in self.produtos:
                raise ValueError("Já existe um produto com esse código")

            if quantidade_inicial < 0:
                raise ValueError("Quantidade inicial inválida")

            self.produtos[produto.codigo] = {
                "produto": produto,
                "quantidade": quantidade_inicial
            }

            print("Produto cadastrado com sucesso")

        except (ValueError, KeyError) as e:
            print(f"Erro ao cadastrar produto: {e}")


    def adicionar_estoque(self, codigo, quantidade):
        try:

            if quantidade <= 0:
                raise ValueError("Quantidade deve ser positiva")

            if codigo not in self.produtos:
                raise KeyError("Produto não encontrado")

            self.produtos[codigo]["quantidade"] += quantidade

            print("Estoque atualizado")

        except (ValueError, KeyError) as e:
            print(f"Erro ao adicionar estoque: {e}")


    def remover_estoque(self, codigo, quantidade):
        try:

            if quantidade <= 0:
                raise ValueError("Quantidade deve ser positiva")

            if codigo not in self.produtos:
                raise KeyError("Produto não encontrado")

            item = self.produtos[codigo]

            if item["quantidade"] < quantidade:
                raise ValueError("Estoque insuficiente")

            item["quantidade"] -= quantidade

            print("Produto removido do estoque.")

        except (ValueError, KeyError) as e:
            print(f"Erro ao remover estoque: {e}")


    def atualizar_estoque(self, codigo, nova_quantidade):
        try:

            if nova_quantidade < 0:
                raise ValueError("Quantidade não pode ser negativa")

            if codigo not in self.produtos:
                raise KeyError("Produto não encontrado")

            self.produtos[codigo]["quantidade"] = nova_quantidade

            print("Quantidade atualizada")

        except (ValueError, KeyError) as e:
            print(f"Erro ao atualizar estoque: {e}")


    def alerta_estoque_baixo(self, limite):
        try:
            produtos_baixos = [item for item in self.produtos.values() if item["quantidade"] <= limite]

            if not produtos_baixos:
                print("Nenhum produto com estoque baixo.")
                return

            print("Produtos com estoque baixo:")

            for item in produtos_baixos:
                produto = item["produto"]
                quantidade = item["quantidade"]
                print(f"{produto.nome} - Quantidade: {quantidade}")

        except (ValueError, KeyError) as e:
            print(f"Erro no alerta de estoque: {e}")