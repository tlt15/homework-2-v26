import unittest
from unittest.mock import patch, mock_open
import subprocess
import xml.etree.ElementTree as ET

# Импортируем функции из вашего скрипта
from hw2 import read_config, get_commit_tree, generate_mermaid_code, write_output

class TestYourScript(unittest.TestCase):


    @patch('subprocess.run')
    def test_get_commit_tree(self, mock_run):
        # Настройка mock объекта
        mock_run.return_value = subprocess.CompletedProcess(
            args=['git', '-C', 'mock_repo', 'log'],
            returncode=0,
            stdout='abc123|Initial commit|Author Name|2024-12-12 12:00:00\n'
                   'def456|Second commit|Author Name|2024-12-13 12:00:00\n',
            stderr=''
        )

        commits = get_commit_tree('mock_repo')
        
        self.assertEqual(len(commits), 2)
        self.assertEqual(commits[0]['hash'], 'abc123')
        self.assertEqual(commits[1]['message'], 'Second commit')

    def test_generate_mermaid_code(self):
        commit_info = [
            {'hash': 'abc123', 'message': 'Initial commit', 'author': 'Author Name', 'date': '2024-12-12 12:00:00'},
        ]
        
        mermaid_code = generate_mermaid_code(commit_info)
        
        expected_code = (
            "graph TD;\n"
            '    abc123["Initial commit\nabc123\n2024-12-12 12:00:00\nAuthor Name\n"]\n'
        )

        self.assertEqual(mermaid_code.strip(), expected_code.strip())



    @patch('builtins.open', new_callable=mock_open)
    def test_write_output(self, mock_file):
        write_output('mock_output.txt', 'some content')
        
        mock_file().write.assert_called_once_with('some content')

if __name__ == '__main__':
    unittest.main()
