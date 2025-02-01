# aiva
AI review assistant

### How to run

Copy `.example.env` content to `.env` file

Start app in dev mode run:
```shell
granian --interface asgi src.main:app --host 0.0.0.0 --port 8080 --reload --no-log
```

Swagger should be available in `127.0.0.1:8080/docs`
