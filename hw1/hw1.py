import unicodedata
from glob import glob
import ntpath
import math
import operator


def simple_split(filename):
    """
    Split a text in words. Returns a list of tuple that contains
    """
    word_list = []
    wcurrent = []
    windex = None
    
    for i, c in enumerate(text):
        if c.isalnum():
            wcurrent.append(c)
     
        elif wcurrent:
            word = u''.join(wcurrent)
            word_list.append(word)
            wcurrent = []

    if wcurrent:
        word = u''.join(wcurrent)
        word_list.append(word)

    return word_list
    

def words_normalize(words):
    """
    Do a normalization precess on words. In this case is just a tolower(),
    """
    normalized_words = []
    for word in words:
        wnormalized = word.lower()
        normalized_words.append(wnormalized)
    return normalized_words

def word_index(text):
    """
   To make the code clean. This function just help to call split word and word normalize
    """
    words = simple_split(text)
    words = words_normalize(words)
    return words

def inverted_index(text):
    """
    Create the inverted dictionary
    """
    inverted = {}

    for word in word_index(text):
        locations = inverted.setdefault(word, [])

    return inverted

def count_word(text):
    """
     Get the term frequency of each word in each documents.
     For example:
       If document a9900247.txt has 'technology' appears 5 times
       My inverted index will show like "technology: {a99000247.txt:5}"
    """
    wordCount={}
    for word in word_index(text):
        if word in wordCount:
            wordCount[word]+=1
        else:
            wordCount[word]=1
    return wordCount

def inverted_index_add(inverted, doc_id, doc_index):

    """
      Use to combine the word and counted frequency
    """
    for word, fq in doc_index.iteritems():
        indices = inverted.setdefault(word, {})
        indices[doc_id] = fq
    return inverted



def get_raw_TF(inverted,queries):

    """
      Get the raw TF of queries' term in the vector space
      If our dictionary is ['texas','a&m','university','winter']
      If queries is "texas winter"
      Then the raw_TF in the vector space is [1 0 0 1]
    """
    query_dict={}
    raw_tf=[]
    for w in queries:
        if inverted.has_key(w):
            query_dict[w]=query_dict.get(w,0.0)+1.0
        else:
            query_dict[w]=0.0

    for term, count in inverted.iteritems():
        if query_dict.has_key(term):
            raw_tf.append(query_dict[term])
        else:
            raw_tf.append(0)

    return raw_tf

    
def getTF(inverted):
    """
     Cacluate the term frequency of each documents in the vector space
    """
    size=len(inverted)
    documents=booleanquery(re)
    doc_TF={}
    for doc in documents:
        TF=[0]*size
        i=0
        for count in inverted.values():
            value=count.get(doc)
            if value:TF[i]=math.log10(value)+1   # get TF, if not exist then assign 0;
            else:TF[i]=0
            i+=1
        doc_TF[doc]=TF
    del documents
    return doc_TF

def getIDF(N,inverted):
    """
      Calculate the IDF of each term in the inverted index
     """
    idf=[]
    for term,count in inverted.iteritems():
        value=math.log10(N/len(count))    # Calculate IDF base on log 10
        idf.append(value)
    return idf

def getTF_IDF(N,inverted):
    """
      Calculate TF_IDF of each documents 
    """
    tf_idf={}
    tfs=getTF(inverted)
    idf=getIDF(N,inverted)
    for docname, tf in tfs.iteritems():
        tf=map(lambda x,y:x*y,tf,idf)
        tf_idf[docname]=tf
    del tfs
    del idf
    return tf_idf
    

    
def getCosineSim(N,inverted,queries):
    """
      Now we can get the Cosine Similarity
    """
    raw_tf=get_raw_TF(inverted,queries)
    tf_idf=getTF_IDF(N,inverted)
    docs=booleanquery(re)
    sim={}
    sorted_sim=[]
    querySum=math.sqrt(sum(map(lambda x:x*x,raw_tf)))
    for doc in docs:
        docvector=tf_idf[doc]
        dotsum=sum(p*q for p,q in zip(raw_tf,docvector))
        sumsq=math.sqrt(sum(map(lambda x:x*x,docvector)))*querySum
        sim[doc]=dotsum/sumsq
    sorted_sim=sorted(sim.iteritems(),key=operator.itemgetter(1))
    del sim
    sorted_sim.reverse()
    return sorted_sim
    
def getunion(queries):
    re=[]
    for term in queries:
        result=[]
        result=list(inverted[term])
        re.append(result)
    del result
    return re

def booleanquery(re):
    documents=set(re[0])
    for r in re:
        documents=documents.intersection(set(r))
    return documents



    
inverted={}

documents={}
N=0   # count how many documents
print "Reading txt file"
"""
# Change Here to the directory where your documents are.  Use * to represent all the file in that directory.
# For example:
#     award/*/*/a*.txt  This will get all the "a*.txt" files under folder "award"
"""
for txtfile in glob('awd/a*.txt'):   
    head,tail=ntpath.split(txtfile) 
    documents[tail]=open(txtfile).read()
    N=N+1;

print "Building inverted index. This may take about 1-2 minute"  # For faster results, please try smaller dataset
for doc_id, text in documents.iteritems():
        doc_index = count_word(text)
        inverted=inverted_index_add(inverted, doc_id, doc_index)


print "finish\n"


while 1:
    print "choose option: "
    print "1. Boolean Query[Press 1]"
    print "2. Vector Space Query[Press 2]"
    print "Input exit to terminate[Type 'exit']"
    
    chose=raw_input('Make your choice\n')



    if chose=='exit':
       break

    if chose=='1':
        queries=raw_input('what you want to query?')
        queries=queries.lower()
        queries=queries.split()
        try:
            re=getunion(queries)
        except:
            print "Some Word does not exist in dictionary\n"
            continue
        docs=booleanquery(re)
        if len(docs)>0:
            for doc in docs:
                print doc
  
        else:
            print "No Match\n"
            
    print "\n"

    if chose=='2':
        queries=raw_input('what you want to query?')
        queries=queries.lower()
        queries=queries.split()
        try:
            re=getunion(queries)
        except:
            print "Some Word does not exist in dictionary\n"
            continue
        sim=getCosineSim(N,inverted,queries)
        if len(sim)>50:
            for i in range(50):
                print sim[i]
        else:
            for x in sim:
                print x
                
        print "\n"
       




  




