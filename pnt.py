import math
import argparse
class nodez:
            
    def __init__(self):    
        self.o =  0
        self.Depth=0
        self.children = []     

    def Set(self,value):
        self.o=value

    def add_parent(self, p):
        self.parent=p

    def setDepth(self, d):
        self.Depth=d

    def getDepth(self):
        return self.Depth
    def ret(self): 
        return self.o   
    def retparent(self): 
        return self.parent  

    def retchild(self): 
        return self.children    
    def IsLeaf(self):
        if(len(self.children)==0):
            return True
        else:
            return False
class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
class Stack:
    def __init__(self):
        self.head = Node("head")
        self.size = 0
    def __str__(self):
        cur = self.head.next
        out = ""
        while cur:
            out += str(cur.value) + "->"
            cur = cur.next
        return out[:-3]
    def getSize(self):
            return self.size
    def isEmpty(self):
            return self.size==0
    def peek(self):
        if self.isEmpty():
                raise Exception("Peeking from an empty stack")
        return self.head.next.value
    def push(self, value):
        node = Node(value)
        node.next = self.head.next
        self.head.next = node
        self.size += 1  
    def pop(self):
        if self.isEmpty():
                raise Exception("Popping from an empty stack")
        remove = self.head.next
        self.head.next = self.head.next.next
        self.size -= 1
        return remove.value
  
################################################################################################
def PossibleMovesFirst(RemainingTokens):
    rm=len(RemainingTokens)/2
    truncrm = math.trunc(rm)
    ChildrenList=[]
    RML=[]
    for token in RemainingTokens:  
        if token%2!=0 and token<rm:
            ChildrenList.append(token)
            temp=RemainingTokens.copy()
            temp.remove(token)
            RML.append(temp)
    return  ChildrenList,RML 
def PossibleMovesNext(RemainingTokens,LastMove):
    ChildrenList=[]
    RML=[]
    for token in   RemainingTokens:  
        if LastMove%token==0 or token%LastMove==0:
            ChildrenList.append(token)
            temp=RemainingTokens.copy()
            temp.remove(token)
            RML.append(temp)

    return  ChildrenList, RML   

def alphabeta(fst,node,depth,Depth,alpha,beta,maximizingPlayer,LastMove,RemainingTokens,choice,children,counter,visit,MDepth,sumc):
    if depth==0:
        if(len(MDepth)==0):
            MDepth.append(Depth)
        else:
            MDepth.pop()
            MDepth.append(Depth)
        counter.append(1)
 #####Heuristics       
        for c in RemainingTokens:
            if c==1:
                return 0
        
        if LastMove==1:
            if len(children)%2==0:
             
                if maximizingPlayer:
                    return  -0.5
                else:
                    return  0.5
            else:   
                if maximizingPlayer:
                    return  0.5
                else:
                    return  -0.5
        p=0
# prime numbers are greater than 1
        if LastMove > 1: 
# check for factors
            for i in range(2,LastMove):
                        if (LastMove % i) == 0:
                            p=1
                            break
            else:
                count=0
                for child in children:
                    if(child%LastMove==0):
                        count=count+1
                if count%2!=0:
                    if maximizingPlayer:
                        return 0.7
                    else:
                        return -0.7
                else:
                    if maximizingPlayer:
                        return -0.7
                    else:
                        return 0.7    
        if p==1:
            p=0
            n=LastMove
            div=2
            ans=2
            maxFact=0
            while n!=0:
                if n%div!=0:
                    div=div+1
                else:
                    maxFact=n
                    n=n/div
                    if n==1:
                            ##print("is the largest prime factor !",maxFact);
                            count=0
                            for child in children:
                                if(child%maxFact==0):
                                    count=count+1
                            if count%2!=0:
                                if maximizingPlayer:
                                    return 0.6
                                else:
                                    return -0.6
                            else:
                                if maximizingPlayer:
                                    return -0.6
                                else:
                                    return 0.6
                            ans=1
                            break
            
    children=[]
    allrT=[]
    if maximizingPlayer:
        v=float('-inf')
        k=float('-inf')
        c=0
        if depth==Depth and fst==0  :
            children,allrT=PossibleMovesFirst(RemainingTokens)
            sumc[0]=sumc[0]+len(children)
            fst=1
        else:
            children,allrT=PossibleMovesNext(RemainingTokens,LastMove)
            sumc[0]=sumc[0]+len(children)
        if len(children)==0:
            #print("min win")
            counter.append(1)
            if(len(MDepth)==0):
                MDepth.append(depth)
            else:
                MDepth.pop()
                MDepth.append(depth)
            return -1
            
        else:
            S = nodez()
            m=0
            if(depth==Depth):
                print("Posible moves evaluation Max")
                print("############################")
            for child in children:
                visit.append(child)
                res=alphabeta(fst,child,depth-1,Depth,alpha,beta,False,child,allrT[m],choice,children,counter,visit,MDepth,sumc)
                m=m+1
                if(depth==Depth):
                    print(child,res)
               
                if res>v:
                    v=res
                   
                if v>alpha:
                    alpha=v
               
                if beta<=alpha:
                    break
                    
                if(res>=k):
                    if(k==res):
                        if(child<c):
                            
                            c=child
                            k=res
                            S.Set(child)
                    else:
                        c=child
                        k=res
                        S.Set(child)
            if(depth==Depth):
                choice.append(S.ret())
            return v
    else:
        v=float('inf')
        k=float('inf')
        c=0
        if depth==Depth and fst==0 :
            children,allrT=PossibleMovesFirst(RemainingTokens)
            sumc[0]=sumc[0]+len(children)
            fst=1
        else:
            children,allrT=PossibleMovesNext(RemainingTokens,LastMove)
            sumc[0]=sumc[0]+len(children)
             
        if len(children)==0:
            counter.append(1)
            if(len(MDepth)==0):
                MDepth.append(depth)
            else: 
                MDepth.pop()
                MDepth.append(depth)
            return 1

        else:        
            S = nodez()
            m=0
            if(depth==Depth):
                print("Posible moves evaluation Min:")
                print("############################")
                
            for child in children:
                visit.append(child)
                res=alphabeta(fst,child,depth-1,Depth,alpha,beta,True,child,allrT[m],choice,children,counter,visit,MDepth,sumc)
                m=m+1
                if(depth==Depth):
                    print(child,res)            
                if res<v:   
                    v=res                          
                if v<beta:
                    beta=v
                    
                if beta<=alpha:
                    break
                    
                if(res<=k):
                    if(k==res):
                        if(child<c):
                            
                            c=child
                            k=res
                            S.Set(child)
                    else:
                        c=child
                        k=res
                        S.Set(child)
                                   
            if(depth==Depth):
                choice.append(S.ret())
            return v

#####The Demo 
if __name__ == '__main__': 
    parser = argparse.ArgumentParser()
    parser.add_argument("game_parameters" , type=int, nargs='+')
    args = parser.parse_args()
   
    print("####################")
    print("Input:",args.game_parameters)
    print("####################")
   
    d = args.game_parameters[-1] #depth
    lm=args.game_parameters[-2] ##last move
    player=args.game_parameters[1]##player
    num=1
    l=[]
    if(player==0):
        fm=0
    else:
        fm=1

    if(player%2==0):
        value=True
    else:
        value=False
    all_tokens = [i+1 for i in range(args.game_parameters[0])]
    print("Original Tokens:",all_tokens)
    l= list(set(args.game_parameters[2:-1]).symmetric_difference(set(all_tokens))) 
    print("Remaining Tokens:",l)
    if(d==0):
        d=len(l)-1

    sumc=[0]
    c=[] 
    ch=[]
    counter=[]
    visit=[]
    MDepth=[]
    print(d)
    print(value)
    print(l)
    res=alphabeta(fm,lm,d,d,float('-inf'),float('inf'),value,lm,l,c,ch,counter,visit,MDepth,sumc)
    if res!=1 and res !=-1:
        if value==True:
            if(d%2==0):
                res=-1
            else:
                res=1
        else:
            if(d%2==0):
                res=1
            else:
                res=-1
    print("#################")
    print("OutPut:")
    print("#################")
    print("Move:",c[0])
    print("Value:",res)   
    print("Number of Nodes Visited:",len(visit)+1) 
    print("Number of Nodes Evaluated:",len(counter)) 
    print("Max Depth Reached:",MDepth[0]) 
    print("Avg Effective Branching Factor:",(len(visit)/((len(visit)+1)-len(counter))))
