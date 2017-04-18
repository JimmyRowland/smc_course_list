import textract
import inspect



print(dir(textract))
print(inspect.getsource(textract))
text = textract.process('pdfFiles/Fall 2015 Grade Distribution- Report.pdf')
# text = textract.process('pdfFiles/selection.pdf')
print(text)
print(str(text).split("\\n"))
print("df")
def write_file(path, data):
    with open(path, 'w') as f:
        f.write(data)
write_file("test.txt",str(text))

