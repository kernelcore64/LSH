import re
from numba import jit

class SyntaxHighlighter:
    def __init__(self, edit):
        self.edit = edit

    @jit
    def syntax_highlight(self, event):
        self.keywords = [
            "if", "else", "for", "while", "function", "local", "return", "end",
            "then", "do", "break", "elseif", "in"
        ]

        code = self.edit.get("1.0", "end-1c")
        pattern = self.__create_pattern(self.keywords)

        tags_to_remove = ["keyword", "string", "print", "()", "numbers", "[]", "<>", "{}", "require"]
        for tag in tags_to_remove:
            self.edit.tag_remove(tag, "1.0", "end")

        for line_number, line in enumerate(code.split("\n"), start=1):
            for match in re.finditer(pattern, line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("keyword", start_index, end_index)
                self.edit.tag_config("keyword", foreground="blue")

            for match in re.finditer(r'(["\'])(?:(?=(\\?))\2.)*?\1', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("string", start_index, end_index)
                self.edit.tag_config("string", foreground="orange")

            for match in re.finditer(r'\bprint\b', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("print", start_index, end_index)
                self.edit.tag_config("print", foreground="salmon")

            for match in re.finditer(r'\brequire\b', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("require", start_index, end_index)
                self.edit.tag_config("require", foreground="salmon")

            for match in re.finditer(r'\b\d+\b', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("numbers", start_index, end_index)
                self.edit.tag_config("numbers", foreground="purple")

            for match in re.finditer(r'[\{\}]', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("{}", start_index, end_index)
                self.edit.tag_config("{}", foreground="yellow")

            for match in re.finditer(r'[\[\]]', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("[]", start_index, end_index)
                self.edit.tag_config("[]", foreground="yellow")

            for match in re.finditer(r'[\<\>]', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("<>", start_index, end_index)
                self.edit.tag_config("<>", foreground="light blue")
    
            for match in re.finditer(r'[\(\)]', line):
                start_index = f"{line_number}.{match.start()}"
                end_index = f"{line_number}.{match.end()}"
                self.edit.tag_add("()", start_index, end_index)
                self.edit.tag_config("()", foreground="yellow")

    @jit
    def __create_pattern(self, keywords):
        return r'\b(?:' + '|'.join(keywords) + r')\b'
