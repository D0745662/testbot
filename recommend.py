import pandas as pd
import numpy as np
import random
import sys

#把recommand list 裡的資料 篩選出之間相似度最高的 作為 推薦
def diy_score(profile_top30list, similarity):
    finalrecommand_list = dict()
    #計算 推薦cocktail list 中item之間的相似度， 進一步推薦更適合的cocktails
    for group_i, profile_i in enumerate(profile_top30list):
        for i, item_i in enumerate(profile_i[1]):
            sum = 0
            for group_j, profile_j in enumerate(profile_top30list):
                    for j, item_j in enumerate(profile_j[1]):
                        simi = pd.Series(similarity[profile_i[0][i]][profile_j[0][j]])
                        sum += item_j*simi
            finalrecommand_list[profile_i[0][i]] = float(sum)
    sortedlist = dict(sorted(finalrecommand_list.items(), key = lambda x: x[1], reverse=True))
    #print('final',sortedlist)
    
    result = []
    cnt = 0
    for key, value in sortedlist.items():
        cnt += 1
        if cnt > 10:
            break
        #print("{}:{}".format(key, value))
        result.append(key)  
    return result          


# So far only for a single name, to test the recommendations
def get_recommendation_list(profile_indices, count, similarity_file, eye_test = False, eval_test = False, extend_test = False):
  # Load similarity matrices, possibly add switch to choose which one to use in the future
  similarity = np.load('data/' + similarity_file + '.npy')
  
  # Indices of titles
  indices = pd.read_csv('data/indices.csv')
  
  # Get the index of the drink given in 'name'
  # idx = indices.Name[indices.Name == "Gin Sonic"].index[0]
 
  scores = []
  
  # Get the sorted scores on the indices .. creating Series gives us the ability to pair drink with its score and retrieve it based on its index
  for i in range(0, len(profile_indices)):
    scores.append(pd.Series(similarity[profile_indices[i]]).sort_values(ascending = False))
    
  top_count = []
  myscoreslist = []
  
  # Get the top 'count'
  for i in range(0, len(profile_indices)):
    top_count += list(scores[i].iloc[1:31].index)
    # ---MY CODE---
    #temp=[[indexArr],[相似度Arr]]對應
    temp = []
    temp.append(list(scores[i].iloc[1:16].index))
    temp.append(list(scores[i].iloc[1:16]))
    #myscoreslist=[profileArr[[indexArr],[相似度Arr]]] 
    myscoreslist.append(temp)

  recommended = []
	
  recommended = fill_recommendation_list(count, top_count, profile_indices)
	
  if eye_test:
    return recommended
	
  if eval_test:
    return top_count

  if extend_test:
    return diy_score(myscoreslist, similarity)
	
  return [get_drinks(recommended)]

  
# Fill the resulting list with drinks randomly from selected top few  
def fill_recommendation_list(count, list, profile):
  recommended = []
  while len(recommended) < count:
    drink = random.choice(list) 
    if drink not in recommended and drink not in profile:
      recommended.append(drink)	
  return recommended
  
  
# Convert index into a cocktail name, for lists  
def get_names(idxs):
  names = []
  indices = pd.read_csv('data/indices.csv')
  for drink in idxs:
    names.append(indices.Name[drink])
  return names 

def get_drink(id, drinks_file):
  if drinks_file is None:
    drinks_file = pd.read_csv('data/recipes.csv')
  return drinks_file.iloc[id].to_json()

def get_drinks(indices):
  drinks_file = pd.read_csv('data/recipes.csv')
  drinks = []
  for index in indices:
    drinks.append(get_drink(index, drinks_file))
  return drinks

# Eye test for easier output of names to console
# Eval test for comparing categories vs about + howto
# Extend test for optimize Eval test result 
def Recommend(profile_indices, count, eye_test = False, eval_test = False, extend_test = False):
  # categories_list = get_recommendation_list(profile_indices, count, 'categories_similarity', eye_test, eval_test)
  # about_howto_list = get_recommendation_list(profile_indices, count, 'about_howto_similarity', eye_test, eval_test)
  # combined_list = get_recommendation_list(profile_indices, count, 'combined_similarity', eye_test, eval_test)
  
  # categories_boosted_list = get_recommendation_list(profile_indices, count, 'categories_similarity_boosted', eye_test, eval_test)
  combined_boosted_list = get_recommendation_list(profile_indices, count, 'combined_similarity_boosted', eye_test, eval_test, extend_test)
  
  return [combined_boosted_list, combined_boosted_list, combined_boosted_list, combined_boosted_list, combined_boosted_list]
  
  
if __name__ == "__main__":
  
    profile = [27,60,80,1563,1012,861,457,950]
    
    rec_list = Recommend(profile, 10, False, True, False);
    # print("\nProfile: \n")
    # print(get_names(profile))
    # print("\n\nBased on Categories: \n")
    # print(get_names(rec_list[0]))
    # print("\n\nBased on About and How To: \n")
    # print(get_names(rec_list[1]))
    # print("\n\nBased on Both: \n")
    # print(get_names(rec_list[2]))
    # print("\n\nBased on Boosted Categories: \n")
    # print(get_names(rec_list[3]))
    print("\n\nBased on Boosted Combined: \n")
    print(get_names(rec_list[4]))
     
    rec_list = Recommend(profile, 10, True, False, False);
    # print("\nProfile: \n")
    # print(get_names(profile))
    # print("\n\nBased on Categories: \n")
    # print(get_names(rec_list[0]))
    # print("\n\nBased on About and How To: \n")
    # print(get_names(rec_list[1]))
    # print("\n\nBased on Both: \n")
    # print(get_names(rec_list[2]))
    # print("\n\nBased on Boosted Categories: \n")
    # print(get_names(rec_list[3]))
    print("\n\nBased on Boosted Combined: \n")
    print(get_names(rec_list[4]))
     
    rec_list = Recommend(profile, 10, False, False, True);
    # print("\nProfile: \n")
    # print(get_names(profile))
    # print("\n\nBased on Categories: \n")
    # print(get_names(rec_list[0]))
    # print("\n\nBased on About and How To: \n")
    # print(get_names(rec_list[1]))
    # print("\n\nBased on Both: \n")
    # print(get_names(rec_list[2]))
    # print("\n\nBased on Boosted Categories: \n")
    # print(get_names(rec_list[3]))
    print("\n\nBased on Boosted Combined: \n")
    print(get_names(rec_list[4]))
    print(get_drinks(rec_list[4]))
      
    # rec_list = Recommend(profile, 10, False, False, False);
    # # print("\nProfile: \n")
    # # print(get_names(profile))
    # # print("\n\nBased on Categories: \n")
    # # print(get_names(rec_list[0]))
    # # print("\n\nBased on About and How To: \n")
    # # print(get_names(rec_list[1]))
    # # print("\n\nBased on Both: \n")
    # # print(get_names(rec_list[2]))
    # # print("\n\nBased on Boosted Categories: \n")
    # # print(get_names(rec_list[3]))
    # print("\n\nBased on Boosted Combined: \n")
    # print(get_names(rec_list[4]))