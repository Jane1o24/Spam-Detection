# -*- coding: utf-8 -*-
"""
Created on Mon Dec 17 11:07:46 2017

@author: Jane
"""

import sqlite3 as db
import pandas as pd
from matplotlib import pyplot as plt
def read_amazon():
    '''
    读取存放在sqlite里的亚马逊商品数据
    '''
    con = db.connect(r"C:\Users\Iris\Desktop\yelp标注数据集_欺诈检测\yelpResData.db")
    con.text_factory = lambda x: str(x, 'latin1')
    df = pd.read_sql_query(
            "select * from review where restaurantID='HOJqzz1WvOmeR9oESJ4d9A'and (flagged=='N'or flagged=='Y')",
            con=con)
    print(df.shape)
    print(df.dtypes)
    print(df.head())
    return df
def read_new(meta_path,review_path): 		#读Yelp数据，并把meta数据与review合并
    meta_file=open(meta_path,'r',encoding="utf-8")
    review_file=open(review_path,'r',encoding="utf-8")
    review_content=[]
    user_id=[]
    prod_id=[]
    rating=[]
    label=[]
    date=[]
    line=meta_file.readline()
    while line:
        split=line.split()
        user_id.append(split[0])
        prod_id.append(split[1])
        rating.append(split[2])
        label.append(split[3])
        date.append(split[4])
        line=meta_file.readline()
    meta_file.close()
    data=pd.DataFrame({'user_id':user_id,'prod_id':prod_id,'rating':rating,'label':label,'date':date})
    print("The shape of data without review content:\n",data.shape)

    rline=review_file.readline()
    while rline:
        split=rline.split("\t")
        review_content.append(split[3])
        rline=review_file.readline()
    review_file.close()
    data['reviewContent']=pd.Series(review_content,index=data.index)
    print('The combined data:\n',data.shape,'\nData Sample:\n',data.head(5))
    # data.to_csv('./result/dataset.csv',sep='\t',encoding="utf-8")
    return data

if __name__ == '__main__':
    m_path='YelpZip/metadata'
    r_path='YelpZip/reviewContent'
    dataset=read_new(m_path,r_path)
    print('Emerging finishe!\n')
