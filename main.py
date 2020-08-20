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

#AQUI REALIZAMOS A CONEXÃO COM O BANCO DE DADOS
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
                vec_aux2 = [list(filter(lambda m: m != '', vec_aux[i])) for i in range(0, len(vec_aux))]
                vec_aux = []
                step = 0
                for i in range(0, len(lat)):
                    vec_aux.append(vec_aux2[step:step+5])
                    step += 5
                vec_aux2 = []
                y = []
                for i in range(0, len(vec_aux)):
                    for j in range(0, 5):
                        vec_aux2 = vec_aux2 + vec_aux[i][j]
                    y.append(vec_aux2)
                    vec_aux2 = []

                tec.append(y)

            TEC.append(tec)
            tec = []

        print('Iniciando armazenamento ANO[{}]'.format(ano))
        armazenarTEC(TEC, ano)#Chamamos a função armazenarTEC para colocálo no bando de dados da API
        return 1

#Função para armazenar os dados TEC no Banco de dados MYSQL da API
def armazenarTEC(TEC, ano_inicial):
        cont = 0
        s = ',%s'
        f107 = 107
        #TEC[i][j] Acesso para as latitudes
        #TEC[i][j][k] Acesso para as longitudes
        for i in range(0, len(TEC)):
            for j in range(0, len(TEC[i])):
                for k in range(0,len(TEC[i][j])):
                    latitude = lat[k]
                    if cont==26:
                        cont=0
                    val = [cont] + [f107] + TEC[i][j][k]
                    with banco.cursor() as cursor:
                        tableName = '20' + str(ano_inicial) + '_' + str(latitude)
                        sql = "INSERT INTO `" + tableName + "` (hora, `F10.7`, `-180`, `-175`, `-170`, `-165`, `-160`, `-155`, `-150`, `-145`, `-140`, `-135`, `-130`, `-125`, `-120`, `-115`, `-110`, `-105`, `-100`, `-95`, `-90`, `-85`, `-80`, `-75`, `-70`, `-65`, `-60`, `-55`, `-50`, `-45`, `-40`, `-35`, `-30`, `-25`, `-20`, `-15`, `-10`, `-5`, `0`, `5`, `10`, `15`, `20`, `25`, `30`, `35`, `40`, `45`, `50`, `55`, `60`, `65`, `70`, `75`, `80`, `85`, `90`, `95`, `100`, `105`, `110`, `115`, `120`, `125`, `130`, `135`, `140`, `145`, `150`, `155`, `160`, `165`, `170`, `175`, `180`) VALUES (%s" + s * 74 + ")"
                        cursor.execute(sql, val)

                cont += 2

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
        ano_inicial = [ano_inicial]
        a = pool.map_async(obterTEC, ano_inicial)
        print(a.get(), time.time()-start)
