import os
import pickle
def join(name):
    pwd = ''
    return os.path.join(pwd, name)
def save_dict(data,id_):
    file = open('trace.pickle','rb')
    current_data = pickle.load(file)
    file.close()
    # current_data = data
    file = open('trace.pickle','wb')
    if not id_ in current_data:
        current_data[id_]=data
    pickle.dump(current_data,file)
    file.close()
    #(current_data)
    return
def get_data(file_name):
    file = open(join(file_name),'rb')
    current_data = pickle.load(file)
    file.close()
    return current_data
# save_dict(0,2)
# #(get_data('trace.pickle'))