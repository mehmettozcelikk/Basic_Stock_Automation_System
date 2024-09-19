import requests
import re
import time
from bs4 import BeautifulSoup

##programın genel hatları bitti. Veri kazımalar yapılacak. ilk önce select1 in verisi kazınacak ->83.videoda 48.dakika da kaldım.

class Stock:
    def __init__(self):
        self.loop = True

    def program(self):
        select = self.menü()

        if select == "1":
            print("Güncel fiyat bilgileri alınıyor..\n")
            time.sleep(2)
            self.currentPrice()
        if select == "2":
            print("Şirket künye bilgileri alınıyor..\n")
            time.sleep(2)
            self.companyIdentity()
        if select == "3":
            print("Cari değer bilgileri alınıyor..\n")
            time.sleep(2)
            self.currentValues()
        if select == "4":
            print("Getiri bilgileri alınıyor..\n")
            time.sleep(2)
            self.returns()
        if select == "5":
            print("Dahil olduğu endekslerdeki ağırlık bilgileri alınıyor...\n")
            time.sleep(2)
            self.includedIndicesRate()
        if select == "6":
            print("Otomasyondan çıkış yapılıyor...\n")
            time.sleep(2)
            self.quit()
        
    def menü(self):
        def selectControl(select):
            if re.search("[^1-6]",select):
                raise Exception("Hatalı karakter girdiniz!!!")
            if len(select)!= 1:
                raise Exception("Hatalı karakter girdiniz!!!")
        
        print("***X Otomasyon Sistemine Hoşgeldiniz***\n\n[1]-Hisse Fiyat Bilgileri\n[2]-Şirket Künye Bilgileri\n[3]-Cari Değer Bilgileri\n[4]-Getiri Bilgileri\n[5]-Dahil Olduğu Endekslerdeki Ağırlık Bilgileri\n[6]-Çıkış Yap\n\n")

        while True:
            try:
                select = input("Lütfen yapmak istediğiniz işlemi seçiniz:")
                selectControl(select)
            except Exception as selectError:
                print(selectError)
                time.sleep(2)
            else:
                break
        return select


    def currentPrice(self):#güncel hisse fiyatlar
        while True:
            try:
                company = input("Hisse ismini giriniz:")

                url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/default.aspx"

                parser = BeautifulSoup(requests.get(url).content,"html.parser")
                
                data = parser.find("a",{"href":"/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(company.upper())}).parent.parent.find_all("td")

                name = data[0].a.string
                price = data[1].string
                changePercentage = data[2].span.string
                changeTL = data[3].string
                volumeTL = data[4].string
                volumePiece = data[5].string

                print("\n****{} Hisse Bilgileri****\n".format(name.strip().upper()))

                print(f"Fiyat:{price}\nDeğişim:%{changePercentage.strip()}\nDeğişim:{changeTL} TL\nHacim:{volumeTL} TL\nHacim:{volumePiece} Adet")
            except AttributeError:
                print("Hatalı hisse adı girdiniz!!")
                time.sleep(2)
            else:
                break
        time.sleep(2)
        self.returnMenü()

    def companyIdentity(self):#şirket künyesi
        while True:
            try:
                company = input("Hisse ismini giriniz:")

                url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(company)

                parser = BeautifulSoup(requests.get(url).content,"html.parser")

                data = parser.find("div",{"id":"ctl00_ctl58_g_6618a196_7edb_4964_a018_a88cc6875488"}).find_all("tr")

                print("\n****{} Hisse Künyesi****\n".format(company.strip().upper()))

                for i in data:
                    title = i.find("th").string
                    statement = i.find("td").string
                    print(f"{title}: {statement}")
            except AttributeError:
                print("Hatalı hisse adı girdiniz!!")
                time.sleep(2)
            else:
                break
        time.sleep(2)
        self.returnMenü()


    def currentValues(self):#cari değerler
        while True:
            try:
                company = input("Hisse ismini giriniz:")

                url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(company)

                parser = BeautifulSoup(requests.get(url).content,"html.parser")

                data = parser.find("div",{"id":"ctl00_ctl58_g_76ae4504_9743_4791_98df_dce2ca95cc0d"}).find_all("tr")

                for i in data:
                    title = i.th.string
                    statement = i.td.string 
                    print(f"{title}: {statement}")
            except AttributeError:
                print("Hatalı hisse adı girdiniz!!")
                time.sleep()
            else:
                break
        time.sleep(2)
        self.returnMenü()


    def returns(self):#getiriler
        while True:
            try:
                company = input("Hisse ismini giriniz:")

                url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(company)

                parser = BeautifulSoup(requests.get(url).content,"html.parser")

                data = parser.find("div",{"id":"ctl00_ctl58_g_aa8fd74f_f3b0_41b2_9767_ea6f3a837982"}).find("tbody").find_all("tr")

                for i in data:
                    data2 = i.find_all("td")
                    print(f"Birim:{data2[0].string} Günlük:{data2[1].string} Haftalık:{data2[2].string} Aylık:{data2[3].string} Yıllık:{data2[4].string}")
            except AttributeError:
                print("Hatalı hisse adı girdiniz!!")
                time.sleep(2)
            else:
                break
        time.sleep(2)
        self.returnMenü()
    
    def includedIndicesRate(self):#Dahil Olduğu Endekslerdeki Ağırlığı
        while True:
            try:
                company = input("Hisse ismini giriniz:")

                url = "https://www.isyatirim.com.tr/tr-tr/analiz/hisse/Sayfalar/sirket-karti.aspx?hisse={}".format(company)

                parser = BeautifulSoup(requests.get(url).content,"html.parser")

                dataTitle = parser.find("div",{"id":"ctl00_ctl58_g_655a851d_3b9f_45b0_a2d4_b287d18715c9"}).find("table").find_all("th")
                
                dataStatement = parser.find("div",{"id":"ctl00_ctl58_g_655a851d_3b9f_45b0_a2d4_b287d18715c9"}).find("table").find_all("td")

                for i in range(0,3):
                    title = dataTitle[i].string
                    statement = dataStatement[i].string
                    print(f"{title}:{statement}")
            except AttributeError:
                print("Hatalı hisse adı girdiniz!!")
                time.sleep(2)
            else:
                break
        time.sleep(2)
        self.returnMenü()

    def quit(self):
        self.loop = False
        exit()

    def returnMenü(self):
        while True:
            select = input("Ana menüye dönmek için 8'i, çıkış yapmak için 9'u giriniz:")

            if select == "8":
                print("Ana menüye dönülüyor..\n")
                time.sleep(2)
                self.program()
                break
            elif select == "9":
                print("Otomasyondan çıkış yapılıyor..\nİyi günler")
                time.sleep(2)
                self.quit()
                break
            else:
                print("Hatalı karakter girdiniz!!!")
                time.sleep(2)
                
system = Stock()

while system.loop:
    system.program()