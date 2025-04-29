# SoManyFeeds in Python

## Running the dev servers

```
make dev-backend
```

```
make dev-frontend
```

The frontend will proxy to the backend for requests under `/api`

## Building the container and running it

```
make container
docker run -p8080:8080 -eSERVER_PORT=8080 -it somanyfeeds-py:latest
```
