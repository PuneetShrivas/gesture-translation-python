import csv
def lookupSeqFromLemma(lemma):
    csv_file = csv.reader(open('./data/dictionary.csv', "r"), delimiter=",")
    for row in csv_file:
    #if current rows 2nd value is equal to input, print that row
        if lemma.lower() == row[1]:
            seq=row[2]
            X_size=int(row[3])
            Y_size=int(row[4])
            return[seq,X_size,Y_size]
    return['S0E',0,0]