# Cache de produtos com Redis e PostgreSQL

Exercício em Python que busca produtos no PostgreSQL e armazena as consultas no Redis por 60 segundos.

## Como executar

1. Suba o PostgreSQL e o Redis:

   ```powershell
   docker compose up -d
   ```

   Na primeira execução, o PostgreSQL cria o banco `redisCache` e carrega os produtos de `produtos.txt`.

2. Instale as dependências Python:

   ```powershell
   pip install -r requirements.txt
   ```

3. Execute o programa com menu:

   ```powershell
   python redis_cache_produtos.py
   ```

4. Para encerrar os containers:

   ```powershell
   docker compose down
   ```
