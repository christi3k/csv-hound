#!/usr/bin/env python
"""
Start of csvhound full screen CLI powered by python-prompt-toolkit.
"""
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

import csvhound.core

model = csvhound.core.BaseHound()
# table = model.get_table_from_file('sample-data/pydata-event.csv')
# model.get_columns()
# exit()
# model.describe_table()
# model.distinct_values('Size', with_count=False)

# create buffers
left_buffer = Buffer()
right_buffer = Buffer()

# sample text to get us going
left_buffer.text = 'test\none\ntwo\nthree'

# create windows; you need a Windor and a BufferControl to display Buffer
# content
left_window = Window(BufferControl(buffer=left_buffer))
right_window = Window(BufferControl(buffer=right_buffer))

# define initial titlebar text
def get_titlebar_text():
    return [
        ('class:title', ' CSV Hound'),
        ('class:title', ' (Press [Ctrl-Q] to quit.)'),
    ]

def get_status_text(message):
    return [
        ('class:red', '     '+message),
    ]

# accept_handler for open command
def do_open(_):

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

    left_buffer.text = contents
    # right_buffer.text = _.text
    # hide previous command buffer control
    command_area.children[0].content = DummyControl()
    status_area.content = FormattedTextControl(get_status_text('file open: ' + _.text))
    app = get_app()
    app.layout.focus(left_buffer)

def do_inspect(_):
    right_buffer.text = "INSPECT:\n"+_.text
    # hide previous command buffer control
    command_area.children[0].content = DummyControl()
    status_area.content = FormattedTextControl(get_status_text('inspect file: ' + _.text))
    app = get_app()
    app.layout.focus(left_buffer)

# to build a TextArea without the widget, you need the following:
#     :class:`~prompt_toolkit.buffer.Buffer`,
#     :class:`~prompt_toolkit.layout.BufferControl` and
#     :class:`~prompt_toolkit.layout.Window`.
# let's try building this incrementally so we can sub in different accept_handlers

# class prompt_toolkit.buffer.Buffer(completer=None, auto_suggest=None, history=None, validator=None, tempfile_suffix=u'', name=u'', complete_while_typing=False, validate_while_typing=False, enable_history_search=False, document=None, accept_handler=None, read_only=False, multiline=True, on_text_changed=None, on_text_insert=None, on_cursor_position_changed=None, on_completions_changed=None, on_suggestion_set=None)

# create a command buffer for a given command, with named accept_handler
def create_cmd_buffer(command):
    completer=PathCompleter()
    # if command == 'open' or command == 'inspect':
        # completer=PathCompleter()
    # else:
        # completer=None
    accept_handler = globals()['do_' + command]
    return Buffer(
        completer=completer,
        name='cmd_buffer_'+command,
        accept_handler=accept_handler,
        multiline=False
    )

# create command buffer control with given command buffer
def create_cmd_control(buffer, prompt='>>>> '):
    return BufferControl(
            buffer,
            input_processors=[BeforeInput(prompt, style='class:text-area.prompt')]
    )

# cmd_buffer_open = create_cmd_buffer("open")

# class prompt_toolkit.layout.BufferControl(buffer=None, input_processors=None, include_default_input_processors=True, lexer=None, preview_search=False, focusable=True, search_buffer_control=None, menu_position=None, focus_on_click=False, key_bindings=None)
# cmd_open_control = BufferControl(cmd_buffer_open, input_processors=[BeforeInput('>>> ', style='class:text-area.prompt')])

# cmd_open_control = create_cmd_control(cmd_buffer_open, prompt='[Open file:] ')

# command_window = Window(BufferControl(Buffer()))
command_window = Window(height=1, style='class:line')
command_area = HSplit([
    command_window,
    Window(height=1, char='-', style='class:line')
    ])

# text_area = TextArea(completer=PathCompleter(),height=1, prompt='>>> ', multiline=False, accept_handler=do_open_file)
# text_area_hsplit = HSplit([
    # text_area,
    # Window(height=1, char='-', style='class:line')
    # ])

main_body = VSplit([
    left_window,

    # A vertical line in the middle. We explicitly specify the width, to make
    # sure that the layout engine will not try to divide the whole width by
    # three for all these windows.
    Window(width=1, char='|', style='class:line'),

    # Display the Result buffer on the right.
    right_window,
])

status_area = Window(
                height=1,
                content=DummyControl(),
                align=WindowAlign.LEFT,
                style='class:reverse')


float_content = HSplit([
    # The titlebar.
    Window(height=1,
           content=FormattedTextControl(get_titlebar_text),
           align=WindowAlign.LEFT,
           style='class:reverse'),
    status_area,
    # Horizontal separator.
    Window(height=1, char='-', style='class:line'),
    command_area,
    # text_area,
    # Window(height=1, char='-', style='class:line'),
    main_body
])

root_container = FloatContainer(
    content = float_content,
    floats=[
        Float(xcursor=True,
              ycursor=True,
              content=CompletionsMenu(max_height=16, scroll_offset=1))
    ]
)



kb = KeyBindings()
kb.add('c-n')(focus_next)
kb.add('c-p')(focus_previous)

@kb.add('c-o')
def _(event):
    """
    attempt to insert a file open command prompt
    """
    cmd_buffer_open = create_cmd_buffer("open")
    cmd_open_control = create_cmd_control(cmd_buffer_open, prompt='[Open file:] ')

    command_area.children[0].content = cmd_open_control 

    app = get_app()
    app.layout.focus(command_area)

@kb.add('c-b')
def _(event):
    """
    attempt to "inspect" a file 
    (this is really to make sure we can add multiple commands with keybindings; c-i isn't working for some reason)
    """
    cmd_buffer_inspect = create_cmd_buffer("inspect")
    cmd_inspect_control = create_cmd_control(cmd_buffer_inspect, prompt='[Inspect file:] ')

    command_area.children[0].content = cmd_inspect_control 

    app = get_app()
    app.layout.focus(command_area)

@kb.add('c-c', eager=True)
@kb.add('c-q', eager=True)
def _(event):
    """
    Pressing Ctrl-Q or Ctrl-C will exit the user interface.

    Setting a return value means: quit the event loop that drives the user
    interface and return this value from the `Application.run()` call.

    Note that Ctrl-Q does not work on all terminals. Sometimes it requires
    executing `stty -ixon`.
    """
    event.app.exit()

application = Application(
    layout=Layout(root_container),
    key_bindings=kb,

    # Let's add mouse support!
    mouse_support=True,

    # Using an alternate screen buffer means as much as: "run full screen".
    # It switches the terminal to an alternate screen.
    full_screen=True)


def run():
    # Run the interface. (This runs the event loop until Ctrl-Q is pressed.)
    application.run()


if __name__ == '__main__':
    run()

