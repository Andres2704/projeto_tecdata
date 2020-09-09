import pymysql.cursors, json, os
from flask import Flask,request, jsonify

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

#Função para obter o TEC específicado na barra de tarefa para determinado lat e ano
def retornaTEC(ano,lat, dia_i, dia_f):
    tecs = []
    linha_i = dia_i*13
    linha_f = dia_f*13
    dbName = str(ano)+'_'+str(lat)
    try:
        with banco.cursor() as cursor:
            cursor.execute("SELECT * FROM `"+dbName+"` ORDER BY id ASC LIMIT "+str(linha_i-13)+","+str(linha_f)+"")
            tecs = cursor.fetchall()
    except:
        print("SELECT * FROM `"+dbName+"` ORDER BY id ASC LIMIT "+str(linha_i-13)+","+str(linha_f)+"")
        print('erro ao listar os TECs para a tabela:', dbName)

    return tecs

def retornaF107(ano,dia_i,dia_f):
    f107 = []
    try:
        with banco.cursor() as cursor:
            cursor.execute("SELECT id, `"+str(ano)+"` FROM `f10.7` ORDER BY id ASC LIMIT "+str(dia_i-1)+","+str(dia_f)+"")
            f107 = cursor.fetchall()
    except:
        print('erro ao listar os dados para a tabela: f10.7',)

    return f107

def retornaRSN(ano,dia_i,dia_f):
    rsn = []
    try:
        with banco.cursor() as cursor:
            cursor.execute("SELECT id, `"+str(ano)+"` FROM rsn ORDER BY id ASC LIMIT "+str(dia_i-1)+","+str(dia_f)+"")
            rsn = cursor.fetchall()
    except:
        print('erro ao listar os os dados para a tabela: rsn',)

    return rsn

def retornaPhotonFlux(ano,dia_i,dia_f):
    PhotonFlux = []
    try:
        with banco.cursor() as cursor:
            cursor.execute("SELECT * FROM photonflux_"+str(ano)+" ORDER BY id ASC LIMIT "+str(dia_i-1)+","+str(dia_f)+"")
            PhotonFlux = cursor.fetchall()
    except:
        print('erro ao listar os os dados para a tabela: PhotonFlux',)

    return PhotonFlux

#Início do código desenvolvido para a construção da API
app = Flask(__name__)
app.config["DEBUG"] = True
###HOME---------------------------------------------------------------------
@app.route('/', methods=['GET'])
def home():
    return "<h1>API para obter dados TEC - F10.7 - Sunspost e Photon Flux</h1><p>Atualmente o Banco de dados está alimentado com dados dos anos de 2017, 2018 e 2019 - Atualizações estão sendo feitas</p><p><span style='font-style: italic'>Andres Benoit</span> - andres.benoit7@gmail.com</p>"

@app.route('/tec/', methods=['GET'])
def obterTECdeBD():
    if 'ano' in request.args:
        ano = int(request.args['ano'])
        lat = float(request.args['lat'])
        dia_i = int(request.args['dia_i'])
        dia_f = int(request.args['dia_f'])
    else:
        return "Error: Existem dados faltantes. Você deve especificar o ano, a latitude(lat) e de que dia a que dia quer obter os dados. Ex: /tec?ano=2019&lat=87.5&dia_i=1&dia_f=10"
    
    resultados = []
    for tec in retornaTEC(ano, lat, dia_i, dia_f):
        resultados.append(tec)
    
    return jsonify(resultados)

@app.route('/f107/', methods=['GET'])
def obterf107deBD():
    if 'ano' in request.args:
        ano = int(request.args['ano'])
        dia_i = int(request.args['dia_i'])
        dia_f = int(request.args['dia_f'])
    else:
        return "Error: Existem dados faltantes. Você deve especificar o ano e de que dia a que dia quer obter os dados. Ex: /f107?ano=2019&dia_i=1&dia_f=10"
    
    resultados = []
    for f107 in retornaF107(ano, dia_i, dia_f):
        resultados.append(f107)
    
    return jsonify(resultados)

@app.route('/rsn/', methods=['GET'])
def obterRSNdeBD():
    if 'ano' in request.args:
        ano = int(request.args['ano'])
        dia_i = int(request.args['dia_i'])
        dia_f = int(request.args['dia_f'])
    else:
        return "Error: Existem dados faltantes. Você deve especificar o ano e de que dia a que dia quer obter os dados. Ex: /rsn?ano=2019&dia_i=1&dia_f=10"
    
    resultados = []
    for rsn in retornaRSN(ano, dia_i, dia_f):
        resultados.append(rsn)
    
    return jsonify(resultados)

@app.route('/photonflux/', methods=['GET'])
def obterphotonfluxdeBD():
    if 'ano' in request.args:
        ano = int(request.args['ano'])
        dia_i = int(request.args['dia_i'])
        dia_f = int(request.args['dia_f'])
    else:
        return "Error: Existem dados faltantes. Você deve especificar o ano e de que dia a que dia quer obter os dados. Ex: /rsn?ano=2019&dia_i=1&dia_f=10"
    
    resultados = []
    for pf in retornaPhotonFlux(ano, dia_i, dia_f):
        resultados.append(pf)
    
    return jsonify(resultados)


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)


