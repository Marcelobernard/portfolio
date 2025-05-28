# 📌 Projeto Post-It Web App

> Sistema web serverless para criação e visualização pública de notas Post-It, usando AWS Lambda, DynamoDB, API Gateway, S3 e GitHub Pages.

---

## 🚀 Visão Geral

Este projeto entrega um app simples onde qualquer usuário pode criar uma nota pública (Post-It) e ver todas as outras notas em tempo real. Backend 100% serverless AWS + front-end estático.

O hospedagem foi pensada no Bucket S3 mas por questões de afinidade pessoal, eu preferi deixar no GitHub Pages.
Segue o link do site no S3:
- https://bernard-dev-br.s3.sa-east-1.amazonaws.com/index.html
- https://bernard-dev-br.s3.sa-east-1.amazonaws.com/postit.html

---

## 🏗 Arquitetura & Tecnologias

| Serviço AWS        | Função                                                          |
|--------------------|----------------------------------------------------------------|
| **Lambda**         | Processa requisições HTTP (GET/POST), integra com DynamoDB     |
| **DynamoDB**       | Banco NoSQL para armazenar notas (id, texto, timestamp)        |
| **API Gateway**    | Roteia chamadas HTTP para Lambda, gerencia CORS                |
| **S3**             | Hospedagem estática do front-end (HTML, CSS, JS)               |
| **GitHub Pages**   | Hospedagem alternativa do front-end com deploy automático      |

---

## 📝 Como Funciona o Sistema Post-It

- **POST:** Envia um JSON com o texto da nota para a API Gateway → Lambda → DynamoDB (salva a nota)  
- **GET:** Requisição para API Gateway → Lambda → DynamoDB (retorna todas as notas)  
- **Front-end:** Captura texto, envia POST e exibe lista atualizada com GET  

---

## 🔄 Fluxo das Chamadas

```mermaid
graph LR
  U[Usuário Front-End] -->|POST /postit-api| API[API Gateway]
  API --> L[Lambda]
  L --> DB[DynamoDB - Insert]

  U -->|GET /postit-api| API
  API --> L
  L --> DB[DynamoDB - Scan]
  DB --> L
  L --> API
  API --> U
