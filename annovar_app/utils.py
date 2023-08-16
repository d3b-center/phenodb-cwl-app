import traceback

class AnnovarException(Exception):
    def __init__(self, exception_string, exception_object):
        print("exception_string:\n"+exception_string)
        print("\n\nexception_object:\n"+str(exception_object))
        print("\n\nTraceback:\n"+"\n".join(traceback.format_stack()))
        outFile = open("exception.txt", "w")
        outFile.write("exception_string:\n"+exception_string)
        outFile.write("\n\n\nexception_object:\n"+str(exception_object))
        outFile.write("\n\n\nTraceback:\n"+"\n".join(traceback.format_stack()))
        outFile.close()
        super().__init__(exception_string, exception_object)
