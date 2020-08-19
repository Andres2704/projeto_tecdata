import pymysql.cursors

lon = [i for i in range(-180, 185, 5)]
lat = []
step = 87.5
while step != -90:
    lat.append(step)
    step -= 2.5

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
        for ano in range(self.ano_inicial, self.ano_final+1):
            for i in lat:
                for j in lon:
                    with banco.cursor() as cursor:
                        dbName = str(ano)+'_'+str(i)+'_'+str(j)
                        sql = "CREATE TABLE `"+dbName+"`(dia int(11), hora0 int(11) not null, hora2 int(11) not null, hora4 int(11) not null, hora6 int(11) not null, hora8 int(11) not null, hora10 int(11) not null, hora12 int(11) not null, hora14 int(11) not null, hora16 int(11) not null, hora18 int(11) not null, hora20 int(11) not null, hora22 int(11) not null, hora24 int(11) not null, f107 double(10,2) NULL DEFAULT NULL)"
                        cursor.execute(sql)
        return 1