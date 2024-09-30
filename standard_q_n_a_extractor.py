from pathlib import Path

def get_qa_pairs(text):
    questions = []
    answers = []
    current_lines = []
    current_type = None
    lines = text.split('\n')

    # Iterate through each line to parse questions and answers
    for line in lines:
        line = line.strip()
        if line == '':
            continue
        if line.startswith('དྲི་བ།'):
            # Save the previous answer if any
            if current_type == 'answer' and current_lines:
                answers.append(''.join(current_lines))
                current_lines = []
            # Save the previous question if any
            elif current_type == 'question' and current_lines:
                questions.append(''.join(current_lines))
                current_lines = []
            # Start collecting a new question
            current_type = 'question'
            current_lines.append(line)
        elif line.startswith('ལན།'):
            # Save the previous question if any
            if current_type == 'question' and current_lines:
                questions.append(''.join(current_lines))
                current_lines = []
            # Save the previous answer if any
            elif current_type == 'answer' and current_lines:
                answers.append(''.join(current_lines))
                current_lines = []
            # Start collecting a new answer
            current_type = 'answer'
            current_lines.append(line)
        else:
            # Continue collecting lines for the current question or answer
            current_lines.append(line)

    # After the loop, save any remaining collected lines
    if current_type == 'question' and current_lines:
        questions.append(''.join(current_lines))
    elif current_type == 'answer' and current_lines:
        answers.append(''.join(current_lines))
    
    return questions, answers


if __name__ in '__main__':
    q_n_a_file_paths = list(Path('./data/standard_Qna').iterdir())
    for q_n_a_file_path in q_n_a_file_paths:
        if q_n_a_file_path.stem == "BO8995":
            text = q_n_a_file_path.read_text(encoding='utf-8')
            questions, answers = get_qa_pairs(text)
            # if len(questions) != len(answers):
            #     print(f"Warning: Number of questions ({len(questions)}) and answers ({len(answers)}) do not match in file {q_n_a_file_path}")
            # else:
            Path(f'./data/Questions/{q_n_a_file_path.stem}.txt').write_text('\n'.join(questions), encoding='utf-8')
            Path(f'./data/Answers/{q_n_a_file_path.stem}.txt').write_text('\n'.join(answers), encoding='utf-8')
            