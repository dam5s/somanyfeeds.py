from os import environ

import uvicorn

port_from_env = int(environ.get("PORT", 8081))
use_reload = environ.get("RELOAD", "false") == "true"

uvicorn.run("backend.apps.api_server.app:app", port=port_from_env, reload=use_reload)
