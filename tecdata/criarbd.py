import pymysql.cursors

try:
    banco=pymysql.connect(
        host='us-cdbr-east-02.cleardb.com',
        user='bfba5ab75e431f',
        password='24aa11e4',
        db='heroku_07568d07459b9e8',
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )
except:
    print('error ao conectar com o banco de dados')

class criaBD():
    def __init__(self, ano_inicial, ano_final):
        self.ano_inicial = ano_inicial
        self.ano_final = ano_final
    
    def bd(self):
        pass