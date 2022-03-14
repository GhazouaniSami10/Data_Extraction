import pandas as pd
import json
import pdfplumber as pdfp
with pdfp.open('Factures/03.02.2022.pdf') as pdf:
    global text
    for page in pdf.pages:
        text = page.extract_text()
        file_object = open('texte.txt', 'a')
        file_object.write(text)
        file_object.close()

df = open("texte.txt")
read = df.read()
df.seek(0)
arr = []
line = 1
for word in text:
    if word == '\n':
        line += 1

labels = ["Numéro de note","Numéro doc",
          "Adresse de livraison","Adresse de facturation",
          "N° de commande","Votre compte chez nous","Numéro TVA du client",
          "VNo. bon d'achat","Contact  client","Pers.  contact  TD-  Sales",
          "Pers.  contact  TD-  Finance","Total H.T.","Taux - Base de calcul","NET A PAYER",
          "Mode d'expédition:","Mode de règlement:","Date d'échéance","N° TVA Tech Data:"]
list = []
for word in labels:
    for i in range(line):
        arr.append(str(df.readline()))
    def findline(word):
        for i in range(len(arr)):
            if word in arr[i] and 0 < i < 59: 
                #print( word, i+1)  
                list.append(i+1)        
        return list
    words = findline(word)

a = read.split('\n')[words[0]]
Numéro_de_note = a[0:10]
Date = a[11:21]
Numéro_doc = a[22:30]
Adresse_de_livraison = read.split('\n')[words[3]+1]
Adresse_de_facturation=read.split('\n')[words[3]+2]
b=read.split('\n')[words[4]]
Votre_compte_chez_nous=b[23:29]
Contact_client=b[45:68]
c = read.split('\n')[words[5]]
num_tva_client=c[21:34]
contact_td_sales=c[59:72]
d= read.split('\n')[words[6]].replace('\t', '/').split("/ ")[1]
num_voucher=d[5:]
contact_td_finance=read.split('\n')[words[6]].replace('\t', '/').split("Finance ")[1]
e=read.split('\n')[words[4]-1].replace('\t', '/ ').split("/ ")[1]
num_commande=e[5:]
f=read.split('\n')[words[4]-1].replace('\t', '/ Date').split("N° de livraison")[0]
date_commande=f[35:]
Total_HT=read.split('\n')[words[8]-1].replace('\t', '').split("Total H.T. ")[1]
Bases_TVA=read.split('\n')[words[8]].replace('\t', '').split("Bases T.V.A. ")[1]
j=read.split('\n')[words[8]+1].replace('\t', '').split("Taux - Base de calcul - montant T.V.A. ")[1]
Taux=j[:7]
k=read.split('\n')[words[8]+1].replace('\t', '').split(" % ")[1]
Base_de_calcul=k[:10]
Montant_TVA=read.split('\n')[words[8]+1].replace('\t', '').split("EUR ")[1]
NET_A_PAYER=read.split('\n')[words[9]].replace('\t', '').split("NET A PAYER ")[1]
Mode_d_expédition=read.split('\n')[words[11]-1].replace('\t', '').split("Mode d'expédition: ")[1]
Mode_de_règlement=read.split('\n')[words[11]].replace('\t', '').split("Mode de règlement: ")[1]
Date_d_échéance=read.split('\n')[words[12]].replace('\t', '').split("Date d'échéance: ")[1]
num_tva_tech_data=read.split('\n')[words[13]].replace('\t', '').split("N° TVA Tech Data: ")[1]

lst = [[Date, Numéro_de_note, Numéro_doc, Adresse_de_livraison, Adresse_de_facturation,
Votre_compte_chez_nous, Contact_client, num_tva_client, contact_td_sales, num_voucher,
contact_td_finance, num_commande, date_commande, Total_HT, Bases_TVA, Base_de_calcul,
Montant_TVA, NET_A_PAYER, Mode_d_expédition, Mode_de_règlement, Date_d_échéance, num_tva_tech_data]]
dataframe = pd.DataFrame(lst, columns =['Date',
                                     'Invoice',
                                     'Amount_Currency',
                                     'Numéro_doc.',
                                     'Adresse_de_livraison',
                                     'Adresse_de_facturation',
                                     'Votre_compte_chez_nous',
                                     'Contact_client',
                                     'num_tva_client',
                                     'contact_td_sales',
                                     'num_voucher',
                                     'contact_td_finance',
                                     'num_commande',
                                     'date_commande',
                                     'Total_HT',
                                     'Bases_TVA',
                                     'Base_de_calcul',
                                     'Montant_TVA',
                                     'Mode_d_expédition',
                                     'Mode_de_règlement',
                                     'Date_d_échéance',
                                     'num_tva_tech_data'], dtype = int)
print(dataframe)
dataframe.to_csv("data.csv",index=False)
dataframe.to_json("data.json",orient="split")

