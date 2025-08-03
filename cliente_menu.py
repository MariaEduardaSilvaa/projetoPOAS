import requests

BASE_URL = "http://localhost:8000/produtos"

def listar_produtos():
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        produtos = response.json()
        for p in produtos:
            print(f"ID: {p['id']}, Nome: {p['nome']}, Preço: {p['preco']}, Estoque: {p['estoque']}")
    else:
        print("Erro ao listar produtos.")

def buscar_por_nome():
    nome = input("Digite o nome do produto para buscar: ").lower()
    response = requests.get(BASE_URL)
    if response.status_code == 200:
        encontrados = [p for p in response.json() if nome in p['nome'].lower()]
        if encontrados:
            for p in encontrados:
                print(f"ID: {p['id']}, Nome: {p['nome']}, Preço: {p['preco']}, Estoque: {p['estoque']}")
        else:
            print("Produto não encontrado.")
    else:
        print("Erro ao buscar produto.")

def cadastrar_produto():
    nome = input("Nome: ")
    preco = float(input("Preço: "))
    estoque = int(input("Estoque: "))
    categoria_id = int(input("ID da Categoria: "))
    fornecedor_id = int(input("ID do Fornecedor: "))
    dados = {
        "nome": nome,
        "preco": preco,
        "estoque": estoque,
        "categoria_id": categoria_id,
        "fornecedor_id": fornecedor_id
    }
    response = requests.post(BASE_URL, json=dados)
    if response.status_code == 200:
        print("Produto cadastrado com sucesso.")
    else:
        print("Erro ao cadastrar produto.")

def deletar_produto():
    id_produto = input("Digite o ID do produto a ser deletado: ")
    response = requests.delete(f"{BASE_URL}/{id_produto}")
    if response.status_code == 200:
        print("Produto deletado com sucesso.")
    else:
        print("Erro ao deletar produto.")

def editar_produto():
    id_produto = input("Digite o ID do produto a ser editado: ")
    get_resp = requests.get(f"{BASE_URL}/{id_produto}")
    if get_resp.status_code != 200:
        print("Produto não encontrado.")
        return
    prod = get_resp.json()
    print("Deixe em branco para manter o valor atual.")

    nome = input(f"Nome [{prod['nome']}]: ") or prod['nome']
    preco = input(f"Preço [{prod['preco']}]: ") or prod['preco']
    estoque = input(f"Estoque [{prod['estoque']}]: ") or prod['estoque']
    categoria_id = input(f"Categoria ID [{prod['categoria_id']}]: ") or prod['categoria_id']
    fornecedor_id = input(f"Fornecedor ID [{prod['fornecedor_id']}]: ") or prod['fornecedor_id']

    dados = {
        "nome": nome,
        "preco": float(preco),
        "estoque": int(estoque),
        "categoria_id": int(categoria_id),
        "fornecedor_id": int(fornecedor_id)
    }
    put_resp = requests.put(f"{BASE_URL}/{id_produto}", json=dados)
    if put_resp.status_code == 200:
        print("Produto atualizado com sucesso.")
    else:
        print("Erro ao atualizar produto.")

def menu():
    while True:
        print("\n--- MENU PRODUTOS ---")
        print("1 - Listar todos os produtos")
        print("2 - Pesquisar produto por nome")
        print("3 - Cadastrar um produto")
        print("4 - Deletar um produto")
        print("5 - Editar um produto")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ")
        if opcao == "1":
            listar_produtos()
        elif opcao == "2":
            buscar_por_nome()
        elif opcao == "3":
            cadastrar_produto()
        elif opcao == "4":
            deletar_produto()
        elif opcao == "5":
            editar_produto()
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida.")

if __name__ == "__main__":
    menu()
