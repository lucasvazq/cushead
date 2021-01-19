"""
Handle jinja extensions.
"""
from jinja2 import ext
from jinja2 import nodes
from jinja2 import parser as jinja2_parser
from jinja2 import runtime


class OneLineExtension(ext.Extension):
    """
    Strip each line inside the extension statement and merge all of them in one line.
    """

    tags = {"oneline"}  # Names that trigger the extension.

    def parse(self, parser: jinja2_parser.Parser) -> nodes.CallBlock:
        """
        Get a node that implements the extension logic and can be used by the AST.

        Args:
            parser: the jinja parser.

        Returns:
            The node.
        """
        next(parser.stream)
        lineno = parser.stream.current.lineno

        body = parser.parse_statements([f"name:end{tagname}" for tagname in self.tags], True)

        method = self.call_method("strip_spaces")
        call_block = nodes.CallBlock(method, [], [], body)
        call_block.set_lineno(lineno)
        return call_block

    @staticmethod
    def strip_spaces(caller: runtime.Macro) -> str:
        """
        Execute the extension logic on a template section.

        Args:
            caller: this is a Macro class instance that can be called to get the template content associated with this extension.

        Returns:
            The parsed template section.
        """
        return "".join(line.strip() for line in caller().split("\n"))
