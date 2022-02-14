
import pickle
#         #  0   1  2  3  4  5  6  7

data = {0:0}

file = open('trace.pickle',"wb")
pickle.dump(data,file)
file.close()
# print(data)
data = [['id', 'username', 'twitter username', 'youtube username', 'bep20 address', 'mail', 'no. of persons referred','referred by','referral link' ,'Hash']]

# print(data)
file = open('airdrop.pickle',"wb")
pickle.dump(data,file)
file.close()


