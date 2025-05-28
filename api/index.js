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
