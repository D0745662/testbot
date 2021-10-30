import pandas as pd
import streamlit as st
import utils1 as utils
#from utils.utils import *


#st.title("Cocktail Recommender")

#st.markdown("Cocktail Recommender is a tool that recommends cocktails based on provided cocktail name or ingredients. You can provide name of a cocktail to find similar cocktails to it or you can write ingedients you like and get recommendations based on that.")

user_input = '155 Belmont'.upper() #st.text_input(label="Please write a cocktail name.").upper()

number_of_recommendations = 5

#算餘弦相似度、 cocktaildb 、向量
similarity_df, cocktails_df, vectorizer = utils.etl_function()


if user_input in cocktails_df['Cocktail Name'].tolist():
    print('in database== is cocktail name')
    #輸出given cocktail的Description
    utils.print_given_cocktail(user_input=user_input, cocktails_df=cocktails_df)
    #推薦 經過嚴選最適合given input 的 cocktails
    utils.recommend_cocktail_key_in_database(user_input=user_input, similarity_df=similarity_df, cocktails_df=cocktails_df, number_of_recommendations=number_of_recommendations)

    
elif user_input:
    print('not in database== is ingredient')
    #推薦 透過 given ingredient 找出 類似成分的 cocktails
    utils.recommend_cocktail_similarity_to_ingredients(user_input=user_input, cocktails_df=cocktails_df, vectorizer=vectorizer, number_of_recommendations=number_of_recommendations)

else:
    pass





