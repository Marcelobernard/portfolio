# 🌐 Projeto bernard.dev.br — Site Pessoal & Ecossistema Web

> Plataforma web multifuncional para divulgação pessoal, portfólio, pequenos sistemas web (como Post-It público) e outras aplicações desenvolvidas com tecnologias modernas e infraestrutura serverless AWS + GitHub Pages.

---

## 🚀 Visão Geral

Este repositório reúne o site pessoal bernard.dev.br, que serve como hub para diversos projetos e funcionalidades, incluindo:

- Site institucional / currículo / portfólio  
- Sistemas web simples e serverless, como o app Post-It público  
- Páginas para projetos pessoais estão no repositório original pois não convém estarem aqui  
- Integração com AWS Lambda, DynamoDB, API Gateway e S3 para backend
- Hospedagem front-end estática via GitHub Pages e S3

---

## 🏗 Arquitetura & Tecnologias

| Serviço AWS        | Função                                                          |
|--------------------|----------------------------------------------------------------|
| **GitHub Pages**   | Hospedagem principal dos sites estáticos com deploy automático |
| **AWS S3**         | Backup / hospedagem estática alternativa e arquivos auxiliares |
| **AWS Lambda**     | Backend serverless para APIs dinâmicas e integrações           |
| **AWS API Gateway**| Roteamento HTTP para Lambdas com suporte a CORS                |
| **DynamoDB**       | Banco NoSQL para armazenamento de dados dinâmicos              |
| **JavaScript/HTML/CSS** | Front-end leve, responsivo e interativo                   |

---

## 📝 Principais Funcionalidades

### Site Pessoal & Portfólio
- Páginas estáticas com informações profissionais, contatos e projetos  
- Estrutura simples, fácil de manter e expandir  

### Sistema Post-It Web App (Exemplo de API Serverless)
- Usuários podem criar notas públicas tipo Post-It  
- Backend AWS processa, armazena e retorna as notas em tempo real  
- Front-end faz requisições REST para API Gateway e exibe resultados  

---

## 🔄 Fluxo do Sistema Post-It

```mermaid
graph LR
  U[Usuário] -->|POST /postit-api| API[API Gateway]
  API --> L[AWS Lambda]
  L --> DB[DynamoDB - Inserir Nota]

  U -->|GET /postit-api| API
  API --> L
  L --> DB[DynamoDB - Listar Notas]
  DB --> L
  L --> API
  API --> U

````

## Segue o código do Node.js:

      const { DynamoDBClient } = require("@aws-sdk/client-dynamodb");
      const { DynamoDBDocumentClient, PutCommand, ScanCommand } = require("@aws-sdk/lib-dynamodb");
      
      const client = new DynamoDBClient({ region: "sa-east-1" });
      const dynamo = DynamoDBDocumentClient.from(client);
      const TABLE_NAME = "bernard-dev-br";
      
      exports.handler = async (event) => {
        const method = event.requestContext?.http?.method || event.httpMethod;
    
      if (method === "POST") {
        const body = JSON.parse(event.body);
        const id = Date.now().toString();
    
        const item = {
          id,
          texto: body.texto || "",
          dataCriacao: new Date().toISOString(),
        };
    
        await dynamo.send(new PutCommand({ TableName: TABLE_NAME, Item: item }));
    
        return {
          statusCode: 201,
          body: JSON.stringify({ message: "Post-it criado", id }),
        };
      }
    
      if (method === "GET") {
        const result = await dynamo.send(
          new ScanCommand({
            TableName: TABLE_NAME,
          })
        );
    
        return {
          statusCode: 200,
          body: JSON.stringify(result.Items),
        };
      }
    
      return {
        statusCode: 405,
        body: JSON.stringify({ message: "Método não permitido" }),
      };
    };
