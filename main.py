import os
import csv
from bs4 import BeautifulSoup
import urllib.request,urllib.error
from urllib.request import Request, urlopen
def getaddphoareaimg( url ):                                                        # Working in the inner pages of the website
    inner_page = urlopen(Request(url,headers=hdr))
    inner_html=inner_page.read()
    inner_page.close()
    soup = BeautifulSoup(inner_html,'html.parser')
    tags=soup.find('div',{'class':'place-info'})
    anchors=tags.findAll('a')
    details=[]
    count=0;
    flag=1
    for anchor in anchors:
        if count==1:
            for i in anchor.text.strip():
                if i.isalpha()==True:
                    details.append('----------')
                    details.append(anchor.text.strip())
                    flag=0
                    break;
        if flag:
            details.append(anchor.text.strip())
        count+=1
    return details

def scrapping(soup):                                                                 # working on the outer pages/Homepage
    tags=soup.findAll("div",{"class":"place-square"})
    records=[]
    records.append(["Name","Image URL","Address","Phone No","Area"])
    for tag in tags:
        new_url=tag.a.get('href',None)
        name=tag.a.text.strip()
        image_url=tag.img.get('src',None).strip()
        rest_details=getaddphoareaimg( new_url )
        all_details=[str(name),str(image_url)]
        all_details.extend(rest_details)
        records.append(all_details)
    return records

if __name__ == "__main__":                                                          #this is where the program starts getting executed
    url = 'https://downtowndallas.com/experience/stay/'
    hdr = {'User-Agent': 'Mozilla/5.0'}
    page = urlopen(Request(url, headers=hdr))
    html = page.read()
    page.close()
    soup = BeautifulSoup(html, 'html.parser')
    title=soup.title.string
    if(os.path.exists('./'+title+'.csv') and os.path.isfile('./'+title+'.csv')):    # Deleting so as to make that same updated file
        os.remove('./'+title+'.csv')
    records=scrapping(soup)                                                         # Record stores a list of list of all details
    flag=0;
    with open(title+'.csv', 'w', newline='') as entry:                              # storing the records/details that we get in a new csv file
        writer = csv.writer(entry)
        for record in records:
            writer.writerow(record)
            if os.path.exists( './'+title+' Images')==False:                        # creating a new folder
                os.mkdir( title+' Images')                                          
            if flag:
                opener = urllib.request.URLopener()
                opener.addheader('User-Agent', 'hello')
                filename, headers = opener.retrieve(record[1],str('./'+title+' Images'+'/'+record[0]+".png")) # saving the images in the newly created folder
            flag=1;
    print("Done!")
