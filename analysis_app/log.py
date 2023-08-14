import datetime
from datetime import datetime
from pytz import timezone


class Log:
    def __init__(self):
        self.text = ""  # single string for analysis descriptions, appended throughout app
        self.time = get_time()

    def append_text(self, text):
        self.text = self.text + text + "\n"

    # write analysis descriptions to file
    def write_log(self, analysis_type):
        out_name = 'Log_' + analysis_type.name + '_' + self.time + '.txt'
        with open(out_name, 'w') as f:
            f.write(self.text + '\n\n')

    # write final variants to csv file
    def write_variants(self, analysis_type, header, variants):
        out_name = 'PhenoDB_Analysis_' + analysis_type.name + '_' + self.time + '.tsv'
        with open(out_name, 'w') as f:
            f.write(header + '\n')
            for var in variants:
                f.write(var + '\n')

    def print_summary(self, analysis_type):
        print('Summary of analysis', analysis_type, '\n')
        print(self.text + '\n\n')


def get_time():
    est = datetime.now(timezone('US/Eastern'))
    return est.strftime('%Y_%m_%d_%H-%M-%S')


# performance debugging print statements
def print_status(location, iter_num, comment):
    status = datetime.utcnow().strftime("%H:%M:%S.%f")
    if location:
        status += ' | ' + location
    if iter_num is not None:
        status += ' | loops: ' + str(iter_num)
    if comment:
        status += ' | ' + comment
    print(status)
