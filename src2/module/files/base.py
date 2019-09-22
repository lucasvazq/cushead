from .head import Head


class Base(Head):
    
    def full_index(self):
        return self.structure(self.full_head())
    
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
