# -*- coding: utf-8 -*-

import create
from config import Config

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(
        app=create.app,
        host=Config.url,
        port=Config.port,
        workers=Config.workers
    )