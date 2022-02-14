import datetime
import io
import os

from aiohttp import web
from beancount.scripts import example  # type: ignore


async def gen_beanfile():
    """Generates a randomized beancount ledger.

    Returns:
        The string contents of the randomized ledger.
    """
    end = datetime.date.today()
    start = datetime.date(end.year - 2, 1, 1)
    birth = datetime.date(end.year - 30, 1, 1)

    with io.StringIO() as s:
        example.write_example_file(birth, start, end, True, file=s)
        s.seek(0)
        return s.read()


async def on_startup(app: web.Application):
    app["beanfile"] = await gen_beanfile()


async def serve(request: web.Request):
    """Serves the stored ledger file contents."""
    return web.Response(text=request.app["beanfile"])


app = web.Application()
app.on_startup.append(on_startup)
app.router.add_get("/", serve)

if __name__ == "__main__":
    host = os.getenv("HOST", "0.0.0.0")
    port = os.getenv("PORT", 8001)

    web.run_app(app, host=host, port=int(port))
