import glob
import os
import sys
from numpy import printoptions
import spacy
from spacy.matcher import Matcher


# takes --input args and returns files applicable as a list
def InputFiles(InputArgsList):
    filesSetToRedact = set()
    # iterate through the input arguments for --input flag.
    for globEle in InputArgsList:
        Tempset = set(glob.glob(str(globEle)))
        filesSetToRedact = (filesSetToRedact | Tempset )  # adding to set like a=a+b, which is empty initially
    # print(filesSetToRedact)
    return filesSetToRedact


# returns content from files to redact
def ReadTextFromFiles(FilesSet):
    FileContentDict = {}
    # iterate on each file, open and read
    for file in FilesSet:
        fileObj = open(file, "r", encoding="utf8")
        FileContentDict[file] = fileObj.read()
        fileObj.close()
        # file contents stored in dict with filename as key.

    return FileContentDict


# readct data by checking arguments
def RedactWord(FileContentDict, redactList):
    Stats = {'DATE':0,'PERSON' :0,'GPE' :0,'GENDER':0,'PHONES' : set(),'SENTENCE' : set()}  # empty dict to Store/tract Redaction stastics
    # print(redactList)
    # load nlp package
    nlp = spacy.load("en_core_web_sm")
    matcher = Matcher(nlp.vocab)
    matcher1 = Matcher(nlp.vocab)
    # (123) 456 7889 or (541) 754-3010 - pattern 1
    # (123) 456 789 or (541) 754-301 - pattern 2
    PhoneNumberpattern1 = [{"ORTH": "("},{"SHAPE": "ddd"},{"ORTH": ")"},{"SHAPE": "ddd"},{"ORTH": "-", "OP": "?"},{"SHAPE": "dddd"},]
    PhoneNumberpattern2 = [{"ORTH": "("},{"SHAPE": "ddd"},{"ORTH": ")"},{"SHAPE": "ddd"},{"ORTH": "-", "OP": "?"},{"SHAPE": "ddd"},]
    matcher.add("PHONE_NUMBER", [PhoneNumberpattern1])
    matcher.add("PHONE_NUMBER", [PhoneNumberpattern2])

    # Iter on each file content
    for Key in FileContentDict.keys():
        doc = nlp(FileContentDict[Key])

        # iter on enties in a file conten
        for e in doc.ents:
            # print(e.text,e.label_)
            # will redact PERSON,GPE and DATE
            if e.label_ in redactList:
                # add to stats
                Stats[e.label_] += FileContentDict[Key].count(e.text)
                # print(FileContentDict[Key].count(e.text))
                # Stats[e.label_].append((e.text, e.label_)) # to add the redacted word also.

                FileContentDict[Key] = str(FileContentDict[Key]).replace( e.text, "XXX-Redacted/" + e.label_ )


            if ("PHONES" in redactList):  # math with mather, it is similar to re( regular expression )
                matches = matcher(doc)
                for match_id, start, end in matches:
                    span = doc[start:end]
                    FileContentDict[Key] = FileContentDict[Key].replace(span.text, "XXX-Redacted/PHONE_NUMBER")

                    # update stats
                    Stats["PHONES"].add(span.text)

                    # print(span.text)

        # no so best method, correlating with a list
        gender_title = ["mr.","sir","monsieur","captain","chief","master","lord","baron","mister","mr","prince","king","mrs.","ms.","miss","lady","madameoiselle","baroness","mistress","mrs","ms","queen","princess","madam","madame", "he","she", "him","her","his","hers"]
        if("GENDER" in redactList):#she/her/hers, and he/him/his
            for tocken in doc:
                if tocken.text in gender_title:
                    # print(tocken.text)
                    Stats['GENDER']+=FileContentDict[Key].count(tocken.text)
                    FileContentDict[Key]=FileContentDict[Key].replace(tocken.text,"XXX-Redacted/Gender")


    # append the Stats dict in the FileContentDict.
    FileContentDict["Stats"] = Stats
    return FileContentDict


# redact concept using spacy, check similarity with sentance
def RedactConcept(FileContentDict, redactConcepts):
    Stats = {}
    Stats = FileContentDict["Stats"] #get existing stats to avoid over writting
    nlp = spacy.load("en_core_web_sm") # use "en_core_web_lg" | "en_core_web_trf" for imporoved accuracy

    #iterate over all concepts passed ( could be one or more.)
    for concept in redactConcepts:

        #iterate on all files contents.
        for Key in FileContentDict.keys():

            #ignore stats as it not redacted,
            if Key == "Stats":
                continue
            doc = nlp(FileContentDict[Key])
            sentences = list(doc.sents)
            for sentence in sentences:
                temp1 = nlp(str(sentence))
                temp2 = nlp(concept)
                #check similarity 0.5 is considerable similarity ( similarity ranges from -1(Less often -ve) to +1(same/equal))
                if temp1.similarity(temp2) > 0.5:  # may get warning about accuracy if small package model is loaded.
                    
                    #updating stats
                    Stats['SENTENCE'].add(str(sentence))
                    FileContentDict[Key] = str(FileContentDict[Key]).replace(str(sentence), "XXX-Redacted/Concept sentence")

    #update stats with stats with latest
    FileContentDict["Stats"] = Stats

    return FileContentDict


# write redacted data .redacted files
def WriteRedactedFiles(FileContentDict, OutPutFoldersList):
    for Folder in OutPutFoldersList:
        # if folder already exists delete all files and remove folder, to remove previous output files
        if os.path.exists(path=Folder):
            for file in os.listdir(Folder):
                os.remove(os.path.join(os.path.join(os.getcwd(), Folder), file))
            os.rmdir(Folder)

        # make directory
        os.mkdir(os.path.join(os.getcwd(), Folder))

        for file in FileContentDict.keys():
            #skip writing stats to redacted files.
            if file == "Stats":
                continue
            filePath = os.path.join(os.path.join(os.getcwd(), Folder), file)
            # filePath
            fileObj = open(filePath + ".redacted", "w")
            fileObj.write(FileContentDict[file])
            fileObj.close()

    print("###########################")
    print("# Redacted Files Generated #")
    print("###########################")


# prints the stats or summary of redacting process.
def Summary(WriteToList, Stats):
    for File in WriteToList:
        for K in Stats.keys():
            if File.lower() == "stderr":
                print(K, ":", str(Stats[K]), file=sys.stderr)
            elif File.lower() == "stdout":
                print(K, ":", str(Stats[K]), file=sys.stdout)
            else:
                fp = open(File, "a")
                print(K, ":", str(Stats[K]), file=fp)
                fp.close()
    print("========================END==========================")
    return True