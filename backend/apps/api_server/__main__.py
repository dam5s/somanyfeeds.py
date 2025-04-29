from os import environ

import uvicorn

port_from_env = int(environ.get("PORT", 8081))
use_reload = environ.get("RELOAD", "false") == "true"

uvicorn.run(
    app="backend.apps.api_server.app:build_app_from_env",
    port=port_from_env,
    factory=True,
    reload=use_reload,
)
