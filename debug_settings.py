from app.core.config import settings

print("DB_USER:", settings.DB_USER)
print("DB_PASSWORD:", settings.DB_PASSWORD)
print("DB_HOST:", settings.DB_HOST)
print("DB_PORT:", settings.DB_PORT)
print("DB_NAME:", settings.DB_NAME)
print("\nFull DATABASE_URL:")
print(settings.DATABASE_URL)
