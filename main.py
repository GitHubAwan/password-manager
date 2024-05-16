from tkinter import *
import random

FONT_NAME = "Courier"
OUTPUT_FILE_PATH ="data/data_password_manager.txt"
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
    # 清除已有的文本并插入新生成的密码
    password_entry.delete(0, END)
    password_entry.insert(0, password)


# ---------------------------- SAVE PASSWORD ------------------------------- #
def save_password():
    website = website_entry.get()
    username = username_entry.get()
    password = password_entry.get()
    print(website,username,password)
    # 创建一行要写入的数据
    data_line=f"{website} | {username} | {password}\n"

    # 追加写入文件，如果文件不存在则创建
    with open(OUTPUT_FILE_PATH, "a") as file:
        file.write(data_line)
    # 清除Entry中的内容
    website_entry.delete(0, END)
    password_entry.delete(0, END)
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
website_entry = Entry(window,width=35)
website_entry.grid(column=1,row=1,columnspan=2)
#通过focus来使软件一运行就到这一行。
website_entry.focus()
username_entry = Entry(window,width=35)
username_entry.grid(column=1,row=2,columnspan=2)
username_entry.insert(0,"alex@gmail.com")
password_entry = Entry(window,width=21)
password_entry.grid(column=1,row=3,columnspan=1)

# 创建Button
generate_pwd_button = Button(window, text="Generate Password", width= 11,command=generate_password)
generate_pwd_button.grid(column=2,row=3,columnspan=1)
add_button = Button(window, text="Add", width=33,command=save_password)
add_button.grid(column=1,row=4,columnspan=2)






window.mainloop()

