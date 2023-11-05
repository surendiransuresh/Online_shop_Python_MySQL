

print("hello")
import mysql.connector
from tabulate import tabulate
import random

con = mysql.connector.connect(host="localhost",user="root",password="root",database="database")

res = con.cursor()

r = random.randint(1111, 9999)
user_id = "%04d" % r
o_id = random.randint(555555,999999)
ord_id = "%06d" % o_id
e_id = random.randint(22111,50909)
emp_code = "%05d" % e_id
p_code = random.randint(1000,3000)
proid = "%4d" % p_code

def user_signup():
    my_user_id = int(user_id)
    name = input("enter User name: ")
    phone_no = int(input("enter the Phone_no: "))
    city = input("enter the City: ")
    print(f"Hello {name}'s User_Id is: {my_user_id}")

    qry = "insert into user values (%s,%s,%s,%s)"
    val = (user_id,name,phone_no,city)
    res.execute(qry,val)
    con.commit()
    print("Sign Up succesfully!" )

def get_user():
    qry = "select user_id from user"
    res.execute(qry,)
    result = res.fetchall()
    # print(tabulate(result, headers=["user_id"]))
    listIds = []
    for i in result:
        listIds.append(i[0])
    return listIds

def get_order():
    user_id = int(input("enter the user_id: "))
    qry = "select order_code from orders where user_id = %s"
    val = (user_id,)
    res.execute(qry,val)
    result = res.fetchall()
    list_of_order = []
    for i in result:
        list_of_order.append(i[0])
    return list_of_order

def show_products_table():
    qry = "select * form products"
    res.execute(qry,)
    result = res.fetchall()
    print(tabulate(result, headers=["product_code","product_category","product_name","price","quantity"]))

def user_login():

    user_id = int(input("enter Your user_id: "))
    users_li = get_user()
    if user_id in users_li:
        print("You There")
        option = int(input("enter the option\n1.view booking\n2.new booking\n3.cancel booking: "))
        if option == 1:
            qry = "select * from orders where user_id = %s"
            val = (user_id,)
            res.execute(qry,val)
            result = res.fetchall()
            print(tabulate(result,headers=["order_code","user_id","product_category","product_name","price","quantity","total_cost"]))
        elif option == 2:
            qry = "select product_category,product_name,price from products"
            res.execute(qry)
            result = res.fetchall()
            print(tabulate(result,headers=["product_category","product_name","price"]))
            product_category = input("Enter the Product Category: ")
            product_name = input("enter the product name: ")
            quantity = int(input(f"enter {product_name} quantity: "))
            my_order_code = int(ord_id)
            print(f"Your order code is {my_order_code}")
            qry = "select price from products where product_name = %s"
            val = (product_name,)
            res.execute(qry,val)
            price_res = res.fetchone()
            price_res = price_res[0]
            total_cost = quantity * price_res
            print("total cost is: ",total_cost)
            try:
                qry = "insert into orders values (%s,%s,%s,%s,%s,%s,%s)"
                val = (my_order_code,user_id,product_category,product_name,price_res,quantity,total_cost)
                res.execute(qry,val)
                con.commit()
            except exception as e:
                print("something went wrong")
            else:
                qry = "select quantity from products where product_name = %s"
                val = (product_name,)
                res.execute(qry,val)
                st_result = res.fetchone()
                stock = st_result[0]
                if stock < quantity:
                    print("out of stock")
                else:
                    cur_stock = stock - quantity
                    qry = "update products set quantity = %s where product_name = %s"
                    val = (cur_stock,product_name)
                    res.execute(qry,val)
                    con.commit()
        elif option == 3:
            order_code = int(input("enter the order code: "))
            cust_ord_list = get_order()
            if order_code in cust_ord_list:
                qry = "select quantity from orders where order_code = %s"
                val = (order_code,)
                res.execute(qry,val)
                cn_qnt = res.fetchone()
                cn_qnt = cn_qnt[0]
                qry = "select product_name from  orders where order_code = %s"
                val = (order_code,)
                res.execute(qry,val)
                cn_pro = res.fetchone()
                cn_pro = cn_pro[0]
                qry = "select quantity from products where product_name = %s"
                val = (cn_pro,)
                res.execute(qry,val)
                st_result = res.fetchone()
                stock = st_result[0]
                updated_stk = stock + cn_qnt        #
                qry = "delete from orders where order_code = %s"
                val = (order_code,)
                res.execute(qry,val)
                con.commit()
                qry = "update products set quantity = %s where product_name = %s"
                val = (updated_stk,cn_pro)
                res.execute(qry,val)
                con.commit()
                print("order cancelled")
            else:
                print("Your Not orders list")
    else:
        print("Some Error")



# Employee Sction

def employee_signp():
    emplo_id = int(emp_code)
    employee_name = input("Enter your name: ")
    gender = input("Enter your gender Male/Female : ")
    age = int(input("Enter Your age: "))
    email_id = input("Enter Your Email Id: ")
    query = "insert into employee values (%s,%s,%s,%s,%s)"
    value = (emplo_id,employee_name,gender,age,email_id)
    res.execute(query,value)
    con.commit()
    print(f"Hey {employee_name}! Your Signup successfully finish.\nYour Employee Id is: {emplo_id}.")

def get_employee():
    query = "select employee_id from employee"
    res.execute(query)
    result = res.fetchall()
    list_of_emp_ids = []
    for i in result:
        list_of_emp_ids.append(i[0])
    return list_of_emp_ids

def employee_login():
    employee_Id = int(input("Enter Your Employee Id :"))
    employee_list = get_employee()
    if employee_Id in employee_list:
        option = int(input("1.Add Product\n2.Update Quantity\nEnter Your option: "))
        if option == 1:
            product_codee = int(p_code)
            product_category = input("Category of product: ")
            product_name = input("'Enter the Name of Product: ")
            price = int(input("Enter Price of Per item of Product: "))
            quantity = int(input(f"{product_name} Quantity amount "))
            query = "insert into products values (%s,%s,%s,%s,%s)"
            value = (product_codee,product_category,product_name,price,quantity)
            res.execute(query, value)
            con.commit()
            print(f"{product_name}'s product Code is : {p_code}")
            print("Product Added succesfully!")
        elif option == 2:

            product_name = input("Enter Product name to update Quanity: ")
            size = int(input(f"Enter the Quantity of {product_name}"))

            qry = "select quantity from products where product_name = %s"
            val = (product_name,)
            res.execute(qry, val)
            st_result = res.fetchone()
            stock = st_result[0]
            total_quantity = int(stock) + size

            qry = "update products set quantity = %s where product_name = %s"
            val = (total_quantity,product_name)
            res.execute(qry, val)
            con.commit()
            print("Quantity Updated Successfully.")
















print("Hello! Welcome to Shopings.")
option = input("A.Customer / B.Employee: ").upper()
if option == "A":
    a = "Customer"
    user = int(input(f"Dear '{a}' your options are, \n1.Sign up\n2.Login\nEnter the Option:  "))
    if user == 1:
        user_signup()
    elif user == 2:
        user_login()
    else:
        print(f"{user} is an invalid option. plz check!")
elif option == "B":
    b = "Employee"
    user = int(input(f"Hello '{b}' your options are, \n1.Sign up\n2.Login\nEnter the Option: "))
    if user == 1:
        employee_signp()
    elif user == 2:
        employee_login()
        pass
    else:
        print(f"{user} invalid option. plz check!")
else:
    print(f"{option} is an Invalid input !")
