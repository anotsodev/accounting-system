import jwt

try:
    print (jwt.decode('eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJleHAiOjE1MTE4Nzk4NzQsImlhdCI6MTUxMTg3OTI3NCwic3ViIjoiYWxiZXJ0X2VpbnN0ZWluIn0.VBU9Oxd7oTuvD2EDSmS_uLDmtnyj72iH-H_5uUCKbu8','secret'))
except jwt.ExpiredSignature:
    print ("Expired")