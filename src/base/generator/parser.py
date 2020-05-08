# -*- coding: utf-8 -*-

import abc
import re
from html import parser as html_parser
from typing import List, NoReturn, Optional, Tuple

from jinja2 import ext
from jinja2 import nodes
from jinja2 import parser as jinja2_parser
from jinja2 import runtime


HTMLTagAttrs = Optional[List[Tuple[str, str]]]


class BaseParser(metaclass=abc.ABCMeta):
    def __init__(self, indentation, base_indentation: int = 0):
        self.indentation = indentation
        self.indent_amount = base_indentation
        self.content = []
        super().__init__()


class CustomPlainTextParser(BaseParser):
    def __init__(self, indentation_trigger=None, new_line_trigger=None, **kwargs):
        self.indentation_trigger = indentation_trigger or ()
        self.new_line_trigger = new_line_trigger or ()
        super().__init__(**kwargs)

    def parse_element(self, *, content: str) -> NoReturn:
        indentation = self.indentation * self.indent_amount
        self.content.append(indentation + content)

    def parse_content(self, content: str) -> NoReturn:
        splited_content = content.split('\n')
        for line in splited_content:
            stripped_line = line.strip()
            if stripped_line:
                if stripped_line.startswith(self.new_line_trigger):
                    self.parse_element(content='')  # add new line
                self.parse_element(content=stripped_line)
                if stripped_line.startswith(self.indentation_trigger):
                    self.indent_amount += 1
        return '\n'.join(self.content)


class CustomScriptParser(BaseParser):
    def __init__(self, new_line_trigger=None, base_indentation=None, **kwargs):
        self.new_line_trigger = new_line_trigger or ()
        self.endstart_delimiters_pattern = re.compile(
            r'^(}|]|\)|;)+'
            r',? '
            r'({|\[|\()+$'
        )
        self.base_indentation = bool(base_indentation)
        self.end_delimiters_pattern = re.compile(r'.*({|\[|\()$')
        self.start_delimiters_pattern = re.compile(r'^(}|]|\)|;)+,?$')
        super().__init__(**kwargs)

    def parse_element(self, *, content: str) -> NoReturn:
        if self.base_indentation:
            indentation = ''
            self.base_indentation = False
        else:
            indentation = self.indentation * self.indent_amount
        self.content.append(indentation + content)

    def parse_content(self, content: str) -> NoReturn:
        cleaned_data = filter(None, [x.strip() for x in content.split('\n')])
        for line in cleaned_data:
            if line:
                if self.endstart_delimiters_pattern.match(line):
                    self.indent_amount -= 1
                    self.parse_element(content=line)
                    self.indent_amount += 1
                elif self.end_delimiters_pattern.match(line):
                    self.parse_element(content=line)
                    self.indent_amount += 1
                elif self.start_delimiters_pattern.match(line):
                    self.indent_amount -= 1
                    self.parse_element(content=line)
                else:
                    if line.startswith(self.new_line_trigger):
                        self.parse_element(content='')  # add new line
                    self.parse_element(content=line)
        return '\n'.join(self.content)


class MLParser(BaseParser, html_parser.HTMLParser, metaclass=abc.ABCMeta):
    def __init__(self, one_line_tags=None, self_close_tags=None, **kwargs):
        super().__init__(**kwargs)
        self.one_line_tags = one_line_tags
        self.self_close_tags = self_close_tags or ()
        self.lastendtag = '???'
        self.one_line = False

    def handle_attrs(self, attrs):
        if attrs:
            attributes = ' ' + ' '.join([
                f"{k}=\"{v}\"" for k, v in dict(attrs).items()
            ])
        else:
            attributes = ''
        return attributes

    def parse_content(self, content):
        self.feed(content)
        return '\n'.join(self.content)

    def handle_endtag(self, tag):
        self.lasttag = f'end_{tag}'


class CustomHTMLParser(MLParser):

    def __init__(self, *,
                 indentation: str,
                 one_line_tags: Optional[Tuple[str]] = None,
                 self_close_tags: Optional[Tuple[str]] = None) -> NoReturn:
        super().__init__(indentation=indentation,
                         one_line_tags=one_line_tags, self_close_tags=self_close_tags)
        self.match_ie_sentence = re.compile(
            r'(?P<starttag>\[if IE]>)'
            r'( |\s)*'
            r'(?P<data>.*(?!<!).)'
            r'( |\s)*'
            r'(?P<endtag><!\[endif])'
        )

    def parse_element(self, *,
                      content: str,
                      one_line: bool = False) -> NoReturn:
        if one_line:
            self.content[-1] += content
        else:
            indentation = self.indentation * self.indent_amount
            self.content.append(indentation + content)

    def handle_decl(self, decl: str) -> NoReturn:
        """This method is called to handle an HTML doctype declaration"""
        self.parse_element(content=f'<!{decl}>')

    def handle_comment(self, data: str) -> NoReturn:
        """This method is called when a comment is encountered"""

        # 3.8
        match = self.match_ie_sentence.match(data.strip())
        if match:
            groups = match.groupdict()
            # Add it with the instruction with one level more of indentation
            self.parse_element(content='<!--' + groups['starttag'])
            self.indent_amount += 1
            self.parse_element(content=groups['data'])
            self.indent_amount -= 1
            self.parse_element(content=groups['endtag'] + '-->')

        # Detect inline html comment and add it without indentation
        elif self.lasttag in self.self_close_tags:
            self.parse_element(content=f'<!--{data}-->', one_line=True)

    def handle_starttag(self, tag: str, attrs: HTMLTagAttrs) -> NoReturn:
        """his method is called to handle the start of a tag"""
        attributes = self.handle_attrs(attrs)

        # Add the tag
        element = f'<{tag}{attributes}>'
        self.parse_element(content=element)

        # When read the content of title,
        # must need to append it to the same line of title,
        # same for it's close tag.
        if tag in self.one_line_tags:
            self.one_line = True

        # If the actual tag is not self closing, the next element must be indented
        if not tag.startswith(self.one_line_tags + self.self_close_tags):
            self.indent_amount += 1

    def handle_endtag(self, tag: str) -> NoReturn:
        """This method is called to handle the end tag of an element"""

        starttag = self.lasttag
        super().handle_endtag(tag)

        if tag.startswith(self.self_close_tags):
            return

        # The close of tag must be in one level below of indentation than of the actual level
        if not tag.startswith(self.one_line_tags):
            self.indent_amount -= 1

        closed_tag = f'</{tag}>'

        # If the attr one_line is defined,
        # or if the last oppened tag is the same to the actual tag and
        # no data was detected, we need add the close tag to the same line
        if self.one_line or (not self.has_data and starttag == tag):
            self.parse_element(content=closed_tag, one_line=True)

            # Revert one line
            if self.one_line:
                self.one_line = False

            # We need to save the attr has_data to True, because the actual
            # element must be part of other element.
            # And, if the next thing to handle is the close of the tag of that
            # parent element, we need to asume that the data if has was this
            # element.
            else:
                self.has_data = True

        else:
            self.parse_element(content=closed_tag)

    def handle_data(self, data: str) -> NoReturn:
        """This method is called to process the text data that are inside of the element"""

        # python 3.8
        # if cleaned_data := data.strip():
        cleaned_data = data.strip()
        if cleaned_data:
            self.has_data = True

            # Add indentation to the code inside an element
            if self.lasttag in ('script', 'style'):
                initial_data = {
                    'indentation': self.indentation,
                    'base_indentation': self.indent_amount,
                }
                content_parser = CustomScriptParser(**initial_data)
                content = content_parser.parse_content(content=data)
                self.parse_element(content=content)

            else:
                if self.one_line:
                    self.parse_element(content=cleaned_data, one_line=True)
                else:
                    self.parse_element(content=cleaned_data)
        else:
            self.has_data = False

# indentation, camel_case_tags, regex_self_close_tags, one_line_tags, self_close_tags


class CustomXMLParser(MLParser):

    def __init__(self, *,
                 indentation: str,
                 camel_case_tags: Optional[Tuple[str]] = None,
                 regex_self_close_tags: Tuple[re.Pattern] = None,
                 one_line_tags: Optional[Tuple[str]] = None,
                 self_close_tags: Optional[Tuple[str]] = None) -> NoReturn:
        super().__init__(indentation=indentation,
                         one_line_tags=one_line_tags, self_close_tags=self_close_tags)
        self.camel_case_tags = camel_case_tags or ()
        self.regex_self_close_tags = regex_self_close_tags or ()

    def handle_pi(self, data: str) -> NoReturn:
        self.parse_element(content=f'<?{data}>')

    def parse_self_close_tags(self, *, tag: str) -> bool:
        if tag in self.self_close_tags:
            return True

        if self.regex_self_close_tags:
            pattern = '|'.join(self.regex_self_close_tags)
            return bool(re.search(pattern, tag))

        return False

    def parse_element(self, *,
                      content: str,
                      one_line: bool = False) -> NoReturn:
        if one_line:
            self.content[-1] += content
        else:
            indentation = self.indentation * self.indent_amount
            if self.parse_self_close_tags(tag=self.lasttag):
                self_close_tag = f'{content[:-1]}/{content[-1]}'
                self.content.append(indentation + self_close_tag)
                self.one_line = True
            else:
                self.content.append(indentation + content)

    def parse_tag(self, *, tag: str) -> NoReturn:
        pattern = re.compile(
            r'(^|[^\w])(?P<tag>'
            f'{tag}'
            r')([^\w]|$)',
            re.I
        )
        elements_to_match = ','.join(self.camel_case_tags)
        # 3.8
        match = pattern.search(elements_to_match)
        if match:
            return match.groupdict()['tag']
        return tag

    def handle_starttag(self, tag: str, attrs: HTMLTagAttrs) -> NoReturn:
        parsed_tag = self.parse_tag(tag=tag)
        self.lasttag = parsed_tag
        attributes = self.handle_attrs(attrs)

        # Add the tag
        element = f'<{parsed_tag}{attributes}>'
        self.parse_element(content=element)

        # When read the content of title,
        # must need to append it to the same line of title,
        # same for it's close tag.
        if parsed_tag in self.one_line_tags:
            if self.one_line:
                self.indent_amount += 1
            self.one_line = True

        # If the actual tag is not self closing, the next element must be indented
        if parsed_tag not in (self.one_line_tags + self.self_close_tags):
            self.indent_amount += 1

    def handle_endtag(self, tag: str) -> NoReturn:
        starttag = self.lasttag
        parsed_tag = self.parse_tag(tag=tag)
        super().handle_endtag(parsed_tag)
        if not self.parse_self_close_tags(tag=parsed_tag):

            if parsed_tag.startswith(self.self_close_tags):
                return

            # The close of tag must be in one level below of indentation than of the actual level
            if not parsed_tag.startswith(self.one_line_tags):
                self.indent_amount -= 1

            closed_tag = f'</{parsed_tag}>'

            # If the attr one_line is defined,
            # or if the last oppened tag is the same to the actual tag and
            # no data was detected, we need add the close tag to the same line
            if self.one_line or (not self.has_data and starttag == parsed_tag):
                self.parse_element(content=closed_tag, one_line=True)

                # Revert one line
                if self.one_line:
                    self.one_line = False

                # We need to save the attr has_data to True, because the actual
                # element must be part of other element.
                # And, if the next thing to handle is the close of the tag of that
                # parent element, we need to asume that the data if has was this
                # element.
                else:
                    self.has_data = True

            else:
                self.parse_element(content=closed_tag)
        else:
            self.indent_amount -= 1

    def handle_data(self, data: str) -> NoReturn:
        # 3.8
        cleaned_data = data.strip()
        if cleaned_data:
            self.has_data = True

            if self.one_line:
                self.parse_element(content=cleaned_data, one_line=True)
            else:
                self.parse_element(content=cleaned_data)
        else:
            self.has_data = False


class OneLineExtension(ext.Extension):
    """
    Removes whitespace between HTML tags at compile time, including tab and newline characters.
    It does not remove whitespace between Jinja2 tags or variables. Neither does it remove whitespace between tags
    """

    # Jinja2 docs:
    # tags = a set of names that trigger the extension.
    tags = {'oneline'}
    endtags = tuple([f'name:end{tagname}' for tagname in tags])

    def parse(self, parser: jinja2_parser.Parser) -> nodes.CallBlock:
        """
        This method is called when any of tags is recognized

        The method apply transformation to the blocks inside the start and the end of the block.
        This transformation is the text without new lines and spaces between.
        The return is a node class initialized with this transformated text.
        The nodes are the elements that are used by the Abstract Syntax Tree of Jinja2 to represent
        the template.

        Args:
            parser: parser processor gived from Jinja2

        Return:
            CallBlock node type
        """

        # The first token is the token that started the tag.
        # Don't need it.
        next(parser.stream)

        # We need actual linenumber to append the final result to this line number
        lineno = parser.stream.current.lineno

        # Get the content inside the extension tag, with the second parameter as True,
        # we dont get, as final token, the end block of the extension tag, because we don't need it.
        body = parser.parse_statements(self.endtags, True)

        # We parse te content calling our custom methods and generate the a CallBlock
        method = self.call_method('strip_spaces')
        call_block = nodes.CallBlock(method, [], [], body)

        # Return CallBlock seeted to the line number
        return call_block.set_lineno(lineno)

    def strip_spaces(self, caller: runtime.Macro) -> str:
        """
        Clean all the spaces and new lines of a content

        Args:
            caller: an anonymous Macro class, generated by CallBlock node.
                This class is callable and return a parsed version (variable replacement) of the content
                gived to the CallBlock.

        Return:
            return the cleaned content of the macro
        """
        return ''.join(caller().split())
