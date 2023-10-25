import traceback
import sys
import subprocess


def run_command(cmd):
    result = subprocess.run(cmd, capture_output=True)
    if result.returncode != 0:
        str_err = result.stderr.decode('utf-8')
        raise AnnovarException('Command could not be executed: ' + ' '.join(cmd) + '' + str_err, '')
    return result.stdout.decode('utf-8')


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
