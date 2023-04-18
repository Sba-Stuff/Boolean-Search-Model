from flask import *
import sys
import os
import PyPDF2 as p2
import os
import nltk
import re
import string
from nltk.corpus import stopwords
from pprint import pprint as pp
from nltk.stem.porter import PorterStemmer
porter_stemmer = PorterStemmer()
from template import mainpage,searchresults
print("Libraries Imported")

def storeinfo():
    f=open(r"DocumentInfo.txt","w")
    count = 1
    path = r'PDF'
    for fp in os.listdir(path):
        pdfFileObj = open(os.path.join(path, fp), 'rb')
        pdfread = p2.PdfFileReader(pdfFileObj)
        info = pdfread.getDocumentInfo()
        #text = .encode('utf-8').decode('ascii', 'ignore')
        f.write(str(count)+ "\n\n")
        print(str(count)+ "\n")
        #f.write("Document: ")
        print("Document: ")
        f.write("Document: " + fp.replace(".pdf", "") + "\n\n")
        print(fp.replace(".pdf", "") + "\n")
        print("\n")
        if not info.title:
            #f.write("No Title\n")
            print("No Title\n")

        else:
            f.write("Title: " + info.title.encode('utf-8').decode('ascii', 'ignore') + "\n")
            print("Title: " + info.title.encode('utf-8').decode('ascii', 'ignore') + "\n")
        if not info.author:
            f.write("No Author \n")
            print("No Author \n")
        else:
            f.write("Author: " + info.author.encode('utf-8').decode('ascii', 'ignore') + "\n")
            print("Author: " + info.author.encode('utf-8').decode('ascii', 'ignore') + "\n")

        print("\n")
        count = count + 1

    f.close()

def pdftoetext():
    d = 1
    path = r'PDF'
    for fp in os.listdir(path):
        pdfFileObj = open(os.path.join(path, fp), 'rb')
        pdfread = p2.PdfFileReader(pdfFileObj)
        #info = pdfread.getDocumentInfo()
        file1 = open(r'Text\\' + fp.replace(".pdf", "") + '.txt','w')
        d = d + 1
        for i in range(pdfread.getNumPages()):
            pinfo = pdfread.getPage(i)
            text = pinfo.extractText()
            text = text.encode('utf-8').decode('ascii', 'ignore')
            file1.write(text)

        file1.close()
def extractText():
    content = " "
    path = r'PDF'
    for fp in os.listdir(path):
        pdfFileObj = open(os.path.join(path, fp), 'rb')
        pdfread = p2.PdfFileReader(pdfFileObj)
        for i in range(pdfread.getNumPages()):

            text_data = pdfread.getPage(i).extractText()
            content = content + text_data


    text_file = open(r'Raw Text.txt', 'w')
    content = content.encode('utf-8').decode('ascii', 'ignore')
    text_file.write(content)
    text_file.close()
    return content

def pprocess(content):

    #converting text into lower case, Removing Numbers, Punctuations, Special Characters and lines
    content = content.lower()
    content = re.sub('\[.*?\]', '' , content)
    content = re.sub('[%s]' % re.escape(string.punctuation), '', content)
    content = re.sub('\w*\d\w*', '', content)
    content = re.sub('[''""_]', '', content)
    content = re.sub('\n', '', content)
    content = re.sub('-', '', content)
    #print(content)

    #Tokenization
    tokens = nltk.word_tokenize(content)
    #print(tokens)

    #Stopwords removal

    tokens_without_sw = []
    en_stops = set(stopwords.words('english'))
    for word in tokens:
        if word not in en_stops:
            tokens_without_sw.append(word)

    #print(tokens_without_sw)

    #Stemming
    stem_words = []
    for w_port in tokens_without_sw:
        #print("Actual: %s  || Stem: %s"  % (w_port,porter_stemmer.stem(w_port)))
        w =porter_stemmer.stem(w_port)
        stem_words.append(w)

    #Removing duplicate values
    #ordered_tokens = set()
    #result = []
    #for word in stem_words:
        #if word not in ordered_tokens:
            #ordered_tokens.add(word)
            #result.append(word)

    #print(result)


    #Filtering empty spaces
    filter_object = filter(lambda x: x != "", stem_words)
    f_list = list(filter_object)
    #print(f_list)



    #Sorting List in Alphabatical Order
    sorted_list = sorted(f_list)

    #print(sorted_list)



    return(sorted_list)

def duplicateWords(list1):
    f_list = set()
    result = []
    for word in list1:
        if word not in f_list:
            f_list.add(word)
            result.append(word)
    return result

def Vocabulary():
    files_with_index = {}
    cn = 1
    file2 = open(r'Vocabulary.txt', 'w')
    for word in final_list:
        text = word.encode('utf-8').decode('ascii', 'ignore')
        file2.write(str(cn) + "   " + text + "\n")
        cn = cn + 1

    file2.close()

    #Vocabulary of Documents

    count = 1
    path = r'Text'
    file = open(r'DocumentVocabulary.txt','w')
    for fp in os.listdir(path):


        file.write(str(count) + "         "  + fp + "\n")
        files_with_index[count] = fp
        count = count + 1

    file.close()
    return files_with_index

def unique_words_and_freq(words):
    words_unique = []
    word_freq = {}
    for word in words:
        if word not in words_unique:
            words_unique.append(word)
    for word in words_unique:
        word_freq[word] = words.count(word)
    return word_freq

def meta_info(files):
    x = ""
    x=x+"<table bgcolor='#FFFFFF' width='100%' border='1'>"
    x=x+"  <tr>"
    x=x+"<td><div align='center'><strong>Author Name </strong></div></td>"
    x=x+"<td><div align='center'><strong>Paper Title </strong></div></td>"
    x=x+"<td><div align='center'><strong>Action</strong></div></td>"
    x=x+"</tr>"
    for f in files:
        fp = f.replace(".txt" , ".pdf")
        path = r'PDF'
        for fp1 in os.listdir(path):
            if fp1 == fp:
                pdfFileObj = open(os.path.join(path, fp1), 'rb')
                pdfread = p2.PdfFileReader(pdfFileObj)
                info = pdfread.getDocumentInfo()
                print(fp)
                x=x+"<tr>"
                x=x+"<td>"+info.author.encode('utf-8').decode('ascii', 'ignore')+"</td>"
                x=x+"<td>"+info.title.encode('utf-8').decode('ascii', 'ignore')+"</td>"
                x=x+"<td><a href='http://127.0.0.1:5000/"+url_for('static', filename='PDF/'+fp.replace(".txt" , ".pdf"))+"' target='blank'>Download</a></td>"
                x=x+"</tr>"
                #x = x+"Title: " + info.title.encode('utf-8').decode('ascii', 'ignore') + "\n"
                #x = x+"Author: " + info.author.encode('utf-8').decode('ascii', 'ignore') + "\n"
                #print("Title: " + info.title.encode('utf-8').decode('ascii', 'ignore') + "\n")
                #print("Author: " + info.author.encode('utf-8').decode('ascii', 'ignore') + "\n")
                #print(f)
                #x=x+"<br>"
                #print("\n")
    x=x+"</table>"
    return x


class Node:
    def __init__(self ,docId = None, freq = None):
        self.freq = freq
        self.doc = docId
        self.next = None
class WlinkedList:
    def __init__(self ,head = None):
        self.head = head

def writefile(filename, arraytowrite):
    with open(filename, 'w', encoding="utf-8") as f:
        for item in arraytowrite:
            if item is not "":
                f.write("%s\n" % item)

def readfile2(filepath):
    words = []
    f = open(filepath, "r")
    lines = f.readlines()
    for line in lines:
            words.append(line.strip())
    return words
#storeinfo()
#print("Information Storage Successfull")
#pdftoetext()
#print("PDF To Text Successfull")
#content = extractText()
#print("Text Extraction Successfull")
#list11 = pprocess(content)
#list1 = duplicateWords(list11)
#final_list = sorted(list1)
#writefile("waji.txt",final_list)
#print("Duplicate Word Removal Successfull")
final_list = readfile2("waji.txt")
files_with_index = Vocabulary()
print("Vocabulary Created")
words_lists = {}
for word in final_list:
    words_lists[word] = WlinkedList()
    words_lists[word].head = Node( 1 ,Node)
word_list = {}
docID = 1
path = r'Text'
for fp in os.listdir(path):
    text_object = open(os.path.join(path, fp), 'r')
    text = text_object.read()
    text = pprocess(text)
    #text = duplicateWords(text)
    word_list = unique_words_and_freq(text)
    for word in word_list.keys():
        link_list = words_lists[word].head
        while link_list.next is not None:
            link_list = link_list.next

        link_list.next = Node(docID ,word_list[word])

    docID +=1
#file = open(r'InvertedIndex.txt','w')
#for word in final_list:
#
#    l_list = words_lists[word].head
#    file.write(word)
#    print(word)
#    while l_list.next is not None:
#        file.write("    ->" +str(l_list.next.doc))
#        print("    ->" +str(l_list.next.doc))
#        l_list = l_list.next
#    file.write("\n")
#file.close()
#print("Inverted Index Created")
app = Flask(__name__,template_folder="template/",static_folder="static/")

@app.route('/',methods=["POST", "GET"])
def hello_world():
    return render_template("index.html")
@app.route('/search',methods=["POST", "GET"])
def lo_world():
    if request.method == "POST":
        lig = request.form["textfield"]
        page = request.form['search']
        query = lig
        query = nltk.word_tokenize(query)
        boolean_words = []
        query_words = []
        for word in query:
            if word.lower() != "and" and word.lower() != "or" and word.lower() != "not":
                query_words.append(word.lower())

            else:
                boolean_words.append(word.lower())

        print(boolean_words)
        files = len(files_with_index)
        zeroes_and_ones_of_single_query = []
        zeroes_and_ones_of_all_words = []
        for word in (query_words):
            if word.lower() in final_list:
                zeroes_and_ones_of_single_query = [0] * files
                linkedlist = words_lists[word].head
                print(word)
                while linkedlist.next is not None:
                    zeroes_and_ones_of_single_query[linkedlist.next.doc - 1] = 1
                    linkedlist = linkedlist.next
                zeroes_and_ones_of_all_words.append(zeroes_and_ones_of_single_query)
            else:
                print(word," not found")
                sys.exit()

        print(zeroes_and_ones_of_all_words)
        binary_result = []
        for word in boolean_words:
            word_list1 = zeroes_and_ones_of_all_words[0]
            word_list2 = zeroes_and_ones_of_all_words[1]
            if word == "and":
                bitwise_op = [w1 & w2 for (w1,w2) in
        zip(word_list1,word_list2)]
                binary_result.insert(0, bitwise_op);
            elif word == "or":
                bitwise_op = [w1 | w2 for (w1,w2) in
        zip(word_list1,word_list2)]
                binary_result.insert(0, bitwise_op);

            elif word == "not":
                bitwise_op = [not w1 for w1 in word_list2]
                bitwise_op = [int(b == True) for b in bitwise_op]
                bitwise_op = [w1 & w2 for (w1,w2) in
        zip(word_list1,bitwise_op)]

                binary_result.insert(0, bitwise_op);
        files = []

        print(binary_result)
        lis = binary_result[0]
        cnt = 1
        for index in lis:
            if index == 1:
                files.append(files_with_index[cnt])
            cnt = cnt+1

        return render_template("search.html",output="<br>"+"Search Results For: "+str(lig)+"<br>"+str(meta_info(files)))#searchresults(lig,"<br>"+str(meta_info(files))) #render_template(searchresults(lig,"HelloFriends"))
    else:
        print("Do Nothing")
if __name__ == '__main__':

    # run() method of Flask class runs the application
    # on the local development server.
    app.run()