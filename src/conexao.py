import redis
import json

def conectarRedis():
    try:
        conexaoRedis = redis.Redis(
            host='',
            port=,
            password=''
        )
        return conexaoRedis
    except Exception as e:
        print(f"Erro ao conectar ao Redis: {e}")
        return None

global conR
conR = conectarRedis()

email = "user-matheus@aa.com"

resposta = conR.get(email)
objetoResposta = json.loads(resposta)
print(objetoResposta["nome"])