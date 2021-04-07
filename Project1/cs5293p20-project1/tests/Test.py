import sys,os
sys.path.append(os.path.abspath(os.path.join('..','Srcproject1')))
import project1
# import project1

# from project1 import project1 #InputFiles,ReadTextFromFiles,RedactWord,WriteRedactedFiles,Summary

# check tests folder to find if it listing all py files
txtFile='t.txt'
s={txtFile}
assert(project1.InputFiles(['*.txt'])==s)


#Read Text from a Dummy and Compare dict value with hardcoded value
TextF={'t.txt':'ram is arrogant,because his father is a Governer.'}
assert(project1.ReadTextFromFiles(s)==TextF)

# Check the Redacted data
TextFRedacted='ram is arrogant,because his father is a XXX-Redacted/PERSON.'
assert(project1.RedactWord(TextF,['PERSON'])['t.txt']==TextFRedacted)

#check Redacted data written format.
RedactedDict={'t.txt':TextFRedacted}
project1.WriteRedactedFiles(RedactedDict,['Output'])
assert(TextFRedacted==open('Output/t.txt.redacted').read())

#check Stats to file or stderr
# project1.Summary(['STDOUT','STDOUT','stderr'],{'ram':1,'father':1})
# assert(Summary(['Stats.txt'],{'ram':1,'father':1})==open('Stats.txt').read())