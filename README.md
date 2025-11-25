1.  Clone o repositório:
    ``` bash
    git clone [https://github.com/seu-usuario/viaje-bem.git](https://github.com/seu-usuario/viaje-bem.git)
    cd viaje-bem
    ```

2.  Crie e ative um ambiente virtual (recomendado):
    Windows:
        ``` bash
        python -m venv venv
        venv\Scripts\activate
        ```
    Linux/Mac:
        ``` bash
        python3 -m venv venv
        source venv/bin/activate
        ```

3.  Instale as dependências:
    ``` bash
    pip install -r requeriments.txt
    ```
    (Nota: Certifique-se de que o nome do ficheiro está correto, no projeto atual está como `requeriments.txt`)

4.  Configure o Banco de Dados:
    Execute as migrações para criar as tabelas no SQLite:
    ``` bash
    python manage.py migrate
    ```
