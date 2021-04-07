import argparse
import  project1 as Redact

def main(args):
    # args.input --parameter passed as argument runtime
    InputFiles=Redact.InputFiles(args.input) # returns list of files to read

    FileContentDict=Redact.ReadTextFromFiles(InputFiles)
    # get all text in each file to a dict using FileObj.read()

    # REDACT NAMES, DATES, PHONES grouped to avoid Redundant code.
    #  as they have almost similar in implementation, so can be grouped.
    AllList=[]
    if args.names:
        AllList.append('PERSON') #PERSON is  key to specify ALL NAME entities need to be redacted, 
    if args.dates:
        AllList.append("DATE")  #similarly DATE key in list specifies dates to be redacted...so on.
    if args.genders:
        AllList.append('GENDER')
    if args.phones:
        AllList.append('PHONES')
    if args.places:
        AllList.append('GPE') # added as additional 
    redactedFileContentDict=Redact.RedactWord(FileContentDict,AllList) #passing list of entity types to redact
    #return the dict redacted keywords

    # REDACT CONCEPT
    if(args.concept!=None):#Check if Arguments are not null, to avoid `TypeError: 'NoneType' object is not iterable`
        redactedFileContentDict=Redact.RedactConcept(redactedFileContentDict,args.concept)

    # STORE OUTPUT TO A FILE
    Redact.WriteRedactedFiles(redactedFileContentDict,args.output)

    # PRINT SUMMARY/Write to File
    if(args.stats!=None):
        Redact.Summary(args.stats,redactedFileContentDict['Stats'])



if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    # only input files, output folder are made required to Redact.
    parser.add_argument("--input", type=str, required=True, help="Input Files to redact"  , nargs='+') 
    # nargs="+" any number of argument 

    #optional(action='store_true') without and argument(required=False)
    parser.add_argument("--names", action='store_true', required=False, help="Name/peron enties flag" )
    parser.add_argument("--genders", action='store_true', required=False, help="if Gender words to redact" )
    parser.add_argument("--dates", action='store_true', required=False, help="Dates to redact" )
    parser.add_argument("--phones", action='store_true', required=False, help="phone numbers to redact" )
    parser.add_argument("--places", action='store_true', required=False, help="GPE Location/Place -Geo political entity " )
    
    parser.add_argument("--concept", type=str, required=False, help="Concept to redact" , nargs='+')
    
    parser.add_argument("--output", type=str, required=True, help="Output file folder path." , nargs='+')
    parser.add_argument("--stats", type=str, required=False, help="file or stderr, stdout to writes the summary of the redaction process" , nargs='+')
    
    args = parser.parse_args()

    main(args)
    