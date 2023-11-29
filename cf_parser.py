import os
import sys #You will get input from node in sys.argv(list)
import time
import json
import requests

from bs4 import BeautifulSoup


headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/110.0'
}

def parse_task(url, index, path):
    page = requests.get(url, headers=headers)

    if not page.text:
        return "Cannot open this page"

    soup = BeautifulSoup(page.text, 'html.parser')
    problem_statement = soup.find("div", class_="problem-statement")
    header = problem_statement.find("div", class_="header")
    title = header.find("div", class_="title").text

    time_limit_block = header.find("div", class_="time-limit")
    time_limit = "Time limit: " + "".join(time_limit_block.find_all(string=True, recursive=False))

    memory_limit_block = header.find("div", class_="memory-limit")
    memory_limit = "Memory limit: " + "".join(memory_limit_block.find_all(string=True, recursive=False))

    input_file_block = header.find("div", class_="input-file")
    input_file = "Input: " + "".join(input_file_block.find_all(string=True, recursive=False))

    output_file_block = header.find("div", class_="output-file")
    output_file = "Output: " + "".join(output_file_block.find_all(string=True, recursive=False))

    divs = problem_statement.find_all("div")
    task_text = divs[10].text
    list_task_text = task_text.split()
    task_text = ""
    for i in range(len(list_task_text)):
        task_text += list_task_text[i]
        if (i + 1) % 15 == 0:
            task_text += "\n"
        else:
            task_text += " "

    input_block = problem_statement.find("div", class_="input-specification")
    input = "Input:\n"
    input_list = input_block.find_all(string=True, recursive=True)
    for i in range(1, len(input_list)):
        input += input_list[i] + " "
    splited_input = input.split()
    input = "Input:\n"
    for i in range(1, len(splited_input)):
        if i % 15 == 0:
            input += "\n"
        input += splited_input[i] + " "

    output_block = problem_statement.find("div", class_="output-specification")
    output = "Output\n"
    output_list = output_block.find_all(string=True, recursive=True)
    for i in range(1, len(output_list)):
        output += output_list[i] + " "
    splited_output = output.split()
    output = "Output:\n"
    for i in range(1, len(splited_output)):
        if i % 15 == 0:
            output += "\n"
        output += splited_output[i] + " "

    test = problem_statement.find("div", class_="sample-test")
    test_divs = test.find_all("div")
    test = ""
    start_index = 0
    if test_divs[1].text == "Input" and test_divs[2].text[:6] != "Output":
        start_index = 1
        
    for i in range(start_index, len(test_divs) - 1):
        if test_divs[i].text == "Output":
            test += "\n"
        test += test_divs[i].text
        test += "\n"

    note_block = problem_statement.find("div", class_="output-specification")
    note = "Note\n"
    note_list = note_block.find_all(string=True, recursive=True)
    for i in range(1, len(note_list)):
        note += note_list[i] + " "
    splited_note = note.split()
    note = "Note:\n"
    for i in range(1, len(splited_note)):
        if i % 15 == 0:
            note += "\n"
        note += splited_note[i] + " "

    task_filename = path + "/task_" + chr(ord('A') + index) + ".txt"
    with open(task_filename, "w") as f:
        f.write(title + "\n\n")
        f.write(time_limit + "\n")
        f.write(memory_limit + "\n")
        f.write(input_file + "\n")
        f.write(output_file + "\n\n")
        f.write(task_text + "\n\n")
        f.write(input + "\n\n")
        f.write(output + "\n\n")
        f.write(test + "\n")
        f.write(note + "\n")

    cpp_filename = path + "/" + chr(ord('A') + index) + ".cpp"
    with open(cpp_filename, "w") as f:
        f.write('// Goodluck :)\n')
        f.write("#include <iostream>\n\n\n")
        f.write("/*\n")
        f.write(test)
        f.write("*/")

    time.sleep(5)

    return "Ok"


def parse_contest(link, path):
    try:
        page = requests.get(link, headers=headers)
    except Exception as e:
        return "Incorrect link"
    
    if page.text:
        soup = BeautifulSoup(page.text, 'html.parser')
        tasks = soup.find("div", class_="datatable")
        if tasks is None:

            return "Incorrect link"
        
        table = tasks.find("table", class_="problems")
        if table is None:

            return "Incorrect link"
        
        path = os.path.join(path, "contest")
        if os.path.isdir(path):

            return "exists"
        try:  
            os.mkdir(path)  
        except OSError as error:  
            # logging.error(error)
            return "Cannot create directory"
        
        trs = table.find_all("tr")
        for i in range(1, len(trs)):
            letter = chr(ord('A') + i - 1)
            result = parse_task(link + "problem/" + letter, i - 1, path)
            if result != "Ok":
                return result

    return "Ok"


if __name__ == "__main__":
    # res = parse_contest("https://codeforces.com/contest/190482301/", "D:/itmo/devtools/cfplugin/cfplugin/")
    # print(res)
    data = json.loads(sys.argv[1])
    link = data["link"]
    path = data["save"]
    message = parse_contest(link, path)
    newdata = {'answer': message}
    print(json.dumps(newdata)) 