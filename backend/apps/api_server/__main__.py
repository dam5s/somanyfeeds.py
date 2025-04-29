from os import environ

import uvicorn

port_from_env = int(environ.get("PORT", 8001))

uvicorn.run('backend.apps.api_server.app:app', port=port_from_env, reload=True)
