from audioop import reverse
from .lookupSeq.lookupSeqFromLemma import lookupSeqFromLemma
import math
import numpy as np


def drawSentenceGesture(lemmas,phrases,meta_datas,POS):

    gestures=[]
    drawgestureframe(lemmas,phrases,meta_datas,POS,gestures)
    return gestures


def drawgestureframe(lemmas,phrases,meta_datas,POS,gestures,skips=0):
    gesture_X_positions=[]
    gesture_Y_positions=[]
    gesture_dir_sequence=[]
    gesture_pressure_variation=[]
    constituents=[]
    i=0
    while i < len(lemmas)-skips:
        print("---")
        print(i)
        print(lemmas)
        if i>2:
            gestures.append({'X_positions':gesture_X_positions,'Y_positions':gesture_Y_positions,'dir_sequence':gesture_dir_sequence,'pressure_variation':gesture_pressure_variation,'angular_vel':0,'data_density':0})
            # print("gestures before recursive call",gestures)
            drawgestureframe(lemmas[3:],phrases[3:],meta_datas[3:],POS[3:],gestures,skips)
            # print("gestures before recursive call",gestures)
            return

        print(POS[i])
        constituents.append({'X_positions':[],'Y_positions':[],'dir_sequence':[],'X_constrained':0,'Y_constrained':0,'pressure_variation':[]})

        #Set origin for gesture
        X_origin_constituent=5
        Y_origin_constituent=1+(i)*7
        [seq,X_size,Y_size]=lookupSeqFromLemma(phrases[i])
        # if seq=='':
        #     del lemmas[i]
        #     del phrases[i]
        #     del meta_datas[i]
        #     del POS[i]
        #     i=i-1
        #     continue
        print(lemmas[i])
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

        # Add grammatizations
        if(POS[i]=='Verb'):
            print('is verb')
            if 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Pres'):
                print('and is present tense')
                constituents[i]['dir_sequence']=[5,5]+constituents[i]['dir_sequence']
            elif 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Past'):
                print('and is past tense')
                constituents[i]['dir_sequence']=[6,6]+constituents[i]['dir_sequence']
            elif 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Fut'):
                print('and is future tense')
                constituents[i]['dir_sequence']=[4,4]+constituents[i]['dir_sequence']
            elif 'Tense' not in meta_datas[i]:
                print('and is present tense')
                print("meta datas: ",meta_datas[i])
                constituents[i]['dir_sequence']=[5,5]+constituents[i]['dir_sequence']
            if 'Aspect' in meta_datas[i] and (meta_datas[i]['Aspect'][0]=='Prog'):
                print('and is continous tense')
                constituents[i]['dir_sequence']=constituents[i]['dir_sequence']+[5,4]
            elif 'Aspect' in meta_datas[i] and (meta_datas[i]['Aspect'][0]=='Perf'):
                print('and is Perf tense')
                constituents[i]['dir_sequence']=constituents[i]['dir_sequence']+[5,6]
    
        if(POS[i]=='Question_Words'):
            print('is question word')
        if(POS[i]=='Modal'):
            print('is modal')
            if(lemmas[i].lower()=='will'):
                for j in range(i+1,len(lemmas)):
                    meta_datas[j]={**meta_datas[j],'Tense':['Fut']}
                print(lemmas)
            
            #fill empty space of modal
            for k in range(i+1,len(lemmas)):
                lemmas[k-1]=lemmas[k]
                phrases[k-1]=phrases[k]
                POS[k-1]=POS[k]
                meta_datas[k-1]=meta_datas[k]
            skips=skips+1
            continue

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

        if(POS[i]=='Punctuation'):
            print('is punctuation')
            if phrases[i]=='.':
                pass
                # gesture_X_positions.append(gesture_X_positions[-1])
                # gesture_Y_positions.append(gesture_Y_positions[-1]+1)
                # gesture_dir_sequence.append(5)
                # gesture_pressure_variation.append(5)
            

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
        
        # Realign constituents going top to down
        if i>=1:
            if(constituents[i]['X_constrained']==0):
                X_shift=0
                if(constituents[i-1]['X_positions'][-1]<=constituents[i]['X_positions'][0]):
                    shifts=[constituents[i-1]['X_positions'][-1]-constituents[i]['X_positions'][0],1-min(constituents[i]['X_positions'])]
                    X_shift=max(shifts)
                elif(constituents[i-1]['X_positions'][-1]>constituents[i]['X_positions'][0]):
                    shifts=[constituents[i-1]['X_positions'][-1]-constituents[i]['X_positions'][0],9-max(constituents[i]['X_positions'])]
                    X_shift=min(shifts)
                constituents[i]['X_positions']=[k + X_shift for k in constituents[i]['X_positions']]
        

        # Fix vertical alignment
        Y_shift=0
        Y_half_size=math.floor((max(constituents[i]['Y_positions'])-min(constituents[i]['Y_positions'])+1)/2)
        Y_half_position=max(constituents[i]['Y_positions'])-Y_half_size
        Y_shift=3 + i*7 - Y_half_position
        constituents[i]['Y_positions']=[k + Y_shift for k in constituents[i]['Y_positions']]

        # Fill gaps values TODO

        # Add pressure variation
        if (POS[i]!='Punctuation'):
            constituents[i]['pressure_variation'] = np.ones(len(constituents[i]['X_positions']), dtype = int).tolist()
            constituents[i]['pressure_variation'][-1]=0
            constituents[i]['pressure_variation']=[x*2+1 for x in constituents[i]['pressure_variation']]

        # Add consitituent to overall gesture
        gesture_X_positions=gesture_X_positions+constituents[i]['X_positions']
        gesture_Y_positions=gesture_Y_positions+constituents[i]['Y_positions']
        gesture_dir_sequence=gesture_dir_sequence+constituents[i]['dir_sequence']
        gesture_pressure_variation=gesture_pressure_variation+constituents[i]['pressure_variation']
        i=i+1

    # print(gesture_pressure_variation)
    # print(gesture_X_positions)
    # print(gesture_Y_positions)
    # print(gesture_dir_sequence)
    gestures.append({'X_positions':gesture_X_positions,'Y_positions':gesture_Y_positions,'dir_sequence':gesture_dir_sequence,'pressure_variation':gesture_pressure_variation,'angular_vel':0,'data_density':0})
    return gestures