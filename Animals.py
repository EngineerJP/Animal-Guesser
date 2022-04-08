#!/usr/bin/env Python3

''' Animals.py - Jacob Paquette -- Saint Leo University - 28 March 2022 '''

import csv
import re

global subjects
global predicates
global facts
global header

# ------------------------------------------------------------------------
def cleanFileLine(myList) :
    truePattern = re.compile('[T|t]rue')
    falsePattern = re.compile('[F|f]alse')
    intPattern = re.compile('[-|+]?[0-9]+$')
    floatPattern = re.compile('[-|+]?[0-9]+[.][0-9]+$')

    for i in range(0,len(myList)) :
        if type(myList[i]) is str :
            myList[i] = myList[i].strip ()
            myList[i] = myList[i].capitalize()
            if truePattern.match(myList[i]) :
                myList[i] = True
            elif falsePattern.match(myList[i]) :
                myList[i] = False
            elif myList[i] in ['None','none','','#N/A'] :
                myList[i] = None
            elif intPattern.match(myList[i]) :
                myList[i] = int(myList[i])
            elif floatPattern.match(myList[i]) :
                myList[i] = float(myList[i])

# ------------------------------------------------------------------------
def loadData(subjects,predicates,facts,header) :

    myFile = open('Animals.CSV', 'r')
    myReader = csv.reader(myFile)
    header.clear()
    header.extend(next(myReader))
    cleanFileLine(header)
    print("header", header)
    for dataLine in myReader :
        cleanFileLine(dataLine)
        print(dataLine)
        # Get index of subject
        
        if dataLine[0] in subjects :
            subjectIndex = subjects.index(dataLine[0])
        else:
            subjects.append(dataLine[0])
            subjectIndex = len(subjects)-1

        if dataLine[1] in predicates :
            predicateIndex = predicates.index(dataLine[1])
        else:
            predicates.append(dataLine[1])
            predicateIndex = len(predicates)-1
        myFact = (subjectIndex,predicateIndex,dataLine[2])
        facts.append(myFact)
        
    myFile.close()
    print(subjects)
    print(predicates)
    print(facts)

# ------------------------------------------------------------------------
def saveData(subjects,predicates,facts,header) :
    myFile = open('Animals.csv', 'w', newline='')
    myWriter = csv.writer(myFile)
    print("header", header)
    myWriter.writerow(header)
    for myFact in facts :
        if myFact[2] is not None :
            myRow = [subjects[myFact[0]],predicates[myFact[1]],
                                    myFact[2]]
            myWriter.writerow(myRow)
            print('File Writing: ',myRow)
    myFile.close()
# ------------------------------------------------------------------------
def yesNoQuestion(myString) :
    retVal = None
    truePattern = re.compile('[T|t]rue')
    yesPattern = re.compile('[Y|y][es]?')
    noPattern = re.compile('[N|n][o]?')
    falsePattern = re.compile('[F|f]alse?')
    while retVal is None :
        userInput = input(myString)
        if truePattern.match(userInput) :
            retVal = True
        elif noPattern.match(userInput) :
            retVal = False
        elif yesPattern.match(userInput) :
            retVal = True
        elif falsePattern.match(userInput) :
            retVal = False
    return retVal

# ------------------------------------------------------------------------
def getFirstUnAsked(questions) :
    ''' return -1 if all elements are True or False, otherwise
        return the index of the first entry which is None'''
    retVal = -1
    if None in questions :
        retVal =  questions.index(None)
    print('Unasked question = ',retVal)
    return retVal

# ------------------------------------------------------------------------
def isNotInFactTable(subjectID, PredicateID, facts) :
    retVal = True
    for item in facts :
        if (subjectID == item[0]) and (PredicateID == item[1]) :
            retVal = False
    return retVal

# ------------------------------------------------------------------------
def updateFactTable(questions, subjectID, facts) :
        # create new facts based on questions
        # and insert them into the database if they are
        # not there already
    for i in range(len(questions)):
        newFact = list([subjectID, i,questions[i]])
        # scan if fact is in dataabase and insert
        if isNotInFactTable(subjectID, i, facts) :
            facts.append(newFact)
            print('Adding ',newFact)
            
# ------------------------------------------------------------------------
def play(subjects, predicates, facts) :
    print('Please think of an animal, and I will ask questions')
    print('I will try and deduce the animal.')

    # create a list of numbers of potential candidates
    candidates = [i for i in range(0,len(subjects))]
    print('Animals: ', candidates)
    questions = [None for i in range(0,len(predicates))]
    print('Questions: ', questions)

    #Three Exit Conditions
    #(1) Run out of Questions
    #       guess at random
    #           if fail, get new animal, store predicates
    # (2) One Animal Left
    #       ask, if not hit get new animal name & store predicates
    # (3) No Animals
    #       get new animal name, store predicates

    nextQuestion = getFirstUnAsked(questions)
    while (len(candidates)>1) and (nextQuestion>=0) :
        # ask the next question
        userReply = yesNoQuestion(
                        'Is it true that you animal ' +
                        predicates[nextQuestion] + '?> ')
        questions[nextQuestion] = userReply

        # Elimate subjects not compatible with this answer
        
        for myFact in facts :
            # myFact[0] = subject index, myFact[1] = predicate,
            # myFact[2] = Truth Values

            if myFact[1] == nextQuestion:
                if (userReply != myFact[2]) :
                    # match on Subject, Not on Truth
                    if myFact[0] in candidates :
                        candidates.remove(myFact[0])
                        print("Your animal is not ",
                              subjects[myFact[0]])
                        print(candidates)
        nextQuestion = getFirstUnAsked(questions)
            
    print('Animals: ', candidates)
    print('Questions: ',questions)

    if (len(candidates)>0) :
        userReply = yesNoQuestion(
                        'Is your animal a(n) ' +
                        subjects[candidates[0]] + '?> ')
        if (userReply) :
            print('Thanks for playing.')
            newSubject = candidates[0]
            updateFactTable(questions, newSubject, facts)
        else :
            newName = input('What is the name of your Animal?')
            newName = newName.strip()
            newName = newName.capitalize()
            # check if this subject is in that database
            # and add it if is not
            if (newName in subjects) :
                newSubject = subjects.index(newName)
            else :
                newSubject = len(subjects)
                subjects.append(newName)
            # insert code to learn a new question
            newPredicate = input('What is a predicate ' +
                        'is True for ' + newName +
                        ' but False for ' +
            subjects[candidates[0]]+'?')
            
            newPredicate = newPredicate.strip()
            newPredicate = newPredicate.capitalize()
            if (newPredicate not in predicates) :
                predicateIndex = len(predicates)
                predicates.append(newPredicate)
            else :
                predicateIndex = predicates.index(newPredicate)
            # insert False predicate for candidates[0]
            if isNotInFactTable(candidates[0],predicateIndex, facts) :
                newFact = list([candidates[0],
                                predicateIndex,False])
                facts.append(newFact)
            if isNotInFactTable(newSubject, predicateIndex, facts) :
                newFact = list([newSubject,predicateIndex,True])
                facts.append(newFact)
            # do regular writeback for questions
            updateFactTable(questions, newSubject, facts)
            print('Thanks for Playing. (2)')
    else :
        # learning a new subject
        print("Cool, I don't know an animal like this.")
        newName = input('What is the name of your Animal?')
        newName = newName.strip()
        newName = newName.capitalize()
        newSubject = len(subjects)
        subjects.append(newName)
        updateFactTable(questions, newSubject, facts)
        print('Thanks for playing. (3)')
        
# ------------------------------------------------------------------------
if __name__ =='__main__' :

    #
    subjects = list()
    predicates = list()
    facts = list()
    header = list()

    # load the data from the file
    loadData(subjects,predicates,facts, header)
    
    # play Animal
    play(subjects, predicates, facts)
    
    # save the data to the file
    saveData(subjects,predicates,facts,header)
    
    
    print('End of Run')
                              
# ------------------------------------------------------------------------
