import os
from api import app
from bot import client

PORT = os.environ.get('PORT', 8080)
TOKEN = os.environ.get('TOKEN', None)

client.loop.create_task(app.run_task('0.0.0.0', PORT))
client.run(TOKEN)
