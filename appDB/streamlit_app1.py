import pandas as pd
import streamlit as st
import sys
import utils1
# from utils import utils1
#st.title("Cocktail Recommender")

#st.markdown("Cocktail Recommender is a tool that recommends cocktails based on provided cocktail name or ingredients. You can provide name of a cocktail to find similar cocktails to it or you can write ingedients you like and get recommendations based on that.")
def getCocktailDetail(string):
    user_input = string.upper()
    similarity_df, cocktails_df, vectorizer = utils1.etl_function()
    
    return utils1.print_given_cocktail(user_input=user_input, cocktails_df=cocktails_df)

# 檢查 輸入 是否有在料庫
# @params string [單一酒品名] 輸入
# @return bool 是或否
def checkCocktailinDB(string):
    similarity_df, cocktails_df, vectorizer = utils1.etl_function()
    user_input = string.upper().strip()
    if user_input in cocktails_df['Cocktail Name'].tolist():
        return True
    else:
        return False


# 執行推薦 -- 主要推薦動作func
# @params string [單一酒品名、多個成分] 輸入 
# @params numbnumber_of_recommendationser 推薦酒品數量 
# @return recommend_list 推薦清單
def doCocktailAnalyDB(string, number_of_recommendations = 5):
    # user_input = '155 Belmont'.upper() #st.text_input(label="Please write a cocktail name.").upper()

    user_input = string.upper().strip()
    #算餘弦相似度、 cocktaildb 、向量
    similarity_df, cocktails_df, vectorizer = utils1.etl_function()
    recommend_cocktailList = []
    
    if user_input in cocktails_df['Cocktail Name'].tolist():
        print('in database== is cocktail name')
        #輸出given cocktail的Description
        utils1.print_given_cocktail(user_input=user_input, cocktails_df=cocktails_df)
        #推薦 經過嚴選最適合given input 的 cocktails
        recommend_cocktailList = utils1.recommend_cocktail_key_in_database(user_input=user_input, similarity_df=similarity_df, cocktails_df=cocktails_df, number_of_recommendations=number_of_recommendations)
        
        
    elif user_input:
        print('not in database == is ingredient')
        print('renew12')
        #推薦 透過 given ingredient 找出 類似成分的 cocktails
        recommend_cocktailList = utils1.recommend_cocktail_similarity_to_ingredients(user_input=user_input, cocktails_df=cocktails_df, vectorizer=vectorizer, number_of_recommendations=number_of_recommendations)
    
    else:
        pass
    
    return recommend_cocktailList


def getImg(name):
    return utils1.getImg(name)
# print(sys.path)

# doCocktailAnalyDB('155 belmont',3)



