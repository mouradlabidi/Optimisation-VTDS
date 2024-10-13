import customtkinter

class ProgressInterface(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Traitement")
        self.geometry("300x100")  # Adjusted size for better layout
        self.resizable(False, False)  # Make window non-resizable
        self.protocol("WM_DELETE_WINDOW", self.disable_event)  # Disable the close button

        # Calculate position to center the window
        screen_width = self.winfo_screenwidth()  # Get screen width
        screen_height = self.winfo_screenheight()  # Get screen height
        x = (screen_width - 300) // 2  # Calculate x position
        y = (screen_height - 100) // 2  # Calculate y position
        self.geometry(f"+{x}+{y}")  # Set the position of the window

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Create and grid the progress bar
        self.progressbar = customtkinter.CTkProgressBar(self)
        self.progressbar.grid(row=0, column=0, padx=20, pady=10, sticky="ew")
        self.progressbar.configure(mode="indeterminate")
        self.progressbar.start()  # Start the indeterminate progress bar

        # Create and grid a label for the waiting message
        self.label = customtkinter.CTkLabel(self, text="Traitement en cours, veuillez patienter...",font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label.grid(row=1, column=0, sticky="ew", padx=20, pady=10)

    def disable_event(self):
        pass  # Do nothing on attempt to close window