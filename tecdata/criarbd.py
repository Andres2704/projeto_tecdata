import pymysql.cursors

lon = [i for i in range(-180, 185, 5)]
lat = []
step = 87.5
while step != -90:
    lat.append(step)
    step -= 2.5

try:
    banco=pymysql.connect(
        host='',
        user='',
        password='',
        db='',
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
                with banco.cursor() as cursor:
                    tableName = '20'+str(ano)+'_'+str(i)
                    sql = "CREATE TABLE IF NOT EXISTS `"+tableName+"`(id int(11) auto_increment, hora int(11) not null, `F10.7` double(10,2) NULL DEFAULT NULL, PRIMARY KEY (`id`))"
                    cursor.execute(sql)
                    for longitude in lon:
                        sql = "ALTER TABLE `"+tableName+"` ADD `"+str(longitude)+"` int(11)"
                        cursor.execute(sql)
                        banco.commit()
                    print('Tabela criada:'+tableName)
        return 1
