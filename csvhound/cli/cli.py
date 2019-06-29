import io

from prompt_toolkit.application import Application
from prompt_toolkit.application.current import get_app
from prompt_toolkit.completion import PathCompleter, WordCompleter
from prompt_toolkit.buffer import Buffer
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.key_binding.bindings.focus import (
    focus_next,
    focus_previous,
)
from prompt_toolkit.layout.containers import (
    Float,
    FloatContainer,
    HSplit,
    VSplit,
    Window,
    WindowAlign,
)
from prompt_toolkit.layout.controls import BufferControl, FormattedTextControl, DummyControl
from prompt_toolkit.layout.layout import Layout
from prompt_toolkit.layout.menus import CompletionsMenu
from prompt_toolkit.layout.processors import (BeforeInput)
from prompt_toolkit.widgets import Box, Button, Frame, Label, TextArea

from csvhound.logger import logger
import csvhound.core

logger.debug(__name__ + ' imported')

class HoundCli(object):
    """
    Abstracts CSVHound CLI
    """

    def __init__(self):
        # create left and right buffers in main area
        self.left_buffer = Buffer()
        self.right_buffer = Buffer()

        # sample text to get us going
        self.left_buffer.text = 'test\none\ntwo\nthree'

        # create windows; you need a Windor and a BufferControl to display Buffer
        # content
        self.left_window = Window(BufferControl(buffer=self.left_buffer))
        self.right_window = Window(BufferControl(buffer=self.right_buffer))

        self.command_window = Window(height=1, style='class:line')
        self.command_area = HSplit([
            self.command_window,
            Window(height=1, char='-', style='class:line')
            ])


        self.main_body = VSplit([
            self.left_window,

            # A vertical line in the middle. We explicitly specify the width, to make
            # sure that the layout engine will not try to divide the whole width by
            # three for all these windows.
            Window(width=1, char='|', style='class:line'),

            # Display the Result buffer on the right.
            self.right_window,
        ])

        self.status_area = Window(
                        height=1,
                        content=DummyControl(),
                        align=WindowAlign.LEFT,
                        style='class:reverse')


        self.float_content = HSplit([
            # The titlebar.
            Window(height=1,
                   content=FormattedTextControl(self.get_titlebar_text),
                   # content=DummyControl(),
                   align=WindowAlign.LEFT,
                   style='class:reverse'),
            self.status_area,
            # Horizontal separator.
            Window(height=1, char='-', style='class:line'),
            self.command_area,
            # text_area,
            # Window(height=1, char='-', style='class:line'),
            self.main_body
        ])

        self.root_container = FloatContainer(
            content = self.float_content,
            floats=[
                Float(xcursor=True,
                      ycursor=True,
                      content=CompletionsMenu(max_height=16, scroll_offset=1))
            ]
        )

        self.kb = KeyBindings()

        self.kb.add('c-n')(focus_next)
        self.kb.add('c-p')(focus_previous)

        @self.kb.add('c-c', eager=True)
        @self.kb.add('c-q', eager=True)
        def _(event):
            """
            Pressing Ctrl-Q or Ctrl-C will exit the user interface.

            Setting a return value means: quit the event loop that drives the user
            interface and return this value from the `Application.run()` call.

            Note that Ctrl-Q does not work on all terminals. Sometimes it requires
            executing `stty -ixon`.
            """
            event.app.exit()

        @self.kb.add('o')
        def _(event):
            """
            attempt to insert a file open command prompt
            """
            self.cmd_buffer_open = self.create_cmd_buffer("open")
            self.cmd_open_control = self.create_cmd_control(self.cmd_buffer_open, prompt='[Open file:] ')

            self.command_area.children[0].content = self.cmd_open_control 

            app = get_app()
            app.layout.focus(self.command_area)

        self.application = None

    # define initial titlebar text
    def get_titlebar_text(self):
        return [
            ('class:title', ' CSV Hound'),
            ('class:title', ' (Press [Ctrl-Q] to quit.)'),
        ]

    def get_status_text(self, message):
        return [
            ('class:red', '     '+message),
        ]

    # accept_handler for open command
    def do_open(self, _):
        logger.debug('attempting to open file...')
        model = csvhound.core.BaseHound()
        # this is only for initial PoC!
        # TODO: add validation, etc.
        table = model.get_table_from_file(_.text)
        # model.get_columns()
        # exit()
        output = io.StringIO()

        model.describe_table(output=output)
        contents = output.getvalue()
        output.close()

        # model.distinct_values('Size', with_count=False)

        self.left_buffer.text = contents
        # right_buffer.text = _.text
        # hide previous command buffer control
        self.command_area.children[0].content = DummyControl()
        self.status_area.content = FormattedTextControl(self.get_status_text('file open: ' + _.text))
        app = get_app()
        app.layout.focus(self.left_buffer)

    def do_inspect(self, _):
        self.right_buffer.text = "INSPECT:\n"+_.text
        # hide previous command buffer control
        self.command_area.children[0].content = DummyControl()
        self.status_area.content = FormattedTextControl(self.get_status_text('inspect file: ' + _.text))
        app = get_app()
        app.layout.focus(self.left_buffer)


    # create a command buffer for a given command, with named accept_handler
    def create_cmd_buffer(self, command):
        completer=PathCompleter()
        # if command == 'open' or command == 'inspect':
            # completer=PathCompleter()
        # else:
            # completer=None
        accept_handler = getattr(self, 'do_' + command)
        return Buffer(
            completer=completer,
            name='cmd_buffer_'+command,
            accept_handler=accept_handler,
            multiline=False
        )

    # create command buffer control with given command buffer
    def create_cmd_control(self, buffer, prompt='>>>> '):
        return BufferControl(
                buffer,
                input_processors=[BeforeInput(prompt, style='class:text-area.prompt')]
        )

    def create_application(self):
        self.application = Application(
            layout=Layout(self.root_container),
            key_bindings=self.kb,

            # Let's add mouse support!
            mouse_support=True,

            # Using an alternate screen buffer means as much as: "run full screen".
            # It switches the terminal to an alternate screen.
            full_screen=True)

    def run_application(self):
        self.application.run()

