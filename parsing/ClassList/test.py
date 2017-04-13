import re
import fasta
filepath ="./your fasta file paht"
def read_data_from_fasta(filepath):
    with open(filepath) as file:
        data = fasta.read(file)

        data = list(data)
        ##!! I have never used fasta format before, I don;t know what it would reaturn.
        ## I assume it will return a list
        return data
def longest_and_shortest(data_list):
    data.sort(key=lambda l: len(l),reverse=True)

    for line in data_list:
        regex = re.complile(r'>\s?(.*)')
        ##identifier or what ever it is
        matches = re.findall(regex,line)


