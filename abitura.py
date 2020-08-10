def read(lst,filename):
    f=open(filename+".txt","r",encoding="utf-8")
    t=[]
    for line in f:
        t=line.split('  ')
        t[-1]=t[-1].strip()
        lst.append(t)

    f.close()
    return lst

def write_result(mode,error_l,happy):
    f=open("result_"+mode+"_2020.txt","w",encoding="utf-8")
    if len(error_l)>0:
        f.write(str(error_l)+"\n\n")

    if mode=="bio":
        name="Биол."

    if mode=="math":
        name="Матем."
        
    f.write('№'+'\t'+'ФИО'+'\t'+'Факультеты'+'\t'+'Общий балл'+'\t'+name+'\t'+'Русс.яз \n')
    
    for i in range(len(happy)):
        f.write(str(i+1)+"\t"+happy[i][0]+"\t"+happy[i][4]+"\t"+str(happy[i][1])+'\t'+str(happy[i][2])+"\t"+str(happy[i][3])+"\n")
        if i==19 or i==49:
            f.write('\n')

    f.close()

def write():
    arr_bio=[]
    arr_math=[]
    error_b=[]
    error_m=[]
    happy_bio=[]
    happy_math=[]
    rus=[]
    fac=""

    arr_bio=read(arr_bio,"bio") ## считываем всех сдававших биологию. положили в массив
    arr_math=read(arr_math,"math")
    rus=read(rus,"rus") ## считываем всех сдававших русский. положили в массив
    id_b=-1
    id_m=-1

    for i in range(len(rus)):
        for j in range(len(arr_bio)):
            if rus[i][1]==arr_bio[j][1]: ##если нашли совпадение фамилий в обоих массивах
                fac=fac+"П"
                id_b=j
                break

        for k in range(len(arr_math)):
            if rus[i][1]==arr_math[k][1]: ##если нашли совпадение фамилий в обоих массивах
                fac=fac+"М"
                id_m=k
                break


        if (id_b!=-1 and id_m!=-1):
                 try:
                    happy_bio.append([rus[i][1],int(rus[i][2])+int(arr_bio[id_b][2]),int(arr_bio[id_b][2]),int(rus[i][2]),fac])
                    happy_math.append([rus[i][1],int(rus[i][2])+int(arr_math[id_m][2]),int(arr_math[id_m][2]),int(rus[i][2]),fac])
                 except:
                    error_b.append([arr_bio[id_b],arr_math[id_m],rus[i]]) ## если произошла ошибка, то кладем в отдельный массив

        if (id_b==-1 and id_m!=-1):
                 try:
                     happy_math.append([rus[i][1],int(rus[i][2])+int(arr_math[id_m][2]),int(arr_math[id_m][2]),int(rus[i][2]),fac])
                 except:
                    error_m.append([arr_math[id_m],rus[i]]) ## если произошла ошибка, то кладем в отдельный массив

        if (id_b!=-1 and id_m==-1):
                 try:
                    happy_bio.append([rus[i][1],int(rus[i][2])+int(arr_bio[id_b][2]),int(arr_bio[id_b][2]),int(rus[i][2]),fac])
                 except:
                    error_b.append([arr_bio[id_b],rus[i]]) ## если произошла ошибка, то кладем в отдельный массив

        id_b=-1
        id_m=-1
        fac=""

    happy_bio.sort(key=lambda t: (t[1], t[2])) ##сортируем по двум параметрам
    happy_bio.reverse()

    happy_math.sort(key=lambda t: (t[1], t[2])) ##сортируем по двум параметрам
    happy_math.reverse() 

    write_result("bio",error_b,happy_bio)
    write_result("math",error_m,happy_math)


write()
