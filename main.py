#welcome
#Captcha
# data et chat_id user_name  're tweet link', 'facebook username', 'bep20 address', 'mail', 'no. of persons referred','referred by'
# ⚒ 📉 ⚠️ 🚸 ✅ ➡️ 💲 🔜


from telegram import *
from telegram.ext import *
from captcha.image import ImageCaptcha
import time
import random
import requests
import init
import save
import pickle
import datetime
from inf import env

def getcsv(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        #(update.message.from_user.id)
        if update.message.from_user.id in env.adminlist:
            from save import getexcel
            context.bot.send_document(chat_id=update.effective_chat.id, document=open(getexcel(), 'rb'))
            return
        else:
            #('not admin')
            update.message.reply_text(f'You are not logged in type (/login #password) to login ')
            return

def add_group(update: Update, context: CallbackContext) -> None:
    print(update.message.chat.type)
    if not update.message.chat.type == 'private':
        #(update.message.from_user.id)
        if update.message.from_user.id in env.adminlist:
            env.GroupName = update.message.chat.id
            print(f'Group name was updated ',env.GroupName)
            return
        else:
            #('not admin')
            update.message.reply_text(f'You are not logged in type (/login #password) to login\n\n !!! Note please do this action in private Chat')
            return

def set_primary_balance(update:Update,context:CallbackContext)->None:
    if update.message.chat.type == 'private':
        if update.message.from_user.id in env.adminlist:
            text = str(update.message.text).split()
            chat_id = text[1]
            new_value = text[2]
            env.users[str(chat_id)]['data'][9]=int(env.users[str(chat_id)]['data'][9])-100+int(new_value)
            new_b = env.users[str(chat_id)]['data'][9]
            Adata = init.get_data('airdrop.pickle')
            trace = init.get_data('trace.pickle')
            Adata[trace[update.message.chat.id]] = env.users[str(chat_id)]['data']
            file = open('airdrop.pickle','wb')
            pickle.dump(Adata,file)
            file.close()
            try:
                update.message.reply_text('Succesfully update databasae')
                context.bot.send_message(chat_id = chat_id , text = f'Your Balance was modified .By the admins . Thank you .\n\nYour new balance is {new_b}')

                return
            except:
                update.message.reply_text('Succesfully update databasae')
                return
            return
        else:
            #('not admin')
            update.message.reply_text(f'You are not logged in type (/login #password) to login ')
            return
    

    return
#Trace the group join
def new_member(update: Update, context: CallbackContext)    -> None:

    env.user_id.append(update.message.chat.id)

    return
#Start
def Welcome(update: Update, context: CallbackContext) -> None:

    if not update.message.chat.id in env.user_list_news:
        env.user_list_news.append(update.message.chat.id)
        dd1 = init.get_data("user_ids.pickle")
        for i in env.user_list_news:
            if not i in dd1:
                dd1.append(i)
        pickle.dump(dd1,open('user_ids.pickle',"wb"))
        #(dd1)

    if update.message.chat.type=='private':
        ref_id = update.message.text.split()
        user = update.effective_user
        context.bot.send_message(chat_id = update.effective_chat.id , text = env.welcome_txt ,parse_mode='HTML')
        #coustom key collect airdrop

        reply_markup = ReplyKeyboardMarkup(env.CollectAirdropKey,resize_keyboard=True)
        update.message.reply_text("Press (Start Earning) button to start",
                        reply_markup=reply_markup)

        if len(ref_id)==2:
            ch_id = int(ref_id[1])
            if not update.message.chat.id in env.l1:
                env.l1.append(update.message.chat.id)
                d1 = init.get_data('trace.pickle')[ch_id]
                d2 = save.openfile('airdrop.pickle')
                d2[d1][6]=f'{int(d2[d1][6])+1}'
                d2[d1][7] = str(ch_id)
                d2[d1][9] = int(d2[d1][9])+env.PerRefToken
                file = open('airdrop.pickle','wb')
                pickle.dump(d2,file)
                file.close()
                return
    return
############ opening part
def CollectAirdrop(update:Update,context:CallbackContext)->None:
    user_name = update.message.from_user.username
    if update.message.chat.type=='private':
        chat_id = update.effective_chat.id
        opts = list()#captcha list
        for i in range(4):
            opts.append(str(random.randint(0,999)))

            #                                                                                                                      0                     1   2   3   4  5  6      7           8                                                             9
            #
            #                                       #0 starts after entering the wallet address                                    1                     2    3  4  5   6  7      8           9                                                             10
        d = {'chat_id':update.effective_chat.id,'steps':int(0),'WalletAddStat':False,'captch_status':True,'captcha':'' ,'data':[str(chat_id),f'@{user_name}','','','0','',int(0),str(),str(f'https://t.me/{env.BotName}?start={update.effective_chat.id}'),int(0)]}
        env.users[str(update.effective_chat.id)] = d
        #captcha part
        image = ImageCaptcha(fonts=['font/LGB.ttf'])
        txt = str(opts[int(random.randint(0,3))])
        env.users[str(update.effective_chat.id)]['captcha'] = txt
        im = image.generate(env.users[str(update.effective_chat.id)]['captcha'] )
        time.sleep(0.3)
        context.bot.send_photo(chat_id = update.effective_chat.id,photo = im)
        time.sleep(0.3)
        update.message.reply_text("Please, Enter The Numbers Shown In The Image Above")
    else:
        update.message.reply_text("please do this action in private")
#Check the group joining
def CHECK(update: Update, context: CallbackContext)    -> None:
    if update.message.chat.type=='private':
        CurrentMemberData = context.bot.get_chat_member(chat_id=env.GroupName,user_id = update.message.from_user.id).to_dict()
        print(CurrentMemberData)
        #(CurrentMemberData)
        if (CurrentMemberData['status'] == 'creator') or (CurrentMemberData['status'] == 'member') or (CurrentMemberData['status'] == 'administrator') or (CurrentMemberData['status'] == 'restricted'):
            reply_markup = ReplyKeyboardRemove()
            context.bot.send_message(chat_id=update.message.chat.id,text='👍 Great job!  You\'re profile has been confirmed.', reply_markup=reply_markup)
            reply_markup = ReplyKeyboardMarkup([['✅ Check Our Channel']],resize_keyboard=True)
            update.message.reply_text(text=env.JoinChannelMessage,
                                    reply_markup=reply_markup,parse_mode='HTML')
        else:
            time.sleep(0.52)
            reply_markup = ReplyKeyboardMarkup([['✅CHECK']],resize_keyboard=True)
            update.message.reply_text(f'⚠️ Sorry we did not find you profile withing our telegram channel.\n\n➡️ Please try joining again 👇\n\nhttps://t.me/nekiva_token',
                            reply_markup=reply_markup,parse_mode='HTML')
    return

def CHECKCHANNEL(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        CurrentMemberData = context.bot.get_chat_member(chat_id=env.ChannelName,user_id = update.message.from_user.id).to_dict()
        print(CurrentMemberData)
        #(data)
        if (CurrentMemberData['status'] == 'creator') or (CurrentMemberData['status'] == 'member') or (CurrentMemberData['status'] == 'administrator') or (CurrentMemberData['status'] == 'restricted'):
            reply_markup = ReplyKeyboardRemove()
            context.bot.send_message(chat_id=update.message.chat.id,text='👍 Excellent!  You have joined our channel.', reply_markup=reply_markup)
            env.users[str(update.effective_chat.id)]['WalletAddStat']=True
            update.message.reply_text(env.twitter_message,parse_mode='HTML')


        else:
            reply_markup = ReplyKeyboardMarkup([['✅ Check Our Channel']],resize_keyboard=True)
            update.message.reply_text(f'⚠️⚠️⚠️\n\nWe didnot find any trace of joining ..\n⚒⚒⚒ Please Rejoin the telegram channel then continue other tasks \n\n\n    ➡️ <a href="{env.ChannelLink}">Join channel</a>   ({env.ChannelLink})\n\n....',
                            reply_markup=reply_markup,parse_mode='HTML')
    return
#dash board
def CompletedPrimary(update: Update, context: CallbackContext) -> None:
    reply_markup = ReplyKeyboardMarkup(env.dashboard,resize_keyboard=True)
    update.message.reply_text("Welcome to Dashboard",
                    reply_markup=reply_markup)
    return

def admin(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type == 'private':
        if update.message.from_user.id in env.adminlist:
            reply_markup = ReplyKeyboardMarkup([['Total Users','DataBase']],resize_keyboard=True)

            update.message.reply_text("Welcome to Dashboard",
                            reply_markup=reply_markup)
            return
        else:
            update.message.reply_text(f'You are not logged in type (/login #password) to login ')
            return

    return

def username(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type=='private':
        data = init.get_data('trace.pickle')
        d2 = init.get_data('airdrop.pickle')
        df = d2[data[update.effective_chat.id]]
        update.message.reply_text(f'Your Provided Data:\n\n Name: {df[1]}\n\n Youtube Usename: {df[3]}\n\n bep20 Address: {df[4]}\n\n Total Reffered: {df[6]} \n\nPlease use /start to update the database ',parse_mode='HTML')
        return

def withdraw(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type=='private':
        update.message.reply_text(f'You would recieve withdrawl after 48 hours and review\n',parse_mode='HTML')
        for i in env.adminlist:
            try:
                chat_id = update.message.chat.id
                context.bot.send_message(chat_id = i , text = f'user with id {chat_id} requested a withdrawal')
            except:
                continue
        return

def Reffral(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type=='private':
        from init import get_data
        user_data = get_data('trace.pickle')[update.effective_chat.id]
        DataSheet = get_data('airdrop.pickle')[user_data][6]
        ref = f'💰⚡️ To increase your balance refer more friends using your referral link, you will earn {env.PerRefToken} for each person you refer.\n\n<b>🎁Referral link:   <code>https://t.me/{env.BotName}?start={update.effective_chat.id}</code>  👥You have {DataSheet} Referrals</b> \n\n '
        ref1 = f'Total reffered</b> {DataSheet}</b>\nTotal gained<b>{DataSheet*env.PerRefToken}</b>'
        update.message.reply_text(parse_mode='HTML',text=ref)
        return

def TotalBalance(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type=='private':
        data = init.get_data('trace.pickle')
        d2 = init.get_data('airdrop.pickle')
        df = d2[data[update.effective_chat.id]]
        a1 = env.PerRefToken
        a2 = 100
        txt = f'💵Balance: {a2} + {a1*int(df[6])}\n\n👥Total referrals: {df[6]}\n\n💰Total Balance: {a1*int(df[6])+a2}\n\n➡️ Click referral button to earn more 💰'
        update.message.reply_text(parse_mode='HTML' , text=txt)

        return

def about(update: Update, context: CallbackContext) -> None:
    update.message.reply_text(env.about_message,parse_mode='HTML')
    return

def support(update: Update, context: CallbackContext) -> None:
    if update.message.chat.type=='private':
        update.message.reply_text(f'🧰 Contact support: \n https://t.me/nekiva_token\n http://twitter.com/nekiva_org',parse_mode='HTML')
        return

def login(update:Update,context:CallbackContext)->None:
    user_id = update.message.from_user.id
    if update.message.chat.type == 'private':
        if not user_id in env.adminlist:
            echo = update.message.text
            inpu = echo.lstrip('/login').lstrip(' ')
            if inpu == env.password:
                env.adminlist.append(update.message.from_user.id)
                update.message.reply_text(f'You are successfully looged in use /admin to interact with dashboard else try /csv to get excel file')
                admin(update,context)
            else:
                update.message.reply_text("wrong Password .Please try again")

        else:
            update.message.reply_text(f'You are already looged in use /admin to interact with dashboard else try /csv to get excel file')


    return

def News_letters(update:Update,context:CallbackContext)->None:
    if update.message.chat.type=='private':
        user_id = update.message.from_user.id
        if user_id in env.adminlist:
            msg = update.message.text.lstrip('/newsletter')
            list_user = init.get_data('user_ids.pickle')
            #(list_user)
            for i in list_user:
                if not str(i) == str(user_id):
                    context.bot.send_message(chat_id = i,text = msg)
                else:
                    update.message.reply_text('Successfully sent the newsletter to the users')
        else:
            update.message.reply_text('login first')

        return

def total_users(update:Update,context:CallbackContext)->None:
    if update.message.chat.type=='private':
        import pickle
        file = open('airdrop.pickle','rb')
        data = pickle.load(file)
        list_user = init.get_data('user_ids.pickle')

        update.message.reply_text(f'Total new user is {len(data)-1}')
        return

def verify(screen_name):
    from twython import Twython
    import tweepy
    following = False
    try :
        auth = tweepy.OAuthHandler('XpxoBNrkfuoBOlvUqkcRLeOlW', 'km7sjihY17vaZForfoabjzzavtEhiZfPsb1JOY5vhg5ztXvutL')
        auth.set_access_token('1487760439530631169-N37EDl7BtvVm6Htmygy60PvPtJeGAH', 'dMJ8w9dDON4Box955rV6U6fSi60feTRMmWbeC4pqZ7MDk')
        api = tweepy.API(auth,wait_on_rate_limit=True)
        public_tweets = api.home_timeline()
        following = api.get_friendship(source_screen_name = screen_name,target_screen_name = 'nekiva_org')[0].following
        print(following)
    except:
        following = False
        pass
    return following

def echo(update: Update, context: CallbackContext) -> None:
    echo = update.message.text
    if update.message.chat.type == 'private':
        chat_id = update.effective_chat.id
        if env.users[str(update.effective_chat.id)]['captch_status']:
            if update.message.text == env.users[str(chat_id)]['captcha']:
                env.users[str(update.effective_chat.id)]['captch_status'] = False
                reply_markup = ReplyKeyboardRemove()
                context.bot.send_message(chat_id=chat_id,text='🎉 That\'s the correct code!', reply_markup=reply_markup)
                time.sleep(1)
                reply_markup = ReplyKeyboardMarkup([['✅CHECK']],resize_keyboard=True)
                update.message.reply_text(text=env.JoinGroupMessage,
                                reply_markup=reply_markup,parse_mode='HTML')
            else:
                update.message.reply_text('⚠️ Sorry you have entered an incorrect code, please try again 👍')
                time.sleep(1)
                CollectAirdrop(update,context)
        if env.users[str(chat_id)]['WalletAddStat']:
            if env.users[str(chat_id)]['steps']==0:
                if verify(str(update.message.text)):
                    env.users[str(chat_id)]['data'][2]=update.message.text                   
                    env.users[str(chat_id)]['steps']=env.users[str(chat_id)]['steps']+2#Youtube suscribe switch
                    update.message.reply_text(env.suscribe,parse_mode='HTML')
                    return
                else:
                    update.message.reply_text('⚠️WARNING - We did not find you following our Page.\n\n👉 Please re-enter your Twitter username (start with @) or profile link.')
                    return
            elif env.users[str(chat_id)]['steps']==2:
                if '@' in echo:
                    env.users[str(chat_id)]['data'][2]=update.message.text                   
                    env.users[str(chat_id)]['steps']=env.users[str(chat_id)]['steps']+1#Comment option
                    update.message.reply_text(env.you_tube_message,parse_mode='HTML')
                    return
                else:
                    update.message.reply_text('⚠️WARNING - We did not find your profile following our twitter page.\n\n👉 Please re-enter your Twitter username (start with @) or profile link.')
                    return
                
            elif env.users[str(chat_id)]['steps']==3:
                n = env.users[str(chat_id)]['data'][2]
                if '@' in str(echo):  
                    link = str(update.message.text)
                    env.users[str(chat_id)]['data'][3]=link
                    env.users[str(chat_id)]['data'][9]=int(env.first_join)
                    env.users[str(chat_id)]['steps']=env.users[str(chat_id)]['steps']+1#2 will be bep20
                    update.message.reply_text('🎉 Good job! Just one more step.',parse_mode='HTML')
                    update.message.reply_text(f'{env.submitt_wallet_message}',parse_mode='HTML')
                    return
                else:
                    update.message.reply_text('⚠️WARNING - Sorry we cannot locate your youtube username in the comment section please enter your youtube username properly with @ sign')
            #bep_20
            elif env.users[str(chat_id)]['steps']==4:
                m_text = str(update.message.text).lstrip(' ')
                if (str(m_text[0:2]) == str('0x')) and (len(m_text)>10):
                    env.users[str(chat_id)]['data'][4]=update.message.text
                    env.users[str(chat_id)]['steps']=str('completed')
                    t = datetime.date.today()
                    d=int(str(t.strftime('%d')))
                    m=int(str(t.strftime('%m')))
                    y=int(str(t.strftime('%Y')))
                    if (d>= env.airdrop_end_date) and (m==env.airdrop_end_month) :
                        env.users[str(chat_id)]['data'][9]=10
                    elif (m>env.airdrop_end_month) :
                        env.users[str(chat_id)]['data'][9]=10
                    Adata = init.get_data('airdrop.pickle')
                    trace = init.get_data('trace.pickle')
                    l1 = list()
                    for i,g in trace.items():
                        l1.append(i)
                    if not update.message.chat.id in l1:
                        from save import write
                        j = write(env.users[str(chat_id)]['data'])
                        from init import save_dict
                        save_dict(j,update.effective_chat.id)
                        #Data saaved
                        #Dash
                        CompletedPrimary(update,context)
                    else:
                        Adata[trace[update.message.chat.id]] = env.users[str(chat_id)]['data']
                        file = open('airdrop.pickle','wb')
                        pickle.dump(Adata,file)
                        file.close()
                        CompletedPrimary(update,context)
                else:
                    update.message.reply_text("⚠️⚠️⚠️ Please Send the wallet address Properly, on Metamask wallet your Bep-20 wallet starts with 0x ")
                return

def main() -> None:
    ##('env')
    data = init.get_data('airdrop.pickle')
    trace = init.get_data('trace.pickle')
    env.user_id = init.get_data("join_group_data.pickle")
    ##(trace)
    ##(f'user_id {env.user_id}')
    env.users =dict()
    for i,j in trace.items():
        env.l1.append(int(i))
    ##(f'l1>{env.l1}')
    for i,j in trace.items():
        env.users[str(i)]={'chat_id':int(i),'steps':"completed",'WalletAddStat':True,'captch_status':False,'captcha':'' ,'data':data[int(j)]}
    #{'chat_id':update.effective_chat.id,'steps':int(0),'WalletAddStat':False,'captch_status':True,'captcha':'' ,'data':[str(chat_id),f'@{user_name}','','','0','',int(0),str()]}
    #(env.users)
    updater = Updater(env.API_KEY)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", Welcome))
    dispatcher.add_handler(CommandHandler("login", login))
    dispatcher.add_handler(CommandHandler("admin", admin))
    dispatcher.add_handler(CommandHandler("dash", CompletedPrimary))
    dispatcher.add_handler(CommandHandler("csv", getcsv))
    dispatcher.add_handler(CommandHandler("edit",set_primary_balance ))
    dispatcher.add_handler(CommandHandler("add_group", add_group))
    # dispatcher.add_handler(CommandHandler("add_channel", getcsv))
    dispatcher.add_handler(CommandHandler("newsletter", News_letters))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'💲 Start Earning 💲'), CollectAirdrop))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'✅CHECK'), CHECK))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'✅ Check Our Channel'), CHECKCHANNEL))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'👨‍💻Profile'), username))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'👥Referral'), Reffral))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'💣Withdraw'), withdraw))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'📈About'), about))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'🧰Support'), support))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'💰Balance'), TotalBalance))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'DataBase'), getcsv))
    dispatcher.add_handler(MessageHandler(Filters.regex(r'Total Users'), total_users))
    dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))
    #Chechks if memeber is join on the group or not?
    updater.dispatcher.add_handler(MessageHandler(Filters.status_update.new_chat_members, new_member))



    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
