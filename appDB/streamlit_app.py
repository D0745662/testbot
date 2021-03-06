import pandas as pd
import streamlit as st
import utils
#from utils.utils import *


st.title("Cocktail Recommender")

st.markdown("Cocktail Recommender is a tool that recommends cocktails based on provided cocktail name or ingredients. You can provide name of a cocktail to find similar cocktails to it or you can write ingedients you like and get recommendations based on that.")

user_input = st.text_input(label="Please write a cocktail name.").upper()

number_of_recommendations = 5


similarity_df, cocktails_df, vectorizer = utils.etl_function()


if user_input in cocktails_df['Cocktail Name'].tolist():

    utils.print_given_cocktail(user_input=user_input, cocktails_df=cocktails_df)
    utils.recommend_cocktail_key_in_database(user_input=user_input, similarity_df=similarity_df, cocktails_df=cocktails_df, number_of_recommendations=number_of_recommendations)


elif user_input:
    utils.recommend_cocktail_similarity_to_ingredients(user_input=user_input, cocktails_df=cocktails_df, vectorizer=vectorizer, number_of_recommendations=number_of_recommendations)

else:
    pass





