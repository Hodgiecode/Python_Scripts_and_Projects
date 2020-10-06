class simplex:
    def __init__(self):
        self.M=20
        self.N=20
        self.epsilon=1e-8
        self.result_string=""
        self.counter=0

    def convert_to_min(self,mat):
        t=[]
        l2=[]
        for i in range(1,len(mat)):
            t.append(mat[i][-1])

        for i in range(len(mat[0])):
            row =[]
            for item in mat:
                row.append(item[i])

            l2.append(row)

        for i in range(len(l2)):
            l2[i]=l2[i][1:]+[l2[i][0]]

        mat=[t]+l2
        return mat

    def equal(self,a,b):
        return abs(a-b)<self.epsilon

    def print_tableau(self,m,n,mat,mes,mode):
        str_="\n"
        self.counter=self.counter+1
        counter2=self.counter
        str_=str_+str(counter2)+'.'+mes+'\n'
        str_=str_+"col: b[i]"
        
        for j in range(n):
            str_=str_+" x"+str(j+1)

        str_=str_+"\n"

        for i in range(m):
            if i==0:
                str_=str_+"max:"
            else:
                str_=str_+"b"+str(i)

            for j in range(n):
                str_=str_+" "+str('{:.2f}'.format(mat[i][j]))

            str_=str_+"\n"

        return str_

    def pivot_on(self,m,n,mat,row,col):
        pivot=mat[row][col]

        for j in range(n):
            mat[row][j]=mat[row][j]/pivot

        for i in range(m):
            multiplier=mat[i][col]
            if i==row:
                continue

            for  j in range(n):
                mat[i][j]=mat[i][j]-multiplier*mat[row][j]

    def find_pivot_column(self,m,n,mat):
        pivot_col=1
        lowest=mat[0][pivot_col]

        for j in range(1,n):
            if mat[0][j]<lowest:
                lowest=mat[0][j]
                pivot_col=j

        self.result_string=self.result_string+"Most negative column in row[0] is col "+str(pivot_col)+"="+str(lowest);

        if lowest>=0:
            return -1

        return pivot_col

    def find_pivot_row(self,m,n,mat,pivot_col):
        pivot_row=0
        min_ratio=-1
        self.result_str=self.result_string+"Ratios A[row_i,0]/A[row_i,%d] = ["+str(pivot_col)+"]";
        
        for i in range(1,m):
            if abs(mat[i][pivot_col])>self.epsilon:
                ratio=mat[i][0]/mat[i][pivot_col]
                self.result_str=self.result_string+str(ratio)+" ";
            else:
                ratio=-1

            if ((ratio>0 and ratio<min_ratio) or min_ratio<0):
                min_ratio=ratio
                pivot_row=i

        self.result_string=self.result_string+"\n"
        
        if min_ratio==-1:
            return -1

        self.result_str=self.result_string+"Found pivot A["+str(pivot_row)+","+str(pivot_col)+"], min positive ratio="+str(min_ratio)+" in row="+str(pivot_row)+".\n"
        return pivot_row


    def add_slack_variables(self,m,n,mat):
        for i in range(m):
            temp=[]
            for j in range(n-len(mat)):
                if i==j+1:
                    temp.append(1)
                else:
                    temp.append(0)

            mat[i]=mat[i]+temp

        return mat
        
    def check_b_positive(self,m,n,mat):
        flag=0
        for i in range(1,m):
            if mat[i][0]>=0:
              flag=1

        return bool(flag)

    def find_basis_variable(self,m,n,mat,col):
        xi=-1
        for i in range(len(mat)):
            if self.equal(mat[i][col],1):
                if xi==-1:
                    xi=i
                else:
                    return -1

            else:
                if (not self.equal(mat[i][col],0)):
                    return -1

        return xi

    def print_optimal_vector(self,m,n,mat,str1):
         str1=str1+" at ";

         for j in range(1,n):
            xi = self.find_basis_variable(m,n,mat,j);
            if (xi != -1):
                str1=str1+"x"+str(j)+"="+str(mat[xi][0])+", ";
            else:
                str1=str1+"x"+str(j)+"=0, ";
 
         self.result_string=self.result_string+str1+"\n";
     

    def simplex(self,m,n,mat,mode):
        s=""
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if j<len(mat[i])-1 or i==0:
                    if mat[i][j]>0 and j>0:
                        s=s+"+"+str('{:.2f}'.format(mat[i][j]))+"x_"+str(j+1)
                    else:
                        s=s+str('{:.2f}'.format(mat[i][j]))+"x_"+str(j+1)
                        
                if j==len(mat[i])-1 and i>0:
                    a="=>" if mode==1 else "<="
                    s=s+a+str('{:.2f}'.format(mat[i][j]))

            if i==0:
                a="min" if mode==1 else "max"
                s=s+"->"+a+"\n"

            s=s+"\n"
        
        self.result_string=self.result_string+s
        
        self.result_string=self.result_string+self.print_tableau(m,n,mat,"Initial",mode)
        if mode==1:
            mat=self.convert_to_min(mat)
            self.result_string=self.result_string+self.print_tableau(m,n,mat,"After convertion minimization problem to maximization problem",mode)
            a=m
            m=n
            n=a
           
        for i in range(len(mat)):
            if i==0:
                for k in range(len(mat[i])):
                    mat[i][k]=mat[i][k]*(-1)
                    
                mat[0]=[0]+mat[0]
            else:
                mat[i]=[mat[i][-1]]+mat[i][:-1]

        loop=0
        initial_n=n
        initial_m=m
        n=n+m+1
        m=m+1
     
        mat=self.add_slack_variables(m,n,mat)
      
        '''Проверить b на положительность'''
        if self.check_b_positive(m,n,mat)==False:
            self.result_string="Check b positive is false"
            return self.result_string

        self.result_string=self.result_string+self.print_tableau(m,n,mat,"Padded with slack variables",mode)

        while(True):
            pivot_col=0
            pivot_row=0
            pivot_col=self.find_pivot_column(m,n,mat)

            if pivot_col<0:
                if (mode==0):
                    self.result_string=self.result_string+"\nFound optimal value=A[0,0]="+str(mat[0][0])+"(no negatives in row 0).\n";
                    self.print_optimal_vector(m,n,mat,"Optimal vector");
                    
                break

            pivot_row=self.find_pivot_row(m,n,mat,pivot_col)
            
            if pivot_row <0:
                break

            self.result_string=self.result_string+"Leaving variable x"+str(pivot_row)+", so pivot_row="+str(pivot_row)+"\n";
            self.pivot_on(m,n,mat,pivot_row,pivot_col)

            if mode==0:
                 self.print_optimal_vector(m,n,mat,"Basic feasible solution");

            self.result_string=self.result_string+self.print_tableau(m,n,mat,"After pivoting",mode)

            if loop>40:
                return -1
                break

            loop=loop+1

        if mode==1:
            k=1
            opt=0
            str_lst=[]
            str1=""

            for x in range(initial_n+1,initial_n+initial_m+1):
                str1=str1+"\nx_"+str(k)+":"+str(mat[0][x])
                k=k+1
        
        if mode==1:
             self.result_string=self.result_string+str1+"\nMin:"+str(mat[0][0])


        return self.result_string


def main_simplex(str1):
    ##theory https://college.cengage.com/mathematics/larson/elementary_linear/4e/shared/downloads/c09s4.pdf
    ##ex. max 0.5 3 1 4,1 1 1 1 40,-2 -1 1 1 10,0 1 0 -1 10"

    mode=0
    mat=[]
    if "max" in str1:
        mode=0
        
    if "min" in str1:
        mode=1

    a=str1.split(",")
    a[0]=a[0].replace("max","").replace("min","")
    for m in range(len(a)):
        b=a[m].split()
        t=[]
        for i in range(len(b)):
            if b[i]!="":
                t.append(float(b[i]))

        mat.append(t)

    n=len(mat[0])
    m=len(mat)-1

    A=simplex()
    s=A.simplex(m,n,mat,mode)
    print(s)
    
    
str1="max 0.5 3 1 4,1 1 1 1 40,-2 -1 1 1 10,0 1 0 -1 10"
#str1="min 0.12 0.15,60 60 300,12 6 36,10 30 90"
#str1="min 3 2, 2 1 6,1 1 4"
str1="min 2 10 8, 1 1 1 6, 0 1 2 8, -1 2 2 4"
#str1="max 1 2, 1 -3 1,-1 2 4" ##error_test
#str1="max 1 3, -1 1 20,-2 1 50" ##error_test
#str1="max 2 7 6 4,1 1 0.83 0.5 65,1.2 1 1 1.2 96,0.5 0.7 1.2 0.4 80"
#str1="max 2.5 1,3 5 15,5 2 10"
main_simplex(str1)

