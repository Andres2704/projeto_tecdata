import multiprocessing as mp
import time, os
import pymysql.cursors
import api
from tecdata import importarz, criarbd

#Dados utilizado futuramente (Latitude e longitude)
lon = [i for i in range(-180, 185, 5)]
lat = []
step = 87.5
while step != -90:
    lat.append(step)
    step -= 2.5

#AQUI REALIZAMOS A CONEXÃO COM O BANCO DE DADOS E LOGO APÓS
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
###########################################################

#Função para obter o TEC dos aquivos IONEX de todo o ano
def obterTEC(ano):
        TEC = []
        tec = []
        for dia in range(1, 366):
            #Com essa condicional selecionamos o número do arquivo correto com base no dia a analisar
            if dia < 10:
                number_file = "00" + str(dia)
            elif (dia > 9) and (dia < 100):
                number_file = "0" + str(dia)
            else:
                number_file = str(dia)
            arquivo = open('tecdata/20' + str(ano) + '/igsg' + number_file + '0.' + str(ano) + 'i', 'r')  # Abrimos o arquivo
            arquivo = arquivo.read()
            arquivo = arquivo.splitlines()

            # //--------------------------Tiramos o header e RMS do arquivo ionex ----------------------------------
            head = arquivo.index('                                                            END OF HEADER       ')
            arquivo1 = arquivo[head + 1::]
            rms = arquivo.index('     1                                                      START OF RMS MAP    ')
            arquivo = arquivo1[0:rms]

            # //--------------------------Pegamos os mapas TEC do arquivo----------------------------------
            ds = 429
            for epoch in range(0, 13):
                teste1 = arquivo[2:ds]
                del arquivo[0:429]

                # //---------------------Apenas dados numéricos--------------------------------------------
                teste1_num = []
                step = 87.5
                j = 0
                while step >= -87.5:
                    teste1_num = teste1_num + teste1[j + 1:j + 6]
                    step -= 2.5
                    j += 6

                # //--------------------------Lidando com os dados numericos------------------------------------------
                p = ['   ', '  ']

                for k in p:
                    teste1_num = [item.replace(k, ';') for item in teste1_num]

                vec_aux = [teste1_num[i].split(';') for i in range(0, len(teste1_num))]
                vec_aux2 = [vec_aux[i][k] for i in range(0, len(vec_aux)) for k in range(0, len(vec_aux[i]))]
                vec_aux2 = list(filter(lambda m: m != '', vec_aux2))
                tec.append(vec_aux2)

            TEC.append(tec)
            tec = []
            vec_aux = []
            vec_aux2 = []
        print('Iniciando armazenamento ANO[{}]'.format(ano))
        armazenarTEC(TEC, ano) #Chamamos a função armazenarTEC para colocálo no bando de dados da API
        return 1

#Função para armazenar os dados TEC no Banco de dados MYSQL da API
def armazenarTEC(TEC, ano_inicial):
        print(str(ano_inicial))
        step_lon = 0
        step = 0
        dia = 0
        for latitude in lat:
            for longitude in range(0,73):
                for i in range(step_lon, step_lon+1):
                    y = [int(TEC[j][i][step_lon]) for j in range(0, 365) for i in range(0, 13)]
                    for j in range(0,365):
                        val = [dia+1] + y[step:step+13] + [90]
                        step += 13
                        dia += 1
                        print(val)
                        with banco.cursor() as cursor:
                            dbName = '20'+str(ano_inicial)+''+str(latitude)+''+str(lon[longitude])
                            sql = "INSERT INTO `" + dbName + "` (dia, hora0, hora2, hora4, hora6, hora8, hora10, hora12, hora14, hora16, hora18, hora20, hora22, hora24, f107) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"
                            cursor.execute(sql, val)
                            banco.commit()
                    dia = 0
                    step=0
                    val = []
                    y = []
            step_lon += 73
        print('done')

if __name__=='__main__':
    op = int(input("1 - Fazer o download de arquivos Z para o PC\n2 - Criar banco de dados para determinado intervalo de tempo(anos)\n3 - Salvar dados na API\n Escolha uma opção: "))
    if op==1:
        ano_inicial = int(input('Digite o ano inicial compactado(19 no lugar de 2019)[0 para sair]: '))
        ano_final = int(input('Digite o ano final compactado(19 no lugar de 2019)[0 para sair]: '))
        importarz.importtec(ano_inicial, ano_final)
        print('Os arquivos foram baixados')
        os._exit(0)
    elif op==2:
        ano_inicial = int(input('Digite o ano inicial compactado(19 no lugar de 2019)[0 para sair]: '))
        ano_final = int(input('Digite o ano final compactado(19 no lugar de 2019)[0 para sair]: '))
        criarbd.criaBD(ano_inicial, ano_final)
    else:
        pool = mp.Pool(4)
        ano_inicial = int(input('Digite o ano compactado(19 no lugar de 2019)[0 para sair]: '))
        if ano_inicial==0:
            os._exit(0)
        start = time.time()
        a = pool.map_async(obterTEC, ano_inicial)
        print(a.get(), time.time()-start)