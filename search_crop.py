import pandas as pd
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity 
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer 

def search(name):
    df=pd.read_csv("crop.csv")
    df['Sno'] = np.arange(len(df))
    crops=df.label.unique().tolist()

    combinedDF=[]
    for i in range(len(crops)):
        k=df[df["label"]==crops[i]]["Sno"].tolist()[0]
        combinedDF.append(str(df[df["Sno"]==k]["N"].values[0])+" "+str(df[df["Sno"]==k]["P"].values[0])+" "+str(df[df["Sno"]==k]["K"].values[0])+" "+str(df[df["Sno"]==k]["temperature"].values[0]))
    feature_extraction=TfidfVectorizer(stop_words='english',min_df=1)
    
    combinedDF=feature_extraction.fit_transform(combinedDF)
    m=name
    m=m.lower()
    similarity=cosine_similarity(combinedDF)
    similar_crops=difflib.get_close_matches(m,crops)

    if len(similar_crops)!=0:
        similar_index=-1
        for i in range(len(crops)):
            if crops[i] == similar_crops[0]:
                similar_index=i
                break
        if similar_index!=-1:
            similar_crop_indexes=list(enumerate(similarity[similar_index]))
            similar_crop_indexes=sorted(similar_crop_indexes,key=lambda x:x[1],reverse=True)
            rest_crops=[]
            for i in range(0,4):
                rest_crops.append(crops[similar_crop_indexes[i][0]])
            return(rest_crops)
        else:
            return(-1)
    else:
        return(-1)