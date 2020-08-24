import multiprocessing as mp
import time, os
import pymysql.cursors
from tecdata import importarz, criarbd


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


#Dados utilizado futuramente (Latitude e longitude)
lon = [i for i in range(-180, 185, 5)]#Longitude
lat = []#Latitude
step = 87.5
while step != -90:
    lat.append(step)
    step -= 2.5

#Função para obter o TEC dos aquivos IONEX de todo o ano
def obterTEC(ano):
        TEC = []
        tec = []
        for dia in range(1, 366):
            if dia < 10:#Com essa condicional selecionamos o número do arquivo correto com base no dia a analisar
                number_file = "00" + str(dia)
            elif (dia > 9) and (dia < 100):
                number_file = "0" + str(dia)
            else:
                number_file = str(dia)

            arquivo = open('tecdata/20' + str(ano) + '/igsg' + number_file + '0.' + str(ano) + 'i', 'r')  # Abrimos o arquivo
            arquivo = arquivo.read()#Transformamos a variável arquivo em string
            arquivo = arquivo.splitlines()#Quebramos em linhas, logo, cada linha do arquivo IONEX pertence a uma lista de n índices
            #onde n=len(arquivo)=Nº de linhas

            # //--------------------------Tiramos o header e RMS do arquivo ionex ----------------------------------
            head = arquivo.index('                                                            END OF HEADER       ')#Encontramos o índice onde acaba o header do IONEX
            arquivo1 = arquivo[head + 1::]#Com base no índice obtido anteriormente tiramos o header
            rms = arquivo.index('     1                                                      START OF RMS MAP    ')#Encontramos o índice onde inicia o mapa RMS(não pertence à nossa análise)
            arquivo = arquivo1[0:rms]#Com base no índice obtido anteriormente tiramos o mapa RMS da variável arquivo

            # //--------------------------Pegamos os mapas TEC do arquivo----------------------------------
            ds = 429 #Cada mapa TEC se repete a cada 429 linhas
            for epoch in range(0, 13): #São 13 mapas TEC
                teste1 = arquivo[2:ds] #Salvamos em teste1 o mapa TEC da época atual
                del arquivo[0:429] #Deletamos ele da variável arquivo

                # //---------------------Apenas dados numéricos--------------------------------------------
                teste1_num = []
                step = 87.5
                j = 0
                while step >= -87.5:
                    teste1_num = teste1_num + teste1[j + 1:j + 6]#Retiro apenas os dados numéricos
                    step -= 2.5
                    j += 6

                # //--------------------------Lidando com os dados numericos------------------------------------------
                p = ['   ', '  '] #Como ainda temos espaços nos índices da lista teste1_num, precisamos retirá-los
                for k in p:
                    teste1_num = [item.replace(k, ';') for item in teste1_num]#Retiramos os espaços e substituimos por ;

                vec_aux = [teste1_num[i].split(';') for i in range(0, len(teste1_num))]#Utilizamos o ; para quebrar cada índice em apenas no número
                vec_aux2 = [list(filter(lambda m: m != '', vec_aux[i])) for i in range(0, len(vec_aux))]#Retiramos os índices vazios
                #Em vec_aux2 teremos uma lista de dim(2)(vec_aux[i][j) onde cada índice i é uma linha do mapa TEC (apenas numeros)
                vec_aux = []
                step = 0
                #------------------------------------------
                for i in range(0, len(lat)):
                    vec_aux.append(vec_aux2[step:step+5])
                    step += 5
                #Como para cada latitude do mapa TEC, para dada época, possuí 5 linhas com lon variando de -180 a 180, aqui armazenamos
                #em vec_aux essas cínco linhas, assim, temos uma lista de dim(3)(TEC[i][j][k]) onde i é uma latitude e cada j uma linha das 5
                #------------------------------------------
                vec_aux2 = []
                y = []
                #------------------------------------------
                for i in range(0, len(vec_aux)):
                    for j in range(0, 5):
                        vec_aux2 = vec_aux2 + vec_aux[i][j]
                    y.append(vec_aux2)
                    vec_aux2 = []
                #Como não é necessário ter uma lista dim(3)(aumentando a complexidade) nesse loop é feita a redução de dimensão
                #armazenando em y uma lista que representa a latitude e cada índice dessa latitude são as longitudes indo de -180 a 180
                #logo, são 73 valores para cada latitude.
                #------------------------------------------
                tec.append(y)#Armazemoas em tec o mapa filtrado

            TEC.append(tec)#Armazenamos em TEC o mapa filtrado anteriormente para a época correspondente, assim, no final
            #temos um mapa TEC completo e numérico, apenas. Sendo este dim(3) TEC[i][j][k], cada i-ésimo indíce representa
            #o mapa TEC(os treze) para cada dia do ano
            tec = []

        print('Iniciando armazenamento ANO[{}]'.format(ano))
        armazenarTEC(TEC, ano)#Chamamos a função armazenarTEC para colocálo no bando de dados da API
        return 1

#Função para armazenar os dados TEC no Banco de dados MYSQL da API
def armazenarTEC(TEC, ano_inicial):
        cont = 0
        s = ',%s'
        #TEC[i][j] Acesso para as latitudes
        #TEC[i][j][k] Acesso para as longitudes
        for i in range(0, len(TEC)):
            for j in range(0, len(TEC[i])):
                for k in range(0,len(TEC[i][j])):
                    latitude = lat[k] #Utilizamos a variável lat para obter a latitude
                    if cont==26: cont=0 #Com isso podemos armazenar a hora correta no banco de dados
                    val = [cont] + TEC[i][j][k] #Em val armazenamos todos os dados necessários para salvar no bd
                    with banco.cursor() as cursor: #Iniciamos o processo de salvar na tabela correspondente do bd
                        tableName = '20' + str(ano_inicial) + '_' + str(latitude) #Obtemos o nome da tabela
                        sql = "INSERT INTO `" + tableName + "` (hora, `-180`, `-175`, `-170`, `-165`, `-160`, `-155`, `-150`, `-145`, `-140`, `-135`, `-130`, `-125`, `-120`, `-115`, `-110`, `-105`, `-100`, `-95`, `-90`, `-85`, `-80`, `-75`, `-70`, `-65`, `-60`, `-55`, `-50`, `-45`, `-40`, `-35`, `-30`, `-25`, `-20`, `-15`, `-10`, `-5`, `0`, `5`, `10`, `15`, `20`, `25`, `30`, `35`, `40`, `45`, `50`, `55`, `60`, `65`, `70`, `75`, `80`, `85`, `90`, `95`, `100`, `105`, `110`, `115`, `120`, `125`, `130`, `135`, `140`, `145`, `150`, `155`, `160`, `165`, `170`, `175`, `180`) VALUES (%s" + s * 73 + ")"
                        cursor.execute(sql, val)

                cont += 2

        print('done')

def main():
    op = int(input(
        "1 - Fazer o download de arquivos Z para o PC\n2 - Criar tabelas para determinado intervalo de tempo(anos)\n3 - Salvar dados na API\n Escolha uma opção[0 para sair]: "))
    if op == 1:
        ano_inicial = int(input('Digite o ano inicial compactado(19 no lugar de 2019)[0 para sair]: '))
        if ano_inicial == 0:os._exit(0)
        ano_final = int(input('Digite o ano final compactado(19 no lugar de 2019)[0 para sair]: '))
        if ano_final == 0:os._exit(0)
        importarz.importtec(ano_inicial, ano_final).importar()#Chamamos o método importar da classe importarTEC (sem instanciar)
        print('Os arquivos foram baixados')
        main()
    elif op == 2:
        ano_inicial = int(input('Digite o ano inicial compactado(19 no lugar de 2019)[0 para sair]: '))
        if ano_inicial == 0:os._exit(0)
        ano_final = int(input('Digite o ano final compactado(19 no lugar de 2019)[0 para sair]: '))
        if ano_final == 0:os._exit(0)
        criarbd.criaBD(ano_inicial, ano_final).bd()#Chamamos o método bd() pertencente a classe criarbr(sem instanciar)
        print('Tabelas criadas')
        main()
    elif op==3:
        pool = mp.Pool(4)#Escolho 4 CPU para paralelizar, com o método mp.cpu_count() utilizaria todos disponíveis
        ano_inicial = int(input('Digite o ano compactado(19 no lugar de 2019)[0 para sair]: '))
        if ano_inicial == 0:os._exit(0)
        start = time.time()#Inicío a contagem para cronometrar o tempo de duração do processo de filtrar e armazenar os dados
        ano_inicial = [ano_inicial]
        a = pool.map_async(obterTEC, ano_inicial)#Utilizo paralelização assíncrona para o processo
        print(a.get(), time.time() - start)
        print('Dados armazenados')
        main()
    else:
        return 0
if __name__=='__main__':
    main()
