import json
import boto3
from datetime import datetime
import os

# Inicializa o cliente do DynamoDB
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        # Obtém os dados do corpo da requisição
        body = json.loads(event['body'])
        
        # Extrai os dados do usuário
        user_data = {
            'email': body['email'],  # Chave primária
            'name': body['name'],
            'picture': body['picture'],
            'last_login': datetime.now().isoformat(),
            'login_count': 1  # Será incrementado se o usuário já existir
        }
        
        # Tenta atualizar o item existente
        try:
            response = table.update_item(
                Key={'email': user_data['email']},
                UpdateExpression='SET name = :name, picture = :picture, last_login = :last_login, login_count = login_count + :inc',
                ExpressionAttributeValues={
                    ':name': user_data['name'],
                    ':picture': user_data['picture'],
                    ':last_login': user_data['last_login'],
                    ':inc': 1
                },
                ReturnValues='UPDATED_NEW'
            )
        except dynamodb.meta.client.exceptions.ResourceNotFoundException:
            # Se o usuário não existir, cria um novo
            table.put_item(Item=user_data)
        
        return {
            'statusCode': 200,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'message': 'Login registrado com sucesso',
                'user': user_data
            })
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'headers': {
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Allow-Methods': 'POST,OPTIONS'
            },
            'body': json.dumps({
                'error': str(e)
            })
        } 