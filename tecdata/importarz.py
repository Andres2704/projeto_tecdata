import urllib.request, os

#url = 'ftp://cddis.nasa.gov/gnss/products/ionex/2019/002/igsg0020.19i.Z'
#urllib.request.urlretrieve(url, 'igsg0020.19i.Z')

class importtec():
    def __init__(self, ano_inicial, ano_final):
        self.anoi = ano_inicial
        self.anof = ano_final

    def importar(self):
        for ano in range(self.anoi, self.anof+1):
            if not os.path.exists('tecdata/20'+str(ano)):
                os.makedirs('tecdata/20'+str(ano))
            for i in range(65, 366):
                if i < 10:
                    number_file = "00" + str(i)
                elif (i > 9) and (i < 100):
                    number_file = "0" + str(i)
                else:
                    number_file = str(i)
                filename = 'igsg' + str(number_file) + '0.' + str(ano) + 'i.Z'
                pathname = 'tecdata/20' + str(ano) + '/' + filename
                url = 'ftp://cddis.nasa.gov/gnss/products/ionex/20' + str(ano) + '/' + str(number_file) + '/' + filename
                print(url)
                urllib.request.urlretrieve(url, pathname)
                
#Ao final do processo você deve extrair os arquivos .Z manualmente.
