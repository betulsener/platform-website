import sqlite3
import re
import time
import json
from sklearn.feature_extraction.text import TfidfVectorizer
import nltk
import os

# Dosya yolunu kontrol edin
db_path = '/Users/betulsener/Desktop/Platform Website/platform-website/db.sqlite3'
if not os.path.exists(db_path):
    raise FileNotFoundError(f"Veritabanı dosyası bulunamadı: {db_path}")

def create_analysis():
    try:
        # SQLite veritabanına bağlan
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        # Mesajları veritabanından çek
        cursor.execute("SELECT id, message FROM tcore_input")
        rows = cursor.fetchall()

        # Türkçe stopwords sözlüğünü yükle
        stopwords = []
        with open("/Users/betulsener/Desktop/Platform Website/platform-website/tcore/turkce-stop-words.txt", 'r', encoding='utf-8') as f:
            stopwords = [line.strip() for line in f]

        def remove_stopwords(text, stopwords):
            words = text.split()
            filtered_words = [word for word in words if word.lower() not in stopwords]
            return ' '.join(filtered_words)

        for row in rows:
            input_id, message = row
            # Metni düzenle ve stopwords'leri kaldır
            message = re.sub(r'[^\w\s]', ' ', message)  # Remove punctuation
            message = re.sub(r'\d+', '', message)  # Remove numbers
            processed_text = remove_stopwords(message, stopwords)

            # TF-IDF vektörleştirici ile anahtar kelimeleri çıkar
            sentences = nltk.sent_tokenize(processed_text)
            vectorizer = TfidfVectorizer(max_features=1000)
            X = vectorizer.fit_transform(sentences)
            terms = vectorizer.get_feature_names_out()
            scores = X.toarray().sum(axis=0)
            keywords = dict(zip(terms, scores))

            # Maksimum kelime sınırlaması
            max_keywords = 20
            sorted_keywords = sorted(keywords.items(), key=lambda x: x[1], reverse=True)
            limited_keywords = dict(sorted_keywords[:max_keywords])

            # İlk 3 anahtar kelimeyi seç
            top_keywords = list(limited_keywords.keys())[:3]
            keywords_json = json.dumps(top_keywords, ensure_ascii=False)

            # Keywords kolonunu güncelle
            cursor.execute("UPDATE tcore_input SET keywords = ? WHERE id = ?", (keywords_json, input_id))

        # Değişiklikleri kaydet
        conn.commit()

    except sqlite3.OperationalError as e:
        print(f"OperationalError occurred: {e}")
        time.sleep(5)  # 5 saniye bekle ve tekrar dene
        create_analysis()  # Yeniden dene

    finally:
        # Veritabanı bağlantısını kapat
        if conn:
            conn.close()

create_analysis()