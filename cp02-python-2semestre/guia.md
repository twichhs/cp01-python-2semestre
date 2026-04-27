# 📦 Documentação — Sistema de Gerenciamento de Estoque, Vendas e Relatórios

> **Arquivo:** `sistema_estoque.py`  
> **Linguagem:** Python 3.10+  
> **Dependências:** somente biblioteca padrão (`datetime`)

---

## Sumário

1. [Visão Geral da Arquitetura](#1-visão-geral-da-arquitetura)
2. [Diagrama de Relacionamento](#2-diagrama-de-relacionamento)
3. [Classe `Produto`](#3-classe-produto)
4. [Classe `Estoque`](#4-classe-estoque)
5. [Classe `Venda`](#5-classe-venda)
6. [Classe `Relatorio`](#6-classe-relatorio)
7. [Fluxo Completo de Uso](#7-fluxo-completo-de-uso)
8. [Tabela de Erros e Exceções](#8-tabela-de-erros-e-exceções)
9. [Guia Rápido de Referência](#9-guia-rápido-de-referência)

---

## 1. Visão Geral da Arquitetura

O sistema é composto por **4 classes** com responsabilidades bem separadas:

| Classe | Responsabilidade |
|---|---|
| `Produto` | Representa um produto do catálogo com dados e desconto |
| `Estoque` | Gerencia o inventário: cadastro, entradas, saídas e alertas |
| `Venda` | Registra uma transação de venda, aplica descontos e emite recibo |
| `Relatorio` | Consolida dados e gera relatórios de vendas, estoque e movimentações |

### Princípios de design

- **Separação de responsabilidades**: cada classe faz exatamente uma coisa.
- **Validação na entrada**: toda operação valida os dados antes de executar.
- **Rastreabilidade**: todas as movimentações de estoque são registradas com data, tipo e motivo.
- **Imutabilidade do histórico**: registros passados nunca são alterados, apenas adicionados.

---

## 2. Diagrama de Relacionamento

```
┌──────────────────┐        ┌───────────────────────────────────────┐
│     Produto      │        │               Estoque                 │
│──────────────────│        │───────────────────────────────────────│
│ nome             │        │ produtos: dict                        │
│ codigo           │◄───────│   { codigo: { produto, quantidade } } │
│ categoria        │        │ historico_movimentacoes: list[dict]   │
│ preco            │        └───────────────────────────────────────┘
│ descricao        │                         ▲
│ fornecedor       │                         │ referência
│ desconto_%       │        ┌────────────────┴──────────────────────┐
│ preco_c/desc ◄──┐│        │               Venda                   │
└──────────────────┘│        │───────────────────────────────────────│
                    └────────│ estoque: Estoque                      │
                             │ itens: list[dict]                     │
                             │ cliente: str                          │
                             │ desconto_global: float                │
                             └───────────────────────────────────────┘
                                              │ dados_venda (dict)
                                              ▼
                             ┌───────────────────────────────────────┐
                             │             Relatorio                 │
                             │───────────────────────────────────────│
                             │ estoque: Estoque                      │
                             │ vendas_registradas: list[dict]        │
                             └───────────────────────────────────────┘
```

---

## 3. Classe `Produto`

Representa um produto individual com seus atributos e lógica de desconto.

### Variáveis de Classe

| Variável | Tipo | Descrição |
|---|---|---|
| `contador_produtos` | `int` | Total de instâncias de `Produto` já criadas. Começa em `0`. |

### Atributos de Instância

| Atributo | Tipo | Obrigatório | Descrição |
|---|---|---|---|
| `nome` | `str` | ✅ | Nome de exibição do produto |
| `codigo` | `int` | ✅ | Identificador único numérico |
| `categoria` | `str` | ✅ | Categoria de agrupamento (ex: `"Papelaria"`) |
| `preco` | `float` | ✅ | Preço original em reais (deve ser `>= 0`) |
| `descricao` | `str` | ✅ | Texto livre de descrição |
| `fornecedor` | `str` | ✅ | Nome do fornecedor |
| `desconto_percentual` | `float` | — | Desconto em %. Inicia em `0.0`. Alterado via `aplicar_desconto()` |

### Propriedades Calculadas

#### `preco_com_desconto` → `float`

Retorna o preço unitário já com o desconto aplicado. Calculado dinamicamente.

```
preco_com_desconto = preco × (1 - desconto_percentual / 100)
```

**Exemplos:**

| `preco` | `desconto_percentual` | `preco_com_desconto` |
|---|---|---|
| R$ 10,00 | 0% | R$ 10,00 |
| R$ 10,00 | 10% | R$ 9,00 |
| R$ 89,90 | 25% | R$ 67,43 |

### Métodos

---

#### `__init__(nome, codigo, categoria, preco, descricao, fornecedor)`

Construtor da classe. Valida todos os campos antes de atribuir.

**Validações realizadas:**

| Campo | Regra | Erro levantado |
|---|---|---|
| `nome` | `str` não vazio | `ValueError: Nome inválido` |
| `codigo` | instância de `int` | `ValueError: Código deve ser inteiro` |
| `categoria` | `str` não vazia | `ValueError: Categoria inválida` |
| `preco` | `>= 0` | `ValueError: Preço não pode ser negativo` |
| `fornecedor` | `str` não vazio | `ValueError: Fornecedor inválido` |

**Exemplo:**
```python
caneta = Produto("Caneta Azul", 1001, "Papelaria", 2.50, "Esferográfica", "Fornecedor A")
```

---

#### `aplicar_desconto(percentual: float)`

Define o desconto percentual do produto. Atualiza `desconto_percentual`.

| Parâmetro | Tipo | Restrição |
|---|---|---|
| `percentual` | `float` | Deve estar entre `0` e `100` (inclusive) |

**Exceção:** `ValueError` se o percentual estiver fora do intervalo.

**Exemplo:**
```python
caneta.aplicar_desconto(10)     # 10% de desconto
print(caneta.preco_com_desconto) # 2.25
```

---

#### `info()`

Exibe no terminal todas as informações do produto, incluindo preço original, desconto e preço final.

**Exemplo de saída:**
```
── Produto ──────────────────
  Nome      : Caneta Azul
  Código    : 1001
  Categoria : Papelaria
  Preço     : R$ 2.50
  Desconto  : 10%
  Preço c/desc: R$ 2.25
  Descrição : Esferográfica
  Fornecedor: Fornecedor A
```

---

#### `contar_produtos()` *(classmethod)* → `int`

Retorna o valor atual de `contador_produtos`.

```python
print(Produto.contar_produtos())  # 3 (se três produtos foram criados)
```

---

## 4. Classe `Estoque`

Gerencia o inventário completo: cadastro de produtos, movimentações e alertas.

### Variáveis de Classe

| Variável | Tipo | Descrição |
|---|---|---|
| `contador_estoques` | `int` | Número de instâncias de `Estoque` criadas |

### Atributos de Instância

| Atributo | Tipo | Descrição |
|---|---|---|
| `produtos` | `dict` | Dicionário principal do inventário. Chave: `codigo (int)`. Valor: `{"produto": Produto, "quantidade": int}` |
| `historico_movimentacoes` | `list[dict]` | Lista de todas as entradas e saídas registradas automaticamente |

### Estrutura do dicionário `produtos`

```python
{
    1001: {
        "produto": <Produto: Caneta Azul>,
        "quantidade": 95
    },
    1002: {
        "produto": <Produto: Caderno 100fls>,
        "quantidade": 78
    }
}
```

### Estrutura de cada registro em `historico_movimentacoes`

```python
{
    "data_hora" : "27/04/2026 10:30:00",  # str formatado
    "tipo"      : "entrada",              # "entrada" ou "saída"
    "codigo"    : 1001,                   # int
    "nome"      : "Caneta Azul",          # str
    "quantidade": 10,                     # int
    "motivo"    : "reposição"             # str livre
}
```

### Métodos

---

#### `__init__()`

Inicializa um estoque vazio (`produtos = {}` e `historico_movimentacoes = []`).

---

#### `cadastrar_produto(produto: Produto, quantidade_inicial: int = 0)`

Registra um novo produto no estoque. Se `quantidade_inicial > 0`, também registra uma entrada no histórico com motivo `"cadastro inicial"`.

| Parâmetro | Tipo | Padrão | Descrição |
|---|---|---|---|
| `produto` | `Produto` | — | Instância de `Produto` a ser cadastrada |
| `quantidade_inicial` | `int` | `0` | Estoque de abertura |

**Erros possíveis:**

| Condição | Mensagem |
|---|---|
| Código já existe | `Já existe um produto com esse código` |
| `quantidade_inicial < 0` | `Quantidade inicial não pode ser negativa` |

---

#### `adicionar_estoque(codigo: int, quantidade: int)`

Incrementa a quantidade de um produto existente. Registra `"entrada"` com motivo `"reposição"` no histórico.

| Parâmetro | Regra |
|---|---|
| `quantidade` | Deve ser `> 0` |
| `codigo` | Deve existir em `self.produtos` |

---

#### `remover_estoque(codigo: int, quantidade: int, motivo: str = "remoção manual")`

Decrementa a quantidade de um produto. Registra `"saída"` no histórico com o `motivo` informado.

> ⚠️ **Atenção:** quando chamado internamente por `Venda.finalizar_venda()`, o motivo é preenchido automaticamente como `"venda #N"`.

| Parâmetro | Regra |
|---|---|
| `quantidade` | Deve ser `> 0` |
| `codigo` | Deve existir em `self.produtos` |
| Estoque atual | Deve ser `>= quantidade` solicitada |

---

#### `atualizar_estoque(codigo: int, nova_quantidade: int)`

Define um valor absoluto de estoque, sobrescrevendo o atual. Calcula a diferença e registra como `"entrada"` ou `"saída"` com motivo `"ajuste manual"`.

| Parâmetro | Regra |
|---|---|
| `nova_quantidade` | Deve ser `>= 0` |

---

#### `alerta_estoque_baixo(limite: int)`

Filtra e exibe todos os produtos com `quantidade <= limite`.

```python
estoque.alerta_estoque_baixo(25)
# ⚠  ALERTA — Estoque baixo (limite: 25)
# ----------------------------------------
#   Mochila Escolar → 20 unidades
```

---

#### `exibir_estoque()`

Exibe um bloco formatado com nome, código, categoria, quantidade, preço e fornecedor de cada produto.

---

#### `_registrar_movimentacao(tipo, codigo, nome, quantidade, motivo)` *(privado)*

Método interno chamado automaticamente por `adicionar_estoque`, `remover_estoque` e `atualizar_estoque`. **Não deve ser chamado diretamente.**

Salva um dicionário com os campos `data_hora`, `tipo`, `codigo`, `nome`, `quantidade` e `motivo` em `historico_movimentacoes`.

---

#### `contar_estoque()` *(classmethod)* → `int`

Retorna o total de instâncias de `Estoque` criadas.

---

## 5. Classe `Venda`

Representa uma transação de venda. Gerencia o carrinho de itens, aplica descontos, debita o estoque automaticamente ao finalizar e emite recibo.

### Variáveis de Classe

| Variável | Tipo | Descrição |
|---|---|---|
| `contador_vendas` | `int` | Total de vendas realizadas. Usado para numerar cada venda sequencialmente. |

### Atributos de Instância

| Atributo | Tipo | Descrição |
|---|---|---|
| `estoque` | `Estoque` | Referência ao estoque que será debitado na finalização |
| `cliente` | `str` | Nome do comprador (padrão: `"Cliente"`) |
| `itens` | `list[dict]` | Lista dos produtos adicionados ao carrinho |
| `data_hora` | `str` | Data/hora capturada no momento da criação da venda |
| `numero_venda` | `int` | Número sequencial único (incrementado via `contador_vendas`) |
| `desconto_global` | `float` | Desconto percentual sobre o valor total. Padrão: `0.0` |

### Estrutura de cada item em `itens`

```python
{
    "produto"       : <Produto: Caneta Azul>,
    "quantidade"    : 5,
    "preco_unitario": 2.25   # preço_com_desconto no momento da venda
}
```

> 🔒 **Importante:** o `preco_unitario` é capturado no momento em que o item é adicionado à venda. Alterações posteriores no desconto do produto **não afetam** vendas já abertas.

### Métodos

---

#### `__init__(estoque: Estoque, cliente: str = "Cliente")`

Inicializa a venda, vinculando-a ao estoque e registrando a data/hora atual.

```python
venda = Venda(estoque, cliente="Maria Silva")
```

---

#### `adicionar_item(codigo: int, quantidade: int)`

Adiciona um produto ao carrinho da venda após validar disponibilidade.

**Checklist de validação:**

1. `quantidade > 0`
2. Produto com `codigo` existe no estoque
3. Estoque disponível `>= quantidade` solicitada

**O que é registrado no item:**
- Objeto `Produto`
- Quantidade solicitada
- `preco_com_desconto` atual do produto (congelado no momento da adição)

---

#### `aplicar_desconto_global(percentual: float)`

Aplica um desconto percentual sobre o **valor total** da venda. Útil para:

- Cupons de desconto
- Promoções por volume de compra
- Clientes com benefícios especiais

| Parâmetro | Regra |
|---|---|
| `percentual` | Entre `0` e `100` |

**Diferença entre desconto de produto e desconto global:**

| Tipo | Onde é aplicado | Quem configura |
|---|---|---|
| `Produto.aplicar_desconto()` | No preço unitário de um produto | No cadastro do produto |
| `Venda.aplicar_desconto_global()` | No valor total da venda inteira | No momento da venda |

**Ambos podem coexistir.** O desconto do produto reduz o `preco_unitario` de cada item; o desconto global reduz o total final.

---

#### `finalizar_venda()` → `dict | None`

Fecha a venda, debita o estoque e retorna os dados estruturados da transação.

**Sequência de execução:**

```
1. Valida que self.itens não está vazio
2. Para cada item:
   └─ chama estoque.remover_estoque(codigo, quantidade, motivo="venda #N")
3. Monta e retorna o dicionário dados_venda
```

**Estrutura do dicionário retornado:**

```python
{
    "numero_venda"   : 1,
    "data_hora"      : "27/04/2026 10:30:00",
    "cliente"        : "Maria Silva",
    "itens"          : [ { "produto": ..., "quantidade": 5, "preco_unitario": 2.25 } ],
    "subtotal"       : 43.05,
    "desconto_global": 5.0,
    "total"          : 40.90
}
```

> ⚠️ **Retorna `None`** se houver erro na finalização (ex: estoque ficou insuficiente entre `adicionar_item` e `finalizar_venda`).

---

#### `emitir_recibo()`

Imprime um recibo formatado no terminal com todos os itens, subtotal, desconto (se houver) e total final.

**Exemplo de saída:**
```
=============================================
           RECIBO DE VENDA
=============================================
  Venda Nº  : 1
  Data/Hora : 27/04/2026 10:30:00
  Cliente   : Maria Silva
---------------------------------------------
  PRODUTO              QTD     UNIT     TOTAL
---------------------------------------------
  Caneta Azul            5     2.25     11.25
  Caderno 100fls         2    15.90     31.80
---------------------------------------------
  Subtotal                          R$   43.05
  Desconto (5%)                     R$    2.15
  TOTAL A PAGAR                     R$   40.90
=============================================
     Obrigado pela preferência! 🛒
=============================================
```

---

#### Métodos de cálculo internos

| Método | Retorno | Descrição |
|---|---|---|
| `_calcular_subtotal()` | `float` | Soma de `preco_unitario × quantidade` de cada item, antes do desconto global |
| `_calcular_total()` | `float` | `subtotal × (1 - desconto_global / 100)` |

---

#### `contar_vendas()` *(classmethod)* → `int`

Retorna o total de vendas finalizadas.

---

## 6. Classe `Relatorio`

Consolida os dados de vendas e do estoque para gerar relatórios gerenciais.

### Atributos de Instância

| Atributo | Tipo | Descrição |
|---|---|---|
| `estoque` | `Estoque` | Referência ao estoque monitorado |
| `vendas_registradas` | `list[dict]` | Lista com todos os dicionários retornados por `Venda.finalizar_venda()` |

### Métodos

---

#### `__init__(estoque: Estoque)`

Inicializa o sistema de relatórios vinculado ao estoque.

```python
relatorio = Relatorio(estoque)
```

---

#### `registrar_venda(dados_venda: dict)`

Salva os dados de uma venda finalizada no histórico interno `vendas_registradas`.

> **Deve ser chamado imediatamente após `Venda.finalizar_venda()`.**

```python
dados = venda.finalizar_venda()
relatorio.registrar_venda(dados)  # ← registra no relatório
```

Se `dados_venda` for `None` (venda com erro), o método exibe aviso e não registra nada.

---

#### `relatorio_vendas()`

Exibe relatório detalhado de todas as vendas registradas.

**Informações exibidas por venda:**
- Número e data/hora
- Nome do cliente
- Tabela com produto, quantidade, preço unitário e subtotal por linha
- Subtotal, desconto global (se houver) e total

**Ao final do relatório:**
- Total geral acumulado de todas as vendas
- Quantidade de vendas realizadas

---

#### `relatorio_estoque()`

Exibe tabela com a situação atual do inventário.

**Colunas exibidas:**

| Coluna | Descrição |
|---|---|
| CÓD | Código do produto |
| NOME | Nome (truncado a 22 caracteres) |
| CAT | Categoria (truncada a 14 caracteres) |
| QTD | Quantidade atual em estoque |
| UNIT | Preço unitário original |
| TOTAL | `preco × quantidade` (valor total em estoque daquele produto) |

**Ao final:** valor total consolidado de todo o estoque e contagem de produtos.

---

#### `historico_movimentacoes()`

Exibe o log completo de todas as entradas e saídas do estoque, lendo diretamente de `estoque.historico_movimentacoes`.

**Colunas exibidas:**

| Coluna | Descrição |
|---|---|
| DATA/HORA | Timestamp da operação |
| TIPO | `ENTRADA` ou `SAÍDA` |
| CÓD | Código do produto |
| PRODUTO | Nome do produto |
| QTD | Unidades movimentadas |
| MOTIVO | Origem da operação (ex: `"venda #1"`, `"reposição"`, `"ajuste manual"`) |

---

## 7. Fluxo Completo de Uso

```
┌─────────────────────────────────────────────────────────┐
│  1. Criar produtos                                      │
│     p = Produto("Nome", codigo, "Cat", preco, ...)      │
│     p.aplicar_desconto(10)   ← opcional                 │
├─────────────────────────────────────────────────────────┤
│  2. Criar estoque e cadastrar produtos                  │
│     e = Estoque()                                       │
│     e.cadastrar_produto(p, quantidade_inicial)          │
├─────────────────────────────────────────────────────────┤
│  3. (Opcional) Repor ou ajustar estoque                 │
│     e.adicionar_estoque(codigo, qtd)                    │
│     e.atualizar_estoque(codigo, nova_qtd)               │
├─────────────────────────────────────────────────────────┤
│  4. Criar relatório vinculado ao estoque                │
│     r = Relatorio(e)                                    │
├─────────────────────────────────────────────────────────┤
│  5. Registrar uma venda                                 │
│     v = Venda(e, cliente="Nome do Cliente")             │
│     v.adicionar_item(codigo, quantidade)                │
│     v.aplicar_desconto_global(5)  ← opcional           │
│     dados = v.finalizar_venda()   ← debita o estoque   │
│     v.emitir_recibo()                                   │
│     r.registrar_venda(dados)      ← salva no relatório │
├─────────────────────────────────────────────────────────┤
│  6. Gerar relatórios                                    │
│     r.relatorio_vendas()                                │
│     r.relatorio_estoque()                               │
│     r.historico_movimentacoes()                         │
└─────────────────────────────────────────────────────────┘
```

---

## 8. Tabela de Erros e Exceções

Todas as exceções são capturadas internamente e exibidas como mensagem amigável. A exceção original **não é propagada** para o chamador (exceto no `__init__` de `Produto`, onde é re-levantada após o print).

| Classe | Método | Condição | Tipo | Mensagem |
|---|---|---|---|---|
| `Produto` | `__init__` | Nome vazio ou não string | `ValueError` | `Erro ao criar produto: Nome inválido` |
| `Produto` | `__init__` | Código não inteiro | `ValueError` | `Erro ao criar produto: Código deve ser inteiro` |
| `Produto` | `__init__` | Preço negativo | `ValueError` | `Erro ao criar produto: Preço não pode ser negativo` |
| `Produto` | `aplicar_desconto` | Percentual fora de 0–100 | `ValueError` | — (propagada) |
| `Estoque` | `cadastrar_produto` | Código duplicado | `ValueError` | `Erro ao cadastrar produto: ...` |
| `Estoque` | `adicionar_estoque` | Quantidade `<= 0` | `ValueError` | `Erro ao adicionar estoque: ...` |
| `Estoque` | `adicionar_estoque` | Produto não encontrado | `KeyError` | `Erro ao adicionar estoque: ...` |
| `Estoque` | `remover_estoque` | Estoque insuficiente | `ValueError` | `Erro ao remover estoque: Estoque insuficiente. Disponível: X, Solicitado: Y` |
| `Venda` | `adicionar_item` | Produto não encontrado | `KeyError` | `Erro ao adicionar item: ...` |
| `Venda` | `adicionar_item` | Estoque insuficiente | `ValueError` | `Erro ao adicionar item: Estoque insuficiente...` |
| `Venda` | `finalizar_venda` | Carrinho vazio | `ValueError` | `Erro ao finalizar venda: ...` |
| `Venda` | `aplicar_desconto_global` | Fora de 0–100 | `ValueError` | — (propagada) |

---

## 9. Guia Rápido de Referência

### Produto

```python
# Criar
p = Produto(nome, codigo, categoria, preco, descricao, fornecedor)

# Desconto
p.aplicar_desconto(percentual)     # define desconto em %
p.preco_com_desconto               # lê o preço com desconto (property)

# Exibir
p.info()
Produto.contar_produtos()
```

### Estoque

```python
e = Estoque()
e.cadastrar_produto(produto, quantidade_inicial=0)
e.adicionar_estoque(codigo, quantidade)
e.remover_estoque(codigo, quantidade, motivo="texto")
e.atualizar_estoque(codigo, nova_quantidade)
e.alerta_estoque_baixo(limite)
e.exibir_estoque()
Estoque.contar_estoque()
```

### Venda

```python
v = Venda(estoque, cliente="Nome")
v.adicionar_item(codigo, quantidade)
v.aplicar_desconto_global(percentual)    # opcional
dados = v.finalizar_venda()              # debita estoque; retorna dict
v.emitir_recibo()
Venda.contar_vendas()
```

### Relatorio

```python
r = Relatorio(estoque)
r.registrar_venda(dados)         # dados = retorno de finalizar_venda()
r.relatorio_vendas()
r.relatorio_estoque()
r.historico_movimentacoes()
```

---

*Documentação gerada para `sistema_estoque.py` — Sistema de Gerenciamento de Estoque, Vendas e Relatórios.*