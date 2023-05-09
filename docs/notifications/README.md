# Notification service

Данный сервис отвечает за настройку уведомлений для пользователей и пересылку их сервисы, которые непосредственно
доставляют уведомления. 

Схема базы данных:

Настройка пользователя хранится в `Redis`, так как на данный момент она очень маленькая, а доставать ее нужно быстро,э,
чтобы обрабатывать входящие события. 

API entrypoints:

    POST /set { status: "active" | "inactive" }
    POST /get { }: 200: { status: "active" | "inactive" }

В обоих методах используется `POST`, так как встроенная библиотека http в Go позволяет делать только POST 
запросы без дополнительных костылей.

Уведомления для отправки в телеграм отправляются в канал `telegram`, сообщения из которого потребляет 
`tgnotifier`

Сам же этот сервис потребляет сообщения из канала `notifications`.

Структура сообщения выглядит так:
    
    Type    string
	Time    time.Time
	Message string
	UserIds []int

Так же в файле рядом можно посмотреть схему