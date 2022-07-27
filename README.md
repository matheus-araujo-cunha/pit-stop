# pit-stop | Introdução

Esse é um projeto Back End de um E-commerce, para armazenar produtos e efetuar a compra dos mesmos a partir do carrinho de compra.

## Endpoints

> ## User
>
> ### Post | Login

`localhost:8000/api/users/login/`

O usuário vai passar seu email e senha e recebera um Token de autenticação com status 200 OK.

`Requisição `

```json
{
  "email": "ivangilhom@mail.com",
  "password": "senhaFOrte1234"
}
```

`Resposta`

```json
{
  "token": "$2a$10$I4dNmZfH/k39xZmGBXlta.7XCbdkHlSlgdjLh7J5G1w7sX1/XOqNK"
}
```

> ### Post | Criação de novo usuário.

`localhost:8000/api/users/`

Requisição para criar um novo usuário na plataforma.

`Requisição `

```json
{
  "email": "kenzinho@mail.com",
  "name": "kenzinho",
  "password": "1234"
}
```

`Resposta | status 201 Created`

```json
{
  "id": 1,
  "name": "Kenzinho",
  "email": "kenzinho@mail.com",
  "is_superuser": false
}
```

> ### Post | Criação de novo usuário ADM.

`localhost:8000/api/users/`

Apenas um usuário ADM pode criar outro usuário ADM.
Necessário `TOKEN` de autenticação.

`Requisição `

```json
{
  "email": "kenzinhoADM@mail.com",
  "name": "kenzinhoADM",
  "password": "1234"
}
```

`Resposta | status 201 Created`

```json
{
  "id": 1,
  "name": "KenzinhoADM",
  "email": "kenzinhoADM@mail.com",
  "is_superuser": true
}
```

`Resposta | Status 401 Unauthorized`

Se não houver `TOKEN` de autentificação.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

> ## Produtos
>
> ### Post | Criação de um novo produto na plataforma.

`localhost:8000/api/products/`

Requisição para criar um novo produto na plataforma.
Necessário `TOKEN` para autentificação do usuário que está criadno o produto. Apenas com um usuário ADM é permitido criar um novo produto. A propriedade "is_superuser" dever ser `TRUE`.

`Requisição `

```json
{
  "name": "shell3",
  "description": "algo novo",
  "manufacturer": "manufaturado",
  "img": "zero",
  "price": 4,
  "categorie": "peça",
  "warranty": 3,
  "stock": {
    "quantity": 4
  }
}
```

`Resposta | Status 201 Created`

```json
{
  "product_uuid": "f709847a-c475-4847-8d66-6f4dc7eb6ec8",
  "name": "shell3",
  "description": "algo novo",
  "manufacturer": "manufaturado",
  "warranty": 3,
  "price": "4.00",
  "categorie": "peça",
  "stock": {
    "quantity": 4.0
  }
}
```

`Resposta | Status 401 Unauthorized`

Se não houver `TOKEN` de autentificação.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

> ### GET | Listagem de produtos.

`localhost:8000/api/products/`

Requisição para listar os produtos da plataforma. Não é preciso autentificação para essa rota.

`Requisição `

> Não tem corpo na requisição.

`Resposta | status 200 OK`

Retorna uma lista de todos os produtos cadastrados na plataforma.
Não precisa do `TOKEN` de autenticação.

```json
[
  {
    "product_uuid": "e7724f7f-0bc2-41b3-86a7-03787047c101",
    "name": "shell",
    "description": "algo novo",
    "manufacturer": "manufaturado",
    "warranty": 3,
    "price": "4.00",
    "categorie": "peça",
    "stock": {
      "quantity": 4.0
    }
  },
  "..."
]
```

> ## Carrinho
>
> ### Post | Adicionar um produto ao carrinho.

`localhost:8000/api/carts/`

Requisição para adicionar um produto ao carrinho do usuário. Deve ser passado dentro de uma lista os "product_uuid" dos respectivos produto que ele deseja adiconar ao carrinho do usuário.
Autenticação de `TOKEN` necessária.

`Requisição `

```json
{
  "list_products": [
    {
      "product_uuid": "e7724f7f-0bc2-41b3-86a7-03787047c101"
    }
  ]
}
```

`Resposta | status 201 Created`

```json
{
  "id": 1,
  "user": {
    "id": 1,
    "name": "Kenzinho",
    "email": "kenzinho@mail.com",
    "is_superuser": false
  },
  "products": [
    {
      "id": 3,
      "price": 4,
      "amount": 1,
      "product": "e7724f7f-0bc2-41b3-86a7-03787047c101"
    }
  ]
}
```

`Resposta | status 400 Bad Request`

Precisa passar um "product_uuid" para dentro do corpor da requisição ou voltará um Error 400.

```json
{
  "list_products": [
    {
      "product_uuid": ["This field is required."]
    }
  ]
}
```

> ### GET | Pegar produtos do carrinho.

`localhost:8000/api/carts/`

Requisição para listar os produtos dentro do carinho do usuário.
Autenticação de `TOKEN` necessária.

`Requisição `

> Sem corpo de requisição.

`Resposta | status 200 OK`

```json
[
  {
    "product_uuid": "e7724f7f-0bc2-41b3-86a7-03787047c101",
    "name": "shell",
    "description": "algo novo",
    "manufacturer": "manufaturado",
    "warranty": 3,
    "price": "4.00",
    "categorie": "peça",
    "stock": {
      "quantity": 4.0
    }
  },
  "..."
]
```

> ### DEL | Deletar produto especifico do carrinho.

`localhost:8000/api/carts/products/e7724f7f-0bc2-41b3-86a7-03787047c101`

Requisição para remover produto especifico do carrinho. Precisa passar o "product_uuid" do produto desejado na URL.
Autenticação de `TOKEN` necessária.

`Requisição `

> Sem corpo de requisição

`Resposta | status 204 No Content`

Produto deletado do carrinho com sucesso!

> Sem corpo de resposta

`Resposta | status 404 Not Found`

Caso passe um "product_uuid" que não exista na plataforma ele retorna uma status 404 Not Found.

```json
{
  "message": "Product not found"
}
```

`Resposta | Status 401 Unauthorized`

Se não houver `TOKEN` de autentificação.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

> ## Ordens
>
> ### GET | Listar todas as ordens.

`localhost:8000/api/order/`

Lista os `ID` das ordem e os usuários que fizeram as requisições dessas ordens, assim como o horário que cada ordem foi feita. Autenticação de `TOKEN` necessária.

`Requisição `

> Sem corpo de requisição

`Resposta | status 200 OK`

```json
[
  {
    "id": 1,
    "date": "2022-07-27T13:44:12.554973Z",
    "user": {
      "id": 1,
      "name": "Kenzinho",
      "email": "kenzinho@mail.com",
      "is_superuser": false
    }
  },
  "..."
]
```

`Resposta | Status 401 Unauthorized`

Se não houver `TOKEN` de autentificação.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

> ### GET | Pegar um ordem especifica.

`localhost:8000/api/order/3`

Deve pasar o `ID` da ordem que deseja pegar no final da URL.
Autenticação de `TOKEN` necessária.

`Requisição `

> Sem corpo de requisição

`Resposta | status 200 OK`

Retorna o usuário que efetuou aquela ordem e o horário que foi feita.

```json
{
  "id": 3,
  "date": "2022-07-27T13:51:17.197102Z",
  "user": {
    "id": 1,
    "name": "Kenzinho",
    "email": "kenzinho@mail.com",
    "is_superuser": false
  }
}
```

`Resposta | status 404 Not Found`

Caso passe um `ID` de uma ordem que não exista.

```json
{
  "detail": "Not found."
}
```

`Resposta | Status 401 Unauthorized`

Se não houver `TOKEN` de autentificação.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

> ### POST | Criar uma nova ordem.

`localhost:8000/api/order/`

Cria uma nova ordem com todos os produtos que estão no carrinho daquele usuário.
Autenticação de `TOKEN` necessária.

`Requisição `

> Sem corpo de requisição

`Resposta | status 201 Created`

Retorna o usuário, data de criação da ordem e os produtos que vieram do carrinho daquele usuário para a ordem.

```json
{
  "id": 3,
  "date": "2022-07-27T13:51:17.197102Z",
  "user": {
    "id": 1,
    "name": "Kenzinho",
    "email": "kenzinho@mail.com",
    "is_superuser": false
  },
  "products": [
    {
      "id": 2,
      "product": {
        "product_uuid": "e7724f7f-0bc2-41b3-86a7-03787047c101",
        "name": "shell",
        "manufacturer": "manufaturado",
        "warranty": 3,
        "img": "",
        "categorie": "peça"
      },
      "value": "4.00",
      "amount": 1,
      "order": 3
    }
  ]
}
```

`Resposta | Status 401 Unauthorized`

Se não houver `TOKEN` de autentificação.

```json
{
  "detail": "Authentication credentials were not provided."
}
```

...

> E é isso! Vamos ver nosso E-commerce.

# Happy codin!!!

