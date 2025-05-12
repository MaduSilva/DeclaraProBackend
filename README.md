# DeclaraPro API

O DeclaraPro é uma aplicação que permite ao contador gerenciar informações de clientes e seus documentos associados, para facilitar o processo da declaração do imposto de renda.

<sub>
Este repositório foi desenvolvido com fins <strong>estritamente acadêmicos</strong>. Algumas boas práticas de segurança, como a proteção de credenciais e dados sensíveis, <strong>não foram aplicadas intencionalmente</strong>, pois <strong>não fazem parte do escopo deste trabalho</strong>.  
O foco principal está na lógica e funcionamento do sistema proposto.</sub>


## Tecnologias Usadas

- Django
- Django REST Framework
- SQLite (banco de dados)

## Endpoints

- Consultar swagger ou postman disponível no repositório

## Requisitos

- Python 3.11.5
- Django
- Django REST Framework

## Instalação

1. Clone o repositório:

   ```
   git clone https://github.com/MaduSilva/DeclaraProBackend.git

   cd DeclaraProBackend
   ```

2. Instale as dependências:

    ```
    pip install -r requirements.txt
    ```

3. Execute as migrações:

    ```
    python manage.py migrate
    ```

4. Inicie o servidor:

    ```
    python manage.py runserver
    ```

5. Acesse a rota: /api/swagger


