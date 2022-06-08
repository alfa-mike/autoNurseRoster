from os import rename
import sys
import time
import json
import operator

sys.setrecursionlimit(10**6)

t1 = time.time()
bestSol = -1
Ass = {}
holder = {}

csvfile = open(sys.argv[1])
number_inp = len(csvfile.readline().split(","))
#print(number_inp)

def f(e):
    return e.strip()
inp = list(map(f,csvfile.readline().split(',')))

Q = -1    # que number
N,D,m,a,e,S,T=0,0,0,0,0,0,0
if number_inp==5:
    Q=1
    N,D,m,a,e = list(map(int,inp))
else:
    Q=2
    N,D,m,a,e,S,T= list(map(int,inp))

VARIABLES = []              #Vij = val(slot) of Nurse i in Day j
for i in range(N):
    for j in range(D):
        s = "V_"+str(i)+"_"+str(j)
        VARIABLES.append(s)

DOMAIN = {}


for v in VARIABLES:
    DOMAIN[v]=["R","M","A","E"]


def rec_backtrack():
    global Ass
    if complete(Ass):
        return Ass

    unass_var = select_UV(Ass)
    #print(unass_var)
    var_todel = ""
    val_todel = "" 
    for val in select_VAL(unass_var,Ass):
        if consistent(val,unass_var,Ass):
            Ass[unass_var] = val
            if val=="M" or val=="E":
                var_todel,val_todel = delete(unass_var)

            #print(ass)
            result = rec_backtrack()
        
            if result!=None:
                return result
            if var_todel!="" and val_todel!="":
                DOMAIN[var_todel].append(val_todel)
            del Ass[unass_var] 

    return None


def rec_backtrack2(count):
    global Ass,holder, bestSol
    
    if (time.time()-t1) >= (T-1):
        return 
    
    if complete(Ass):
        
        #holder,count = optimize(Ass)
        if count > bestSol:
            
            bestSol = count
            holder = format(Ass)
            
            #dumpans(holder)

        return   

    unass_var = select_UV(Ass)
    
    var_todel = ""
    val_todel = "" 
    
    for val in select_VAL2(unass_var,Ass):
        if consistent(val,unass_var,Ass):
            Ass[unass_var] = val
            if val=="M" or val=="E":
                var_todel,val_todel = delete(unass_var)
            if checkSoft(unass_var):                      #check if nurse is spcial or not
                count+=1
            
            rec_backtrack2(count)
            if var_todel!="" and val_todel!="":
                DOMAIN[var_todel].append(val_todel)
            del Ass[unass_var] 
    return 


def delete(var):
    _, i, j = var.split("_")
    j = str(int(j)+1)
    if int(j)==D:
        return "",""
    var_todel = "V_"+i+"_"+j
    val_todel = "M"
    if val_todel in DOMAIN[var_todel]:
        DOMAIN[var_todel].remove(val_todel)
    return var_todel,val_todel 


def dumpans(d):
    with open("solution.json" , 'w') as file:
        json.dump(d,file)
        file.write("\n")
    return


def checkSoft(var):
    _,i,j=var.split('_')
    if int(i)<S:
        return True
    return False


def complete(ass):
    if len(ass)==N*D:
        return True 
    return False

def select_UV(ass):
    p = float('inf')
    var = ""
    luv = []
    for v in VARIABLES:
        if v not in ass:
            luv.append(v)
            _, _, j = v.split('_')
            j = int(j)
            if j<p:
               p=j 
               var = v
    return var


def select_VAL(var,ass):
    flag = 0
    _, index, j= var.split('_')
    index = int(index)
    j = int(j)
    week_no = (j//7)
    bound = j%7
    strt = index*D + 7*week_no 
    end = strt+7
    if end>bound:
        end = strt+bound
    for i in range(strt,end):
        if VARIABLES[i] in ass: 
            if ass[VARIABLES[i]]=="R":
                flag=1
                break
    domain = []
    for ele in DOMAIN[var]:
        if ele!="R":
            domain.append(ele)
    if flag==1:
        domain.append("R")
    else:
        domain = ["R"]+domain
        
    #print(domain) 
    return domain


def select_VAL2(var,ass):
    flag = 0
    _, index, j= var.split('_')
    index = int(index)
    j = int(j)
    week_no = (j//7)
    bound = j%7
    strt = index*D + 7*week_no 
    end = strt+7
    if end>bound:
        end = strt+bound
    for i in range(strt,end):
        if VARIABLES[i] in ass: 
            if ass[VARIABLES[i]]=="R":
                flag=1
                break
    domain = []
    for ele in DOMAIN[var]:
        if ele!="R":
            domain.append(ele)
    
    if index<S:
        if flag==1:
            if "M" in DOMAIN[var]:
                return ["M","E","A","R"]
            else:
                return ["E","A","R"]
        else:
            if "M" in DOMAIN[var]:
                return ["M","E","R","A"]
            else:
                return ["E","R","A"]

    if flag==1:
        domain.append("R")
    else:
        domain = ["R"]+domain
        
    #print(domain)
    return domain

    
def consistent(val, var, ass):
    # C3 - exactly m ,a,e nurses in a day 
            
    _,idx,j = var.split("_")
    tempv = "V_"+idx+"_"+str(int(j)-1)
    if tempv in ass and (ass[tempv]=="M" or ass[tempv]=="E" ) and val == "M":
        return False
    cnt = 0
    for i in range(N):
        v = "V_"+str(i)+"_"+j
        if v in ass:
            if ass[v]==val:
                cnt+=1

    if val=="M" and cnt>m-1:
        return False
    if val=="A" and cnt>a-1:
        return False
    if val=="E" and cnt>e-1:
        return False
    if val=='R' and cnt>N-(m+a+e)-1:
        return False

    
    # C4 - check for no R in a week for each nurse
    no_day = int(j)
    if no_day!=0 and no_day%6==0:
        cnt_r=0
        week_no = (int(j)//7)
        strt = int(idx)*D + 7*week_no 
        for i in range(strt,strt+7):
            if VARIABLES[i] in ass: 
                if ass[VARIABLES[i]]=="R":
                    cnt_r+=1
        if cnt_r==0:
            return False
    return True


def format(ass):
    if len(ass)==0:
        return {}
    ans = {}
    for j in range(D):
        for i in range(N):
            v = "V_"+str(i)+"_"+str(j)
            s = "N"+str(i)+"_"+str(j)
            ans[s] = ass[v]
    
    return ans

def cnt(s):
    n = 0
    for e in s:
        if e=="M" or e=="E":
            n+=1
    return n

def decode(l):
    dic = {}
    for j in range(D):
        for i in range(N):
            k = "N"+str(i)+"_"+str(j)
            dic[k] = l[i][j]

    return dic


def optimize(ass):
    l = []
    for i in range(N):
        s = ""
        for j in range(D):
            tv = "N"+str(i)+"_"+str(j)
            s+=ass[tv]
        l.append(s)
    tempass = {}
    for i in range(len(l)):
        tempass[l[i]] = cnt(l[i])
    #print(l)
    sorted_x = sorted(tempass.items(), key=operator.itemgetter(1),reverse=True)
    #print(sorted_x)
    
    f=[]
    for (k,v) in sorted_x:
        f.append(k)

    return decode(f)


################################################################

if m+a+e>=N:
    print("NO SOLUTION")
    dumpans({})
    exit()

no_rest = N-(m+a+e)
if  (7*no_rest) < (N):
    print("NO SOLUTION")
    dumpans({})
    exit()

if no_rest+a<m:
    print("NO SOLUTION")
    dumpans({})
    exit()

if Q==1:
    rec_backtrack()
    dumpans(format(Ass))
    exit()
else:
    rec_backtrack2(0)
    dumpans(optimize(holder))
    

    
