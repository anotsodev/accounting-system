import jwt
import uuid
token_key = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTIwMjgwNzIsImlhdCI6MTUxMjAyNzQ3Miwic3ViIjoia3lsZV9oYWxvZyJ9.01kfhYCVIuIDbPlld4lTTkxpQq-8eAr0vRN_7nGM3F4"
# print(jwt.decode(token_key, 'secret', algorithms=['HS256'])['sub'])

print(uuid.uuid1())