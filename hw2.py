import subprocess
import xml.etree.ElementTree as ET
import os

def read_config(config_path):
    tree = ET.parse(config_path)
    root = tree.getroot()
    config = {
        'visualizer_path': root.find('visualizer_path').text,
        'repo_path': root.find('repo_path').text,
        'output_path': root.find('output_path').text
    }
    return config

def get_commit_tree(repo_path):
    result = subprocess.run(
        ['git', '-C', repo_path, 'log', '--pretty=format:%H|%s|%an|%ad', '--date=iso', '--reverse'],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding='utf-8'
    )
    
    if result.returncode != 0:
        print("Ошибка при получении коммитов:", result.stderr)
        return []

    commits = result.stdout.splitlines()
    commit_info = []  # информация для каждого коммита
    
    for commit in commits:
        hash_value, message, author, date = commit.split('|')
        commit_info.append({
            'hash': hash_value,
            'message': message,
            'author': author,
            'date': date
        })

    return commit_info

def generate_mermaid_code(commit_info):
    lines = ["graph TD;"]
    
    for i in range(len(commit_info)):
        commit = commit_info[i]
        node_id = commit['hash'][:7]    
        commit_block = (
            f"{commit['message']}\n"
            f"{commit['hash'][:10]}\n"
            f"{commit['date']}\n"
            f"{commit['author']}\n"
        )
        lines.append(f'    {node_id}["{commit_block}"]')
        
        if i > 0:
            parent_id = commit_info[i - 1]['hash'][:7]
            lines.append(f'    {parent_id} --> {node_id}')

    return "\n".join(lines)

def write_output(output_path, content):
    with open(output_path, 'w') as f:
        f.write(content)

def main(config_path):
    config = read_config(config_path)
    commit_info = get_commit_tree(config['repo_path'])
    mermaid_code = generate_mermaid_code(commit_info)
    print(mermaid_code)
    write_output(config['output_path'], mermaid_code)

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Использование: python script.py <config.xml>")
        sys.exit(1)
    
    main(sys.argv[1])
