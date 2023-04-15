# Telegram-бот для дистанционного управления компьютером
# Примечания
* Отдельно скачайте и поместите в папку со скриптом файл ffmpeg.exe
# Что нового
* Версия 0.0
  * 3 кнопки ("Запустить калькулятор", "Запустить Chrome", "Запустить Firefox") + 1 текстовая команда ("Убить Firefox")
* Версия 1.0
  * 3 кнопки, при нажатии на которые присылается сообщение с прикреплёнными callback-кнопками:
    * Запустить приложение
      * Запустить Firefox
    * Убить приложение
      * Убить Firefox
    * Выключение
      * Выключить
      * Перезагрузить
      * Заблокировать
      * Выйти
  * Распознавание речи и реакция на глосовые команды
    * заблокировать
    * калькулятор
    * блокнот
    * закрыть
    * Интер
    * скрин
  * Если текстовая команда не распознана, она выполяется как команда для командной строки
* Версия 2.0
  * Разрешено использование только пользователем с прописанным в текстовом файле tg_id.txt id Telegram
  * Если текстовая или голосовая команда ошибочная для командной строки, то синтезируется голосовое сообщение с набранным или произнесённым текстом соответственно
* Версия 3.0
  * Кнопки, при нажатии на некоторые присылается сообщение с прикреплёнными callback-кнопками:
    * 💻О системе
    * 🌐IP-адрес
    * 🏁Запустить приложение
      * Запустить Firefox
      * Запустить Фотошоп
    * 🔫Убить приложение
      * Убить Firefox
      * Запустить Фотошоп
    * 🖥Скриншот
    * 📷Камера
      * [Отображается список камер, при нажатии на кнопку отправлляется фотография с конкретной камеры]
    * Выключение
      * Выключить
      * Перезагрузить
      * Заблокировать
      * Выйти
    * Медиа/громкость
      * ⏮
      * ⏹
      * ⏯
      * ⏯
      * ⏯
      * 🔈
      * 🔊
      * 🔇
  * Распознавание речи и реакция на глосовые команды
    * закрыть
    * интер
    * скриншот
  * Если текстовая команда не распознана, она выполяется как команда для командной строки
  * Если текстовая или голосовая команда ошибочная для командной строки, то синтезируется голосовое сообщение с набранным или произнесённым текстом соответственно
* Версия 4.0
  * Добавлена функция сохранения файла в папке скрипта, при отправления боту документа
* Версия 5.0
  * Изменения кнопок:
    * 🖥Скриншот
      * Скриншот
      * Стрим
    * ⌨Клавиатура
      * /start
      * ⬆
      * ❌
      * ⬅
      * ⬇
      * ➡
      * Win
      * Enter
      * Другое
    * 📤📥Файлы
    * 👨‍💻Ввод команды
  * Теперь при ошибках бот перезапускается
* Версия 6.0
  * Теперь при нажатии на кнопку 📤📥Файлы присылается сообщения с содержимым папки и команды для перехода на родительскую папку, папки и в папке и работа с файлами в папке
* Версия 7.0
  * Информация выводимая при нажатии на кнопки 💻О системе и 🌐IP-адрес обрамлена тегами <code></code>
* tg_id.txt - текстовый файл с вашим id Telegram
* tg_token.txt - текстовый файл с токеном Telegram-бота
![изображение](https://user-images.githubusercontent.com/104255472/232228557-41a9e090-0b95-43d6-a533-6302df4ce919.png)
