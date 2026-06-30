# 🚀 Инструкция по деплою Python бота на Railway

## Шаг 1: Создайте таблицу donate_queue в Railway MySQL

### Вариант A: Через командную строку

```bash
mysql -h reseau.proxy.rlwy.net -u root -p --port 44404 --protocol=TCP railway
```

Пароль: `jlCtItyZXPAzzoLBwGlVDfxFWmkUXEtX`

Затем выполните:

```sql
CREATE TABLE IF NOT EXISTS `donate_queue` (
  `id` int NOT NULL AUTO_INCREMENT,
  `nickname` varchar(255) NOT NULL,
  `email` varchar(255) DEFAULT NULL,
  `commands` text NOT NULL COMMENT 'Команды разделенные через |',
  `price` decimal(10, 2) DEFAULT NULL,
  `status` enum('pending','processing','completed','failed') DEFAULT 'pending',
  `attempts` int NOT NULL DEFAULT '0' COMMENT 'Количество попыток выдачи',
  `created_at` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `executed_at` timestamp NULL DEFAULT NULL,
  `error_message` text,
  PRIMARY KEY (`id`),
  KEY `idx_status` (`status`),
  KEY `idx_created` (`created_at`),
  KEY `idx_nickname` (`nickname`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
```

### Вариант B: Через phpMyAdmin или HeidiSQL

1. Скачайте **HeidiSQL**: https://www.heidisql.com/download.php
2. Подключитесь:
   - Host: `reseau.proxy.rlwy.net`
   - User: `root`
   - Password: `jlCtItyZXPAzzoLBwGlVDfxFWmkUXEtX`
   - Port: `44404`
   - Database: `railway`
3. Откройте файл `config/add-donate-queue.sql` и выполните его

---

## Шаг 2: Создайте GitHub репозиторий для бота

### 1. Откройте командную строку в папке бота:

```bash
cd "c:\Users\a2807\Downloads\RageMine by LightLeak\DeltaWorld-Python-Bot"
```

### 2. Инициализируйте Git (если ещё не сделали):

```bash
git init
git add .
git commit -m "Python donate bot for DeltaWorld"
```

### 3. Создайте репозиторий на GitHub:

Зайдите на https://github.com/new и создайте новый репозиторий:
- Название: `deltaworld-python-bot` (или любое другое)
- Приватный или публичный - на ваш выбор
- **НЕ создавайте** README, .gitignore, license (у вас уже есть файлы)

### 4. Подключите и запушьте:

```bash
git remote add origin https://github.com/ВАШ_USERNAME/deltaworld-python-bot.git
git branch -M main
git push -u origin main
```

Замените `ВАШ_USERNAME` на ваш GitHub username!

---

## Шаг 3: Деплой на Railway

### 1. Зайдите на Railway:

https://railway.app/dashboard

### 2. Создайте новый проект:

- Нажмите **"New Project"**
- Выберите **"Deploy from GitHub repo"**
- Выберите репозиторий `deltaworld-python-bot`

### 3. Добавьте Environment Variables:

Зайдите в **Settings → Variables** и добавьте:

```env
DB_HOST=reseau.proxy.rlwy.net
DB_PORT=44404
DB_USER=root
DB_PASSWORD=jlCtItyZXPAzzoLBwGlVDfxFWmkUXEtX
DB_NAME=railway

RCON_HOST=d20.aurorix.net
RCON_PORT=25575
RCON_PASSWORD=2557525575

CHECK_INTERVAL=10
MAX_ATTEMPTS=3
```

### 4. Railway автоматически задеплоит бота! 🎉

---

## Шаг 4: Проверьте что бот работает

### 1. Откройте логи бота в Railway:

Railway Dashboard → Ваш проект Python бота → Deployments → Latest → View Logs

### 2. Должно быть примерно так:

```
🚀 DeltaWorld Donate Bot started!
📊 Check interval: 10s
🔌 RCON: d20.aurorix.net:25575
🗄️ MySQL: reseau.proxy.rlwy.net:44404
🔍 Testing RCON connection...
```

**ВАЖНО**: Если RCON выдаёт ошибку `ECONNREFUSED`, это значит что порт 25575 закрыт или заблокирован файрволом. Нужно:
- Открыть порт 25575 на хостинге сервера
- Проверить что в `server.properties` есть `enable-rcon=true`
- Если хостинг не позволяет открыть порт - использовать альтернативный метод (плагин MysqlInventoryBridge)

---

## Шаг 5: Протестируйте систему

### 1. Сделайте покупку на сайте DeltaWorld

Зайдите на ваш сайт (на Railway) и купите что-нибудь в тестовом режиме.

### 2. Проверьте что заказ попал в базу:

```sql
SELECT * FROM donate_queue WHERE status = 'pending';
```

Должна появиться запись с вашим никнеймом и командами!

### 3. Подождите 10 секунд

Бот проверяет БД каждые 10 секунд.

### 4. Проверьте логи бота:

Должно появиться:
```
📦 Found 1 orders in queue
🎮 Processing order #123 for ваш_ник
✅ RCON executed: lp user ваш_ник parent set cobra
✅ Order #123 completed successfully!
```

### 5. Зайдите на сервер Minecraft и проверьте донат!

Если всё работает - команды выполнились и у вас есть донат!

---

## 🔧 Решение проблем

### ❌ RCON connection refused

**Проблема**: Порт 25575 закрыт или недоступен из интернета.

**Решение**:
1. Попросите хостинг открыть порт 25575
2. Проверьте `server.properties`: `enable-rcon=true`, `rcon.port=25575`
3. Перезапустите сервер Minecraft
4. Проверьте что файрвол не блокирует порт

**Альтернатива**: Если не получается открыть порт, используйте плагин который сам проверяет БД со стороны сервера (см. MYSQL_DONATE_SETUP.md)

---

### ❌ Database connection failed

**Проблема**: Не подключается к Railway MySQL.

**Решение**:
1. Проверьте переменные `DB_HOST`, `DB_PORT`, `DB_USER`, `DB_PASSWORD`, `DB_NAME`
2. Убедитесь что в Railway MySQL включен **Public Network**
3. Проверьте что таблица `donate_queue` создана: `SHOW TABLES;`

---

### ❌ Commands not executing

**Проблема**: Команды не выполняются на сервере.

**Решение**:
1. Проверьте формат команд - они должны быть БЕЗ `/`
2. Проверьте что LuckPerms установлен на сервере
3. Проверьте логи сервера Minecraft на ошибки

---

## 📊 Мониторинг системы

### Проверить очередь донатов:

```sql
-- Сколько ждёт выдачи
SELECT COUNT(*) FROM donate_queue WHERE status = 'pending';

-- Последние 10 заказов
SELECT * FROM donate_queue ORDER BY created_at DESC LIMIT 10;

-- Неудавшиеся попытки
SELECT * FROM donate_queue WHERE status = 'failed';

-- Успешно выданные
SELECT COUNT(*) FROM donate_queue WHERE status = 'completed';
```

### Логи бота в реальном времени:

Railway Dashboard → Ваш Python бот → Deployments → Latest → View Logs

---

## 💰 Стоимость Railway

**Starter план** (бесплатно):
- ✅ $5 кредитов в месяц
- ✅ ~500 часов работы (достаточно!)
- ✅ Автоматические перезапуски
- ✅ Логи в реальном времени

Python бот очень лёгкий, бесплатного плана хватит!

Если нужно больше → **Hobby план**: $5/месяц

---

## ✅ Готово!

Теперь система работает так:

1. 🛒 Покупка на сайте → запись в `donate_queue`
2. 🤖 Python бот проверяет БД каждые 10 сек
3. 🎮 Находит новый заказ → выполняет команды через RCON
4. ✅ Обновляет статус на `completed`
5. 🎉 Игрок получает донат!

**Всё автоматически, 24/7! 🚀**

---

## 🆘 Поддержка

Если что-то не работает:
1. Проверьте логи бота в Railway
2. Проверьте что таблица `donate_queue` создана
3. Проверьте что RCON порт открыт: `telnet d20.aurorix.net 25575`
4. Проверьте переменные окружения в Railway

Всё должно работать! 🎉
