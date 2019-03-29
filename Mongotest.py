from companyRank import rank
from pymongo import MongoClient
import datetime
class rankDB():
    def database_of_rank(self,item,company):
        client = MongoClient('localhost',27017)
        newrank=rank()
        database = client.baiducompete
        company_set = database['company']
        ranknum=newrank.main(item,company)
        companyDict={}
        now=datetime.datetime.now()
        time=now.strftime("%Y-%m-d %H:%M:%S")
        companyDict['company']=company
        companyDict['item']=item
        companyDict['time']=time
        companyDict['rank']=ranknum
        rs = company_set.insert_one(companyDict)
