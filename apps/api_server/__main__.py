import uvicorn

from apps.api_server.app import build_app

uvicorn.run('apps.api_server.app:app', port=8000, reload=True)