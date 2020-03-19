# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 13:56:36 2020

@author: Dhamodaran
"""

import csv

# data science imports
import pandas as pd
from sklearn.neighbors import NearestNeighbors

# utils import
from fuzzywuzzy import fuzz

class recommendation_system:
    def __init__(self):
        self.model = NearestNeighbors(algorithm='brute',metric='cosine',n_jobs=None)
    
    def content_based_recommender(self,user):
        job_ids=[]
        with open("E:\machine learning\ML PROJECTS\job recommendation system\job details.csv",'r') as job_file:
            csv_obj=csv.reader(job_file)
            for row in csv_obj:
                if len(job_ids)<3:
                    if user.domain==row[2]:
                            if user.sub_domain==row[3]:
                                flag=False
                            if user.field==row[4]:
                                flag=True
                                if (fuzz.partial_ratio(row[5].lower(),user.skillset.lower())) >60 :
                                    if user.emp_score<=int(row[6]):
                                        job_ids.append([row[0],row[1]])
                                    
                                if len(job_ids)<3 and flag==False:
                                    if user.emp_score<=int(row[6]):
                                        job_ids.append([row[0],row[1]])
                                
                            
        if len(job_ids)==0:
            print("Oops!!No matching jobs found")
            return None
        print("The students with match with Your profile are")
        for job_name,job_id in job_ids:
            print(job_name)
        return job_ids
    
    def content_recommender(self,job_name,job_ids):
        req_sub_domain=[]
        req_field=[]
        req_job_id=[]
        hash_map=dict()
        with open("E:\machine learning\ML PROJECTS\job recommendation system\job details.csv",'r') as job_file:
            csv_obj=csv.reader(job_file)
            for row in csv_obj:
                if row[0]==job_name:
                    req_sub_domain.append(row[3])
                    req_field.append(row[4])
        sub_domain=req_sub_domain[0]
        field=req_field[0]
        del req_sub_domain,req_field
        job_idss=[]
        for i in range(0,len(job_ids)):
            job_idss.append(job_ids[i][0])
        del job_ids
        with open("E:\machine learning\ML PROJECTS\job recommendation system\job details.csv",'r') as job_file:
            csv_obj=csv.reader(job_file)
            for row in csv_obj:
                if row[3]==sub_domain and row[0]!=job_name:
                    if row[4]==field:
                        if row[1] not in job_idss:
                            req_job_id.append(row[1])
                            hash_map[row[1]]=row[0]
        return req_job_id,hash_map
        
    def data_extraction(self,job_name,job_ids):
        data=[]
        req_job_id,hash_map=self.content_recommender(job_name,job_ids)
        with open("E:\machine learning\ML PROJECTS\job recommendation system\job feedback score.csv",'r') as job_file:
            csv_obj=csv.reader(job_file)
            for row in csv_obj:
                if (row[0] in req_job_id):
                    data.append(row[1:50])
        data_matrix=pd.DataFrame(data)
        del data
        data_matrix=data_matrix.transpose()
        lst=data_matrix.values.tolist()
        del data_matrix
        data=pd.DataFrame(lst,columns=req_job_id)
        del lst
        return data,hash_map,req_job_id
    
    def inference(self,model,job_name,job_ids):
        data,hash_map,req_job_id=self.data_extraction(job_name,job_ids)
        data=data.transpose()
        self.model.fit(data)
        dist,ind=self.model.kneighbors(data,n_neighbors=3)
        #ic=0
        #for i in ind:
            #jc=0
            #for j in i:
                #if jc==0:
                    #print("The nearest neighbors of the job",hash_map[req_job_id[j]],"are as follows:")
                #elif jc>0:
                    #print(hash_map[req_job_id[j]],"\tdistance",dist[ic][jc])
                #jc+=1
            #ic+=1
       
        return dist,ind,hash_map,req_job_id
            
    def score_prediction(self,job_name,job_ids):
        dist,ind,hash_map,req_job_id=self.inference(self.model,job_name,job_ids)
        avg=[]
        with open("E:\machine learning\ML PROJECTS\job recommendation system\job feedback score.csv",'r') as job_file:
            csv_obj=csv.reader(job_file)
            for row in csv_obj:
                if (row[0] in req_job_id):
                   sum1=0.00
                   for k in range(1,101):
                       sum1+=float(row[k])
                   ans=sum1/100
                   avg.append(ans)
        job_guess=dict()    
        ic=0
        for i in ind:
            jc=0
            num_sum=0
            denom_sum=0
            for j in i:
                if jc>0:
                    num_sum=(1/dist[ic][jc])*avg[j]
                    denom_sum+=(1/dist[ic][jc])
                jc+=1
            ic+=1
            job_guess[hash_map[req_job_id[j]]]=(float(num_sum/denom_sum))
        print("The predicted score")
        print(job_guess)
        return job_guess
            
               
    def recommend(self,user):
        job_ids=self.content_based_recommender(user)
        if len(job_ids)!=0:
            for i in range(0,len(job_ids)):
                job_guess=self.score_prediction(job_ids[i][0],job_ids)
                print(job_ids[i][0])
                n_recommendations=3
                i=1
                for key,value in sorted(job_guess.items(),key=lambda item:item[1],reverse=True):
                    print(key)
                    if i==n_recommendations:
                        break
                    i+=1
                
class User:
    
    def get_details(self):

        self.j_name=input("Enter the jobs which you already know(enter comma between jobs)")
        self.domain=input("Enter the doamin which you are interested in")
        self.sub_domain=input("Enter the sub-doamin that you are interested in")
        self.field=input("Enter the field in which you are looking for:")
        self.skillset=input("Enter the skillsets you prefer:")
        self.emp_score=int(input("enter emp score"))
    



    
if __name__ == '__main__':
    print("\t\t WELCOME TO job RECOMMENDATION SYSTEM")
    user=User()
    user.get_details()
    recommender = recommendation_system()
    recommender.recommend(user)