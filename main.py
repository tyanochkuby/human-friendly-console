import spacy
import os
from pathlib import Path
import webbrowser
import psutil
import signal 
from getpass import getuser
import en_core_web_sm


def open_program(program_name):
    founded = []
    paths = [
    list(Path(r'C:\ProgramData\Microsoft\Windows\Start Menu\Programs').rglob('*')), 
    list(Path(os.path.join('C:\\Users', getuser(), 'AppData\\Roaming\\Microsoft\\Windows\\Start Menu\\Programs')).rglob('*'))
    ]
    for p in paths:
        f = [path for path in p if program_name.lower() in path.name.lower() and 'uninstall' not in path.name.lower() and 'lnk' in path.name.split('.')[-1]]
        founded.extend(f)

    if len(founded) > 1:
        print('Found multiple programs, choose one to start:')
        for i in range(len(founded)):
            print(f'\t{i} {founded[i].name[:-4]}')
        index = int(input('Enter index or q to abort: '))
        while index not in range(len(founded)) and index != 'q':
            index = int(input('Bad index. Enter index or q: '))
        if index != 'q':
            try:
                os.startfile(founded[index])
            except OSError:
                print('Cannot open this program')
                return False
            return True
        return False
    elif len(founded) == 1:
        os.startfile(founded[0])
        return True
    else:
        print(f'No program named {program_name} found')
        return False


def open_website(url):
    webbrowser.open(url)
    return True


def close_program(program_name):
    processes =  [process for process in psutil.process_iter() if program_name.lower() in process.name().lower()]
    if len(processes) > 1:
        print('Found multiple processes:')
        for i in range(len(processes)):
            print(f'\t{i} PID: {processes[i].pid}, Name: {processes[i].name()}')
        inp = input('Enter index / indexes separated by a space / all to close eveyrthing / q to abort: ')

        if inp == 'q':
            return 
        
        elif inp == 'all':
            for process in processes:
                try:
                    os.kill(process.pid, signal.SIGTERM)
                except PermissionError:
                    print('Cannot close this program. Try to run as administrator')
                except:
                    print('Something went wrong')
            return True
        
        else:
            processes_to_kill = [int(n) for n in inp.split(' ')]
            while any(i not in range(len(processes)) for i in processes_to_kill):
                inp = input('Bad PID. Enter PID to kill or q: ')
                if inp == 'q':
                    return False
                processes_to_kill = [int(n) for n in inp.split(' ')]
            for i in processes_to_kill:
                try:
                    os.kill(processes[i].pid, signal.SIGTERM)

                except PermissionError:
                    print('Cannot close this program. Try to run as administrator')
                except:
                    print('Something went wrong')

    elif len(processes) == 1:
        os.kill(processes[0].pid, signal.SIGTERM)

    else:
        print(f'No process named {program_name} found')
        return False


def open_document(document_name):
    founded = []
    paths = [os.path.join(r'C:\Users', getuser(), 'Documents'), r'J:\Documents']
    for p in paths:
        try:
            i_paths = list(Path(p).rglob('*'))
            f = [path for path in i_paths if document_name.lower() in path.name.lower()]
            founded.extend(f)
        except:
            pass
    for path in founded:
        os.startfile(path)
        return True
    return False


def get_open_type(doc):
    if '.' not in doc:
        return 'program'
    else:
        if doc.split('.')[-1] in ['doc', 'docx', 'txt', 'pdf', 'ppt', 'pptx', 'xls', 'xlsx', 'csv', 'json', 'xml', 'sln', 'html', 'css', 'py', 'cpp', 'c', 'js', 'java', 'php', 'sql', 'cs']:
            return 'document'
        else:
            return 'website'


def __main__():
    nlp = spacy.load("en_core_web_sm")
    
    nlp = en_core_web_sm.load()
    while True:
        doc = nlp(input('Enter your command / help / exit: '))
        
        # print("""POS TAGGING""")
        # for token in doc:
        #     print((token.text, token.pos_), end=' ')
        # print()
        if doc[0].text == 'help':
            print('open <program_name> - open program \nclose <program_name> - close program\nopen <website_url> - open website\nopen <document_name> - open document\n')
        elif doc[0].text == 'open':
            desired_function = get_open_type(str(doc[1].text))
            if(desired_function == 'program'):
                if open_program(doc[1].text):
                    print('Program opened successfully')
                else:
                    print('Program not found')
            elif(desired_function == 'website'):
                if open_website(doc[1].text):
                    print('Website opened successfully')
                else:
                    print('Website not found')
            elif(desired_function == 'document'):
                if open_document(doc[1].text):
                    print('Document opened successfully')
                else:
                    print('Document not found')
        elif(doc[0].text == 'close'):
            if close_program(doc[1].text):
                print('Program(s) closed successfully')
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

if __name__ == '__main__':
    __main__()