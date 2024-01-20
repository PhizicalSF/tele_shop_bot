import sqlite3
db=sqlite3.connect('my_database_telebot.db')
cursor=db.cursor()

# cursor.execute(""" CREATE TABLE users (
#                 user_id integer,
#                 user_first_name text,
#                 user_name text,
#                 user_number text,
#                 user_email text,
#                 user_balance integer,
#                 user_status int
#                 )
#                 """)
# cursor.execute("""CREATE TABLE products (
#                 product_id integer PRIMARY KEY AUTOINCREMENT,
#                 product_name text,
#                 product_price integer,
#                 product_quantity integer,
#                 product_category integer,
#                 product_subcategory integer,
#                 product_disk text,
#                 product_photo text
#                 )   
#                 """)
# cursor.execute("""CREATE TABLE busket (
#                 busket_id integer,
#                 product_id integer
#                 )   
#                 """)
# cursor.execute("""CREATE TABLE orders (
#                 order_id integer PRIMARY KEY AUTOINCREMENT,
#                 order_name text,
#                 order_date text,
#                 order_busket text,
#                 order_comm text,
#                 order_adress text,
#                 order_status integer
#                 )   
#                 """)
# cursor.execute(""" CREATE TABLE category (
#                 category_id integer PRIMARY KEY AUTOINCREMENT,
#                 category_name text
#                 )
#                 """)
# cursor.execute(""" CREATE TABLE subcategory (
#                 subcategory_id integer PRIMARY KEY AUTOINCREMENT,
#                 category_id integer,
#                 subcategory_name text
#                 )
#                 """)
# cursor.execute("INSERT INTO users VALUES (1231231123,'Perviy','Perviy','+11111111111','1@1.ru',9999999,0)")
# cursor.execute("drop table orders")
# print(cursor.fetchall())
# Функция добавления пользователя
def new_user(message,db):
    cursor=db.cursor()
    user_id=message.from_user.id
    user_first_name=message.from_user.first_name
    user_name=message.from_user.username
    user_number=0
    user_email=0
    user_balance=0
    user_status=1
    sql= "INSERT INTO users VALUES (" + str(user_id ) +" , '"+str(user_first_name) +"' , '"+str(user_name)+"' , '"+str(user_number)+"','"+str(user_email)+"',"+str(user_balance)+","+str(user_status)+")"
    print(sql)
    cursor.execute(sql)
    db.commit()
# Функция существования пользователя
def user_exist(message,db):
    cursor=db.cursor()
    user_id=message.from_user.id
    sql= "SELECT user_id FROM users WHERE user_id = " + str(user_id)
    cursor.execute(sql)
    items=cursor.fetchall()
    if items:
        return True
    else:return False
def product_exist(usl,db):
    cursor=db.cursor()
    user_id=usl[0]
    product_id=usl[1]
    sql= "SELECT p.* FROM products AS p JOIN busket AS b ON p.product_id = b.product_id WHERE b.busket_id = "+str(user_id)+" AND p.product_id = "+str(product_id)
    cursor.execute(sql)
    items=cursor.fetchall()
    if items:
        return True
    else:return False
def new_product_add(message,db):
    cursor=db.cursor()
    poduct_name=message[1]
    product_price=message[2]
    product_quantity=message[3]
    product_category=message[4]
    product_subcategory=message[5]
    product_disk=message[6]
    sql= "INSERT INTO products(product_name,product_price,product_quantity,product_category,product_subcategory,product_disk) VALUES ('" +str(poduct_name) +"' , '"+str(product_price)+"' , '"+str(product_quantity)+"','"+str(int(product_category)-1)+"',"+str(int(product_subcategory)-1)+",'"+str(product_disk)+"')"
    print(sql)
    cursor.execute(sql) 
    db.commit()
def selectTable(db,table,usl=[]):
    cursor=db.cursor()
    if usl==[]:
        sql= "SELECT * from "+ table
        cursor.execute(sql) 
        a=cursor.fetchall()
        return(a)
    else:
        sql= "SELECT * from "+ table+ " WHERE "+ usl[0]+" = '"+str(usl[1])+"'"
   
        cursor.execute(sql) 
       
        a=cursor.fetchall()
        return(a)
def selectProducts(db,message):
    cursor=db.cursor()
    id_subcategory=selectTable(db,"subcategory",usl=["subcategory_name",message.text])
    sql= "SELECT * from products Where product_category = '" +str(id_subcategory[0][1])+ "' and product_subcategory = '"+str(id_subcategory[0][0])+"'"
    cursor.execute(sql) 
    a=cursor.fetchall()
    return(a)

def delete_product(message,db):
    cursor=db.cursor()
    delete_product_id=message

    sql= "DELETE from products where product_id=" + str(delete_product_id)

    cursor.execute(sql) 
    db.commit()
def product_in_busket(busket_info,db):
    cursor=db.cursor()
    sql="INSERT INTO busket VALUES( '"+str(busket_info[0])+"','"+str(busket_info[1])+" ')"
    cursor.execute(sql)
    db.commit()
def product_out_busket(busket_info_out,db):
    cursor=db.cursor()
    user_id=busket_info_out[0]
    product_id=busket_info_out[1]

    sql="DELETE FROM busket WHERE rowid IN (SELECT rowid FROM busket WHERE product_id = "+str(product_id)+" AND busket_id = "+str(user_id)+ " LIMIT 1)"
    print(sql)
    cursor.execute(sql)
    db.commit()
def new_order_for_user(order_info,db):
    cursor=db.cursor()
    order_name=order_info[0]
    order_date=order_info[1]
    order_busket=order_info[2]
    order_comm=order_info[3]
    order_adress=order_info[4]
    order_status=0
    sql="INSERT INTO orders (order_name, order_date, order_busket, order_comm,order_adress,order_status) VALUES( '"+str(order_name)+"','"+str(order_date) +"','"+str(order_busket)+"','"+str(order_comm)+"','"+str(order_adress)+"','"+str(order_status)+"')"
    cursor.execute(sql)
    db.commit()

# cursor.execute("INSERT INTO subcategory (subcategory_name,category_id) VALUES ('Яичница',5)")
#cursor.execute("UPDATE users set user_number=0 where user_status=0")
#cursor.execute("SELECT * from products")
# print(cursor.fetchall())print(selectTable(db,"subcategory",usl=["subcategory_name","Молоко"]))
def user_busket_select(db,busket_id):
    cursor=db.cursor()
    sql="Select busket_id, product_id,count(product_id) from busket WHERE busket_id= "+str(busket_id) +" group by product_id"
    cursor.execute(sql)
    a=cursor.fetchall()
    return a
def user_orders_select(db,order_name):
    cursor=db.cursor()
    sql="Select * from orders WHERE order_name= '"+str(order_name) +"'"
    cursor.execute(sql)
    a=cursor.fetchall()
    return a
def set_phone_number(db,phone_number):
    cursor=db.cursor()
    sql="UPDATE users set user_number= +"+str(phone_number)
    cursor.execute(sql)
    db.commit()
def admin_orders_activitu(db):
    cursor=db.cursor()
    sql="Select * from orders WHERE order_status ='"+str(0) +"' or order_status = '" + str (1)+"'"
    cursor.execute(sql)
    a=cursor.fetchall()
    return a
def admin_orders_complited(db):
    cursor=db.cursor()
    sql="Select * from orders WHERE order_status= '"+str(-1) +"' or order_status = '"+str(2)+"'"
    cursor.execute(sql)
    a=cursor.fetchall()
    return a
def setOrderStatus(db,order_status):
    cursor=db.cursor()
    order_id=order_status[0]
    order_stat=order_status[1]

    sql="UPDATE orders set order_status = "+str(order_stat)+ " Where order_id = "+ str(order_id)
    cursor.execute(sql)
    db.commit()
# cursor.execute("INSERT INTO products (product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чай зеленый', 100, 50, 1, 1, 'Зеленый чай')")
# cursor.execute("INSERT INTO products (product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чай черный', 70, 100, 1, 1, 'Черный чай')")
# cursor.execute("INSERT INTO products (product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чай фруктовый', 150, 30, 1, 1, 'Фруктовый чай')")
# cursor.execute("INSERT INTO products (product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чай зеленый с мятой', 170, 40, 1, 1, 'Зеленый чай с мятой')")
# cursor.execute("INSERT INTO products (product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чай ромашковый', 100, 60, 1, 1, 'Ромашковый чай')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Red Bull', 150.0, 10, 1, 2, '250 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Monster Energy', 180.0, 8, 1, 2, '500 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Burn', 100.0, 15, 1, 2, '330 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Rockstar', 200.0, 5, 1, 2, '473 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('5-Hour Energy', 70.0, 20, 1, 2, '59 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Молоко Домик в деревне', 80.0, 20, 1, 3, '1 литр')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Молоко Простоквашино', 100.0, 15, 1, 3, '950 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Молоко Белый Город', 120.0, 10, 1, 3, '0,5 литра')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Молоко Савушкин продукт', 150.0, 12, 1, 3, '900 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Молоко Петмол', 200.0, 8, 1, 3, '1,5 литра')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Сок Яблочный', 70.0, 20, 1, 4, '1 литр')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Сок Апельсиновый', 90.0, 15, 1, 4, '950 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Сок Грушевый', 100.0, 10, 1, 4, '0,5 литра')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Сок Вишневый', 120.0, 12, 1, 4, '900 мл')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Сок Томатный', 150.0, 8, 1, 4, '1,5 литра')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Кофе растворимый', 50.0, 20, 1, 5, '100 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Кофе молотый', 80.0, 15, 1, 5, '250 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Кофе в зернах', 120.0, 10, 1, 5, '500 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Кофе молотый арабика', 150.0, 12, 1, 5, '200 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Кофе молотый робуста', 200.0, 8, 1, 5, '250 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чипсы сольные', 70.0, 20, 2, 6, '150 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Чипсы сметана и лук', 90.0, 15, 2, 6, '120 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Лейс оригинальные', 100.0, 10, 2, 6, '200 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Принглс волшебные', 120.0, 12, 2, 6, '180 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Картофельные чипсы', 150.0, 8, 2, 6, '250 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Крекеры с сыром', 60.0, 30, 2, 7, '100 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Крекеры с орехами', 80.0, 25, 2, 7, '150 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Соленые крекеры', 90.0, 20, 2, 7, '120 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Крекеры с луком', 110.0, 18, 2, 7, '180 грамм')")
# cursor.execute("INSERT INTO products(product_name, product_price, product_quantity, product_category, product_subcategory, product_disk) VALUES ('Итальянские крекеры', 130.0, 15, 2, 7, '200 грамм')")

db.commit()
db.close()