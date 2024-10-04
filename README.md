# DeclaraPro API

O DeclaraPro é uma aplicação que permite ao contador gerenciar informações de clientes e seus documentos associados, para facilitar o processo da declaração do imposto de renda.

## Tecnologias Usadas

- Django
- Django REST Framework
- SQLite (banco de dados)

## Endpoints

### 1. Listar Todos os Clientes

**GET** `/customers/`

Retorna uma lista de todos os clientes.

**Exemplo de Resposta:**

```
[
    {
        "id": 1,
        "name": "João Silva",
        "cpf": "123.456.789-00",
        "birthDate": "1990-01-01",
        "email": "joao@example.com",
        "phone": "11987654321",
        "status": "pendente",
        "documents": "Sem documentos cadastrados"
    },
    {
        "id": 2,
        "name": "Maria Oliveira",
        "cpf": "987.654.321-00",
        "birthDate": "1985-05-15",
        "email": "maria@example.com",
        "phone": "11876543210",
        "status": "em processamento",
        "documents": [
            {
                "id": 1,
                "name": "RG",
                "document_type": "pdf",
                "file": "documents/rg_maria.pdf",
                "uploaded_at": "2023-09-24T00:00:00Z"
            }
        ]
    }
]
```

### 2. Criar um Novo Cliente

**POST** `/customers/`

Adiciona um novo cliente ao sistema.

**Exemplo de Requisição:**

```
{
    "name": "Ana Costa",
    "cpf": "111.222.333-44",
    "birthDate": "1992-02-02",
    "email": "ana@example.com",
    "phone": "11912345678",
    "status": "pendente"
}
```

### 3. Deletar um Cliente

**DELETE** `/customers/{id}/`

Remove um cliente e seus documentos associados do sistema.


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

