from .lookupSeq.lookupSeqFromLemma import lookupSeqFromLemma
import math
import numpy as np
def drawSentenceGesture(lemmas,phrases,meta_datas,POS):

    # gesture['X_positions']=[]
    # gesture.Y_positions=[]
    # gesture.dir_sequence=[]
    # gesture.pressure_variation=[]
    gesture_X_positions=[]
    gesture_Y_positions=[]
    gesture_dir_sequence=[]
    gesture_pressure_variation=[]

    gesture=[]
    constituents=[]
    for i in range(0,len(lemmas)):
        print("---")
        constituents.append({'X_positions':[],'Y_positions':[],'dir_sequence':[],'X_constrained':0,'Y_constrained':0,'pressure_variation':[]})

        #Set origin for gesture
        X_origin_constituent=5
        Y_origin_constituent=1+(i)*7
        [seq,X_size,Y_size]=lookupSeqFromLemma(phrases[i])
        print(lemmas[i],X_size,Y_size,seq)
        X_origin_constituent=5-math.floor(X_size/2)
        Y_origin_constituent=4+(i)*7-math.floor(Y_size/2)
        #Generate gesture from dir sequence     
        seq=seq[1::]
        seq = seq[:-1:]
        start_dir=int(seq[0])
        seq=seq[1::]
        constituents[i]['dir_sequence'].append(start_dir)
        for iter in range(0,len(seq)):
            dirs = [1,2,3,4,5,6,7,8]
            dirs = np.roll(dirs,1-start_dir)
            shift_by=int(seq[iter])
            shifted_dirs=np.roll(dirs,shift_by)
            constituents[i]['dir_sequence'].append(shifted_dirs[0])
            start_dir=shifted_dirs[0]

        # Add grammatization
        if(POS[i]=='Verb'):
            print('is verb')
            if 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Pres'):
                print('and is present tense')
                constituents[i]['dir_sequence']=[5,5]+constituents[i]['dir_sequence']
            elif 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Past'):
                print('and is past tense')
                constituents[i]['dir_sequence']=[6,6]+constituents[i]['dir_sequence']
        if(POS[i]=='Noun'):
            print('is noun')
        if(POS[i]=='Adverb'):
            print('is adverb')
        if(POS[i]=='Adjective'):
            print('is adjective')
        if(POS[i]=='Pronoun'):
            print('is pronoun')
            if 'Number' in meta_datas[i] and (meta_datas[i]['Number'][0]=='Sing'):
                print('and is Singular')
            if 'Number' in meta_datas[i] and (meta_datas[i]['Number'][0]=='Plur'):
                print('and is Plural')
            if 'Person' in meta_datas[i] and (meta_datas[i]['Person'][0]=='1'):
                print('and is First Person')
                constituents[i]['X_constrained']=1
                X_origin_constituent=1
            if 'Person' in meta_datas[i] and (meta_datas[i]['Person'][0]=='2'):
                print('and is Second Person')
                constituents[i]['X_constrained']=1
                X_origin_constituent=5
            if 'Person' in meta_datas[i] and (meta_datas[i]['Person'][0]=='3'):
                print('and is Third Person')
                constituents[i]['X_constrained']=1
                X_origin_constituent=9

        # Generate constituent gesture
        constituents[i]['X_positions'].append(X_origin_constituent)
        constituents[i]['Y_positions'].append(Y_origin_constituent)
        for step in range(1,len(constituents[i]['dir_sequence'])):
            prop_dir=int(constituents[i]['dir_sequence'][step])
            if prop_dir>1 and prop_dir<5:
                constituents[i]['X_positions'].append(constituents[i]['X_positions'][-1]+1)
            if prop_dir>5 and prop_dir<9:
                constituents[i]['X_positions'].append(constituents[i]['X_positions'][-1]-1) 
            if prop_dir>3 and prop_dir<7:
                constituents[i]['Y_positions'].append(constituents[i]['Y_positions'][-1]+1) 
            if prop_dir<3 or prop_dir>7:
                constituents[i]['Y_positions'].append(constituents[i]['Y_positions'][-1]-1)
            if prop_dir==1 or prop_dir==5:
                constituents[i]['X_positions'].append(constituents[i]['X_positions'][-1])
            if prop_dir==7 or prop_dir==3:
                constituents[i]['Y_positions'].append(constituents[i]['Y_positions'][-1])
        
        if i>=2:
            if(constituents[i]['X_constrained']==0):
                X_shift=0
                if(constituents[i-1]['X_positions'][-1]<=constituents[i]['X_positions'][0]):
                    shifts=[constituents[i-1]['X_positions'][-1]-constituents[i]['X_positions'][0],1-min(constituents[i]['X_positions'])]
                    X_shift=max(shifts)
                elif(constituents[i-1]['X_positions'][-1]>constituents[i]['X_positions'][0]):
                    shifts=[constituents[i-1]['X_positions'][-1]-constituents[i]['X_positions'][0],9-max(constituents[i]['X_positions'])]
                    X_shift=min(shifts)
                constituents[i]['X_positions']=[k + X_shift for k in constituents[i]['X_positions']]
        
        constituents[i]['pressure_variation'] = np.ones(len(constituents[i]['X_positions']), dtype = int).tolist()
        constituents[i]['pressure_variation'][-1]=0

        # Add consitituent to overall gesture
        gesture_X_positions=gesture_X_positions+constituents[i]['X_positions']
        gesture_Y_positions=gesture_Y_positions+constituents[i]['Y_positions']
        gesture_dir_sequence=gesture_dir_sequence+constituents[i]['dir_sequence']
        gesture_pressure_variation=gesture_pressure_variation+constituents[i]['pressure_variation']

    gesture={'X_positions':gesture_X_positions,'Y_positions':gesture_Y_positions,'dir_sequence':gesture_dir_sequence,'pressure_variation':gesture_pressure_variation,'angular_vel':0,'data_density':0}
    return gesture