from .lookupSeq.lookupSeqFromLemma import lookupSeqFromLemma
import math
def drawSentenceGesture(lemmas,phrases,meta_datas,POS):

    # gesture['X_positions']=[]
    # gesture.Y_positions=[]
    # gesture.dir_sequence=[]
    # gesture.pressure_variation=[]

    gesture=[]
    constituents=[]
    for i in range(0,len(lemmas)):
        print("---")
        print(phrases[i])
        # constituents[i].X_positions=[]
        # constituents[i].Y_positions=[]
        
        # constituents[i].X_constrained=0
        # constituents[i].Y_constrained=0

        #Set origin for gesture
        X_origin_constituent=5
        Y_origin_constituent=1+(i-1)*7
        [seq,X_size,Y_size]=lookupSeqFromLemma(lemmas[i])
        print(lemmas[i],X_size,Y_size,seq)
        X_origin_constituent=5-math.floor(X_size/2)
        Y_origin_constituent=4+(i-1)*7-math.floor(Y_size/2)

        #Generate gesture from dir sequence     
        seq=seq[1::]
        seq = seq[:-1:]
        start_dir=seq[0]
        seq=seq[1::]

    return gesture