# project1 Module
================
## project1 modules import glob, os, sys, numpy,spacy and spacy.matcher.
----------------------------------------------------------------------

 glob,os,sys modules comes with python, 
 The glob module finds all the pathnames matching a specified pattern according to the rules used by the Unix shell

 os module is used to interact with operating system level commands,it provides a portable way of using operating system dependent functionality.

 sys module provides access to some variables used or maintained by the interpreter and to functions that interact strongly with the interpreter. It is always available.

 NumPy is the fundamental package for scientific computing in Python, it required by Spacy nlp module. It is a Python library that provides a multidimensional array object, various derived objects

 spacy is nlp( ) module,spaCy’s trained pipelines can be installed as Python packages. This means that they’re a component of your application, just like any other module. They’re versioned and can be defined as a dependency in your requirements.txt. Trained pipelines can be installed from a download URL or a local directory, manually or via pip. Their data can be located anywhere on your file system
 
 spacy.matcher is submodule in spacy, used to match the relativity of two strings od nlp type.

## Funtion Overview
----------
### InputFiles() - It takes input files as a list glob type that are to be redacted, and lists all files applicable as per GLOB syntax.
        ex: InputFiles('*.txt') would return list all .txt files in that folder

### ReadTextFromFiles()- It takes set of file names and return a dictonary with keys and values, keys- filename and value-Conetent of File.
        ex: ReadTextFromFiles('a.txt') would return {'a.txt': 'all content in file a.txt \n ..'}

### RedactWord()- would take the dict (return of ReadTextFromFiles() ) and redact all flags entites using spacy and returns redacted dict along with stats
        ex: RedactWord() would return {'a.txt': 'all content in XXXXX/Redacted.Name a.txt \n ..',  'Stats':....}

### RedactConcept() function is similar to RedactWord except it check similarity of sentance to key word and redact it.
        ex: same as RedactWord() return a complete matching sentance would be redacted if any.

### WriteRedactedFiles() function would write redacted data to files in keys in dictonary passed as input argument.
        ex: WriteRedactedFiles({'a.txt': ' XXXXX/Redacted.Name jksdlfkxt \n ..'},[Output]) would create a.txt in Output folder and Writes value to file

### Summar() would print the stastical summary of Redact process on data to stdout or stderr or a file.
        ex: Names-Redacted :10, ....



### For detailed functional Logic explanation refer to code comments. 
