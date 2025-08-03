import requests

BASE_URL = "http://localhost:8000/produtos"

def ler_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Valor inválido, digite um número válido.")

def ler_int(prompt):
    while True:
        try:
            return int(input(prompt))
        except ValueError:
            print("Valor inválido, digite um número inteiro válido.")

def listar_produtos():
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        produtos = response.json()
        if produtos:
            for p in produtos:
                print(f"ID: {p.get('pro_id', 'N/A')}, Nome: {p.get('pro_nome', 'N/A')}, Preço: {p.get('pro_preco', 'N/A')}, Estoque: {p.get('pro_quantidade', 'N/A')}")
        else:
            print("Nenhum produto encontrado.")
    except requests.RequestException as e:
        print(f"Erro ao listar produtos: {e}")

def buscar_por_nome():
    nome = input("Digite o nome do produto para buscar: ").strip().lower()
    try:
        response = requests.get(BASE_URL)
        response.raise_for_status()
        encontrados = [p for p in response.json() if nome in p.get('pro_nome', '').lower()]
        if encontrados:
            for p in encontrados:
                print(f"ID: {p.get('pro_id', 'N/A')}, Nome: {p.get('pro_nome', 'N/A')}, Preço: {p.get('pro_preco', 'N/A')}, Estoque: {p.get('pro_quantidade', 'N/A')}")
        else:
            print("Produto não encontrado.")
    except requests.RequestException as e:
        print(f"Erro ao buscar produto: {e}")

def cadastrar_produto():
    nome = input("Nome: ").strip()
    custo = ler_float("Custo: ")
    preco = ler_float("Preço: ")
    estoque = ler_int("Estoque: ")
    categoria_id = ler_int("ID da Categoria: ")
    fornecedor_id = ler_int("ID do Fornecedor: ")
    dados = {
        "pro_nome": nome,
        "pro_custo": custo,
        "pro_preco": preco,
        "pro_quantidade": estoque,
        "pro_cat_id": categoria_id,
        "pro_forn_id": fornecedor_id
    }
    try:
        response = requests.post(BASE_URL, json=dados)
        if response.status_code in (200, 201):
            print("Produto cadastrado com sucesso.")
        else:
            print(f"Erro ao cadastrar produto. Status: {response.status_code}")
            print("Mensagem:", response.text)
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")

def deletar_produto():
    id_produto = input("Digite o ID do produto a ser deletado: ").strip()
    confirmar = input(f"Tem certeza que deseja deletar o produto {id_produto}? (s/n): ").strip().lower()
    if confirmar != 's':
        print("Operação cancelada.")
        return
    try:
        response = requests.delete(f"{BASE_URL}/{id_produto}")
        response.raise_for_status()
        print("Produto deletado com sucesso.")
    except requests.RequestException as e:
        print(f"Erro ao deletar produto: {e}")

def editar_produto():
    id_produto = input("Digite o ID do produto a ser editado: ").strip()
    try:
        get_resp = requests.get(f"{BASE_URL}/{id_produto}")
        get_resp.raise_for_status()
        prod = get_resp.json()
    except requests.RequestException:
        print("Produto não encontrado.")
        return

    print("Deixe em branco para manter o valor atual.")

    nome = input(f"Nome [{prod.get('pro_nome', '')}]: ").strip() or prod.get('pro_nome', '')
    
    preco_input = input(f"Preço [{prod.get('pro_preco', '')}]: ").strip()
    preco = float(preco_input) if preco_input else prod.get('pro_preco', 0.0)
    
    custo_input = input(f"Custo [{prod.get('pro_custo', '')}]: ").strip()
    custo = float(custo_input) if custo_input else prod.get('pro_custo', 0.0)
    
    estoque_input = input(f"Estoque [{prod.get('pro_quantidade', '')}]: ").strip()
    estoque = int(estoque_input) if estoque_input else prod.get('pro_quantidade', 0)
    
    categoria_input = input(f"Categoria ID [{prod.get('pro_cat_id', '')}]: ").strip()
    categoria_id = int(categoria_input) if categoria_input else prod.get('pro_cat_id', 0)
    
    fornecedor_input = input(f"Fornecedor ID [{prod.get('pro_forn_id', '')}]: ").strip()
    fornecedor_id = int(fornecedor_input) if fornecedor_input else prod.get('pro_forn_id', 0)

    dados = {
        "pro_nome": nome,
        "pro_custo": custo,
        "pro_preco": preco,
        "pro_quantidade": estoque,
        "pro_cat_id": categoria_id,
        "pro_forn_id": fornecedor_id
    }

    try:
        put_resp = requests.put(f"{BASE_URL}/{id_produto}", json=dados)
        put_resp.raise_for_status()
        print("Produto atualizado com sucesso.")
    except requests.RequestException as e:
        print(f"Erro ao atualizar produto: {e}")

def menu():
    while True:
        print("\n--- MENU PRODUTOS ---")
        print("1 - Listar todos os produtos")
        print("2 - Pesquisar produto por nome")
        print("3 - Cadastrar um produto")
        print("4 - Deletar um produto")
        print("5 - Editar um produto")
        print("6 - Sair")

        opcao = input("Escolha uma opção: ").strip()
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
