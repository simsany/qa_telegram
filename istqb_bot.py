from pymongo import MongoClient
import requests
from telegram.ext import *
import random
client = MongoClient('mongodb+srv://sanyika:Nem99@cluster0.hg5xp.mongodb.net/orders?retryWrites=true&w=majority')
db=client['orders']
question_list=list(db['questions'].find())
good_answer=0





print('the bot started')
key='1778753485:AAG0y9lCd65wFdVTdMy5OOQoDboQJGQ65n4'

def responses(text):
    num=random.randint(0,len(question_list)-1)
    if text.lower() in ('i want a question','i want a question!','y','yes','skip'):
        q_text=question_list[num]['text']
        answers=question_list[num]['answers']
        shuffled_answers=random.sample(answers,len(answers))
        for index,item in enumerate(shuffled_answers):
            if item == answers[0]:
                shuffled_answers[index]=str(index+1)+'. '+item
                globals()['good_answer']=index+1
            else:
                shuffled_answers[index]=str(index+1)+'. '+item


        return q_text+'\n\n'+'Answers: \n\n'+'\n\n'.join(shuffled_answers)+'\n\nPlease enter the number of the correct answer\nor type "skip" for a new question!'
    
    if int(text) and int(text)==globals()['good_answer']:

        return 'Greaaaat! Want a new one?'

    if int(text) and not int(text) == globals()['good_answer']:

        return 'Not good! :( Try again! Or type "skip" for a new question'
    
    
    

def start_command(update,context):
    update.message.reply_text('''If you want a question, type:
    "yes"''')

def handle_message(update,context):
    text=str(update.message.text)
    reponse= responses(text)
    update.message.reply_text(reponse)

def main():
    updater=Updater(key,use_context=True)
    dp=updater.dispatcher
    dp.add_handler(CommandHandler("start",start_command))
    dp.add_handler(MessageHandler(Filters.text,handle_message))

    updater.start_polling()
    updater.idle()

main()