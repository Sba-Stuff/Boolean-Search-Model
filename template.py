from flask import *
def mainpage():
    x=""
    x+="<!DOCTYPE html PUBLIC \"-//W3C//DTD XHTML 1.0 Transitional//EN\" \"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd\">"
    x+="<html xmlns=\"http://www.w3.org/1999/xhtml\">"
    x+="<head>"
    x+="<meta http-equiv=\"Content-Type\" content=\"text/html; charset=iso-8859-1\" />"
    x+="<!-- TemplateBeginEditable name=\"doctitle\" -->"
    x+="<title>Welcome To Legal Document Search Engine</title>"
    x+="<!-- TemplateEndEditable -->"
    x+="<!-- TemplateBeginEditable name=\"head\" -->"
    x+="<!-- TemplateEndEditable -->"
    x+="</head>"
    x+="<body>"
    x+="<p><a href=\"tfidf\">TF-IDF Search</a></p>"
    x+="<p><a href=\"bm25\">BM-25 Search</a> </p>"
    x+="</body>"
    x+="</html>"
    return x
def searchresults(lig,results):
    x=""
    x = x+"<img src='"+url_for('static', filename='1.jpg')+"'>"
    x+="<form id=\"form1\" name=\"form1\" method=\"post\" action=\"\">"
    x+="<label>Search:"
    x+="<input type=\"text\" name=\"textfield\" style=\"width:80%\" value=\""+lig+"\"/>"
    x+="</label>"
    x+="<input name=\"search\" type=\"submit\" id=\"search\" value=\"Search\" />"
    x+=results;
    x+="</form>"
    return x;