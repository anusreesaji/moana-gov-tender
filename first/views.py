#import neccasary libraries

from django.shortcuts import render
import datetime
from bs4 import BeautifulSoup
import requests
import csv
import time
from selenium import webdriver
from selenium.webdriver.support.select import Select
import re

listOfTender=[]
def get_soup(link):
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html,"html5lib")
    return soup
    
def openInnerLinks3(link,browser):
    tender={}
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html,"html5lib")
    #gets all tables with the class=standard-table and assigns to tables variable
    tables = soup.findAll('table', {'class': 'tablebg'})
    cellno=0
    #loops through all tables
    for table in tables:
        #for each table it finds all the table data cells
        cells = table.findAll('td')
        #in each table, loop through each table cell and prints the text, stripping off the whitespace in front and back.
        for cell in cells:
            if(cellno==1):
                tender["Department"] =(cell.text.strip())
            if(cellno==93):
                tender["Name"]=(cell.text.strip())
            if(cellno==101):
                tender["size"]=(cell.text.strip())
            if(cellno==131):
                tender["date"]=(cell.text.strip())
            cellno+=1
    tender["url"]=(link)
    listOfTender.append(tender)
    #out_file = open(('data.csv'),'a')
    #csvwriter = csv.DictWriter(out_file, delimiter=',', fieldnames=fields)
    #csvwriter.writerow(petStore)
    #out_file.close()

    
def openInnerLinks2(link,browser):
    browser.get(link)
    html = browser.page_source
    soup = BeautifulSoup(html,"html5lib")
    table = browser.find_element_by_id("table")
    links = [link.get_attribute('href') for link in table.find_elements_by_tag_name('a')]
    for link3 in links:
        openInnerLinks3(link3,browser)
        
def openInnerLinks1(category,browser):
    select = Select(browser.find_element_by_id('productCategory'))
    select.select_by_visible_text(category)
    elem = browser.find_element_by_id('Search') # Find the search box
    elem.click()
    html = browser.page_source
    soup = BeautifulSoup(html,"html5lib")
    table = browser.find_element_by_id("table")
    links = [link.get_attribute('href') for link in table.find_elements_by_tag_name('a')]
    for link2 in links:
        openInnerLinks2(link2,browser)
    

def generalPageLinks(browser):

     category=["Civil Works - Bridges"]
     #"Civil Works - Buildings","Civil Works - Canal","Civil Works - Highways","Civil Works - Lift Irrigation Schemes","Civil Works - Others","Civil Works - Roads","Civil Works - Water Works"]
     for work in category:
            link="https://etenders.kerala.gov.in/nicgep/app?page=FrontEndTendersByOrganisation&service=page"
            browser.get(link)   
            openInnerLinks1(work,browser)


now = datetime.datetime.now().strftime('%H:%M:%S')
# Create your views here
def login (request):
	browser = webdriver.Chrome()
	generalPageLinks(browser)
	links=[]
	name=[]
	department=[]
	size=[]
	url=[]
	date=[]
	for item in listOfTender:
		department.append(item["Department"])
		name.append(item["Name"])
		try:
			date.append(item["date"])
		except:
			date.append("null")
		size.append(item["size"])
		url.append(item["url"])

	ListOfTender={"name":name,"url":url,"date":date,"size":size, "department":department}

	return render (request,'first/login.html',ListOfTender )
	
	