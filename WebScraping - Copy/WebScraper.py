from hashlib import new
import os
import threading
import requests
from bs4 import BeautifulSoup

def removeSpace(inp : str) -> str:
    if  inp[len(inp)-1] == ' ':
            return inp[:-1]
    else: return inp

def makeValid(filename: str, invalidChar: str) -> str:
    for nonochar in invalidChar:
        newstr = filename.replace(nonochar,"")
    return newstr

def checkurl(url : str) -> bool:
    if "https://www.education.gov.za" in url:
        return False
    else:
         return True

def downYear(pap : any):
    ipaper = 0
    for pap1 in pap :
        if  pap1.contents[0] == "NON LANGUAGES" or pap1.contents[0] == "LANGUAGES" :
            continue
        
        ipaper = ipaper + 1
        downloads = pap1.parent.parent.find_all('td', class_ = "DownloadCell")
        titles = pap1.parent.parent.find_all('td', class_ = "TitleCell")

        pap1.contents[0] = removeSpace(pap1.contents[0])
        
        if not os.path.isdir(filedir + str(pap1.contents[0])):
            os.makedirs(filedir  + str(pap1.contents[0]))

        i = 0
        for download in downloads:
            file = open( makeValid(filedir + str(pap1.contents[0]) + "\\" + str(titles[i].findChild('a').contents[0]) + '.pdf',"\/:*?|<>"), 'wb')

            if checkurl(str(download.find("a").get('href'))):
                file.write(requests.get("https://www.education.gov.za" + str(download.find("a").get('href'))).content)
            else:
               file.write(requests.get(str(download.find("a").get('href'))).content) 

            file.close()
            i = i + 1
            print("downloaded : " + str(i * ipaper * iyear) + "/" + str(len(downloads) * len(years) * len(papers)) )


URL = 'https://www.education.gov.za/Curriculum/NationalSeniorCertificate(NSC)Examinations/NSCPastExaminationpapers.aspx'
soup = BeautifulSoup(requests.get(URL).content,"html.parser").find(id="dnn_ctr1741_Links_lstLinks")

years = soup.find_all("a", href = True)

iyear = 0
for year in years:
    iyear = iyear + 1
    if checkurl(year.get('href')):
        page = BeautifulSoup(requests.get("https://www.education.gov.za" + year.get("href")).content,'html.parser')
    else:
         page = BeautifulSoup(requests.get(year.get("href")).content,'html.parser')

    papers = page.find_all('span', class_ = "eds_containerTitle")
    

    filedir = os.path.dirname(os.path.realpath(__file__)) + '\\papers\\' +  removeSpace(makeValid(year.contents[0],"\/:*?|<>") )+ '\\'

    t = threading.Thread(target=downYear, args =[papers])
    t.start()

t.join()
print("finished downloading papers!")
    
    
        



input()
#for year in years:
    #print(year)
