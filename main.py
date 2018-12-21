# //
# BY @ES3N1N 20!8 T.ME/ES3N1N
# Hard to read that code, i know
#//
#///////////////////////////////////////////////////////////////////////////////////////////////////
import telebot
# /////////////////////////////////////////////////
promos = ['#es3n1n', '#debug']                                                                     #Обьявление в массив самих промокодов
market = ['gowno - 123p']                                                                          #Товары в шопе
skidSum = 50                                                                                       #сумма скидона в рублях

mainmenuText = 'Main Menu\nМеня сбил троллейбус, когда вышел за клинским\nDeveloper - @es3n1n'     #Текст, который бот пишет в меню
enterPromoText = 'Enter ur promocode'                                                              #Текст, которым бот запрашивает промокод
PromoErrorText = "Error. Incorrect promocode."                                                     #Текст, который бот пишет, если нет такого промокода
AlreadyUsedPromoText = 'You already used promocode'                                                #Текст, который бот пишет, если челик уже заюзал промокод
SuccesfullPromoText = 'Succesfull activated promocode {0}'                                         #Текст, который бот пишет когда ты заюзал промокод
PaymentWithSkid = 'Сумма к оплате вместе со скидкой - {0}'
PaymentWithoutSkid = 'Сумма к оплате - {0}'

bot_Token = ''                                        #Токен бота, который берется у @BotFather
bot = telebot.TeleBot(bot_Token)                                                                   #Создание самого объекта бота, лучше не трогать, чтобы ничего не сломалось

promostate = []                                                                                    #Массив, в который бот для себя пишет тех, кто хочет активнуть промик
usedpromo = []                                                                                     #Массив с идами людей, которые уже заюзали промокод любой
promoActivated = []                                                                                #Массив с идами людей, которые активнули промик промик
# /////////////////////////////////////////////////

def mainmenu(message):
    keyboard = telebot.types.InlineKeyboardMarkup() #сама клавиатура, которую возвращает функция
    if message.from_user.id in promoActivated:
        for marketId in market:
            keyboard.add(telebot.types.InlineKeyboardButton(text='{0} - {1}p'.format(marketId.split('-')[0],
                                                                                     int(marketId.split('-')[1].replace(' ', '').replace('p', '')) - skidSum),
                                                            callback_data=marketId.split('-')[0]))
    else:
        for marketId in market:
            keyboard.add(telebot.types.InlineKeyboardButton(text=marketId,
                                                            callback_data=marketId.split('-')[0]))#что может пойти не так
    if message.from_user.id not in usedpromo:
        keyboard.add(telebot.types.InlineKeyboardButton(text=enterPromoText, callback_data="promo"))
    return keyboard

@bot.message_handler(commands=['start'])
def msg(message):
    if message.chat.title != None:
        return #pCode
    bot.send_message(message.chat.id, mainmenuText, reply_markup=mainmenu(message))

@bot.message_handler(content_types=["text"])
def msg(message):
    if not message.text.startswith("#"):
        return
    if message.chat.title != None:
        return
    if message.from_user.id in promostate:
        if message.text in promos:
            usedpromo.append(message.from_user.id)
            promoActivated.append(message.from_user.id)
            promostate.remove(message.chat.id)
            bot.send_message(message.chat.id, SuccesfullPromoText.format(message.text))
            bot.send_message(message.chat.id, mainmenuText, reply_markup=mainmenu(message))
        else:
            bot.send_message(message.chat.id, PromoErrorText)
            promostate.remove(message.chat.id)
            bot.send_message(message.chat.id, mainmenuText, reply_markup=mainmenu(message))

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message and call.data == "promo":
        if call.from_user.id in usedpromo:
            bot.send_message(call.message.chat.id, AlreadyUsedPromoText)
            bot.send_message(call.message.chat.id, mainmenuText, reply_markup=mainmenu(call.message))
            return
        else:
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=enterPromoText)
            promostate.append(call.from_user.id)
    else:
        for marketID in market:
            if call.data == marketID.split('-')[0] and call.from_user.id in promoActivated:
                bot.send_message(call.message.chat.id,PaymentWithSkid.format(int(marketID.split('-')[1].replace(' ', '').replace('p', '')) - skidSum))
                return
        bot.send_message(call.message.chat.id, PaymentWithoutSkid.format(marketID.split('-')[1].replace(' ', '')))

bot.skip_pending = True
while True:
    try:
        bot.infinity_polling()
    except Exception as e:
        print('***********************************')
        print('[ERROR] {0}'.format(e))
        print('***********************************')
        from time import sleep
        sleep(5)