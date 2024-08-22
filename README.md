# My Favorite Novel

## Описание

**My Favorite Novel** — это веб-приложение для чтения интерактивных новелл, позволяющее пользователям следить за прогрессом чтения, а также возвращаться к диалогам, которые они уже прошли. Приложение предоставляет удобный интерфейс для погружения в увлекательные истории, разбитые на эпизоды и диалоги.

## Особенности

- **Чтение новелл**: Удобный интерфейс для чтения интерактивных новелл.
- **Отслеживание прогресса**: Приложение запоминает, на каком эпизоде и диалоге пользователь остановился.
- **Сохранение прогресса**: Прогресс пользователя сохраняется автоматически и может быть восстановлен при следующем посещении.
- **Статус новеллы**: Показывает статус новеллы (новая, в процессе, завершена).
- **Интерактивный UI**: Кнопки и анимации обеспечивают приятное взаимодействие с пользователем.

## Структура проекта

- **backend/**: Серверная часть, написанная на Django, отвечает за API и логику обработки данных.
- **web/**: Клиентская часть на React, предоставляет интерфейс для взаимодействия с пользователем.
- **models.py**: Модели данных для хранения информации о новеллах, пользователях и их прогрессе.
- **api/views.py**: Виды, обеспечивающие обработку запросов к API для работы с новеллами и прогрессом пользователя.
- **serializers.py**: Сериализаторы для преобразования данных между Python-объектами и форматами JSON.
- **static/**: Статические файлы, такие как изображения и стили CSS.

## Установка

### 1. Клонирование репозитория

```bash
git clone https://github.com/Polina-Solovyova/VisualNovels.git
cd VisualNovels
```
### 2. Установка зависимостей
#### Backend

```bash
cd backend
pip install -r requirements.txt
python manage.py migrate
```

#### Frontend
```bash
cd web
npm install
```

### 3. Запуск проекта
#### Backend


```bash
cd backend
python manage.py runserver
```
#### Frontend

```bash
cd frontend
npm start
```

## Использование
1. Зарегистрируйтесь или войдите в систему. 
2. Выберите новеллу из списка доступных. 
3. Начните чтение, нажимая на соответствующую новеллу. 
4. Прогресс будет сохранен автоматически.
### Пример использования
1. Регистрация и авторизация

Для работы с сервисом пользователю необходимо авторизоваться в системе. Страница авторизации открывается по умолчанию. Чтобы зарегистрироваться в сервисе, нужно нажать на кнопку «Регистрация», которая находится в правом нижнем углу.

![](./docs/img/login.png)

После этого необходимо указать свой e-mail адрес (нельзя создать несколько аккаунтов с одним и тем же e-mail), создать уникальное имя пользователя и пароль длиной от 8 до 128 символов. Затем нажмите на кнопку «Зарегистрироваться».

![](./docs/img/registration.png)

Если регистрация прошла успешно, автоматически откроется окно авторизации. Для входа в сервис укажите своё имя пользователя и пароль, а затем нажмите на кнопку «Войти».

2. Начало чтения новеллы

Чтобы начать читать новеллу, перейдите на вкладку «Novels», если вы не находитесь на главной странице. Выберите интересующую вас новеллу из доступного списка и нажмите на неё.
![](./docs/img/novels_carousel.png)
![](./docs/img/novels_filter.png)
После выбора новеллы откроется страница с её описанием и возможностью начать чтение. Нажмите кнопку «Read», чтобы приступить к чтению.
![](./docs/img/novel_detail.png)
Прогресс чтения будет сохраняться автоматически. Если вы уже читали эту новеллу ранее, приложение вернет вас к последнему сохранению.

3. Продолжение чтения

Для продолжения чтения ранее начатой новеллы снова выберите её из каталога. Если новелла уже была начата, вы автоматически вернетесь к последнему сохранению.

Прогресс чтения будет обновляться по мере прохождения диалогов. Вы также сможете увидеть текущий прогресс чтения в процентах на странице новеллы.

4. Завершение новеллы

После завершения последнего эпизода и диалога статус новеллы изменится на «Completed», а прогресс будет отображаться как 100%. Кнопка «Read» станет неактивной и поменяет цвет на серый.
![](./docs/img/novel_completed.png)


5. Просмотр результатов

Для просмотра вашего прогресса и статистики прочитанных новелл перейдите на вкладку «Profile». Здесь вы сможете увидеть список завершенных новелл и прогресс по текущим.
![](./docs/img/profile_page.png)

Возможность детального анализа прочитанных новелл и получения рекомендаций находится в разработке.



## Требования
- Python 3.11+
- Django 5.0.7+
- Node.js 14+
- npm 10.8.2+
- React 17+
