import networkx as nx
import ast
import math

def preProcess(filename):
    names={}
    tweets=[]
    with open(filename) as f:
        for line in f:
           tweets.append(ast.literal_eval(line))
    f.close()
    for i in range(len(tweets)):
        mentation=set()
        for j in range(len(tweets[i]['entities']['user_mentions'])):
            mentation.add(tweets[i]['entities']['user_mentions'][j]['screen_name'])
        names[tweets[i]['user']['screen_name']]=mentation
            
	

    return names



def buildGraph(filename):
    names=preProcess(filename)
    G=nx.DiGraph()
    for tweeter, value in names.iteritems():
        G.add_node(tweeter)
        G.node[tweeter]['auth']=1
        G.node[tweeter]['hub']=1
        for mentioned in value:
            G.add_node(mentioned)
            G.node[mentioned]['auth']=1
            G.node[mentioned]['hub']=1
            if mentioned !=tweeter:
                G.add_edge(tweeter,mentioned)

    return G

def copyGraph(old,new):
    for page in new.nodes():
        old.add_node(page)
        old.node[page]['auth']=new.node[page]['auth']
        old.node[page]['hub']=new.node[page]['hub']
    return old
    
def HITS(filename):
    oldG=nx.DiGraph() 
    G=buildGraph(filename)
    old=copyGraph(oldG,G)
    
    for k in range(5):
        norm=0
        for people in G.nodes():
            G.node[people]['auth']=0
            inEdges=G.in_edges(people)
            for inEdge in inEdges:
                G.node[people]['auth']+=oldG.node[inEdge[0]]['hub']
            norm+=(G.node[people]['auth']*G.node[people]['auth'])
        norm=math.sqrt(norm)

        for people in G.nodes():
            G.node[people]['auth']=G.node[people]['auth']/norm
        norm=0

        for people in G.nodes():
            G.node[people]['hub']=0
            outEdges=G.out_edges(people)
            for outEdge in outEdges:
                G.node[people]['hub']+=oldG.node[inEdge[1]]['auth']
            norm+=(G.node[people]['hub']*G.node[people]['hub'])
        norm=math.sqrt(norm)

        for people in G.nodes():
            G.node[people]['hub']=G.node[people]['hub']/norm

        oldG=copyGraph(oldG,G)
   
    
    return G



def get_HITS_Rank(filename):
    print "Calculating...about 10s"
    graph=HITS(filename)
    auth=[]
    hub=[]
    for page in graph.nodes():
        auth.append((page,graph.node[page]['auth']))
        hub.append((page,graph.node[page]['hub']))

    auth=sorted(auth,key=lambda x:x[1])
    hub=sorted(hub,key=lambda x:x[1])

    auth.reverse()
    hub.reverse()
    print "TOP 10 Hub\n"
    for i in range(10):
        print hub[i]
        
    print "TOP 10 Authority\n"
    for i in range(10):
        print auth[i]






        
            
