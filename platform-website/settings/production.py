# production.py
from .base import *

# Production ortamında DEBUG kapalı
DEBUG = True

# Production domainlerini ekle
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']

# Production veritabanı (örnek: PostgreSQL, SQLite da olabilir)
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
        'USER': os.getenv("DATABASE_USER"),         # .env'deki kullanıcı
        'PASSWORD': os.getenv("DATABASE_PASSWORD"), # .env'deki şifre
        'HOST': os.getenv("DATABASE_HOST", "localhost"),
        'PORT': os.getenv("DATABASE_PORT", "5432"),
    }
}

# Statik ve medya dosyaları prod için
STATIC_ROOT = BASE_DIR / 'staticfiles'
MEDIA_ROOT = BASE_DIR / 'mediafiles'

# Güvenlik ekleri (opsiyonel)
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True

# Secret key hala .env'den çekiliyor
SECRET_KEY = os.getenv("SECRET_KEY")
