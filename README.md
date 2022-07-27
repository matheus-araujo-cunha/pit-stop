<h1 align = "center">
  Pitstop - API
</h1>

<p align = "center">
Este é o backend da aplicação Pitstop - um e-commerce de autopeças onde o usuário consegue adicionar produtos ao carrinho e realizar um pedido.
</p>


## Endpoints
A api tem um total de 10 endpoints, sendo em volta do usuário, conseguindo visualizar os produtos disponíveis, podendo cadastrar uma conta para adicionar os produtos ao carrinho, e realizar um pedido quando for necessário.


O URL base da api é: <https://pitstop-api.herokuapp.com>

## Rotas que não precisam de autenticação



<h2 align = "center"> Listando Produtos </h2>
Nessa aplicação o usuário sem estar autenticado, consegue visualizar os produtos ja cadastrados na API, da seguinte forma:

`GET /api/products/ - FORMATO DA RESPOSTA - STATUS 200`
```json


```