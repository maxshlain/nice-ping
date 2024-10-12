from nicegui import ui

class Demo:
    def __init__(self):
        self.target = ""

    def ping(self):
        ui.notify(f"Pinging {self.target}")

demo = Demo()

# Create a container for centering and width control
with ui.column().classes('w-full items-center'):
    # Card with 'nice-py' class, centered and up to 80% width
    with ui.card().classes('nice-py w-full max-w-[80%]'):
        with ui.row().classes('items-center w-full'):
            ui.label('Target').classes('mr-2')
            ui.input().bind_value(demo, 'target').classes('flex-grow mr-2')
            ui.button('Ping', on_click=demo.ping)

ui.run()
