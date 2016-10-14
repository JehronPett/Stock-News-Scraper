#!/usr/bin/python
import requests #I feel like this does the same thing^
import bs4 #This is where the money is made, this module allows me to scrape information from websites
import smtplib
import datetime

def isValidNews(s):
    if ("Current Report Filing" in s):
        return False
    elif ("Statement of Changes in Beneficial Ownership" in s):
        return False
    elif ("Report of Foreign Issuer" in s):
        return False
    elif ("Statement of Beneficial Ownership" in s):
        return False
    elif ("Securities Registration Statement" in s):
        return False
    elif ("Prospectus Filed Pursuant to Rule" in s):
        return False
    elif ("Confidential Treatment Order" in s):
        return False
    elif ("Proxy Statement" in s):
        return False
    elif ("Statement of Ownership" in s):
        return False
    else:
        #final.append(myCompanies[c])
        return True

class Company:
    '''
        Each instance of a company object will know it's ticker,
        it's price, and the headline of the article that was released
        that specific day.
    '''
    ticker = ""
    price = 0
    newsHeadline = ""
    
    #Intializer for Company object
    def __init__(self, t, p, n):
        self.ticker = t
        self.price = p
        self.newsHeadline = n
    
    def string(self):
        return self.ticker + ": $" + str(self.price) + "\nHeadline: " + self.newsHeadline

#Create a new list to hold all Company objects
listCompanies = []

a = 1;
while (a < 30):
    print "Fetching data from page " + str(a) + "..."
    #Download the page
    news = requests.get('http://investorshub.advfn.com/boards/recentnews.aspx?page=' + str(a))
    news.raise_for_status()
    #Passes html content to BeautifulSoup and creates a new object
    stockNews = bs4.BeautifulSoup(news.text, "lxml")
    #Selects the <a> tagged elements of the website within the table
    #The table is where the news feed is
    elems = stockNews.select('table a')
    
        #Remove first two empty links
    if (len(elems) > 0):
        elems.remove(elems[0])
        elems.remove(elems[0])
    
        '''Loop through the company tickers, prices, and news headline, and create
            new objects respectively'''
        x = 0
        while (x < len(elems) - 3):
            #print x
            if (x % 3 == 0):
                try:
                    if ((float(elems[x+1].getText().strip()) < 10.0)):
                        if (isValidNews(elems[x+2].getText().strip())):
                            listCompanies.append(Company(elems[x].getText().strip(),
                            float(elems[x+1].getText().strip()),
                            elems[x+2].getText().strip()))
                except ValueError:
                    elems.insert(x+1, elems[x])
            x = x + 1
        a = a + 1
    else:
        a = a + 1

myCompanies = []
#Use the list to remove all the tickers that I do not want
for b in range(len(listCompanies) - 1):
    if (0.1 < listCompanies[b].price < 10.0):
        myCompanies.append(listCompanies[b])

for x in myCompanies:
    print x.string()
    print ""
