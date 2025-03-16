FROM python:3.13-alpine AS base
FROM node:lts-alpine AS vue-build
WORKDIR /vue-app

COPY frontend/package*.json ./
RUN npm install

COPY frontend .
RUN npm run build-only -- --outDir dist


FROM base AS backend-build
WORKDIR /app

COPY backend/requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY --from=vue-build /vue-app/dist static
COPY backend .

CMD [ "python", "-u", "-m", "fastapi", "run" ]

#CMD [ "tail", "-f", "/dev/null" ]
