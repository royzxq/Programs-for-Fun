
import string

def replace(text):
	text = string.replace(text,'<p>','')
	text = string.replace(text,'</p>','')
	text = string.replace(text,'<code>','')
	text = string.replace(text,'</code>','')
	text = string.replace(text,'</i>','')
	text = string.replace(text,'<i>','')
	text = string.replace(text,'<b>','')
	text = string.replace(text,'</b>','')
	text = string.replace(text,'<em>',' ')
	text = string.replace(text,'</em>',' ')
	text = string.replace(text,'\n',' ')
	text = string.replace(text,'\t',' ')
	text = string.replace(text,'<br>','\n')
	text = string.replace(text,'(E)','')
	text = string.replace(text,'(M)','')
	text = string.replace(text,'(H)','')
	return text