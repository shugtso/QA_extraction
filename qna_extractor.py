from pathlib import Path



def preprocess_text(text):
    text = text.replace('\n', '')
    text = text.replace('།','། ')
    text = text.replace('། །','།།')
    text = text.replace('  ',' ')
    text = text.replace('།།།','།།')
    text = text.replace('།།།','།།')
    text = text.replace('ལན།','\nལན།')
    return text

def get_qa_pairs(text):
    qa_pairs = []
    for line in text.split('\n'):
        if line:
            line = line.split()
            qa_pairs.append((' '.join(line[:-1]), line[-1]))
    return qa_pairs

def get_data_in_dict(text):
    text=preprocess_text(text)
    data=get_qa_pairs(text) 

    datadic={'question':[],'answer':[]}
    try:
        for i in range(len(data)):
            datadic['question'].append(data[i][1])
            datadic['answer'].append(data[i+1][0])
    except:
        print('done')

    return datadic


def get_annotated_data(datadic):
    questions = ''
    answers = ''
    for question in datadic['question']:
        questions+=question+'\n'
    for answer in datadic['answer']:
        answers+=answer+'\n'
    return questions,answers

if __name__ == '__main__':

    q_n_a_file_paths = list(Path('./data/random').iterdir())
    for q_n_a_file_path in q_n_a_file_paths:
        text = q_n_a_file_path.read_text(encoding='utf-8')
        data_dic = get_data_in_dict(text)
        questions,answers = get_annotated_data(data_dic)
        # if len(questions) != len(answers):
        #     print(f"Warning: Number of questions ({len(questions)}) and answers ({len(answers)}) do not match in file {q_n_a_file_path}")
        # else:
        Path(f'./data/Questions/{q_n_a_file_path.stem}.txt').write_text(questions, encoding='utf-8')
        Path(f'./data/Answers/{q_n_a_file_path.stem}.txt').write_text(answers, encoding='utf-8')
