#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      llima
#
# Created:     25/02/2015
# Copyright:   (c) llima 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
from bs4 import BeautifulSoup as Soup


def parseReviews(str_review, rss_name):
    soup = Soup(str_review)
    if rss_name == "Folha":
        return parseReviewsFolha(soup)
    return {}

def parseReviewsFolha(soup):
    reviews =[]
    for li in soup.findAll("li"):
        review={"data_id": "",
            "user_info":{"link":"", "name":""},
            "interact" :{"likes":0, "dislikes":0},
            "text":""
        }
        try:
            review['data_id'] = li.find('article').attrs["data-id"]
            info = li.select('article div h6 span a')[0]
            review['str_data'] =  li.select('article div h6')[0].text.replace('\n','').replace('\t','')
            review['user_info']['link'] = info.attrs['href']
            review['user_info']['name'] = info.text
            review['interact']['likes'] = int(li.select('article div ul li.to-thumb a.good')[0].text)
            review['interact']['dislikes'] = int(li.select('article div ul li.to-thumb a.bad')[0].text)
            review['text'] = li.select('article div.comment-body p')[0].text
            reviews.append(review)
        except:
            review['data_id'] = "error"
    return reviews

def main():
    pass

if __name__ == '__main__':
    main()
