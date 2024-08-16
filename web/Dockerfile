FROM node:18-alpine

# Устанавливаем рабочую директорию внутри контейнера
WORKDIR /app

# Копируем package.json и package-lock.json в контейнер
COPY package*.json ./

# Устанавливаем зависимости
RUN npm install

# Копируем все файлы проекта в контейнер
COPY . .

# Сборка приложения
RUN npm run build

# Устанавливаем сервер для обслуживания статики
RUN npm install -g serve

# Экспортируем порт
EXPOSE 3000

# Запуск команды для обслуживания статики
CMD ["serve", "-s", "build", "-l", "3000"]
