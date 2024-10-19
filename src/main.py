import asyncio
import os
from nicegui import ui


class PingApp:
    def __init__(self):
        self.target = "1.1.1.1"  # Set default value to '1.1.1.1'
        self.terminal_output = ""  # New attribute to store terminal output
        self.process = None  # To store the current ping process
        self.abort_button = None  # To store the abort button UI element
        self.container = None  # To store the UI container context

    def get_command(self):
        if os.name == "nt":  # Windows
            return ["ping", "-n", "4", self.target]
        return ["ping", "-c", "14", self.target]

    async def ping(self):
        self.terminal_output = ""  # Clear the previous terminal output
        arguments = self.get_command()
        self.process = await asyncio.create_subprocess_exec(
            *arguments, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
        )

        # Show the "Abort" button
        await self.show_abort_button()

        # Read the output asynchronously
        try:
            while True:
                line = await self.process.stdout.readline()
                if not line:
                    break
                self.terminal_output += line.decode() + "<br>"  # Add line break for HTML
                self.update_terminal()
        except asyncio.CancelledError:
            if self.process and self.process.returncode is None:
                self.process.terminate()
                await self.process.wait()

        # Hide the "Abort" button after the process completes
        self.hide_abort_button()

    def on_input_change(self, e):
        # Update the target with the input value and call ping on Enter
        self.target = e.value
        if e.key == "Enter":
            asyncio.create_task(self.ping())

    def update_terminal(self):
        # Safely update the div inside a UI context
        with self.terminal:
            self.terminal.set_content(self.terminal_output)
            # Add JavaScript to scroll to the bottom of the div
            ui.run_javascript(
                'document.querySelector(".terminal-output").scrollTop = document.querySelector(".terminal-output").scrollHeight'
            )

    def abort(self):
        if self.process:
            self.process.terminate()  # Terminate the process if it exists

    async def show_abort_button(self):
        # Ensure the "Abort" button is created in the correct UI context
        with self.container:
            if self.abort_button is None:
                # Create the "Abort" button dynamically and ensure it has the same width as the rest of the controls
                self.abort_button = ui.button("Abort", on_click=self.abort).classes(
                    "bg-red-500 text-white w-full"
                )
            else:
                # If the button already exists, just make it visible
                self.abort_button.visible = True

    def hide_abort_button(self):
        if self.abort_button:
            # Hide the button when the process finishes
            self.abort_button.visible = False


app = PingApp()

# Create a container for centering and width control
with ui.column().classes("w-full items-center") as container:
    app.container = container  # Store the container context
    # Card with 'nice-py' class, centered and up to 80% width
    with ui.card().classes("nice-py w-full max-w-[80%]"):
        with ui.row().classes("items-center w-full"):
            ui.label("Target").classes("mr-2")
            ui.input(value=app.target, on_change=app.on_input_change).classes(
                "flex-grow mr-2"
            )
            ui.button("Ping", on_click=lambda: asyncio.create_task(app.ping()))

    # New card for terminal-like div
    with ui.card().classes("nice-py w-full max-w-[80%] mt-4"):
        app.terminal = ui.html().classes(
            "terminal-output w-full h-40 font-mono bg-gray-100 text-gray-800 overflow-y-auto p-2"
        )

    # Place the abort button outside and ensure it matches width
    with ui.column().classes("w-full max-w-[80%] mt-2"):
        app.abort_button = ui.button("Abort", on_click=app.abort).classes("w-full bg-red-500 text-white")


ui.run()
