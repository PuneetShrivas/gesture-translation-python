from fastapi import FastAPI
from fastapi.responses import FileResponse
from txt2gest_fun.drawSentenceGesture import drawSentenceGesture
from txt2gest_fun.gestureToPlot import gestureToPlot
from txt2gest_fun.gestureToPlot import  gestureToGif
from txt2gest_fun.docParse import parse_doc

# Instantiate the class
app = FastAPI()

# Define a GET method on the specified endpoint 
@app.get("/txt2gest/{text}")
async def readitem(text: str, t:str = None, overlay:bool=None,frame:int=None,speed:int=None,halt:int=None):
    [phrases,lemmas,meta_datas,POS] = parse_doc(text)
    if halt==None: halt=2
    gestures=drawSentenceGesture(phrases,lemmas,meta_datas,POS,halt)
    for gesture in gestures:
        print("S"+"".join([str(x) for x in gesture['dir_sequence'] ]) + "E")
        # for i in range(0,len(gesture['X_positions'])):
        #     print('(' + str(gesture['X_positions'][i]) + ',' + str(gesture['Y_positions'][i]) + ')', end = ' ')
  
    
    if t=='gif':
        gestureToGif(gestures,overlay,frame,speed)
        return FileResponse('plot.gif')
    else:
        gestureToPlot(gestures)
        return FileResponse('plot.png')
