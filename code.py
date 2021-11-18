from numpy import fabs
import pytesseract as tess
from pytesseract import Output
tess.pytesseract.tesseract_cmd=r'C:/Users/HP/AppData/Local/Tesseract-OCR/tesseract.exe'
from PIL import Image

zz="0009"
img = Image.open(zz+".jpg")

text=tess.image_to_string(img, config='-c preserve_interword_spaces=1')
#print(text)


import re
result = [x for x in re.split("\s{2,}",text) if x]

n=len(result)
i=1
while i<n:
    pass
    if result[i][0]==":" or result[i][0]==">" or result[i][0]=="<":
        result[i-1]=result[i-1]+result[i]
        result.pop(i)
    else:
        i+=1
    n=len(result)
i=0
while i<len(result):
    x=result[i].splitlines()
    if len(x)>1:
        result[i]=x[0]
        i+=1
        for j in range(1,len(x)):
            result.insert(i,x[j])
            i+=1
    else:
        i+=1
c=1
for x in result:
    print(c," - ",x)
    c+=1
print(len(result))



def isSubSequence(string1, string2, m, n):
    if m == 0:
        return True
    if n == 0:
        return False
    if string1[m-1] == string2[n-1]:
        return isSubSequence(string1, string2, m-1, n-1)
    return isSubSequence(string1, string2, m, n-1)



Features = ["Test Description", "Value", "Unit", "Biological Ref Interval"]
out=[]
f=0
a=0
while a <len(result):
    i=result[a]
    x=[" " for _ in range(len(Features))]
    if(isSubSequence("endofreport",result[a].lower() , len("endofreport"), len(result[a]))):
        x[0]=result[a]
        out.append(x)
        break
    if f==0:
        if ":" in i or ">" in i or "<" in i:
            x[0]=result[a]
            out.append(x)
            f=1
        a+=1
        continue
    if ":" in i or ">" in i or "<" in i:
        x[0]=result[a]
        out.append(x)
        a+=1
        continue
    """if i in Features:
        a+=1
        continue"""
    if result[a]==Features[0]:
        print(result[a])
        a+=len(Features)
        out.append(Features)
        continue
    if a+1<len(result) and not (str(result[a+1]).isnumeric() or str(result[a+1]).replace('.', '', 1).isdigit() or result[a+1]=="B" or result[a+1]=="Positive"):
        x[0]=result[a]
        out.append(x)
        a+=1
        continue

    
    x[0]=result[a]
    a+=1
    if a<len(result) and (str(result[a]).isnumeric() or str(result[a]).replace('.', '', 1).isdigit() or result[a]=="B" or result[a]=="Positive"):
        x[1]=result[a]
        a+=1
    """if a<len(result) and ("%" == result[a] or "mm" == result[a] or "Milli" == result[a] or "fL" in result[a] or "pg" == result[a] or "/cumm" in result[a]):
        x[2]=result[a]
        a+=1"""
    if a<len(result) and ("-" in result[a] or "~" in result[a]):
        x[3]=result[a]
        a+=1
    elif a+1<len(result) and ("-" in result[a+1] or "~" in result[a+1]):
        x[2]=result[a]
        x[3]=result[a+1]
        a+=2
    
    out.append(x)


for o in out:
    print(o)

import xlsxwriter
workbook = xlsxwriter.Workbook(zz+'.xlsx')
worksheet = workbook.add_worksheet()
col=0
for row,data in enumerate(out):
    worksheet.write_row(row,col,data)
workbook.close()

