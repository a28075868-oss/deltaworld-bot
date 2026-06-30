# 🤖 DeltaWorld Donate Bot (Python)

Автоматический бот для выдачи донатов через RCON. Запускается на Railway.

## 🚀 Деплой на Railway:

### 1. Создайте GitHub репозиторий:

```bash
cd "путь_к_папке_DeltaWorld-Python-Bot"
git init
git add .
git commit -m "DeltaWorld Donate Bot"
git remote add origin https://github.com/ВАШ_USERNAME/deltaworld-bot.git
git branch -M main
git push -u origin main
```

### 2. Зайдите на Railway:

https://railway.app/dashboard

### 3. Создайте новый проект:

- Нажмите **"New Project"**
- Выберите **"Deploy from GitHub repo"**
- Выберите репозиторий `deltaworld-bot`

### 4. Добавьте Environment Variables:

```bash
# Railway MySQL (если используете Railway MySQL)
DB_HOST=${{ MySQL.MYSQLHOST }}
DB_PORT=${{ MySQL.MYSQLPORT }}
DB_USER=${{ MySQL.MYSQLUSER }}
DB_PASSWORD=${{ MySQL.MYSQLPASSWORD }}
DB_NAME=${{ MySQL.MYSQLDATABASE }}

# Или вручную (если внешняя БД):
DB_HOST=reseau.proxy.rlwy.net
DB_PORT=44404
DB_USER=root
DB_PASSWORD=jlCtItyZXPAzzoLBwGlVDfxFWmkUXEtX
DB_NAME=railway

# RCON настройки
RCON_HOST=d20.aurorix.net
RCON_PORT=25575
RCON_PASSWORD=2557525575

# Опциональные настройки
CHECK_INTERVAL=10
MAX_ATTEMPTS=3
```

### 5. Railway автоматически задеплоит!

---

## 📊 Проверка работы:

### В Railway логах должно быть:

```
🚀 DeltaWorld Donate Bot started!
✅ RCON OK! Response: There are 5 of a max of 100 players online
✅ Database OK!
✅ All systems ready!
📦 Found 1 orders in queue
🎮 Processing order #123 for fastword
✅ RCON executed: lp user fastword parent set god
✅ Order #123 completed successfully!
```

---

## 🎮 На сервере Minecraft:

Убедитесь что в `server.properties`:

```properties
enable-rcon=true
rcon.port=25575
rcon.password=2557525575
```

**Перезапустите сервер после изменений!**

---

## ✅ Тестирование:

1. Сделайте покупку на сайте
2. Зайдите в Railway логи бота
3. Через 10 секунд должно появиться:
   ```
   📦 Found 1 orders in queue
   🎮 Processing order #...
   ✅ Order completed!
   ```
4. В игре проверьте донат!

---

## 🔧 Управление:

### Просмотр логов:
Railway Dashboard → Your Bot Service → Logs

### Перезапуск:
Railway Dashboard → Your Bot Service → ⋮ → Restart

### Остановка:
Railway Dashboard → Your Bot Service → Settings → Delete Service

---

## 💰 Стоимость:

Railway бесплатный план:
- ✅ 500 часов в месяц (достаточно!)
- ✅ Автоматические перезапуски
- ✅ Логи в реальном времени

Если нужно больше → Hobby план $5/месяц

---

## 🆘 Решение проблем:

### RCON не работает:

1. Проверьте переменные `RCON_HOST`, `RCON_PORT`, `RCON_PASSWORD`
2. Проверьте что порт 25575 открыт на сервере
3. Проверьте `server.properties`

### База данных не подключается:

1. Если используете Railway MySQL - используйте `${{ MySQL.MYSQL_URL }}`
2. Если внешняя БД - проверьте что Public Network включен
3. Проверьте данные подключения

### Бот не запускается:

1. Проверьте что `Procfile` есть в репозитории
2. Проверьте логи Railway
3. Проверьте что все переменные заданы

---

## ✨ Преимущества:

- ✅ Работает 24/7 в облаке
- ✅ Не нужен доступ к серверу Minecraft
- ✅ Автоматический перезапуск при ошибках
- ✅ Подробные логи
- ✅ Легко обновлять (git push)

---

**🎉 Готово! Бот автоматически выдает донаты через RCON!**
