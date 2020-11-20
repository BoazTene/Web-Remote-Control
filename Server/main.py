from fastapi import FastAPI
from fastapi.responses import HTMLResponse
# from Server.MachineClient import MachineClient

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def root():
    return """
    <html>
        <head>
            <title>Some HTML in here</title>
        </head>
        <body>
            <h1>Look ma! HTML!</h1>
        </body>
    </html>
    """


