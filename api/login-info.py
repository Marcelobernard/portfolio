import json
import boto3
from datetime import datetime
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['DYNAMODB_TABLE'])

def lambda_handler(event, context):
    try:
        if 'body' in event and isinstance(event['body'], str):
            body = json.loads(event['body'])
        elif 'body' in event and isinstance(event['body'], dict):
            body = event['body']
        else:
            body = event

        if not all(k in body for k in ('email', 'name', 'picture')):
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'Campos obrigatórios: email, name, picture'})
            }

        user_data = {
            'email': body['email'],
            'name': body['name'],
            'picture': body['picture'],
            'last_login': datetime.now().isoformat()
        }

        table.update_item(
            Key={'email': user_data['email']},
            UpdateExpression='SET #n = :name, picture = :picture, last_login = :last_login, login_count = if_not_exists(login_count, :zero) + :inc',
            ExpressionAttributeNames={
                '#n': 'name'
            },
            ExpressionAttributeValues={
                ':name': user_data['name'],
                ':picture': user_data['picture'],
                ':last_login': user_data['last_login'],
                ':inc': 1,
                ':zero': 0
            },
            ReturnValues='UPDATED_NEW'
        )

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
            'body': json.dumps({'error': str(e)})
        }