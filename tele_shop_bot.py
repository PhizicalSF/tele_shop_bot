import random
import webbrowser
import sqlite3
import telebot
from my_database import new_user, user_exist, selectTable,new_product_add, delete_product, selectProducts, product_in_busket,user_busket_select, product_exist,product_out_busket,new_order_for_user,set_phone_number,user_orders_select,admin_orders_activitu,admin_orders_complited,setOrderStatus
from telebot import types
import requests
from geopy.geocoders import Nominatim
import datetime

db=sqlite3.connect('my_database_telebot.db', check_same_thread=False)

bot=telebot.TeleBot('6589767577:AAGKFb8zb4x5gxNr0Gnn3_jVE1hyn_GYHDc')
answers=['Я вас не понял']
#Продукты из базы данных!
cat=selectTable(db,"category")
button_list_products=[0]*len(selectTable(db,"subcategory"))
all_products=[0]*len(selectTable(db,"subcategory"))
k=0
for i in range(len(cat)):
    for j in range(len(selectTable(db,"subcategory",usl=["category_id",i+1]))):
        button_list_products[k]=str(selectTable(db,"subcategory",usl=["category_id",i+1])[j][2]) 
        k+=1
#!!!
#только продукты
buy_product=selectTable(db,"Products")
name_products=[0]*len(buy_product)
for i in range(len(buy_product)):
    name_products[i]=buy_product[i][1]

#!!!
@bot.message_handler(commands=['start'])
def welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Товары')
    button5=types.KeyboardButton('Корзина')
    button6=types.KeyboardButton('Заказы')
    button3=types.KeyboardButton('Справка')
    user_ex=user_exist(message,db)
    now_user=selectTable(db,'users',usl=['user_id',message.from_user.id])
    markup.row(button1,button3)
    markup.row(button5,button6)
    print(now_user)

  

   
    if(not user_ex):
        new_user(message,db)
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nРад с вами познакомиться!',reply_markup=markup)
    else:
        bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!\nО, это снова вы! Я скучал по вам',reply_markup=markup)
    
    if(now_user[0][6]==0):
        button4=types.KeyboardButton('Админ-панель')
        markup.row(button4)
@bot.message_handler(content_types='photo')
def get_photo(message):
    bot.send_message(message.chat.id, 'Я пока что не могу смотреть фотографии, но в будующем все может быть...')


@bot.message_handler()
def info(message):
    if message.text=='Товары':
        goodsChapterFirstStep(message)
    elif message.text=='Настройки':
        settingsChapter(message)
    elif message.text=='В меню':
        welcome(message)
    elif message.text in name_products:
        oneProductSelect_message(message)
    elif message.text.startswith('В корзине ='):
        bot.reply_to(message=message,text="Нажав на имя товара вы можете изменить его количество в выпадающем сообщении")
    elif message.text=='Корзина':
        my_busket_message(message)
    elif message.text=='Справка':
        infoChapter(message)
    elif message.text=='Заказы':#Я ТУТ
        my_orders(message)
    elif message.text=='Заказать':
        process_order_user_one(message)
    elif message.text=='Админ-панель':
        adminPanel(message)
    elif message.text in button_list_products:
        goodsChapterTwoStep(message)
    elif message.text=='Назад в меню':
        welcome(message)
    elif message.text=='Назад к операциям':
        productAdmin(message)
    elif message.text=='Назад':
        goodsChapterFirstStep(message)
    elif message.text=='Наш VK':
        markup = types.InlineKeyboardMarkup()
        button1=types.InlineKeyboardButton(text='Наш VK',url="https://vk.com/miracleinsaid")
        markup.add(button1)
        bot.send_message(message.chat.id, 'Работаем до 23:00',reply_markup=markup)
    elif message.text=='Написать оператору':
        markup = types.InlineKeyboardMarkup()
        button1=types.InlineKeyboardButton(text='Написать оператору',url="https://t.me/MarkMenson")
        markup.add(button1)
        bot.send_message(message.chat.id, 'Работаем до 23:00',reply_markup=markup)
    elif message.text=='Операции с товарами':
        productAdmin(message)
    elif message.text=='Операции с заказами':
        ordersAdmin(message)
    elif message.text=='Просмотр активных заказов':
        ordersAdmin_activity(message)
    elif message.text=='Просмотр выполненных заказов':
        ordersAdmin_complited(message)
    elif message.text=='Добавить товар':
        new_product_admin(message)
    elif message.text=='Просмотр всех товаров':
        seeAllnew_product(message)
    elif message.text=='Удалить товар':
        delete_product_one(message)
    elif message.text=='В корзину':
        new_order_product(message)
    else:
        welcome(message)
        bot.send_message(message.chat.id, answers[0]+ " и отправил в главное меню.")
    
@bot.callback_query_handler(func=lambda call: True)
def handle_button_click(call):
    if call.data in name_products:    
        oneProductSelect_call(call)
    elif call.data.split(":")[0]=="В корзину":
        busket_info = [call.from_user.id, call.data.split(':')[1]]
    # Добавление продукта в корзину пользователя
        product_in_busket(busket_info, db)
    
        markup = types.InlineKeyboardMarkup()
        button1=types.InlineKeyboardButton('Посмотреть корзину',callback_data="Добавили товар")
        markup.row(button1)
        text_message="Продукт добавлен в корзину!"
        bot.send_message(call.message.chat.id,text_message,reply_markup=markup)   
    elif call.data.split(":")[0]=="Из корзины":
        busket_info = [call.from_user.id, call.data.split(':')[1]]
    # Добавление продукта в корзину пользователя
        product_out_busket(busket_info, db)
    
        markup = types.InlineKeyboardMarkup()
        button1=types.InlineKeyboardButton('Посмотреть корзину',callback_data="Добавили товар")
        markup.row(button1)
        text_message="Продукт убран"
        bot.send_message(call.message.chat.id,text_message,reply_markup=markup)   
    elif call.data=="Добавили товар":
        my_busket_call(call)
    elif call.data.split(":")[0]=="Информация о":
        order_id=call.data.split(":")[1]
        order=selectTable(db,"orders",usl=["order_id",order_id])
        bot.send_message(call.message.chat.id, order[0][1])




    elif call.data.split(":")[0]=="Принять":
        order_id=call.data.split(":")[1]
        order_status=[order_id,1]
        setOrderStatus(db,order_status)
        bot.send_message(call.message.chat.id, "Заказ принят")


    elif call.data.split(":")[0]=="Выполнить":
        order_id=call.data.split(":")[1]
        order_status=[order_id,-1]
        setOrderStatus(db,order_status)
        bot.send_message(call.message.chat.id, "Заказ выполнен")
    elif call.data.split(":")[0]=="Отклонить":
        order_id=call.data.split(":")[1]
        order_status=[order_id,2]
        setOrderStatus(db,order_status)
        bot.send_message(call.message.chat.id, "Заказ отклонен")

def oneProductSelect_call(call):
    product_info=selectTable(db,"Products",usl=["product_name",call.data])
    user_busket=user_busket_select(db,busket_id=call.from_user.id)
    if(product_exist(usl=[call.from_user.id,product_info[0][0]],db=db ) ):
        markup = types.InlineKeyboardMarkup()
        button_data = f"В корзину:{product_info[0][0]}"
        button2_data = f"Из корзины:{product_info[0][0]}"
        button1=types.InlineKeyboardButton('В корзину',callback_data=button_data)
        button2=types.InlineKeyboardButton('Убрать из корзины',callback_data=button2_data)
        markup.row(button1,button2)
        price=product_info[0][2]
        quantity_in_busket=find_product_in_basket(user_busket,product_name=product_info[0][0])
        quantity=product_info[0][3]
        discript=product_info[0][6]
        text_message="Название: "+ str(call.data) +"\nЦена: " + str(price) +" Рублей \n"+"В наличии: "+str(quantity) +" штук\n" +"Описание: "+str(discript) +"\nВ корзине: "+str(quantity_in_busket[2]) 
        bot.send_message(call.message.chat.id,text_message,reply_markup=markup) 
    else:
        markup = types.InlineKeyboardMarkup()
        button_data = f"В корзину:{product_info[0][0]}"   
        button1=types.InlineKeyboardButton('В корзину',callback_data=button_data)
        markup.row(button1)
        price=product_info[0][2]
        quantity=product_info[0][3]
        discript=product_info[0][6]
        text_message="Название: "+ str(call.data) +"\nЦена: " + str(price) +" Рублей \n"+"В наличии: "+str(quantity) +" штук\n" +"Описание: "+str(discript) 
        bot.send_message(call.message.chat.id,text_message,reply_markup=markup) 


def oneProductSelect_message(message):
    product_info=selectTable(db,"Products",usl=["product_name",message.text])
    user_busket=user_busket_select(db,busket_id=message.from_user.id)
    if(product_exist(usl=[message.from_user.id,product_info[0][0]],db=db ) ):
        markup = types.InlineKeyboardMarkup()
        button_data = f"В корзину:{product_info[0][0]}"
        button2_data = f"Из корзины:{product_info[0][0]}"
        button1=types.InlineKeyboardButton('В корзину',callback_data=button_data)
        button2=types.InlineKeyboardButton('Убрать из корзины',callback_data=button2_data)
        markup.row(button1,button2)
        price=product_info[0][2]
        quantity_in_busket=find_product_in_basket(user_busket,product_name=product_info[0][0])
        quantity=product_info[0][3]
        discript=product_info[0][6]
        text_message="Название: "+ str(message.text) +"\nЦена: " + str(price) +" Рублей \n"+"В наличии: "+str(quantity) +" штук\n" +"Описание: "+str(discript) +"\nВ корзине: "+str(quantity_in_busket[2]) 
        bot.send_message(message.chat.id,text_message,reply_markup=markup) 
    else:
        markup = types.InlineKeyboardMarkup()
        button_data = f"В корзину:{product_info[0][0]}"   
        button1=types.InlineKeyboardButton('В корзину',callback_data=button_data)
        markup.row(button1)
        price=product_info[0][2]
        quantity=product_info[0][3]
        discript=product_info[0][6]
        text_message="Название: "+ str(message.data) +"\nЦена: " + str(price) +" Рублей \n"+"В наличии: "+str(quantity) +" штук\n" +"Описание: "+str(discript) 
        bot.send_message(message.chat.id,text_message,reply_markup=markup) 

def goodsChapterFirstStep(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True,row_width=5)
    markup.add(*[types.KeyboardButton(name) for name in button_list_products])
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button5)
    bot.send_message(message.chat.id, 'Выберите категорию товаров:',reply_markup=markup)

def goodsChapterTwoStep(message):
    tap_subcategory_product=selectProducts(db,message)
    keyboard=[0]*len(selectTable(db,'category'))
    for i in range(len(tap_subcategory_product)):
        keyboard[i]=[types.InlineKeyboardButton(text=str(tap_subcategory_product[i][1]),callback_data=str(tap_subcategory_product[i][1]))]  
    markup=types.InlineKeyboardMarkup(keyboard=keyboard)
    bot.send_message(message.chat.id, 'Выберите товар:', reply_markup=markup)


def settingsChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Настройка 1')
    button2=types.KeyboardButton('Настройка 2')
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button1,button2)
    markup.row(button5)
    bot.send_message(message.chat.id, 'Настройки',reply_markup=markup)

def infoChapter(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Написать оператору',)
    button2=types.KeyboardButton('Наш VK')
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button1,button2)
    markup.row(button5)
    bot.send_message(message.chat.id, 'Информация',reply_markup=markup)

def adminPanel(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Операции с товарами',)
    button2=types.KeyboardButton('Операции с заказами')
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button1,button2)
    markup.row(button5)
    bot.send_message(message.chat.id, 'Панель администратора',reply_markup=markup)
def productAdmin(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Просмотр всех товаров')
    button2=types.KeyboardButton('Добавить товар')
    button3=types.KeyboardButton('Удалить товар')
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button1)
    markup.row(button2,button3)
    markup.row(button5)
    bot.send_message(message.chat.id,'Операции с товарами',reply_markup=markup)
def new_product_admin(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    msg=bot.send_message(message.chat.id, 'Введите имя продукта')
    bot.register_next_step_handler(msg, process_name_product)
    button5=types.KeyboardButton('Назад к операциям')
    markup.row(button5)
new_product=[0]*7
def process_name_product(message):
    try:
        new_product[1]=message.text
        msg=bot.send_message(message.chat.id, 'Введите цену продукта')
        bot.register_next_step_handler(message, process_price_product)
    except Exception as e:
        bot.reply_to(message, 'Ошибочка вышла...')
def process_price_product(message):
    try:
        new_product[2]=message.text
        msg=bot.send_message(message.chat.id, 'Введите количество продукта')
        bot.register_next_step_handler(msg, process_quantity_product)
    except Exception as e:
        bot.reply_to(message, 'Ошибочка вышла...')

def process_quantity_product(message):
    try:
        new_product[3]=message.text
        keyboard=[0]*len(selectTable(db,'category'))
        for i in range(len(selectTable(db,'category'))):
            keyboard[i]=[types.InlineKeyboardButton(text=str(i+1)+" - "+selectTable(db,'category')[i][1],callback_data="123")]
        markup=types.InlineKeyboardMarkup(keyboard=keyboard)

        msg=bot.send_message(message.chat.id, 'Выберите категорию продукта(Введите только номер)',reply_markup=markup)
        bot.register_next_step_handler(msg, process_category_product)
    except Exception as e:
        bot.reply_to(message, 'Ошибочка вышла...')  

def process_category_product(message):

    new_product[4]=message.text
    keyboard=[0]*len(selectTable(db,'subcategory',usl=['category_id',new_product[4]]))
    for i in range(len(selectTable(db,'subcategory',usl=['category_id',new_product[4]]))):
        keyboard[i]=[types.InlineKeyboardButton(text=str(i+1)+" - "+str(selectTable(db,'subcategory',usl=['category_id',new_product[4]])[i][2]),callback_data="123")]
    markup=types.InlineKeyboardMarkup(keyboard=keyboard)

    msg=bot.send_message(message.chat.id, 'Выберите подкатегорию продукта(Введите только номер)',reply_markup=markup)
    bot.register_next_step_handler(msg, process_subcategory_product)

def process_subcategory_product(message):
    try:
        new_product[5]=message.text
        msg=bot.send_message(message.chat.id, 'Напишите описание продукта')
        bot.register_next_step_handler(msg, process_finaly_product)
    except Exception as e:
        bot.reply_to(message, 'Ошибочка вышла...')
def process_finaly_product(message):

    new_product[6]=message.text
    new_product_add(new_product,db)
    msg=bot.send_message(message.chat.id, 'Ваш товар добавлен')

def seeAllnew_product(message):
    products=selectTable(db,'products')
    
    for i in products:
        msg=bot.send_message(message.chat.id, "Название: "+i[1]+"\b"+"Цена: "+ str(i[2])+"\b"+"Количесто: "+ str(i[3]))
    msg=bot.send_message(message.chat.id, 'Вот все товары')

def delete_product_one(message):
    products=selectTable(db,'products')

    for i in products:
        msg=bot.send_message(message.chat.id,  "ID продукта: "+str(i[0])+"\b"+"Название: "+i[1]+"\b"+"Цена: "+ str(i[2])+"\b"+"Количесто: "+ str(i[3]))
    msg=bot.send_message(message.chat.id, 'Введите ID продукта для удаления: ')          
    bot.register_next_step_handler(msg, delete_product_two)
def delete_product_two(message):
    delete_produc=message.text
    delete_product(delete_produc,db)
    msg=bot.send_message(message.chat.id, 'Продукт удален.')          

def my_busket_call(call):
    user_busket_now=user_busket_select(db,busket_id=call.from_user.id)
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard=[0]*len(user_busket_now)
    for i in range(len(user_busket_now)):
        text1=str(selectTable(db,"products",usl=["product_id",user_busket_now[i][1]])[0][1]) 
        text2="В корзине = "+ str (user_busket_now[i][2])
        keyboard[i]=types.KeyboardButton(text=text1)
        markup.row(keyboard[i],text2)
    button6=types.KeyboardButton('Заказать')
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button5,button6)
    bot.send_message(call.message.chat.id, 'Ваша корзина', reply_markup=markup)
def my_busket_message(message):
    
    user_busket_now=user_busket_select(db,busket_id=message.from_user.id)
    if(len(user_busket_now)==0):
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button6=types.KeyboardButton('Товары')
        button5=types.KeyboardButton('Назад в меню')
        markup.row(button5,button6)
        bot.send_message(message.chat.id, 'Ваша корзина пуста, но не расстраивайтесь, вы всегда можете выбрать товары', reply_markup=markup)
    else:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard=[0]*len(user_busket_now)
        for i in range(len(user_busket_now)):
            text1=str(selectTable(db,"products",usl=["product_id",user_busket_now[i][1]])[0][1]) 
            text2="В корзине = "+ str (user_busket_now[i][2])
            keyboard[i]=types.KeyboardButton(text=text1)
            markup.row(keyboard[i],text2)
        button6=types.KeyboardButton('Заказать')
        button5=types.KeyboardButton('Назад в меню')
        markup.row(button5,button6)
        bot.send_message(message.chat.id, 'Ваша корзина', reply_markup=markup)
def my_orders(message):#ЭТО СДЕЛАТЬ
    user_id=message.from_user.id
    order_name=message.from_user.username
    user_orders_now=user_orders_select(db,order_name)
    status=""
    print(user_orders_now)
    markup_reply=types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn=types.KeyboardButton('В меню')
    markup_reply.add(btn)
    bot.send_message(message.chat.id,"Ваши заказы:",reply_markup=markup_reply)
    
    for order in user_orders_now:
        if order[6] == 0:
            status = "В обработке"
        elif order[6] == 1:
            status = "Принят"
        elif order[6] == 2:
            status = "Отклонен"
        elif order[6] == -1:
            status = "Выполнен"
            
        text = f"Заказ №{order[0]}\nДата: {order[2]}\nСтатус: {status}"
        callback_info_btn = f"Информация о:{order[0]}"
        keyboard = types.InlineKeyboardMarkup()
        btn = types.InlineKeyboardButton("Информация", callback_data=callback_info_btn)
        
        keyboard.add(btn)
        bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
    
def find_product_in_basket(basket, product_name):
    for item in basket:
        if item[1] == product_name:
            return item
    return None
order_info=[0]*5

def process_order_user_one(message):
    user_id=message.from_user.id
    
    now_user=selectTable(db,"users",usl=["user_id",user_id])
    order_info[0]=now_user[0][2]
    order_info[2]=[i for i in selectTable(db,"busket",usl=["busket_id",user_id])]

    if (now_user[0][3]=='0'):
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        btn=types.KeyboardButton('Отправить номер телефона',request_contact=True)
        markup.add(btn)
        bot.send_message(message.chat.id,'Введите номер телефона',reply_markup=markup)
        bot.register_next_step_handler(message,process_order_user_two)
    else:
        markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
        btn=types.KeyboardButton('Продолжить')
        btn2=types.KeyboardButton('Изменить')
        markup.add(btn,btn2)
        bot.send_message(message.chat.id,"Ваш номер телефона: "+str(now_user[0][3])+"?",reply_markup=markup)
        bot.register_next_step_handler(message,process_order_user_two)


def process_order_user_two(message):
    if(hasattr(message.contact,'phone_number')):
        set_phone_number(db,message.contact.phone_number)
    else:
        pass
    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    btn=types.KeyboardButton('Отправить мой адрес',request_location=True)
    markup.add(btn)
    bot.send_message(message.chat.id,'Отправьте ваш адрес:',reply_markup=markup)
    bot.register_next_step_handler(message,process_order_user_theree)
def process_order_user_theree(message):
    a=get_address(message.location.latitude,message.location.longitude)
    order_info[4]=a
    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    btn=types.KeyboardButton('Продолжить')
    markup.add(btn)
    bot.send_message(message.chat.id,'Оставьте комментарий к заказу (необязательно): ',reply_markup=markup)
    bot.register_next_step_handler(message,process_order_user_four)

def process_order_user_four(message):
    if(message.text=="Продолжить"):
        order_info[3]="_"
    else: order_info[3]=message.text
    markup=types.ReplyKeyboardMarkup(one_time_keyboard=True,resize_keyboard=True)
    btn=types.KeyboardButton('Сделать заказ')
    btn2=types.KeyboardButton('Вернуться в корзину')
    markup.add(btn,btn2)
    bot.send_message(message.chat.id,'Оформить заказ?',reply_markup=markup)
    bot.register_next_step_handler(message,process_order_user_final)
def process_order_user_final(message):
    if(message.text=='Сделать заказ'):
        order_info[1]=str(datetime.datetime.now().day) +"."+str(datetime.datetime.now().month)+"."+str(datetime.datetime.now().year) + "-"+str(datetime.datetime.now().hour)+":"+str(datetime.datetime.now().minute)+":"+str(datetime.datetime.now().second)
        print(order_info)
        new_order_for_user(order_info,db)
        bot.reply_to(message,text='Заказ успешно оформлен!')   
        my_orders(message)
    elif(message.text=='Вернуться в корзину'):
        my_busket_message(message)

def ordersAdmin(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton('Просмотр активных заказов')
    button2=types.KeyboardButton('Просмотр выполненных заказов')
    button5=types.KeyboardButton('Назад в меню')
    markup.row(button1,button2)
    markup.row(button5)
    bot.send_message(message.chat.id,'Заказы',reply_markup=markup)
def ordersAdmin_activity(message):
    orders_activitu=admin_orders_activitu(db)
    status=""
    for order in orders_activitu:
        if order[6]==0:
            status="В обработке"
            text = f"Заказ №{order[0]}\nКлиент: {order[1]}\nДата: {order[2]}\nСтатус: {status}"
            callback_info_btn = f"Принять:{order[0]}"
            callback_info_btn2 = f"Отклонить:{order[0]}"
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("Принять", callback_data=callback_info_btn)
            btn2 = types.InlineKeyboardButton("Отклонить", callback_data=callback_info_btn2)
            keyboard.add(btn,btn2)
            bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
        elif order[6]==1:
            status="Принят"
            text = f"Заказ №{order[0]}\nКлиент: {order[1]}\nДата: {order[2]}\nСтатус: {status}"
            callback_info_btn = f"Выполнить:{order[0]}"
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("Выполнить заказ", callback_data=callback_info_btn)
            keyboard.add(btn)
            bot.send_message(message.chat.id, text=text, reply_markup=keyboard)

   
def ordersAdmin_complited(message):
    orders_activitu=admin_orders_complited(db)
    for order in orders_activitu:
        if order[6]==-1:

            status="Выполнен"
            text = f"Заказ №{order[0]}\nКлиент: {order[1]}\nДата: {order[2]}\nСтатус: {status}"
            callback_info_btn = f"Информация о:{order[0]}"
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("Информация", callback_data=callback_info_btn)
            keyboard.add(btn)
            bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
        else:
            status="Отклонен"
            text = f"Заказ №{order[0]}\nКлиент: {order[1]}\nДата: {order[2]}\nСтатус: {status}"
            callback_info_btn = f"Информация о:{order[0]}"
            keyboard = types.InlineKeyboardMarkup()
            btn = types.InlineKeyboardButton("Информация", callback_data=callback_info_btn)
            keyboard.add(btn)
            bot.send_message(message.chat.id, text=text, reply_markup=keyboard)
def get_address(latitude, longitude):
    geolocator = Nominatim(user_agent="AIzaSyD34Emf6Ev1-rvaLNznRk-WpoKZwPe_OO8")
    location = geolocator.reverse((latitude, longitude))
    return location.address

bot.polling(none_stop=True)

