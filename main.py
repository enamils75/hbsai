import requests
from bs4 import BeautifulSoup
import sqlite3
from transformers import pipeline

# تهيئة قاعدة البيانات
conn = sqlite3.connect('learning_db.sqlite')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS learned_data (id INTEGER PRIMARY KEY, content TEXT)''')
conn.commit()

# تهيئة نموذج الذكاء الاصطناعي
nlp = pipeline("text-generation", model="gpt-2")

def learn_from_internet(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text()
    # تخزين النص الذي تم تعلمه في قاعدة البيانات
    c.execute("INSERT INTO learned_data (content) VALUES (?)", (text,))
    conn.commit()
    return text

def learn_from_comments(comment):
    # استخدام النموذج لتعلم من التعليقات
    generated_text = nlp(comment, max_length=50, num_return_sequences=1)
    # تخزين النص الذي تم تعلمه في قاعدة البيانات
    c.execute("INSERT INTO learned_data (content) VALUES (?)", (generated_text[0]['generated_text'],))
    conn.commit()
    return generated_text

def main():
    # مثال لجلب البيانات من الإنترنت
    url = "https://example.com"
    learned_text = learn_from_internet(url)
    print("Learned from internet:", learned_text)

    # مثال للتعلم من تعليقات المستخدمين
    user_comment = "This is a user comment."
    learned_comment = learn_from_comments(user_comment)
    print("Learned from user comment:", learned_comment)

if __name__ == "__main__":
    main()
