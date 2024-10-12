from nicegui import ui

class Demo:
    def __init__(self):
        self.target = "1.1.1.1"  # Set default value to '1.1.1.1'
        self.terminal_output = ""  # New attribute to store terminal output

    def ping(self):
        ui.notify(f"Pinging {self.target}")
        # Simulate terminal output
        self.terminal_output += f"Pinging {self.target}...\n"
        self.update_terminal()

    def on_input_change(self, e):
        if e.key == 'Enter':
            self.ping()

    def update_terminal(self):
        # Update the terminal textarea
        self.terminal.value = self.terminal_output

demo = Demo()

# Create a container for centering and width control
with ui.column().classes('w-full items-center'):
    # Card with 'nice-py' class, centered and up to 80% width
    with ui.card().classes('nice-py w-full max-w-[80%]'):
        with ui.row().classes('items-center w-full'):
            ui.label('Target').classes('mr-2')
            ui.input(value=demo.target, on_change=demo.on_input_change).classes('flex-grow mr-2')
            ui.button('Ping', on_click=demo.ping)
    
    # New card for terminal-like textarea
    with ui.card().classes('nice-py w-full max-w-[80%] mt-4'):
        demo.terminal = ui.textarea(label='Terminal Output').classes('w-full h-40 font-mono bg-gray-100 text-gray-800')
        demo.terminal.read_only = True

ui.run()
