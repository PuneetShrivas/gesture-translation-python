from audioop import reverse
from .lookupSeq.lookupSeqFromLemma import lookupSeqFromLemma
import math
import numpy as np


def drawSentenceGesture(lemmas,phrases,meta_datas,POS,halt):

    gestures=[]
    drawgestureframe(lemmas,phrases,meta_datas,POS,gestures,halt)
    return gestures


def drawgestureframe(lemmas,phrases,meta_datas,POS,gestures,halt,skips=0):
    gesture_X_positions=[]
    gesture_Y_positions=[]
    gesture_dir_sequence=[]
    gesture_pressure_variation=[]
    constituents=[]
    i=0
    while i < len(lemmas)-skips:
        print("---")
        print(i)
        if i>1 and max(constituents[i-1]['Y_positions'])>18:
            gestures.append({'X_positions':gesture_X_positions,'Y_positions':gesture_Y_positions,'dir_sequence':gesture_dir_sequence,'pressure_variation':gesture_pressure_variation,'angular_vel':0,'data_density':0})
            # print("gestures before recursive call",gestures)
            drawgestureframe(lemmas[i:],phrases[i:],meta_datas[i:],POS[i:],gestures,halt,skips)
            # print("gestures before recursive call",gestures)
            return

        print(POS[i])
        constituents.append({'X_positions':[],'Y_positions':[],'dir_sequence':[],'X_constrained':0,'Y_constrained':0,'pressure_variation':[],'halt_after':1})

        #Set origin for gesture
        [seq,X_size,Y_size]=lookupSeqFromLemma(phrases[i])
        print(lemmas[i])
        X_origin_constituent=5-math.floor(X_size/2)
        Y_origin_constituent=4+(i)*7-math.floor(Y_size/2)

        if i>0:
            X_origin_constituent=constituents[i-1]['X_positions'][-1]
            Y_origin_constituent=constituents[i-1]['Y_positions'][-1]

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
            if 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Fut'):
                print('and is future tense')
                constituents[i]['dir_sequence']=[4,4]+constituents[i]['dir_sequence']
            elif 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Pres'):
                print('and is present tense')
                constituents[i]['dir_sequence']=[5,5]+constituents[i]['dir_sequence']
            elif 'Tense' in meta_datas[i] and (meta_datas[i]['Tense'][0]=='Past'):
                print('and is past tense')
                constituents[i]['dir_sequence']=[6,6]+constituents[i]['dir_sequence']
            
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
            if 'Gender' in meta_datas[i] and (meta_datas[i]['Gender'][0]=='Masc'):
                print('and is Masculine')
                constituents[i]['dir_sequence'] = [6,6] + constituents[i]['dir_sequence'] 
            if 'Gender' in meta_datas[i] and (meta_datas[i]['Gender'][0]=='Fem'):
                print('and is Masculine')
                constituents[i]['dir_sequence'] = [5,7,3,3,7] + constituents[i]['dir_sequence'] 
            if 'Number' in meta_datas[i] and (meta_datas[i]['Number'][0]=='Sing'):
                print('and is Singular')
            if 'Number' in meta_datas[i] and (meta_datas[i]['Number'][0]=='Plur'):
                print('and is Plural')
                constituents[i]['dir_sequence'] = constituents[i]['dir_sequence'] + [2,2,5,5]
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

        try:
            if(POS[i+1]=='Punctuation'):
                print('next is punctuation')
                last_dir=constituents[i]['dir_sequence'][-1]
                dirs = [1,2,3,4,5,6,7,8]
                if phrases[i+1]=='.':
                    start_dir=np.roll(dirs,3-last_dir)[0]
                    opp_dir=np.roll(dirs,5-start_dir)[0]
                    constituents[i]['dir_sequence'] = constituents[i]['dir_sequence'] + [start_dir, opp_dir, opp_dir]
                elif phrases[i+1]==',':
                    start_dir=last_dir
                    opp_dir=np.roll(dirs,5-start_dir)[0]
                    constituents[i]['dir_sequence'] = constituents[i]['dir_sequence'] + [start_dir, opp_dir]
                elif phrases[i+1]=='?':
                    start_dir=np.roll(dirs,3-last_dir)[0]
                    first_dir=np.roll(dirs,7-start_dir)[0]
                    sec_dir=np.roll(dirs,7-first_dir)[0]
                    constituents[i]['dir_sequence'] = constituents[i]['dir_sequence'] + [start_dir, first_dir, sec_dir]
                skips=skips+1
        except:
            print("no punctuations to draw")   

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
        
        #Fix horizontal alignment
        if max(constituents[i]['X_positions'])>9:
            X_shift = 9-max(constituents[i]['X_positions'])
            constituents[i]['X_positions']=[k + X_shift for k in constituents[i]['X_positions']]
        elif min(constituents[i]['X_positions'])<1:
            X_shift = 1-min(constituents[i]['X_positions'])
            constituents[i]['X_positions']=[k + X_shift for k in constituents[i]['X_positions']]

        # # Fix vertical alignment
        # Y_shift=0
        # Y_half_size=math.floor((max(constituents[i]['Y_positions'])-min(constituents[i]['Y_positions'])+1)/2)
        # Y_half_position=max(constituents[i]['Y_positions'])-Y_half_size
        # Y_shift=3 + i*7 - Y_half_position
        # constituents[i]['Y_positions']=[k + Y_shift for k in constituents[i]['Y_positions']]

        # Fill gaps values TODO

        # Add pressure variation
        constituents[i]['pressure_variation'] = np.ones(len(constituents[i]['X_positions']), dtype = int).tolist()

        pres_len=len(constituents[i]['pressure_variation'])
        try:
            if(POS[i+1]=='Punctuation'):
                if phrases[i+1]=='.':
                     for iter in range(pres_len-3,pres_len):
                         constituents[i]['pressure_variation'][iter]=2
                elif phrases[i+1]==',':
                    for iter in range(pres_len-2,pres_len):
                         constituents[i]['pressure_variation'][iter]=2
                elif phrases[i+1]=='?':
                    for iter in range(pres_len-4,pres_len):
                         constituents[i]['pressure_variation'][iter]=2
                
                if i<len(lemmas)-skips-1:
                    for k in range(i+1,len(lemmas)):
                        lemmas[k-1]=lemmas[k]
                        phrases[k-1]=phrases[k]
                        POS[k-1]=POS[k]
                        meta_datas[k-1]=meta_datas[k]
        except:
             print("no punctuations to pressurize")
        # constituents[i]['pressure_variation'][-1]=0
        constituents[i]['pressure_variation']=[x*2+1 for x in constituents[i]['pressure_variation']]
        

        #Adding a halt after each word
        if constituents[i]['halt_after']:
            for x in range(0,halt):
                constituents[i]['X_positions']=constituents[i]['X_positions'] + [constituents[i]['X_positions'][-1]]
                constituents[i]['Y_positions']=constituents[i]['Y_positions'] + [constituents[i]['Y_positions'][-1]]
                constituents[i]['pressure_variation']=constituents[i]['pressure_variation'] + [constituents[i]['pressure_variation'][-1]]
                # constituents[i]['X_positions']=constituents[i]['X_positions'] + constituents[i]['X_positions'][-1]


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
    gesture_pressure_variation = gesture_pressure_variation + [gesture_pressure_variation[-1]]
    gestures.append({'X_positions':gesture_X_positions,'Y_positions':gesture_Y_positions,'dir_sequence':gesture_dir_sequence,'pressure_variation':gesture_pressure_variation,'angular_vel':0,'data_density':0})
    return gestures