import sqlite3
import re
import time
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import TfidfVectorizer
import json
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
        cursor.execute("SELECT message FROM tcore_input")
        rows = cursor.fetchall()
        messages = [row[0] for row in rows]

        processed_texts = []

        # Türkçe stopwords sözlüğünü yükle
        stopwords = []
        with open("/Users/betulsener/Desktop/Platform Website/platform-website/tcore/turkce-stop-words.txt", 'r', encoding='utf-8') as f:
            stopwords = [line.strip() for line in f]

        def remove_stopwords(text, stopwords):
            words = text.split()
            filtered_words = [word for word in words if word.lower() not in stopwords]
            return ' '.join(filtered_words)

        # Metinleri düzenle ve stopwords'leri kaldır
        for text in messages:
            text = re.sub(r'[^\w\s]', ' ', text)  # Remove punctuation
            text = re.sub(r'\d+', '', text)  # Remove numbers
            processed_texts.append(remove_stopwords(text, stopwords))

        final_text = ' '.join(processed_texts)

        # TF-IDF vektörleştirici ile anahtar kelimeleri çıkar
        sentences = nltk.sent_tokenize(final_text)
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

        # WordCloud oluştur
        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(limited_keywords)

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')
        wordcloud_path = "/Users/betulsener/Desktop/Platform Website/platform-website/media/analysis/wordcloud.png"

        # Klasörün var olup olmadığını kontrol edin, yoksa oluşturun
        if not os.path.exists(os.path.dirname(wordcloud_path)):
            os.makedirs(os.path.dirname(wordcloud_path))

        plt.savefig(wordcloud_path, format='png')
        plt.close()

        # WordCloud görselini BLOB formatında oku
        with open(wordcloud_path, 'rb') as file:
            wordcloud_blob = file.read()

        # input_id'yi belirle
        input_id = 1  # Uygun bir değer belirleyin veya 1 kullanabilirsiniz

        # Veritabanına tek bir analiz sonucu ekle
        cursor.execute("INSERT INTO tcore_analysis (wordcloud, keywords) VALUES (?, ?)", (wordcloud_blob, keywords_json))

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