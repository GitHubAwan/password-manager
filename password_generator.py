import random
import pyperclip

# ---------------------------- PASSWORD GENERATOR ------------------------------- #

class PasswordGenerator:
    @staticmethod
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

        return password
