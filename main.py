import sqlite3
# import os
from tkinter import *
from tkinter import messagebox,ttk
import random
import pyperclip #当点击创建密码时自动复制到剪贴板。https://pypi.org/project/pyperclip/


FONT_NAME = "Courier"
DATABASE_PATH = "data/password_manager.db"
user_id_mumber = 0
password_dict = {}  # 用于存储实际密码的字典

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

def generate_password():
    letters_lowercase=['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x',
                       'y', 'z']
    letters_uppercase=['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X',
                       'Y', 'Z']
    numbers=['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    symbols=['!', '#', '$', '%', '&', '(', ')', '*', '+']

    # 生成密码
    strong_password=[]
    strong_password.extend(random.sample(letters_lowercase, 6))
    strong_password.extend(random.sample(letters_uppercase, 4))
    strong_password.extend(random.sample(numbers, 3))
    strong_password.extend(random.sample(symbols, 3))
    # 打乱密码顺序
    random.shuffle(strong_password)
    # 将密码列表转换为字符串
    password=''.join(strong_password)
    # 当点击创建密码时自动复制到剪贴板。https://pypi.org/project/pyperclip/
    pyperclip.copy(password)
    # pyperclip.paste()
    # 清除已有的文本并插入新生成的密码
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    print(website, username, password)

    if not website or not username or not password:
        messagebox.showwarning(
            title="Oops",
            message="Please don't leave any fields empty!"
        )
    else:
        # 创建要写入的数据
        data_entry=(website, username, password)
        bubbles_message = f"These are the details entered:\n website: {website}\n username: {username}\n password: {password}\n Is it ok to save?"
        user_check = messagebox.askyesno(title="Form",
                                         message=bubbles_message,
                                         icon='info')

        if user_check:
            # 连接到SQLite数据库（如果数据库不存在会自动创建）
            conn = sqlite3.connect(DATABASE_PATH)
            cursor = conn.cursor()

            # 创建数据表（如果不存在）
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS passwords (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    website TEXT NOT NULL,
                    username TEXT NOT NULL,
                    password TEXT NOT NULL
                )
            ''')

            # 插入新数据
            cursor.execute('''
                INSERT INTO passwords (website, username, password)
                VALUES (?, ?, ?)
            ''', data_entry)

            # 提交事务并关闭连接
            conn.commit()
            conn.close()

            # 清除Entry中的内容
            website_entry.delete(0, END)
            password_entry.delete(0, END)

# ---------------------------- SEARCH ------------------------------- #
def search():
    website=website_entry.get()
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row  # 设置行工厂,这行很关健
    cursor = conn.cursor()
    # search数据
    cursor.execute('''SELECT * FROM passwords WHERE website = ?''', (website,))
    rows=cursor.fetchall()

    if rows:
        # 如果找到匹配的数据
        row=rows[0]
        bubbles_message=f"These are your details:\n Website: {row['website']}\n Username: {row['username']}\n Password: {row['password']}\n"
        # bubbles_message = f"These are your details:\n Website: {rows[0][1]}\n Username: {rows[0][2]}\n Password: {rows[0][3]}\n"
        messagebox.showinfo(title="Form", message=bubbles_message, icon='info')
    else:
        # 如果没有找到匹配的数据
        messagebox.showinfo(title="Form", message="No details found for the specified website.", icon='info')

    # 提交事务并关闭连接
    conn.commit()
    conn.close()


    # 清除Entry中的内容
    website_entry.delete(0, END)
    password_entry.delete(0, END)

# ---------------------------- Display ALL DATA ------------------------------- #

def display_all_data():
    # 连接到SQLite数据库
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute('''SELECT * FROM passwords''')
    rows = cursor.fetchall()
    conn.close()

    # 清空Treeview内容
    for item in tree.get_children():
        tree.delete(item)

    # if rows:
    #     for row in rows:
    #         tree.insert("", END, values=(row["website"], row["username"], row["password"]))

    # 清空密码字典
    password_dict.clear()

    if rows:
        for row in rows:
            masked_password = '*' * len(row["password"])  # 将密码替换为星号
            tree.insert("", END, values=(row["website"], row["username"], masked_password))
            # 将实际密码保存到字典中
            password_dict[(row["website"], row["username"])] = row["password"]

# ---------------------------- ITEM SELECTED EVENT ------------------------------- #

def on_item_selected(event):
    global user_id_mumber
    selected_item = tree.focus()
    item = tree.item(selected_item)
    values = item['values']

    if values:
        website_entry.delete(0, END)
        website_entry.insert(0, values[0])
        username_entry.delete(0, END)
        username_entry.insert(0, values[1])
        # password_entry.delete(0, END)
        # password_entry.insert(0, values[2])

        password_entry.delete(0, END)
        masked_password = '*' * len(password_dict[(values[0], values[1])])
        password_entry.insert(0, masked_password)  # 显示星号密码
        # 获取实际密码并复制到剪贴板
        actual_password = password_dict[(values[0], values[1])]
        pyperclip.copy(actual_password)
        # # 当点击时密码自动复制到剪贴板。https://pypi.org/project/pyperclip/
        # password=password_entry.get()
        # pyperclip.copy(password)

        # 获取主键值
        website=website_entry.get()
        username=username_entry.get()
        user_id_mumber = get_user_id_by_name_and_age(website,username)
        print(f"The ID of Charlie is: {user_id_mumber}")

# ---------------------------- 查找ID值 ------------------------------- #

def get_user_id_by_name_and_age(website, username):

    conn=sqlite3.connect(DATABASE_PATH)
    cursor=conn.cursor()

    cursor.execute('''
    SELECT id FROM passwords WHERE website = ? AND username = ?
    ''', (website, username))
    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]
    else:
        return None



# ---------------------------- 更新函数 ------------------------------- #
def update_website_user_pass_by_id(user_id,website,username,password):
    conn=sqlite3.connect(DATABASE_PATH)
    cursor=conn.cursor()
    cursor.execute('''
    UPDATE passwords
    SET website = ?, username = ?, password = ?
    WHERE id = ?
    ''', (website,username,password,user_id))
    # 提交事务并关闭连接
    conn.commit()
    conn.close()

# ---------------------------- UPDATE DATA ------------------------------- #
def update_data():
    website=website_entry.get()
    username=username_entry.get()
    password=password_entry.get()
    if not website or not username or not password:
        messagebox.showwarning(
            title="Oops",
            message="Please don't leave any fields empty!"
        )
    else:
        # 提示用户确认删除
        usercheck_message=f"Are you sure you want to update the entry for:\nWebsite: {website}\nUsername: {username}\nPassword: {password}?"
        user_ckeck=messagebox.askyesno(
            title="Confirm Deletion",
            message=usercheck_message,
            icon='info'
        )
        if user_ckeck:
            update_website_user_pass_by_id(user_id_mumber,website,username,password)

            messagebox.showinfo(title="Success", message="Entry Update successfully!")
            # 清除Entry中的内容
            website_entry.delete(0, END)
            password_entry.delete(0, END)

            # 更新显示的数据
            display_all_data()

# ---------------------------- DELETE DATA ------------------------------- #
def delete_data():
    website=website_entry.get()
    username=username_entry.get()
    password=password_entry.get()
    if not website or not username or not password:
        messagebox.showwarning(
            title="Oops",
            message="Please don't leave any fields empty!"
        )
    else:
        #提示用户确认删除
        usercheck_message = f"Are you sure you want to delete the entry for:\nWebsite: {website}\nUsername: {username}\nPassword: {password}?"
        user_ckeck = messagebox.askyesno(
            title="Confirm Deletion",
            message=usercheck_message,
            icon='info'
        )
        if user_ckeck:
            # 连接到SQLite数据库
            conn=sqlite3.connect(DATABASE_PATH)
            cursor=conn.cursor()
            # 删除数据
            cursor.execute('''
                DELETE FROM passwords
                WHERE website = ? AND username = ? AND password = ?
            ''', (website, username, password))
            # 提交事务并关闭连接
            conn.commit()
            conn.close()

            messagebox.showinfo(title="Success",message="Entry deleted successfully!")
            # 清除Entry中的内容
            website_entry.delete(0,END)
            password_entry.delete(0,END)

            # 更新显示的数据
            display_all_data()



# ---------------------------- UI SETUP ------------------------------- #

window = Tk()
window.title("Password Manager")
window.config(padx=20,pady=20)



canvas = Canvas(width=200,height=200,highlightthickness=0)
logo_img = PhotoImage(file="images/logo.png")
canvas.create_image(100,100,image=logo_img)
canvas.grid(column=1,row=0)

# 创建label
website_label = Label(text="Website", font=(FONT_NAME, 15))
website_label.grid(column=0, row=1)
username_label = Label(text="Email/Username", font=(FONT_NAME, 15))
username_label.grid(column=0, row=2)
password_label = Label(text="Password", font=(FONT_NAME, 15))
password_label.grid(column=0, row=3)

# 创建Entry
website_entry = Entry(window,width=20)
website_entry.grid(column=1,row=1,columnspan=1)
#通过focus来使软件一运行就到这一行。
website_entry.focus()
username_entry = Entry(window,width=35)
username_entry.grid(column=1,row=2,columnspan=2)
username_entry.insert(0,"alex@gmail.com")
password_entry = Entry(window,width=20)
password_entry.grid(column=1,row=3,columnspan=1)

# 创建Button
search_button = Button(window, text="Search", width=11,command=search)
search_button.grid(column=2,row=1,columnspan=1)

generate_pwd_button = Button(window, text="Generate Password", width= 11,command=generate_password)
generate_pwd_button.grid(column=2,row=3,columnspan=1)
add_button = Button(window, text="Add", width=33,command=save_password)
add_button.grid(column=1,row=4,columnspan=2)

delete_data_button = Button(window, text="Delete Data", width=10, command=delete_data)
delete_data_button.grid(column=0, row=5, columnspan=1)

update_data_button = Button(window, text="Update Data", width=18, command=update_data)
update_data_button.grid(column=1, row=5, columnspan=1)

display_all_button = Button(window, text="Display All Data", width=11, command=display_all_data)
display_all_button.grid(column=2, row=5, columnspan=1)





# 创建显示数据的Treeview
columns = ("website", "username", "password")
tree = ttk.Treeview(window, columns=columns, show="headings")
tree.heading("website", text="Website")
tree.heading("username", text="Username")
tree.heading("password", text="Password")
tree.grid(column=0, row=6, columnspan=3, pady=10)

# 设置列宽
tree.column("website", width=130)
tree.column("username", width=130)
tree.column("password", width=170)

# 绑定双击事件
tree.bind("<Double-1>", on_item_selected)



window.mainloop()

