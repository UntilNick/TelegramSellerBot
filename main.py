#///////////////////////////////////////////////////////////////////////////////////////////////////
import telebot
# /////////////////////////////////////////////////
promos = ['#es3n1n', '#debug']                                                                     #Обьявление в массив самих промокодов
market = ['gowno - 123p', 'ssaka - 123p', 'parasha - 135р', 'sosatb - 101p']                       #Товары в шопе
skidSum = 50                                                                                       #сумма скидона в рублях

mainmenuText = 'Main Menu\n\nDeveloper - @es3n1n'                                                  #Текст, который бот пишет в меню
enterPromoText = 'Enter ur promocode'                                                              #Текст, которым бот запрашивает промокод
PromoErrorText = "Error. Incorrect promocode."                                                     #Текст, который бот пишет, если нет такого промокода
AlreadyUsedPromoText = 'You already used promocode'                                                #Текст, который бот пишет, если челик уже заюзал промокод
SuccesfullPromoText = 'Succesfull activate promocode {0}'                                          #Текст, который бот пишет когда ты заюзал промокод
PaymentWithSkid = 'Сумма к оплате вместе со скидкой - {0}'
PaymentWithoutSkid = 'Сумма к оплате - {0}'

bot_Token = 'token here'                                                                           #Токен бота, который берется у @BotFather
bot = telebot.TeleBot(bot_Token)                                                                   #Создание самого объекта бота, лучше не трогать, чтобы ничего не сломалось

promostate = [0]                                                                                   #Массив, в который бот для себя пишет тех, кто хочет активнуть промик
usedpromo = [0]                                                                                    #Массив с идами людей, которые уже заюзали промокод любой
promoActivated = [0]                                                                               #Массив с идами людей, которые активнули промик промик
# /////////////////////////////////////////////////

def mainmenu(message):
    keyboard = telebot.types.InlineKeyboardMarkup() #сама клавиатура, которую возвращает функция
    allowPromo = 1
    skidon = 0
    for userID in range(len(promoActivated)):
        if message.from_user.id == promoActivated[userID]:
            for marketId in range(len(market)):
                keyboard.add(telebot.types.InlineKeyboardButton(text='{0} - {1}p'.format(market[marketId].split('-')[0],
                                                                                         int(market[marketId].split('-')[1].replace(' ', '').replace('p', '')) - skidSum),
                                                                callback_data=market[marketId].split('-')[0])) #Большое кол-во говнокода, чтобы все автоматизировать блять
                skidon = 1  #У человека есть скидка
    if skidon == 0: #Если у человека нет скидки
        for marketId in range(len(market)):
            keyboard.add(telebot.types.InlineKeyboardButton(text=market[marketId],
                                                            callback_data=market[marketId].split('-')[0]))#Добавляем в название то, что лежит в массиве и в калбек дату название товара(что может пойти не так xD)
    for i in range(len(usedpromo)):
        if message.from_user.id == usedpromo[i]: #Если уже заюзал промик
            allowPromo = 0 #Ставит переменную в 0 и ему не отправляется кнопка для активации промокода
    if allowPromo == 1:
        keyboard.add(telebot.types.InlineKeyboardButton(text=enterPromoText, callback_data="promo"))
    return keyboard

@bot.message_handler(content_types=["text"]) #Если бот получает текст от челика
def msg(message):
    for state in range(len(promostate)):
        if message.from_user.id == promostate[state]:#Если человек должен активнуть промик
            for i in range(len(promos)):
                if message.text == promos[i]: # Тут уже пиши логику для активации промокода, я не знаю, что вам там нужно
                    usedpromo.append(message.from_user.id) #Добавление в массив заюзавших ид юзера
                    promoActivated.append(message.from_user.id) #Добавление в массив тех, кто заюзал, но пока не купил ничего
                    promostate.pop(state) #Удаление из массива тех, кто должен ввести промик
                    bot.send_message(message.chat.id, SuccesfullPromoText.format(promos[i])) #Оповещение о том, что все прошло успешно
                    bot.send_message(message.chat.id, mainmenuText, reply_markup=mainmenu(message))#Отправление меню
                    return#Уходим, чтобы он дальше не начал творить хуету
            bot.send_message(message.chat.id, PromoErrorText)#Отправляем ошибку
            promostate.pop(state)#Удаление из массива юзеров, которые должны ввести промик
            bot.send_message(message.chat.id, mainmenuText, reply_markup=mainmenu(message))#Отправляем меню
    if message.text.startswith('/start'):#Если текст со стартом бота
        bot.send_message(message.chat.id, mainmenuText, reply_markup=mainmenu(message))#Отправляем меню главное

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:#Проверяем, если это каллбек кнопки
        if call.data == "promo":#Если каллбек промокода
            for i in range(len(usedpromo)):
                if call.from_user.id == usedpromo[i]: #Если челик уже заюзал промокод
                    bot.send_message(call.message.chat.id, AlreadyUsedPromoText) #Оповещаем о том, что уже юзал
                    bot.send_message(call.message.chat.id, mainmenuText, reply_markup=mainmenu(call.message)) #Отправляем меню
                    return#Уходим
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=enterPromoText)#Просим ввести текст
            promostate.append(call.from_user.id)#Удаляем из массива юзеров, которые должны ввести промик
        for marketID in range(len(market)):
            if call.data == market[marketID].split('-')[0]:#Если каллбек с предметом из массива маркета
                for userID in range(len(promoActivated)):
                    if call.from_user.id == promoActivated[userID]:#Если активирован промокод
                        bot.send_message(call.message.chat.id,
                                         PaymentWithSkid.format(int(market[marketID].split('-')[1].replace(' ', '').replace('p', '')) - skidSum)) #Вычитаем из предмета скидку и отправляем юзеверу
                        return#Уходим
                bot.send_message(call.message.chat.id, PaymanetWithoutSkid.format(market[marketID].split('-')[1].replace(' ', ''))) #Отправляем сумму
                return#Уходим

try:
    bot.polling(none_stop=True)
except Exception as e:
    print('***********************************')
    print('[ERROR] {0}'.format(e))
    print('***********************************')
    from time import sleep
    sleep(5)