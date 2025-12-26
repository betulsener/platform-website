from .base import *

# Geliştirme ortamı
DEBUG = True

# Geliştirme sunucusu için allowed hosts
ALLOWED_HOSTS = ["localhost", "127.0.0.1"]

# Database override edilebilir
DATABASES['default']['NAME'] = BASE_DIR / "db.sqlite3"

# Buraya develop branch için başka ayarlar ekleyebilirsin
