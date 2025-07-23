import random
from random import randint
import telebot
import time
import os

##############
# переменные

BOT_TOKEN = 'YOUR BOT TOKEN'

bot = telebot.TeleBot(BOT_TOKEN)

last_word = False
# переключатель
memory_switcher = True



def add_to_markov(words):
    global last_word

    for i  in range(len(words)):

        current_word = words[i]

        if i != len(words)-1:
            next_word = words[i + 1]

            res = [next_word]
        else:
            last_word = words[i]
            res = False

        #adding

        if res:
            if current_word in database:
                database[current_word].extend(res)
            else:
                database[current_word] = res
        else:
            print('добавление в оперативную память завершено')
            return

def logic_ansfer(work_word,poet_mode):
    ansfer = []
    # чтоб 2функции соеденить
    if type(poet_mode) == int:
        argument = poet_mode
    elif poet_mode:
        argument = randint(50, 100)
    else:
        argument = randint(1, 10)

    for i in range(argument):
        # если он есть в бд
        if database.get(work_word, False):
            # однострочка
            # добавляем случайное значение в переменную цикла а потом ответа
            work_word = random.choice(database[work_word])
            ansfer.append(work_word)
        else:
            work_word = random.choice(list(database))
            ansfer.append(work_word)
    ansfer = ' '.join(ansfer).capitalize()
    return ansfer

def reply_mess(answer,message,title):
    answer = ' '.join(answer)
    bot.reply_to(message, f'я сочинил рассказ на тему "{title}" \n {answer}')
    print('я отправил текст')



with open('links.txt', 'r',encoding='Utf-8') as f:
    global database
    database = {}
    file = f.read().split()
    add_to_markov(file)

def memory_add(message):

    words = message.text.lower().split()

    with open('links.txt','a+') as file:
        if message.text in file:
            print('я ничего добавил, тк строчка повторяется')
            return
        else:
            file.write(message.text + '\n')
            print(f'Я добавил в файловую базу данных: \n{message.text}')

    # связующее м.у последним и первым сообщением

    if last_word:
        if last_word in database:

            database[last_word].append(words[0])
        else:
            database[last_word] = [words[0]]

    # добавляем в цепь
    add_to_markov(words)

def zahlop_ansfer(message):

    work_word = message.text.split()[-1]

    ansfer = logic_ansfer(work_word,False)

    if randint(1,400) == 37:
        for _ in range(14):
            time.sleep(1)
            bot.send_message('Zahlop has been hacked')
            ansfer = 'Zahlop has been hacked'
            print('пасхалка активировалась')

    bot.reply_to(message,ansfer)
    print('я отправил:',ansfer)




###########################################################################
@bot.message_handler(commands=['datainfo'])
def data_info(message):
    with open('links.txt','r',encoding='Utf-8') as temp:
        info = temp.read().split()
        bot.reply_to(message,f'я запомнил {len(info)} слов и {len(' '.join(info))} символов')
        print('я отправил инфу о бд')

@bot.message_handler(commands=["poet"])
def poet(message):
    title = random.choice(list(database))
    comands = message.text.split()
    work_word = title
    # проверяем наличие доп аргументов

    if len(comands) == 1:
        ## если их нет, то выполняем код программы

        answer = logic_ansfer(work_word, True)
        print('я отправил рассказ',answer)
        bot.reply_to(message,f'Я сочинил рассказ на тему "{title}"\n\n{answer}')

    # если дополнительные аргументы есть

    else:

        # пытаемся  перевести в инт аргумент

        try:
            argument = int(comands[-1])

        # не получилось (

        except ValueError:
            bot.reply_to(message,'EROR, вы указали неверный тип данных в качестве аргумента')

        # получилось

        else:

            # защита от нечисти
            if argument <= 500:

                answer = logic_ansfer(work_word,argument)
                bot.reply_to(message,f'Я сочинил рассказ на тему "{title}"\n\n{answer}')

            else:
                bot.reply_to(message,'ошибка ваше запрос слишком длинный,максимальный запрос - 500слов')

@bot.message_handler(commands=['switch'])
def switcher(message):
    global memory_switcher
    comand = message.text.split()
    if len(comand) == 2:
        if comand[-1] == 'y' or comand[-1] == 'on':
            memory_switcher = True
            print('включаю запоминание')
            bot.reply_to(message,'успешно, я включен')
        elif comand[-1] == 'n' or comand[-1] == 'off':
            memory_switcher = False
            print('выключаю запоминание')
            bot.reply_to(message, 'успешно, я выключен')
        else:
            bot.reply_to(message,'EROR, вы вели некоректный аргумент("on" или "y" чтобы включить "off" или "n" чтобы выключить)')
    else:
        bot.reply_to(message,'EROR, у меня нет аргументов\n"on" или "y" чтобы включить "off" или "n" чтобы выключить)')


@bot.message_handler(commands=['del'])

def delete_message(message):
    global database
    # проверяем на избранность

    with open('primelist.txt','r') as f:
        prime = f.read().split()

    if str(message.from_user.id) not in prime:
        bot.reply_to(message,'EROR, вы не избранный')
        return

    # если человек избранный


    comands = message.text.split()
    # если есть аргумент в команде
    if len(comands) == 2:

        with open('links.txt','r') as file:
            bd = file.read().split()

        # проверка есть ли это слово в бд
        if bd.count(comands[-1]) != 0:

            for _ in range(bd.count(comands[-1])):
                del bd[bd.index(comands[-1])]


            with open('links.txt','w+') as f:
                f.write(' '.join(bd))
                database = add_to_markov(f.read())


            print('успешно удалил слово -',comands[-1])
            bot.reply_to(message,'Успешно, я удалил ваше слово из базы данных')

        else:
            bot.reply_to(message,'EROR, слово которое вы указали нет в базе данных')
    # проверка на аргумент
    else:
        bot.reply_to(message,'EROR, вы не указали аргумент')



@bot.message_handler(commands=[ 'start'])
def send_welcome(message):
    bot.reply_to(message, """
привет ты попал на бота который разработан OpenDoor3786(github)!     
Это чат-бот на основе цепи маркова! """)


@bot.message_handler(commands=["help"])
def help_send(message):
    bot.reply_to(message,
f"""!!!Список команд!!!:\n\n1.Захлоп игнор(захлоп не будет запоминать сообщение в котором присутствует эта фраза)
2./datainfo (высвечивает информацию о базе данных захлопа)\n3. /Poet (генерирует рассказ (можно указать длинну рассказа
пример /poet 100(выведет рассказ в 100 слов)))\n4. /switch (off чтобы выключить бота)\n5. /switch on (чтобы включить бота)
6. /del n-message (удаляет сообщение(только для избранных))"""
    )


@bot.message_handler(content_types=['text'])
def speak_and_memory(message):
    # сообщение
    check = message.text.lower()
    # проверяем включен ли он
    if memory_switcher and 'захлоп игнор' not in check:

        if 'захлоп' in check or '@Zahlop_bot' in message.text:
            zahlop_ansfer(message)

        elif message.reply_to_message and message.reply_to_message.from_user.id == bot.get_me().id:
            zahlop_ansfer(message)

        else:
            memory_add(message)

    else:
        print('я сплю')
        return








if __name__ == '__main__':
    bot.infinity_polling()