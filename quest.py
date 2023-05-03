import random
import PyPDF2
from PyPDF2 import PdfReader
import re

def parse_pdf(file_path):
    # Open the PDF file
    pdf_reader = PdfReader(file_path)
    # Get the number of pages in the PDF
    num_pages = len(pdf_reader.pages)
    
    questions = []
    nonstatic_ans = {}
    
    f = open('ans_for_non_definitive', 'r')
    f_lines = f.readlines()
    
    for line in f_lines:
        s = line.split(',')
        nonstatic_ans[s[0]] = s[1].strip()
    
    # Iterate through each page
    for i in range(num_pages):
        page = pdf_reader.pages[i]
        text = page.extract_text()
        lines = text.split("\n")
        question = ""
        answers = []
        num = 0
        while num < (len(lines)):
            # check if the line starts with a number
            lines[num] = lines[num].replace('www.uscis.gov', '')
            match = re.search(r'\d+', lines[num])
            if match and lines[num][0].isdigit() and lines[num][len(match.group())] == '.':
                question = lines[num].replace('\t', ' ')[len(match.group())+1:].strip()
            elif lines[num].startswith("  ▪  "):
                while num < len(lines):
                    if not lines[num].startswith("  ▪  "):
                        num -= 1
                        break
                    else:
                        curr_ans = lines[num][5:].strip()
                        if ('Visit uscis.gov' in curr_ans or 'Answers will vary' in curr_ans) and question in nonstatic_ans:
                            curr_ans = nonstatic_ans.get(question)
                        answers.append(curr_ans)
                        num += 1
            else:
                num += 1
                continue
            if question and answers:
                questions.append({"question": question, "answer": answers})
                question = ""
                answers = []
            num += 1
        f = open('answers.txt','w')
        for q in questions:
            f.write(', '.join(q['answer']) + '\n')
        f.close()
    return questions


def test(questions):
    score = 0
    for i, q in enumerate(random.sample(questions, len(questions))):
        user_answer = input(f"{i+1}. {q['question']}: ")
        print(q['answer'])
    print(f"You scored {score} out of {len(questions)}.")

questions = parse_pdf("100q.pdf")
test(questions)
