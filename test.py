


# import pandas as pd
# import json
# df1 = pd.DataFrame([['a', 'b'], ['c', 'd']],columns=['col 1', 'col 2'])
# g = json.loads([['a', 'b'], ['c', 'd']])

# #(g)
# df1.to_excel("output.xlsx")
import pickle

#         #  0   1  2  3  4  5  6  7
data = {0:0}
file = open('trace.pickle',"wb")
pickle.dump(data,file)
file.close()
 
data = [['id', 'username', 'twitter username', 'Youtube username', 'bep20 address', 'mail', 'no. of persons referred','referred by','Refrral_link','Total_Gained_Tokens']]
file = open('airdrop.pickle',"wb")
pickle.dump(data,file)
file.close()



data = []
file = open('user_ids.pickle',"wb")
pickle.dump(data,file)
file.close()

data = list()
file = open('join_group_data.pickle',"wb")
pickle.dump(data,file)
file.close()
# file = open('dict.pickle','rb')
# example = pickle.load(file)
# #(type(example))
