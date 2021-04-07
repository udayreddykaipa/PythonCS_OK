# redactor.py Script
================
## redactor.py script import project1,argparser
----------------------------------------------------------------------

 The project1 module is project specific module, it contains all function (logical entities)  required to perform redact on files. it is used to improve readability
 argparse: argparse IS AN MODULE TO PARSE RUNTIME ARGUMENTS IN PYTHON AND IT HELPS TO SPECIFY TO MANDATORY ARGUMENTS BY SETTING required ATTRIBUTE TO TRUE.
 THE PYTHON CODE EXECUTION IS HALTED IF required ATTRIBUTE IS NOT PASSED DURING RUNTIME.


## Code Overview
----------

### if __name__ == '__main__': IT IS BASICALLY ENTRY POINT OF THE SCRIPT.

### parser.add_argument - is used to runtime arguments with flag, and other attributes such as required(mandatory), number of arguments for flag and help string if to remind if not passed.
        parser.add_argument("--input", type=str, required=True, help="Input Files to redact"  , nargs='+')

### parser.parse_args() : CONTAINS ALL RUNTIME ARGUMENT BUNDLED, PASSED BY USER,
        args = parser.parse_args()

### def main(args):- The main function is called when the argparser doesn't halt script due missing of mandatory arguments. main takes all runtime arguments.

       
### InputFiles=Redact.InputFiles(args.input) - would invoke InputFiles function in project1 module. because project1 is imported as Redact.
        ex: input - '*.txt'
            return - ['a.txt',...](all txt files)

    
### FileContentDict=Redact.ReadTextFromFiles(InputFiles) - would get contents of inputFiles into FileContentDict dictonary object.

### Redact Entities - if flag is passed those entities are reomved.
     AllList=[]
    if args.names:
        AllList.append('PERSON')
    if args.dates:
        AllList.append("DATE")
    if args.genders:
        AllList.append('genders')
    if args.phones:
        AllList.append('phones')
    if args.place:
        AllList.append('GPE')

    redactedFileContentDict=Redact.RedactWord(FileContentDict,AllList)

### Redact Concept - Using Key word check the similarity with sentance and redact if similar.
        sanitisedDict=Redact.RedactConcept(redactedFileContentDict,args.concept)


### Generate Redacted files,  would writed the content to files with .redacted extension
        Redact.WriteRedactedFiles(sanitisedDict,args.output)
        
### Redaction process summary. prints to a file or stderr stdout
        Redact.Summary(args.stats,sanitisedDict['Stats'])

### For detailed functional Logic explanation refer to code comments. 
