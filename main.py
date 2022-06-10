from fastapi import FastAPI
from fastapi.responses import FileResponse
from txt2gest_fun.drawSentenceGesture import drawSentenceGesture
from txt2gest_fun.gestureToPlot import gestureToPlot
from txt2gest_fun.docParse import parse_doc

# Instantiate the class
app = FastAPI()

# Define a GET method on the specified endpoint
@app.get("/txt2gest/{text}")
async def readitem(text: str):
    [phrases,lemmas,meta_datas,POS] = parse_doc(text)
    gesture=drawSentenceGesture(phrases,lemmas,meta_datas,POS)
    gestureToPlot(gesture)  
    # POS_string = '-->'.join(map(str, POS))
    return FileResponse('plot.png')
