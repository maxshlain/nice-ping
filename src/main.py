import asyncio
import os

from nicegui import ui


class PingApp:
    def __init__(self):
        self.target = "1.1.1.1"  # Set default value to '1.1.1.1'
        self.terminal_output = ""  # New attribute to store terminal output

    def get_command(self):
        if os.name == "nt":  # Windows
            return ["ping", "-n", "4", self.target]
        return ["ping", "-c", "4", self.target]

    async def ping(self):
        self.terminal_output = ""  # Clear the previous terminal output

        arguments = self.get_command()
        process = await asyncio.create_subprocess_exec(
            *arguments, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # Read the output asynchronously
        while True:
            line = await process.stdout.readline()
            if not line:
                break
            self.terminal_output += line.decode()
            self.update_terminal()

        # Handle any errors if needed
        await process.wait()

    def on_input_change(self, e):
        # Update the target with the input value and call ping on Enter
        self.target = e.value
        if e.key == "Enter":
            asyncio.create_task(
                self.ping()
            )  # Use asyncio to run the ping command asynchronously

    def update_terminal(self):
        # Safely update the textarea inside a UI context
        with self.terminal:
            self.terminal.value = self.terminal_output
            self.terminal.update()
            # Add JavaScript to scroll to the bottom of the textarea
            ui.run_javascript(
                'document.querySelector("textarea").scrollTop = document.querySelector("textarea").scrollHeight'
            )


app = PingApp()

# Create a container for centering and width control
with ui.column().classes("w-full items-center"):
    # Card with 'nice-py' class, centered and up to 80% width
    with ui.card().classes("nice-py w-full max-w-[80%]"):
        with ui.row().classes("items-center w-full"):
            ui.label("Target").classes("mr-2")
            ui.input(value=app.target, on_change=app.on_input_change).classes(
                "flex-grow mr-2"
            )
            ui.button("Ping", on_click=lambda: asyncio.create_task(app.ping()))

    # New card for terminal-like textarea
    with ui.card().classes("nice-py w-full max-w-[80%] mt-4"):
        app.terminal = ui.textarea(label="Terminal Output").classes(
            "w-full h-40 font-mono bg-gray-100 text-gray-800"
        )
        app.terminal.read_only = True

ui.run()
