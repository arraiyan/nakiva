import pickle
from time import timezone
import pandas as pd
from datetime import datetime
from init import join
def openfile(file_name):
    file = open(join(file_name),'rb')
    data = pickle.load(file)
    file.close()
    return data
def write(new_data):
    current_data = openfile('airdrop.pickle')
    file = open('airdrop.pickle','wb')
    if not new_data in current_data:
        current_data.append(new_data)
    pickle.dump(current_data,file)
    file.close()
    #(current_data)
    return (len(current_data)-1)
    #0     1               2            3              4         5               6           7        8          9
# chat_id telegram_id wallet_address fb_link twitter_link number_of_refrall total_income   Refrral_link Total Tokens
def getexcel():
    file = open('airdrop.pickle','rb')
    data = pickle.load(file)
    file.close()
    df1 = pd.DataFrame(data,columns=['col 1', 'col 2','col3','Youtube_user_name','col5','col6','col7','col8','col9','col10'])
    n = str(f'static/aridrop{datetime.date(datetime.now())}.xlsx')
    df1.to_excel(n)
    return n