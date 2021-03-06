import pandas as pd
import streamlit as st
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer, ENGLISH_STOP_WORDS
from sklearn.metrics.pairwise import linear_kernel
from PIL import Image
import matplotlib.pyplot as plt

preimg = {}

def cocktail_recommender(cocktail_name, similarity_df, cocktails_df, num_recommendations=10):

    '''
    This function gets cocktail_name and provides recommendations using similarity values.

    inputs:
    cocktail_name (str): Name of a cocktail provided by the user.
    similarity_df (pandas dataframe): Dataframe that contains similarity values between cocktails
    cocktails_df (pandas dataframe): Dataframe that contains cocktails with recipes and ingredients
    num_recommendations (int): Number of recommendations 

    outputs:
    recommendations_df (pandas dataframe): Dataframe that contains recommended cocktails with recipes and ingredients
    
    '''



    recommendations = similarity_df[cocktail_name].sort_values(ascending=False)[1:num_recommendations]
    recommendations.name = 'Similarity'
    
    cocktails_details = cocktails_df[cocktails_df['Cocktail Name'].isin(recommendations.index)].set_index('Cocktail Name')
    # print('recommendations:')
    # print(cocktails_details.index, )
    recommendations_df = pd.concat([cocktails_details,recommendations], axis=1).sort_values(by='Similarity', ascending=False)
    
    return recommendations_df



def etl_function():


    '''
    This function employs Extract Transform Load (ETL) pipeline.
    The function reads data from csv files, merges the datasets, preprocess data, 
    applies tf-idf vectorizer, calculates cosine similarities between vectors.


    Inputs: None
    
    Outputs:
    similarity_df (pandas dataframe): Dataframe that contains similarity values between cocktails
    cocktails_df (pandas dataframe): Dataframe that contains cocktails with recipes and ingredients
    vectorizer (sklearn class): Tf-idf vectorizer class fit to the data

    '''



    cocktails_df1 = pd.read_csv('./appDB/cocktails1.csv')
    cocktails_df2 = pd.read_csv('./appDB/newcocktails_db1.csv')
    cocktails_df = pd.concat([cocktails_df1, cocktails_df2], axis=0)

    cocktails_df['Cocktail Name'] = cocktails_df['Cocktail Name'].str.upper()

    cocktails_df.drop(columns=['Bartender', 'Location', 'Bar/Company', 'Glassware', 'Notes'], inplace=True)
    
    cocktails_df.drop_duplicates(subset='Cocktail Name', inplace=True)

    cocktails_df.fillna('', inplace=True)

    cocktails_df['All Ingredients'] = cocktails_df['Ingredients'] + ',' + cocktails_df['Garnish']
    # print(cocktails_df['All Ingredients'])
    additional_stop_words = frozenset(['oz', 'simple', 'dash', 'bsp', 'drops'])

    cocktail_stop_words = ENGLISH_STOP_WORDS.union(additional_stop_words)

    vectorizer = TfidfVectorizer(stop_words=cocktail_stop_words, token_pattern=r'\b[^\d\W][^\d\W]+\b')
    # print(cocktail_stop_words)
    tfidf_matrix = vectorizer.fit_transform(cocktails_df['All Ingredients'])

    cocktail_feature_df = pd.DataFrame(tfidf_matrix.toarray() ,columns=vectorizer.get_feature_names(), index=cocktails_df['Cocktail Name'])

    similarity_matrix = linear_kernel(tfidf_matrix, tfidf_matrix)

    similarity_df = pd.DataFrame(similarity_matrix, columns=cocktail_feature_df.index, index=cocktail_feature_df.index)
    
    
    # similarity_df.to_csv('etl1.csv', index=False)
    # cocktails_df.to_csv('etl2.csv', index=False)
    # print(vectorizer)
    return similarity_df, cocktails_df, vectorizer




def print_given_cocktail(user_input, cocktails_df):


    '''
    This function prints the details of the given cocktail by the user.
    
    inputs:
    user_input (str): Name of a cocktail provided by the user.
    cocktails_df (pandas dataframe): Dataframe that contains cocktails with recipes and ingredients
    
    Output: None
    '''
    given_cocktail = {}
    provided_cocktail = cocktails_df[cocktails_df['Cocktail Name'] == user_input]
    
    image = provided_cocktail['Image'].iloc[0]
    name = provided_cocktail['Cocktail Name'].iloc[0]
    ingredients = provided_cocktail['Ingredients'].iloc[0]
    garnish = provided_cocktail['Garnish'].iloc[0]
    preparation = provided_cocktail['Preparation'].iloc[0]
    
    given_cocktail['image'] = image
    given_cocktail['name'] = name
    given_cocktail['ingredients'] = ingredients
    given_cocktail['garnish'] = garnish
    given_cocktail['preparation'] = preparation
    
    # st.markdown("**Given Cocktail is** {}".format(name))
    # st.markdown("Ingredients: {}".format(ingredients))
    # st.markdown("Garnish: {}".format(garnish))
    # st.markdown("Preparation: {}".format(preparation))
    return given_cocktail




def recommend_cocktail_key_in_database(user_input, similarity_df, cocktails_df, number_of_recommendations):


    '''
    This function is called when user given cocktail name is present in the database. 
    It uses cocktail_recommender function to give single recommendation. It plots bar chart and prints
    recommendations for the web app. 

    inputs:
    user_input (str): Name of a cocktail provided by the user.
    similarity_df (pandas dataframe): Dataframe that contains similarity values between cocktails
    cocktails_df (pandas dataframe): Dataframe that contains cocktails with recipes and ingredients
    number_of_recommendations (int): Number of recommendations 

    Output: None
    '''


    recommended = cocktail_recommender(cocktail_name=user_input, similarity_df=similarity_df, cocktails_df=cocktails_df)

    chart_data = similarity_df[user_input].sort_values(ascending=False)[1:6]
    fig, ax = plt.subplots()
    ax.barh(chart_data.index, chart_data.values)
    ax.invert_yaxis()
    ax.set_title('Similarities to given cocktail')
    # st.pyplot(fig)
   

    # image = Image.open('./great_gatsby.jpg')
    # st.image(image, use_column_width=True)

    # st.success('Recommended based on the name of cocktail provided!')
    temp_dict ={}
    recommend_cocktailList = []
    for i in range(0,number_of_recommendations):
        name = recommended.iloc[i].name
        image = recommended.iloc[i].Image
        print('image url: '+ image)
        j = i
        while image == '':
            j += 4
            if len(recommended)<=j:
                j = len(recommended)-1
            image = recommended.iloc[j].Image
            preimg[name] = image
        ingredients = recommended.iloc[i].Ingredients
        garnish = recommended.iloc[i].Garnish
        preparation = recommended.iloc[i].Preparation
        
        temp_dict['image'] = image
        temp_dict['name'] = name
        temp_dict['ingredients'] = ingredients
        temp_dict['garnish'] = garnish
        temp_dict['preparation'] = preparation
        
        recommend_cocktailList.append(dict(temp_dict))
        
        # st.markdown("**Recommended Cocktail is** {}".format(name))
        # st.markdown("Ingredients: {}".format(ingredients))
        # st.markdown("Garnish: {}".format(garnish))
        # st.markdown("Preparation: {}".format(preparation))
        # st.text("\n")
        # st.text("\n")
    
    print(recommend_cocktailList) 
    
    # my_expander = st.beta_expander('Show more recommendations')
    # with my_expander:
            
    #     for i in range(2, number_of_recommendations):

    #         name = recommended.iloc[i].name
    #         ingredients = recommended.iloc[i].Ingredients
    #         garnish = recommended.iloc[i].Garnish
    #         preparation = recommended.iloc[i].Preparation

    #         # st.markdown("**Recommended Cocktail is** {}".format(name))
    #         # st.markdown("Ingredients: {}".format(ingredients))
    #         # st.markdown("Garnish: {}".format(garnish))
    #         # st.markdown("Preparation: {}".format(preparation))
    #         # st.text("\n")
    #         # st.text("\n")
            

    return recommend_cocktailList
    



def recommend_cocktail_similarity_to_ingredients(user_input, cocktails_df, vectorizer, number_of_recommendations):
    print('test')
    
    '''
    This function is called when user input is the ingredients present in the database. 
    It applies tf-idf vectorization to user input, calculates cosine similarities and 
    prints recommendations for the web app. 

    inputs:
    user_input (str): Name of a cocktail provided by the user.
    cocktails_df (pandas dataframe): Dataframe that contains cocktails with recipes and ingredients
    vectorizer (sklearn class): Tf-idf vectorizer class fit to the data
    number_of_recommendations (int): Number of recommendations 

    Output: None
    '''


    tfidf_matrix = vectorizer.transform(cocktails_df['All Ingredients'])
    # print('tfidf_matrix', tfidf_matrix)
    # print()
    user_input_vector = vectorizer.transform([user_input])
    # print('user_input_vector', user_input_vector)
    # print()
    similarity_vector = linear_kernel(tfidf_matrix, user_input_vector)
    # print('similarity_vector', similarity_vector)
    # print()
    similarity_pd = pd.DataFrame(similarity_vector, columns=['Similarity'], index=cocktails_df['Cocktail Name']).sort_values(by='Similarity', ascending=False)
    # print('similarity_pd', similarity_pd)
    # print()
    
    temp_dict ={}
    recommend_cocktailList = []
    if similarity_pd.iloc[0]['Similarity'] > 0.1:

        for i in range(0, number_of_recommendations):
            name = similarity_pd.iloc[i].name
            image = cocktails_df[name == cocktails_df['Cocktail Name']]['Image'].iloc[0]
            j = i
            while image == '':
                j+=4
                image = cocktails_df[similarity_pd.iloc[j].name == cocktails_df['Cocktail Name']]['Image'].iloc[0]
                preimg[name] = image
            ingredients = cocktails_df[name == cocktails_df['Cocktail Name']]['Ingredients'].iloc[0]
            garnish = cocktails_df[name == cocktails_df['Cocktail Name']]['Garnish'].iloc[0]
            preparation = cocktails_df[name == cocktails_df['Cocktail Name']]['Preparation'].iloc[0]

            # st.markdown("**Recommended Cocktail is** {}".format(name))
            # st.markdown("Ingredients: {}".format(ingredients))
            # st.markdown("Garnish: {}".format(garnish))
            # st.markdown("Preparation: {}".format(preparation))
            # st.text("\n")
            # st.text("\n")
            print("**Recommended Cocktail is** {}".format(name))
            print("Ingredients: {}".format(ingredients))
            print("Garnish: {}".format(garnish))
            print("Preparation: {}".format(preparation))
            print("\n")
            print("\n")
            temp_dict['image'] = image
            temp_dict['name'] = name
            temp_dict['ingredients'] = ingredients
            temp_dict['garnish'] = garnish
            temp_dict['preparation'] = preparation
            
            recommend_cocktailList.append(dict(temp_dict))
        # image = Image.open('./ingredient.jpg')
        #st.image(image, use_column_width=True)
        #st.success('Recommended based on the ingredients provided!')


        # my_expander = st.beta_expander('Show more recommendations')
        # with my_expander:


        #     for i in range(2, number_of_recommendations):

        #         name = similarity_pd.iloc[i].name
        #         ingredients = cocktails_df[name == cocktails_df['Cocktail Name']]['Ingredients'].iloc[0]
        #         garnish = cocktails_df[name == cocktails_df['Cocktail Name']]['Garnish'].iloc[0]
        #         preparation = cocktails_df[name == cocktails_df['Cocktail Name']]['Preparation'].iloc[0]

        #         # st.markdown("**Recommended Cocktail is** {}".format(name))
        #         # st.markdown("Ingredients: {}".format(ingredients))
        #         # st.markdown("Garnish: {}".format(garnish))
        #         # st.markdown("Preparation: {}".format(preparation))
        #         # st.text("\n")
        #         # st.text("\n")
        #         print("**Recommended Cocktail is** {}".format(name))
        #         print("Ingredients: {}".format(ingredients))
        #         print("Garnish: {}".format(garnish))
        #         print("Preparation: {}".format(preparation))
        #         print("\n")
        #         print("\n")

        return recommend_cocktailList
    else:
        # st.error('Please provide more information.')
        print('Error : not found')
        print()
        # image = Image.open('./error_image.jpg')
        # st.image(image, use_column_width=True)
        return []

def getImg(name):
    return preimg[name]