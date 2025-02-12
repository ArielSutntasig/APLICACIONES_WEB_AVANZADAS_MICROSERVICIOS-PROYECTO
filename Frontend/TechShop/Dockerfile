# Etapa 1: Build de la aplicación con Node.js
FROM node:18-alpine AS builder

# Establece el directorio de trabajo
WORKDIR /app

# Copia package.json y package-lock.json (si existe) y luego instala las dependencias
COPY package*.json ./
RUN npm install

# Copia el resto de la aplicación y ejecuta el build
COPY . .
RUN npm run build

# Etapa 2: Servir la aplicación con Nginx
FROM nginx:alpine

# Elimina el contenido por defecto de Nginx
RUN rm -rf /usr/share/nginx/html/*

# Copia la carpeta "dist" generada en la etapa de build al directorio de Nginx
COPY --from=builder /app/dist /usr/share/nginx/html

# Expone el puerto 80, que es el que Nginx usará para servir la aplicación
EXPOSE 80

# Inicia Nginx en primer plano
CMD ["nginx", "-g", "daemon off;"]
