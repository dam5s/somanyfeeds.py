# SoManyFeeds in Python

## Running the dev servers

```
make dev
```

The frontend will automatically proxy to the backend for requests under `/api`

## Running tests before push

```
make check
```

Before committing you can run automated fixes before the tests:
```
make fix check
```

## Building the container and running it

```
make container
docker run -p8080:8080 --expose 8080 -eSERVER_PORT=8080 -it somanyfeeds-py:latest
```
