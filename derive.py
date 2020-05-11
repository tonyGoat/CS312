#Tony Yang 931001023
#Xianglu Peng  930990871

#! /usr/bin/python3
import string
import sys
def derivation():
    
    #read user's input length and filename 
    N=0
    N = int(sys.argv[1][2])
    filename = sys.argv[2]
    repeat_list = []
    #read the grammar from txt file and use dic to store it 
    with open(filename,'r', encoding = 'UTF-8') as grammar:
        dic = {}
        firstspace = 0 
        worklist1 = []
        for i in grammar:
            glist = i.split()
            print(glist)
    
            if glist[0] in dic:
                dic[glist[0]].append(glist[2:len(i)-1]) 
                

            
            else:
                emptylist = [] 
                emptylist.append(glist[2:len(i)-1])  
                dic[glist[0]] = emptylist
                worklist1.append(glist[0])
                #
              
            
    
    
    worklist = []
    #push the start symbol into worklist 
    worklist.append(worklist1[0])
    print(worklist)
    
    print(dic)
 
    while len(worklist)!= 0:
        #s will store the potential derivation starting from the start symbol  
        s = worklist.pop()
        # if length of the derivation in s exceeds the user's input, exit the loop 
        if len(s) > N:
            continue 

        leftmost_NT_index = 0
        count_terminal = 0
        print(s)
        
        #sss = []
        #sss.append(s)
        #print(sss)
        for i in range(len(s)):
            #if i not in dic, we count it
            
            if str(s[i]) not in dic:
                count_terminal = count_terminal + 1
                #print("nooooo")
            else: 
                #store the leftmost index and we can locate the index of the key later 
                leftmost_NT_index = i
                #print("innnnn")
                break
       
        #if count equals the teminals in s, we print s out.
        if count_terminal==len(s):
            if s not in repeat_list:
                repeat_list.append(s)
                for i in s:
                  print (i,end=" ")
                print ()

        else:
            #find the key we want to derive 
            key = s[leftmost_NT_index] 
            for j in range(len(dic[key])):
                tmp = list(s)
                tmp.pop(leftmost_NT_index)
                #print("first ", tmp)
                #use the loop to go through the value of the corresponding key, store in tmp, and append it to the worklist 
                for k in range(len(dic[key][j])):
                    tmp.insert( k + leftmost_NT_index, dic[key][j][k])
                #print("second " , tmp)
                worklist.append(tmp)
    

if __name__ == "__main__":
     derivation()
      
