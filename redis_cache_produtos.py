import psycopg2
import redis

# Conectar ao Redis
r = redis.Redis(host='localhost', port=6379, decode_responses=True)

# Conectar ao PostgreSQL
conn = psycopg2.connect(
    host="localhost",
    database="redisCache",
    user="postgres",
    password="senha123"
)
cursor = conn.cursor()





CACHE_TTL = 60

def buscar_produto(id_produto):
    chave = f"produto:{id_produto}"

    if r.exists(chave):
        print("Produto carregado do cache (Redis - HASH).")
        produto = r.hgetall(chave)
    else:
        print("Produto não está no cache. Buscando no banco de dados...")
        cursor.execute("SELECT nome, preco FROM produtos WHERE id = %s", (id_produto,))
        resultado = cursor.fetchone()

        if not resultado:
            print("Produto não encontrado no banco.")
            return

        nome, preco = resultado

        r.hset(chave, mapping={
            "nome": nome,
            "preco": str(preco)
        })

        r.expire(chave, CACHE_TTL)

        print(f"Produto salvo no cache com TTL de {CACHE_TTL} segundos.")
        produto = {"nome": nome, "preco": str(preco)}  # para manter estrutura uniforme

    # Exibe resultado
    print(f"Produto: {produto['nome']} - R$ {float(produto['preco']):.2f}")

def listar_chaves_produtos():
    print("\nChaves de produtos presentes no Redis:")
    cursor_redis = 0
    encontrou = False

    while True:
        cursor_redis, chaves = r.scan(cursor=cursor_redis, match="produto:*", count=100)
        for chave in chaves:
            produto = r.hgetall(chave)
            if produto:
                print(f"\n{chave}")
                for campo, valor in produto.items():
                    print(f"  {campo}: {valor}")
                encontrou = True
        if cursor_redis == 0:
            break

    if not encontrou:
        print("Nenhum produto encontrado no cache.")


def menu():
    while True:
        print("\n--- MENU ---")
        print("1 - Buscar produto")
        print("2 - Listar produtos no cache")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            id_produto = input("Digite o ID do produto: ")

            try:
                id_produto = int(id_produto)
                buscar_produto(id_produto)
            except ValueError:
                print("Digite um ID válido.")

        elif opcao == "2":
            listar_chaves_produtos()

        elif opcao == "0":
            print("Encerrando...")
            break

        else:
            print("Opção inválida.")

    cursor.close()
    conn.close()

menu()
