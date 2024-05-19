from tkinter import *
from tkinter import messagebox, ttk
from password_generator import PasswordGenerator
from database import DatabaseManager
import pyperclip #当点击创建密码时自动复制到剪贴板。https://pypi.org/project/pyperclip/


class PasswordManagerApp:
    def __init__(self, window):
        self.db = DatabaseManager()
        self.window = window
        self.user_id_number = 0

        self.window.title("Password Manager")
        self.window.config(padx=20, pady=20)

        self.canvas = Canvas(width=200, height=200, highlightthickness=0)
        self.logo_img = PhotoImage(file="images/logo.png")
        self.canvas.create_image(100, 100, image=self.logo_img)
        self.canvas.grid(column=1, row=0)

        self.setup_ui()

    def setup_ui(self):
        # 创建label
        self.website_label = Label(text="Website", font=("Courier", 15))
        self.website_label.grid(column=0, row=1)
        self.username_label = Label(text="Email/Username", font=("Courier", 15))
        self.username_label.grid(column=0, row=2)
        self.password_label = Label(text="Password", font=("Courier", 15))
        self.password_label.grid(column=0, row=3)
        # 创建Entry
        self.website_entry = Entry(self.window, width=20)
        self.website_entry.grid(column=1, row=1, columnspan=1)
        #通过focus来使软件一运行就到这一行。
        self.website_entry.focus()
        self.username_entry = Entry(self.window, width=35)
        self.username_entry.grid(column=1, row=2, columnspan=2)
        self.username_entry.insert(0, "alex@gmail.com")
        self.password_entry = Entry(self.window, width=20)
        self.password_entry.grid(column=1, row=3, columnspan=1)
        # 创建Button
        self.search_button = Button(self.window, text="Search", width=11, command=self.search)
        self.search_button.grid(column=2, row=1, columnspan=1)

        self.generate_pwd_button = Button(self.window, text="Generate Password", width=11, command=self.generate_password)
        self.generate_pwd_button.grid(column=2, row=3, columnspan=1)
        self.add_button = Button(self.window, text="Add", width=33, command=self.save_password)
        self.add_button.grid(column=1, row=4, columnspan=2)

        self.delete_data_button = Button(self.window, text="Delete Data", width=10, command=self.delete_data)
        self.delete_data_button.grid(column=0, row=5, columnspan=1)

        self.update_data_button = Button(self.window, text="Update Data", width=18, command=self.update_data)
        self.update_data_button.grid(column=1, row=5, columnspan=1)

        self.display_all_button = Button(self.window, text="Display All Data", width=11, command=self.display_all_data)
        self.display_all_button.grid(column=2, row=5, columnspan=1)
        # 创建显示数据的Treeview
        self.columns = ("website", "username", "password")
        self.tree = ttk.Treeview(self.window, columns=self.columns, show="headings")
        self.tree.heading("website", text="Website")
        self.tree.heading("username", text="Username")
        self.tree.heading("password", text="Password")
        self.tree.grid(column=0, row=6, columnspan=3, pady=10)
        # 设置列宽
        self.tree.column("website", width=130)
        self.tree.column("username", width=130)
        self.tree.column("password", width=170)
        # 绑定双击事件
        self.tree.bind("<Double-1>", self.on_item_selected)
# ---------------------------- PASSWORD GENERATOR ------------------------------- #

    def generate_password(self):
        password = PasswordGenerator.generate_password()
        # 清除已有的文本并插入新生成的密码
        self.password_entry.delete(0, END)
        self.password_entry.insert(0, password)
# ---------------------------- SAVE PASSWORD ------------------------------- #

    def save_password(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
        else:
            # 创建要写入的数据
            data_entry = (website, username, password)
            bubbles_message = f"These are the details entered:\nWebsite: {website}\nUsername: {username}\nPassword: {password}\nIs it ok to save?"
            user_check = messagebox.askyesno(title="Form", message=bubbles_message, icon='info')

            if user_check:
                self.db.add_password(website, username, password)
                # 清除Entry中的内容
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)
# ---------------------------- SEARCH ------------------------------- #

    def search(self):
        website = self.website_entry.get()
        rows = self.db.search_password(website)

        if rows:
            # 如果找到匹配的数据
            row = rows[0]
            bubbles_message = f"These are your details:\nWebsite: {row['website']}\nUsername: {row['username']}\nPassword: {row['password']}\n"
            messagebox.showinfo(title="Form", message=bubbles_message, icon='info')
        else:
            # 如果没有找到匹配的数据
            messagebox.showinfo(title="Form", message="No details found for the specified website.", icon='info')
        # 清除Entry中的内容
        self.website_entry.delete(0, END)
        self.password_entry.delete(0, END)
# ---------------------------- Display ALL DATA ------------------------------- #

    def display_all_data(self):
        rows = self.db.get_all_passwords()
        # 清空Treeview内容
        for item in self.tree.get_children():
            self.tree.delete(item)

        if rows:
            for row in rows:
                self.tree.insert("", END, values=(row["website"], row["username"], row["password"]))
# ---------------------------- ITEM SELECTED EVENT ------------------------------- #

    def on_item_selected(self, event):
        selected_item = self.tree.focus()
        item = self.tree.item(selected_item)
        values = item['values']

        if values:
            self.website_entry.delete(0, END)
            self.website_entry.insert(0, values[0])
            self.username_entry.delete(0, END)
            self.username_entry.insert(0, values[1])
            self.password_entry.delete(0, END)
            self.password_entry.insert(0, values[2])
            # 当点击时密码自动复制到剪贴板。https://pypi.org/project/pyperclip/
            password = self.password_entry.get()
            pyperclip.copy(password)
            # 获取主键值
            website = self.website_entry.get()
            username = self.username_entry.get()
            self.user_id_number = self.db.get_user_id_by_website_and_username(website, username)

     # ---------------------------- UPDATE DATA ------------------------------- #
    def update_data(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
        else:
            # 提示用户确认
            usercheck_message = f"Are you sure you want to update the entry for:\nWebsite: {website}\nUsername: {username}\nPassword: {password}?"
            user_check = messagebox.askyesno(title="Confirm Update", message=usercheck_message, icon='info')

            if user_check:
                self.db.update_password(self.user_id_number, website, username, password)
                messagebox.showinfo(title="Success", message="Entry updated successfully!")
                # 清除Entry中的内容
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)
                # 更新显示的数据
                self.display_all_data()

# ---------------------------- DELETE DATA ------------------------------- #
    def delete_data(self):
        website = self.website_entry.get()
        username = self.username_entry.get()
        password = self.password_entry.get()

        if not website or not username or not password:
            messagebox.showwarning(title="Oops", message="Please don't leave any fields empty!")
        else:
            #提示用户确认删除
            usercheck_message = f"Are you sure you want to delete the entry for:\nWebsite: {website}\nUsername: {username}\nPassword: {password}?"
            user_check = messagebox.askyesno(title="Confirm Deletion", message=usercheck_message, icon='info')

            if user_check:
                self.db.delete_password(website, username, password)
                messagebox.showinfo(title="Success", message="Entry deleted successfully!")
                # 清除Entry中的内容
                self.website_entry.delete(0, END)
                self.password_entry.delete(0, END)
                # 更新显示的数据
                self.display_all_data()

if __name__ == "__main__":
    window = Tk()
    app = PasswordManagerApp(window)
    window.mainloop()
