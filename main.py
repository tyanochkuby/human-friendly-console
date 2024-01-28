import spacy
import os
from pathlib import Path
import webbrowser
import psutil
import signal 
from getpass import getuser


def open_program(program_name):
    for path in Path(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs').rglob('*'):
        if program_name in path.name.lower():
            os.startfile(path)
            return True
    return False

def open_website(url):
    webbrowser.open(url)

def close_program(program_name):
    processes =  [process for process in psutil.process_iter() if program_name in process.name().lower()]
    if len(processes) > 1:
        print('found multiple processes:')
        for i in range(len(processes)):
            print(f'\t{i} PID: {p.pid}, Name: {p.name()}')
        pid = int(input('Enter PID to kill or q: '))
        while pid not in [p.pid for p in processes] and pid != 'q':
            pid = int(input('Bad PID. Enter PID to kill or q: '))
        os.kill(pid, signal.SIGTERM)
    elif len(processes) == 1:
        os.kill(processes[0].pid, signal.SIGTERM)
    else:
        print(f'No process named {program_name} found')
        return False

def open_document(document_name):
    docs = []
    try:
        docs.append(Path(os.path.join(r'C:\Users', getuser(), 'Documents')).rglob('*'))
    except:
        pass
    try:
        docs.append(Path(r'J:\Documents').rglob('*'))
    except:
        pass

    for path in docs:
        if document_name in path.name.lower():
            os.startfile(path)
            return True
    return False

def get_open_type(doc):


nlp = spacy.load("en_core_web_sm")
import en_core_web_sm
nlp = en_core_web_sm.load()
while True:
    doc = nlp(input('Enter your command: '))
    
    print("""POS TAGGING""")
    for token in doc:
        print((token.text, token.pos_), end=' ')
    print()
    if(doc[0] == 'open'):
        desired_function = get_open_type(doc[1:])
    # if doc[0].tag_ != 'VB':
    #     print('Error! Not a command!')
    #     continue
    # else:
    #     print('Great! It\'s a command')
    #     if doc[1].pos_ == 'ADP':
    #         print("action: ", doc[0].text, doc[1].text)
    #         doc = doc[2:]
    #     else:
    #         print("action: ", doc[0].text)
    #         doc = doc[1:]
    #     print('object: ', end="")
    #     for token in doc:
    #         print(token.text, end=' ')
    print()