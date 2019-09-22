from os import path

from .head import Head


class Base(Head):
    
    def full_index(self):
        return {
            'index': {
                'content': self.structure(self.full_head()),
                'destination_path': path.join(
                    self.config.get('output_folder_path', ''),
                                    'index.html'
                ),
            },
        }
    
    def structure(self, head):
        indent = "    "  # 4 spaces
        formated_head = ''.join([
            f"{indent*2}{tag}\n"
            for conjunt in head
            for tag in conjunt
        ])
        return ( "<html>\n"
                f"{indent}<head>\n"
                f"{formated_head}"  # Already have newline
                f"{indent}</head>\n"
                 "</html>")
