import telebot
from telebot import apihelper
import numpy
import  PIL
from PIL import Image
import time
import subprocess
import os.path

bot = telebot.TeleBot("TOKEN")
apihelper.proxy = { 'https':'http://NAME:PASSWORD@000.000.00.000:00000/'}

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
	bot.reply_to(message, "Hello, to get 3D Recovery of your body you have to \n1) Send photo as file named ryota.png \n2) Send mask as file named ryota_mask.png \n3) Write /calc and after 15sec you will get the result \nTo get examples of photo and mask write /examples")

@bot.message_handler(commands=['examples'])
def send_example(message):
  doc = open('sample_images/ok_images/ryota.png', 'rb')
  bot.send_document(message.chat.id, doc)
  doc = open('sample_images/ok_images/ryota_mask.png', 'rb')
  bot.send_document(message.chat.id, doc)


@bot.message_handler(commands=['calc'])
def calc(message):
  bot.reply_to(message, "Calculating..... Please, wait 15 sec.")
  if os.path.exists('sample_images/ryota.png') and os.path.exists('sample_images/ryota_mask.png'):
    subprocess.call("sh test.sh", shell=True)
  else:
    subprocess.call("sh test2.sh", shell=True)
  time.sleep(15)
  doc = open('eval_results/fanimp_col/result_ryota.obj', 'rb')
  bot.send_message(message.chat.id, "Ok ready, here is the file")
  bot.send_document(message.chat.id, doc)



@bot.message_handler(content_types=['document'])
def photo(message):
    file_id = message.document.file_name
    if file_id =='ryota.png' or file_id =='ryota_mask.png':
        file_id_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_id_info.file_path)
        with open ( 'sample_images/'+file_id , 'wb') as new_file:
            new_file.write(downloaded_file)
        bot.reply_to(message, "OK")
    else:
        bot.reply_to(message, "File should be named ryota.png or ryota_mask.png \n Please rename the file \n (c) 3D rec Bot")



@bot.message_handler(commands=['check'])
def send_welcome(message):
  if os.path.exists('sample_images/ryota.png'):
    bot.reply_to(message, "Exists")
  else:
    bot.reply_to(message, "Doesnt exist")



@bot.message_handler(func=lambda m: True)
def echo_all(message):
	bot.reply_to(message, message.text)





bot.polling()
