import os
import fitz
from datetime import datetime
import re
import requests
import json
import re


def sort(lst,grant,contract, priority):
    if lst == []:
        return [],[0,0,0,0,0,0,0,0]


    for i in range(len(lst)):
        for j in range(i+1,len(lst)):
            if int(lst[i][-1])<int(lst[j][-1]):
                lst[i],lst[j] = lst[j],lst[i]
                
            if int(lst[i][-1])==int(lst[j][-1]) and priority!=-1:
                if lst[i][0][priority]<lst[j][0][priority]:
                    lst[i],lst[j] = lst[j],lst[i]
                else:
                    if lst[i][0][0][0]>lst[j][0][0][0]:
                        lst[i],lst[j] = lst[j],lst[i]


    grant_min = int(lst[grant-1][-1])
    grant_max = int(lst[0][-1])
    grant_avg = 0

    contract_max = int(lst[grant][-1])
    contract_min = int(lst[contract-1][-1])
    contract_avg = 0
    
    for i in range(len(lst)):
        if i<grant: grant_avg = grant_avg + int(lst[i][-1])
        if i>grant and i<contract: contract_avg = contract_avg + int(lst[i][-1])


    stats=[len(lst),grant_max,grant_min,float(grant_avg)/grant,contract_max,contract_min,float(contract_avg)/(contract-grant)]
    return lst,stats

def get_data(predmet, label, grant, contract):
    flist = os.listdir()
    file = ""
    tmp_name = ""
    
    for x in flist:
        if "PDF" or "pdf" in x:
            if predmet in x and not "МАГИСТР" in x:
                file = x
                tmp_name = label+"_res"
                array = []
                
                f = open(tmp_name + ".txt","w",encoding="utf-8")
                with fitz.open(file) as doc:
                    text = ""
                    for page in doc:
                        d = page.getText().split("\n")
                        for x in range(len(d)):
                            if ("." in d[x] and d[x].strip()[:-1].isnumeric()):
                                f.write('\n')
                            else:
                                if (x>0 and d[x-1].strip().isnumeric()):
                                   f.write('\n')
                               
                            f.write(d[x])

                f.close()
                
                #########################
                tmp_var = []
                i = 0
                dt = ""
                
                f = open(tmp_name + ".txt","r",encoding="utf-8")
                for line in f:
                    if i == 0:
                       match = re.search(r'\d{2}.\d{2}.\d{4}', line)
                       dt = datetime.strptime(match.group(), '%d.%m.%Y').date()
                    
                    if i>0 and len(line.strip())>0:
                        d = line.strip().split(" ")
                        if len(d)==1 and d[0].isnumeric():
                            tmp_var = d
                            continue

                        if tmp_var!=[]:
                            array.append(tmp_var+d)
                            tmp_var = []
                        else:
                            array.append(d)
                           
                    i=i+1      
        
                f.close()
                array,stats = sort(array, grant, contract, -1)
                
                ##########################

                f = open(tmp_name + ".txt","w",encoding="utf-8")
                cmt = ['Количество','Макс. оценка грант','Мин. оценка грант','Средняя оценка грант','Макс. оценка контракт','Мин. оценка контракт','Средняя оценка контракт']
                for i in range(7):
                    f.write(cmt[i]+" : "+str(stats[i])+"\n")

                f.write("\n")
                
                for i in range(len(array)):
                    array[i] = array[i][1:]
                    s = " ".join(array[i])

                    if len(s)<30:
                        for p in range(30-len(s)):
                            s = s + " "
                            
                    f.write(str(i+1)+"."+ s + "\n")
                    if i==grant-1 or i==contract-1:
                        f.write("\n")
                f.close()
                return array,dt

    return [],-1

def get_general(a_m,a_r,a_b,a_rs,a_l,profile,grant,contract):
    all_stats = []
    for i in range(len(a_r)):
        name_r = " ".join(a_r[i][:-1])
        stat = []
        stat.append([name_r,int(a_r[i][-1]),-1,-1, -1,-1]) #фио русский математика биология рисо филология
        
        for j in range(len(a_m)):
            name_m = " ".join(a_m[j][:-1])
            if name_r.strip() == name_m.strip():
                stat[0][2] = int(a_m[j][-1])
                break

        for k in range(len(a_b)):
            name_b = " ".join(a_b[k][:-1])
            if name_r.strip() == name_b.strip():
                stat[0][3] = int(a_b[k][-1])
                break

        for k in range(len(a_rs)):
            name_rs = " ".join(a_rs[k][:-1])
            if name_r.strip() == name_rs.strip():
                stat[0][4] = int(a_rs[k][-1])
                break

        for k in range(len(a_l)):
            name_l = " ".join(a_l[k][:-1])
            if name_r.strip() == name_l.strip():
                stat[0][5] = int(a_l[k][-1])
                break

        all_stats.append(stat)

    if profile=="ПМиИ":
        pivot_index = 2
        msg = "Математ."
        
    if profile=="Биология":
        pivot_index = 3
        msg = "Биолог."
        
    if profile=="РЕКЛАМА И СВЯЗИ С ОБЩЕСТВЕННОСТЬЮ":
        pivot_index = 4
        msg = "Обществ."
        
    if profile=="ФИЛОЛОГИЯ":
        pivot_index = 5
        msg = "Литерат."

    data_list = []
    for i in range(len(all_stats)):
        if all_stats[i][0][pivot_index]!=-1:
            res = int(all_stats[i][0][1])+int(all_stats[i][0][pivot_index])
            all_stats[i].append(res)
            data_list.append(all_stats[i])

    array,stats = sort(data_list,grant,contract,pivot_index)
   
    f = open(profile+".txt","w",encoding="utf-8")
    cmt = ['Количество','Макс. оценка грант','Мин. оценка грант','Средняя оценка грант','Макс. оценка контракт','Мин. оценка контракт','Средняя оценка контракт']
    for i in range(7):
        f.write(cmt[i]+" : "+str(stats[i])+"\n")

    f.write("\n")

    t = "Ф-т.\t" + msg + "Рус.\tОбщий балл\n"
    f.write("№ "+"%-37s"%"ФИО"+"%-20s"%t)

    for i in range(len(array)):
        mode = ""
        for k in range(2,6):
            if array[i][0][k]!=-1:
                if k==2: mode=mode+"М"
                if k==3: mode=mode+"П"
                if k==4: mode=mode+"Р"
                if k==5: mode=mode+"Ф"

        if len(array[i][0][0])<30:
            for p in range(30-len(array[i][0][0])):
                array[i][0][0] = array[i][0][0] + " "

        s = str(i+1)+"."+str(array[i][0][0])+"\t"+mode+"\t"+str(array[i][0][pivot_index])+"\t"+str(array[i][0][1])+"\t"+str(array[i][1])+"\n"
        f.write(s)
            
        if i==grant-1 or i==contract-1: f.write("\n")
        
    f.close()

                

def main():
    url='https://msu.dvaoblaka.ru/api/tags/%D0%9D%D0%BE%D0%B2%D0%BE%D1%81%D1%82%D0%B8/articles?page=24'
    r = requests.get(url).json()
    title_lst = []
    for serial,article in enumerate(r):
        if "Результаты" in article['title']:
            urls = re.findall("href=[\"\'](.*?)[\"\']", article['text'])
            title = urls[0].split("/")[-1]
            title = title.replace("%20","_")
            r = requests.get(urls[0], allow_redirects=True)
            open(title, 'wb').write(r.content)
            title_lst.append(title)


    a1,d1 = get_data("МАТЕМАТИКА","math",24,60)
    a21,d21 = get_data("РУССКИЙ_ЯЗЫК","rus_(MATH_AND_PSY)",24,60)
    a22,d22 = get_data("РУССКИЙ_ЯЗЫК","rus_(RISO_AND_FILOLOGIYA)",20,50)

    #if d21!=d22: #если по двум ведомостям
        #for i in range(len(a22)):
            #a21.append(a22[i])

    a3,d3 = get_data("БИОЛОГИЯ","bio",24,60)
    a4,d4 = get_data("ОБЩЕСТВОЗНАНИЕ","soc",20,50)
    a5,d5 = get_data("ЛИТЕРАТУРА","lit",20,50)

    get_general(a1,a21,a3,a4,a5,"ПМиИ",24,60)
    get_general(a1,a21,a3,a4,a5,"Биология",24,60)
    get_general(a1,a22,a3,a4,a5,"РЕКЛАМА И СВЯЗИ С ОБЩЕСТВЕННОСТЬЮ",20,50)
    get_general(a1,a22,a3,a4,a5,"ФИЛОЛОГИЯ",20,50)

main()
