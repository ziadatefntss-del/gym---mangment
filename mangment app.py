
# import tkinter as tk
# from tkinter import ttk, messagebox, filedialog
# import sqlite3
# from datetime import datetime, timedelta
# import pandas as pd
# import shutil
# from reportlab.lib.pagesizes import A4
# from reportlab.pdfgen import canvas
# import smtplib
# from email.mime.text import MIMEText
# from email.mime.multipart import MIMEMultipart
# from reportlab.pdfbase import pdfmetrics
# from reportlab.pdfbase.ttfonts import TTFont
# # إعداد قاعدة البيانات
# def initialize_db():
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
    
#     # إنشاء جدول المشتركين إذا لم يكن موجودًا
#     cursor.execute('''CREATE TABLE IF NOT EXISTS members (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         name TEXT,
#                         age INTEGER,
#                         phone TEXT,
#                         id_number TEXT,
#                         subscription_type TEXT,
#                         start_date TEXT,
#                         end_date TEXT,
#                         paid_amount REAL,
#                         remaining_amount REAL,
#                         email TEXT
#                     )''')
    
#     # إنشاء جدول المستخدمين إذا لم يكن موجودًا
#     cursor.execute('''CREATE TABLE IF NOT EXISTS users (
#                         id INTEGER PRIMARY KEY AUTOINCREMENT,
#                         username TEXT UNIQUE,
#                         password TEXT,
#                         role TEXT
#                     )''')
    
#     # إضافة مستخدم مدير افتراضي إذا لم يكن موجودًا
#     cursor.execute("INSERT OR IGNORE INTO users (username, password, role) VALUES (?, ?, ?)", 
#                    ("admin", "admin123", "مدير"))
    
#     conn.commit()
#     conn.close()

# # إضافة عمود email إذا لم يكن موجودًا
# def add_email_column():
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     try:
#         cursor.execute("ALTER TABLE members ADD COLUMN email TEXT")
#         conn.commit()
#         print("تمت إضافة العمود 'email' بنجاح!")
#     except sqlite3.OperationalError as e:
#         print(f"العمود موجود بالفعل أو حدث خطأ: {e}")
#     finally:
#         conn.close()

# # تسجيل الدخول
# def login(username, password):
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT role FROM users WHERE username = ? AND password = ?", (username, password))
#     user = cursor.fetchone()
#     conn.close()
#     return user[0] if user else None

# # إضافة مشترك إلى قاعدة البيانات
# def add_member(name, age, phone, id_number, sub_type, start_date, end_date, paid_amount, remaining_amount, email):
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("INSERT INTO members (name, age, phone, id_number, subscription_type, start_date, end_date, paid_amount, remaining_amount, email) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
#                    (name, age, phone, id_number, sub_type, start_date, end_date, paid_amount, remaining_amount, email))
#     conn.commit()
#     conn.close()

# # حذف مشترك من قاعدة البيانات
# def delete_member(member_id):
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("DELETE FROM members WHERE id = ?", (member_id,))
#     conn.commit()
#     conn.close()

# # تعديل بيانات مشترك
# def update_member(member_id, name, age, phone, id_number, sub_type, start_date, end_date, paid_amount, remaining_amount, email):
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("UPDATE members SET name=?, age=?, phone=?, id_number=?, subscription_type=?, start_date=?, end_date=?, paid_amount=?, remaining_amount=?, email=? WHERE id=?",
#                    (name, age, phone, id_number, sub_type, start_date, end_date, paid_amount, remaining_amount, email, member_id))
#     conn.commit()
#     conn.close()

# # تمديد الاشتراك
# def extend_subscription(member_id, days):
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT end_date FROM members WHERE id = ?", (member_id,))
#     end_date = cursor.fetchone()[0]
#     new_end_date = (datetime.strptime(end_date, "%Y-%m-%d") + timedelta(days=days)).strftime("%Y-%m-%d")
#     cursor.execute("UPDATE members SET end_date = ? WHERE id = ?", (new_end_date, member_id))
#     conn.commit()
#     conn.close()
#     return new_end_date

# # جلب المشتركين من قاعدة البيانات
# def fetch_members(search_query=""):
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     if search_query:
#         cursor.execute("SELECT * FROM members WHERE id LIKE ? OR name LIKE ? OR phone LIKE ?", (f"%{search_query}%", f"%{search_query}%", f"%{search_query}%"))
#     else:
#         cursor.execute("SELECT * FROM members")
#     rows = cursor.fetchall()
#     conn.close()
#     return rows

# # حساب الإحصائيات
# def calculate_statistics():
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT subscription_type, end_date FROM members")
#     rows = cursor.fetchall()
#     conn.close()

#     total_members = len(rows)
#     active_members = 0
#     expired_members = 0
#     subscription_counts = {"أسبوعي": 0, "نصف شهري": 0, "شهري": 0, "ربع سنوي": 0, "سنوي": 0}

#     for sub_type, end_date in rows:
#         end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
#         if end_date_obj >= datetime.now():
#             active_members += 1
#         else:
#             expired_members += 1
#         if sub_type in subscription_counts:
#             subscription_counts[sub_type] += 1

#     return total_members, active_members, expired_members, subscription_counts

# # تصدير البيانات إلى Excel
# def export_to_excel():
#     conn = sqlite3.connect("gym.db")
#     df = pd.read_sql_query("SELECT * FROM members", conn)
#     conn.close()
#     file_path = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=[("Excel files", "*.xlsx")])
#     if file_path:
#         df.to_excel(file_path, index=False)
#         messagebox.showinfo("نجاح", "تم تصدير البيانات بنجاح!")

# # إنشاء نسخة احتياطية من قاعدة البيانات
# def backup_database():
#     backup_path = filedialog.asksaveasfilename(defaultextension=".db", filetypes=[("SQLite files", "*.db")])
#     if backup_path:
#         shutil.copyfile("gym.db", backup_path)
#         messagebox.showinfo("نجاح", "تم إنشاء نسخة احتياطية بنجاح!")

# # إنشاء بطاقة اشتراك
# pdfmetrics.registerFont(TTFont('Arial', 'arial.ttf'))  # تأكد من وجود ملف الخط في نفس المجلد

# def generate_membership_card(member_id, name, sub_type, end_date):
#     file_name = f"membership_card_{member_id}.pdf"
#     c = canvas.Canvas(file_name, pagesize=A4)
    
#     # استخدام الخط الذي يدعم العربية
#     c.setFont("Arial", 16)
    
#     # كتابة النصوص باللغة العربية
#     c.drawString(100, 750, "بطاقة اشتراك الجيم")
#     c.setFont("Arial", 12)
#     c.drawString(100, 700, f"رقم المشترك: {member_id}")
#     c.drawString(100, 670, f"الاسم: {name}")
#     c.drawString(100, 640, f"نوع الاشتراك: {sub_type}")
#     c.drawString(100, 610, f"تاريخ انتهاء الاشتراك: {end_date}")
    
#     c.save()
#     messagebox.showinfo("نجاح", f"تم إنشاء بطاقة الاشتراك وحفظها كـ {file_name}")

# # إرسال إشعارات
# def send_notification(email, member_name, end_date):
#     sender_email = "your_email@example.com"  # استخدم بريدك الإلكتروني
#     sender_password = "your_password"  # كلمة مرور البريد الإلكتروني
#     subject = "تنبيه: اقتراب انتهاء اشتراكك في الجيم"
#     body = f"عزيزي/عزيزتي {member_name},\n\nاشتراكك في الجيم سينتهي في تاريخ {end_date}. يرجى تجديد الاشتراك لتجنب الانقطاع.\n\nشكرًا لثقتك بنا."

#     message = MIMEMultipart()
#     message["From"] = sender_email
#     message["To"] = email
#     message["Subject"] = subject
#     message.attach(MIMEText(body, "plain"))

#     try:
#         with smtplib.SMTP("smtp.gmail.com", 587) as server:  # استخدم خادم بريدك
#             server.starttls()
#             server.login(sender_email, sender_password)
#             server.sendmail(sender_email, email, message.as_string())
#         messagebox.showinfo("نجاح", f"تم إرسال الإشعار إلى {email}")
#     except Exception as e:
#         messagebox.showerror("خطأ", f"فشل إرسال الإشعار: {e}")

# # التحقق من المشتركين وإرسال الإشعارات
# def check_expiring_members():
#     conn = sqlite3.connect("gym.db")
#     cursor = conn.cursor()
#     cursor.execute("SELECT name, end_date, email FROM members")
#     rows = cursor.fetchall()
#     conn.close()

#     for name, end_date, email in rows:
#         end_date_obj = datetime.strptime(end_date, "%Y-%m-%d")
#         days_remaining = (end_date_obj - datetime.now()).days
#         if 0 < days_remaining <= 7:  # إرسال إشعار إذا بقي أقل من أسبوع
#             send_notification(email, name, end_date)

# # واجهة المستخدم
# def main():
#     # إنشاء نافذة Tkinter الرئيسية
#     root = tk.Tk()
#     root.title("نظام إدارة الجيم")
#     root.geometry("1200x800")

#     # إخفاء النافذة الرئيسية حتى يتم تسجيل الدخول
#     root.withdraw()

#     # نافذة تسجيل الدخول
#     def login_gui():
#         def attempt_login():
#             username = username_entry.get()
#             password = password_entry.get()
#             role = login(username, password)
#             if role:
#                 login_window.destroy()
#                 show_main_window(role)
#             else:
#                 messagebox.showerror("خطأ", "اسم المستخدم أو كلمة المرور غير صحيحة!")

#         login_window = tk.Toplevel(root)
#         login_window.title("تسجيل الدخول")
#         login_window.geometry("300x150")

#         tk.Label(login_window, text="اسم المستخدم:").grid(row=0, column=0, padx=5, pady=5)
#         username_entry = ttk.Entry(login_window)
#         username_entry.grid(row=0, column=1, padx=5, pady=5)

#         tk.Label(login_window, text="كلمة المرور:").grid(row=1, column=0, padx=5, pady=5)
#         password_entry = ttk.Entry(login_window, show="*")
#         password_entry.grid(row=1, column=1, padx=5, pady=5)

#         login_button = ttk.Button(login_window, text="تسجيل الدخول", command=attempt_login)
#         login_button.grid(row=2, column=0, columnspan=2, pady=10)

#     # نافذة البرنامج الرئيسية
#     def show_main_window(role):
#         root.deiconify()
#         if role == "موظف":
#             delete_button.config(state=tk.DISABLED)
#             update_button.config(state=tk.DISABLED)
#             export_button.config(state=tk.DISABLED)
#             backup_button.config(state=tk.DISABLED)
#             clear_all_button.config(state=tk.DISABLED)

#     # تهيئة قاعدة البيانات وتحديث الجدول والإحصائيات
#     initialize_db()
#     add_email_column()  # تأكد من إضافة العمود email إذا لم يكن موجودًا

#     # فتح نافذة تسجيل الدخول
#     login_gui()

#     # إطار تفاصيل المشتركين
#     details_frame = ttk.LabelFrame(root, text="إضافة/تعديل مشترك")
#     details_frame.pack(fill="x", padx=10, pady=10)

#     tk.Label(details_frame, text="الاسم:").grid(row=0, column=0, padx=5, pady=5)
#     name_entry = ttk.Entry(details_frame)
#     name_entry.grid(row=0, column=1, padx=5, pady=5)

#     tk.Label(details_frame, text="العمر:").grid(row=0, column=2, padx=5, pady=5)
#     age_entry = ttk.Entry(details_frame)
#     age_entry.grid(row=0, column=3, padx=5, pady=5)

#     tk.Label(details_frame, text="رقم الهاتف:").grid(row=1, column=0, padx=5, pady=5)
#     phone_entry = ttk.Entry(details_frame)
#     phone_entry.grid(row=1, column=1, padx=5, pady=5)

#     tk.Label(details_frame, text="الرقم القومي:").grid(row=1, column=2, padx=5, pady=5)
#     id_number_entry = ttk.Entry(details_frame)
#     id_number_entry.grid(row=1, column=3, padx=5, pady=5)

#     tk.Label(details_frame, text="نوع الاشتراك:").grid(row=2, column=0, padx=5, pady=5)
#     sub_type_combo = ttk.Combobox(details_frame, values=["أسبوعي", "نصف شهري", "شهري", "ربع سنوي", "سنوي"])
#     sub_type_combo.grid(row=2, column=1, padx=5, pady=5)

#     tk.Label(details_frame, text="تاريخ البداية (YYYY-MM-DD):").grid(row=2, column=2, padx=5, pady=5)
#     start_date_entry = ttk.Entry(details_frame)
#     start_date_entry.grid(row=2, column=3, padx=5, pady=5)

#     tk.Label(details_frame, text="تاريخ النهاية (YYYY-MM-DD):").grid(row=3, column=0, padx=5, pady=5)
#     end_date_entry = ttk.Entry(details_frame)
#     end_date_entry.grid(row=3, column=1, padx=5, pady=5)

#     tk.Label(details_frame, text="المدفوع:").grid(row=3, column=2, padx=5, pady=5)
#     paid_amount_entry = ttk.Entry(details_frame)
#     paid_amount_entry.grid(row=3, column=3, padx=5, pady=5)

#     tk.Label(details_frame, text="الباقي:").grid(row=4, column=0, padx=5, pady=5)
#     remaining_amount_entry = ttk.Entry(details_frame)
#     remaining_amount_entry.grid(row=4, column=1, padx=5, pady=5)

#     tk.Label(details_frame, text="البريد الإلكتروني:").grid(row=4, column=2, padx=5, pady=5)
#     email_entry = ttk.Entry(details_frame)
#     email_entry.grid(row=4, column=3, padx=5, pady=5)

#     def add_member_gui():
#         name = name_entry.get()
#         age = age_entry.get()
#         phone = phone_entry.get()
#         id_number = id_number_entry.get()
#         sub_type = sub_type_combo.get()
#         start_date = start_date_entry.get()
#         end_date = end_date_entry.get()
#         email = email_entry.get()
#         try:
#             paid_amount = float(paid_amount_entry.get())
#             remaining_amount = float(remaining_amount_entry.get())
#         except ValueError:
#             messagebox.showerror("خطأ في الإدخال", "يجب إدخال قيم رقمية صحيحة للمدفوع والباقي!")
#             return

#         if not all([name, age, phone, id_number, sub_type, start_date, end_date, email]):
#             messagebox.showerror("خطأ في الإدخال", "جميع الحقول مطلوبة!")
#             return

#         add_member(name, age, phone, id_number, sub_type, start_date, end_date, paid_amount, remaining_amount, email)
#         messagebox.showinfo("نجاح", "تم إضافة المشترك بنجاح!")
#         clear_entries()
#         update_table()
#         update_statistics()

#     def clear_entries():
#         name_entry.delete(0, tk.END)
#         age_entry.delete(0, tk.END)
#         phone_entry.delete(0, tk.END)
#         id_number_entry.delete(0, tk.END)
#         sub_type_combo.set("")
#         start_date_entry.delete(0, tk.END)
#         end_date_entry.delete(0, tk.END)
#         paid_amount_entry.delete(0, tk.END)
#         remaining_amount_entry.delete(0, tk.END)
#         email_entry.delete(0, tk.END)

#     def delete_member_gui():
#         selected_item = table.selection()
#         if not selected_item:
#             messagebox.showerror("خطأ", "يجب اختيار مشترك لحذفه!")
#             return

#         member_id = table.item(selected_item, "values")[0]
#         delete_member(member_id)
#         messagebox.showinfo("نجاح", "تم حذف المشترك بنجاح!")
#         update_table()
#         update_statistics()

#     def update_member_gui():
#         selected_item = table.selection()
#         if not selected_item:
#             messagebox.showerror("خطأ", "يجب اختيار مشترك لتعديل بياناته!")
#             return

#         member_id = table.item(selected_item, "values")[0]
#         name = name_entry.get()
#         age = age_entry.get()
#         phone = phone_entry.get()
#         id_number = id_number_entry.get()
#         sub_type = sub_type_combo.get()
#         start_date = start_date_entry.get()
#         end_date = end_date_entry.get()
#         email = email_entry.get()
#         try:
#             paid_amount = float(paid_amount_entry.get())
#             remaining_amount = float(remaining_amount_entry.get())
#         except ValueError:
#             messagebox.showerror("خطأ في الإدخال", "يجب إدخال قيم رقمية صحيحة للمدفوع والباقي!")
#             return

#         if not all([name, age, phone, id_number, sub_type, start_date, end_date, email]):
#             messagebox.showerror("خطأ في الإدخال", "جميع الحقول مطلوبة!")
#             return

#         update_member(member_id, name, age, phone, id_number, sub_type, start_date, end_date, paid_amount, remaining_amount, email)
#         messagebox.showinfo("نجاح", "تم تعديل بيانات المشترك بنجاح!")
#         clear_entries()
#         update_table()
#         update_statistics()

#     def extend_subscription_gui():
#         selected_item = table.selection()
#         if not selected_item:
#             messagebox.showerror("خطأ", "يجب اختيار مشترك لتمديد الاشتراك!")
#             return

#         member_id = table.item(selected_item, "values")[0]
#         days = days_entry.get()
#         try:
#             days = int(days)
#             if days <= 0:
#                 raise ValueError
#         except ValueError:
#             messagebox.showerror("خطأ", "يجب إدخال عدد أيام صحيح موجب!")
#             return

#         new_end_date = extend_subscription(member_id, days)
#         messagebox.showinfo("نجاح", f"تم تمديد الاشتراك حتى {new_end_date}")
#         update_table()

#     def update_table():
#         for row in table.get_children():
#             table.delete(row)
#         for member in fetch_members(search_entry.get()):
#             try:
#                 end_date = datetime.strptime(member[7], "%Y-%m-%d")
#                 status_color = "green" if end_date >= datetime.now() else "red"
#             except ValueError:
#                 status_color = "red"  # إذا كان التاريخ غير صالح، ضع اللون الأحمر
#             table.insert("", tk.END, values=member, tags=(status_color,))
#         table.tag_configure("green", background="lightgreen")
#         table.tag_configure("red", background="lightcoral")

#     def update_statistics():
#         total, active, expired, counts = calculate_statistics()
#         stats_text = (
#             f"إجمالي المشتركين: {total}\n"
#             f"الاشتراكات السارية: {active}\n"
#             f"الاشتراكات المنتهية: {expired}\n"
#             f"أسبوعي: {counts['أسبوعي']} | نصف شهري: {counts['نصف شهري']}\n"
#             f"شهري: {counts['شهري']} | ربع سنوي: {counts['ربع سنوي']} | سنوي: {counts['سنوي']}"
#         )
#         stats_label.config(text=stats_text)

#     def search_member():
#         update_table()

#     def print_membership_card():
#         selected_item = table.selection()
#         if not selected_item:
#             messagebox.showerror("خطأ", "يجب اختيار مشترك لطباعة البطاقة!")
#             return

#         member_id, name, _, _, _, sub_type, _, end_date, _, _, _ = table.item(selected_item, "values")
#         generate_membership_card(member_id, name, sub_type, end_date)

#     def clear_all_data():
#         confirm = messagebox.askyesno("تأكيد", "هل أنت متأكد أنك تريد مسح جميع البيانات؟")
#         if confirm:
#             conn = sqlite3.connect("gym.db")
#             cursor = conn.cursor()
#             cursor.execute("DELETE FROM members")
#             conn.commit()
#             conn.close()
#             messagebox.showinfo("نجاح", "تم مسح جميع البيانات بنجاح!")
#             update_table()

#     add_button = ttk.Button(details_frame, text="إضافة المشترك", command=add_member_gui)
#     add_button.grid(row=5, column=0, padx=5, pady=10)

#     update_button = ttk.Button(details_frame, text="تعديل المشترك", command=update_member_gui)
#     update_button.grid(row=5, column=1, padx=5, pady=10)

#     delete_button = ttk.Button(details_frame, text="حذف المشترك", command=delete_member_gui)
#     delete_button.grid(row=5, column=2, padx=5, pady=10)

#     print_card_button = ttk.Button(details_frame, text="طباعة بطاقة الاشتراك", command=print_membership_card)
#     print_card_button.grid(row=5, column=3, padx=5, pady=10)

#     # إضافة الأزرار الجديدة في الصف السادس
#     export_button = ttk.Button(details_frame, text="تصدير إلى Excel", command=export_to_excel)
#     export_button.grid(row=6, column=0, padx=5, pady=5)

#     backup_button = ttk.Button(details_frame, text="إنشاء نسخة احتياطية", command=backup_database)
#     backup_button.grid(row=6, column=1, padx=5, pady=5)

#     clear_all_button = tk.Button(details_frame, text="مسح جميع البيانات", 
#                                 command=clear_all_data, bg='red', fg='white')
#     clear_all_button.grid(row=6, column=2, padx=5, pady=5)

#     # إطار تمديد الاشتراك
#     extend_frame = ttk.LabelFrame(root, text="تمديد الاشتراك")
#     extend_frame.pack(fill="x", padx=10, pady=10)

#     tk.Label(extend_frame, text="عدد الأيام:").grid(row=0, column=0, padx=5, pady=5)
#     days_entry = ttk.Entry(extend_frame)
#     days_entry.grid(row=0, column=1, padx=5, pady=5)

#     extend_button = ttk.Button(extend_frame, text="تمديد الاشتراك", command=extend_subscription_gui)
#     extend_button.grid(row=0, column=2, padx=5, pady=5)

#     # إطار البحث
#     search_frame = ttk.LabelFrame(root, text="بحث عن مشترك")
#     search_frame.pack(fill="x", padx=10, pady=10)

#     tk.Label(search_frame, text="بحث (بكود المشترك أو الاسم أو الهاتف):").grid(row=0, column=0, padx=5, pady=5)
#     search_entry = ttk.Entry(search_frame)
#     search_entry.grid(row=0, column=1, padx=5, pady=5)

#     search_button = ttk.Button(search_frame, text="بحث", command=search_member)
#     search_button.grid(row=0, column=2, padx=5, pady=5)

#     # إطار جدول المشتركين
#     table_frame = ttk.LabelFrame(root, text="قائمة المشتركين")
#     table_frame.pack(fill="both", expand=True, padx=10, pady=10)

#     columns = ("رقم المشترك", "الاسم", "العمر", "رقم الهاتف", "الرقم القومي", "نوع الاشتراك", "تاريخ البداية", "تاريخ النهاية", "المدفوع", "الباقي", "البريد الإلكتروني")
#     table = ttk.Treeview(table_frame, columns=columns, show="headings")
#     for col in columns:
#         table.heading(col, text=col)
#         table.column(col, width=100)
#     table.pack(fill="both", expand=True)

#     # إطار الإحصائيات مع شريط تمرير
#     stats_frame = ttk.LabelFrame(root, text="إحصائيات")
#     stats_frame.pack(fill="x", padx=10, pady=10)

#     # إنشاء Canvas وشريط التمرير
#     stats_canvas = tk.Canvas(stats_frame)
#     stats_canvas.pack(side="left", fill="both", expand=True)

#     scrollbar = ttk.Scrollbar(stats_frame, orient="vertical", command=stats_canvas.yview)
#     scrollbar.pack(side="right", fill="y")

#     stats_canvas.configure(yscrollcommand=scrollbar.set)
#     stats_canvas.bind("<Configure>", lambda e: stats_canvas.configure(scrollregion=stats_canvas.bbox("all")))

#     stats_label = tk.Label(stats_canvas, text="", justify="left")
#     stats_canvas.create_window((0, 0), window=stats_label, anchor="nw")

#     # تحديث الجدول والإحصائيات
#     update_table()
#     update_statistics()

#     root.mainloop()

# if __name__ == "__main__":
#     main()

