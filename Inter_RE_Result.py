import customtkinter
import os
class RE_Result(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Configure window
        self.title("Recherche Exhaustive")
        self.geometry("350x150")  # Adjusted size for better layout
        self.resizable(False, False)  # Make window non-resizable

        # Calculate position to center the window
        screen_width = self.winfo_screenwidth()  # Get screen width
        screen_height = self.winfo_screenheight()  # Get screen height
        x = (screen_width - 350) // 2  # Calculate x position
        y = (screen_height - 150) // 2  # Calculate y position
        self.geometry(f"+{x}+{y}")  # Set the position of the window

        # Configure grid layout
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        # Create and grid a label for the waiting message
        self.label = customtkinter.CTkLabel(self, text="La recherche exhaustive est terminée.\nVoulez-vous ouvrir le fichier 'Recherche.xlsx' ?", font=customtkinter.CTkFont(size=12, weight="bold"))
        self.label.grid(row=0, column=0, columnspan=2, sticky="ew", padx=20, pady=10)

        self.btn_open= customtkinter.CTkButton(self, text="Ouvrir", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                           command=self.openFichierExcel)
        self.btn_open.grid(row=1, column=0, padx=20, pady=(10, 10))

        # Create and grid the button to open the resultRE folder
        self.btn_open_folder = customtkinter.CTkButton(self, text="Ouvrir Dossier", font=customtkinter.CTkFont(size=13, weight="bold"),
                                                       command=self.openResultFolder)
        self.btn_open_folder.grid(row=1, column=1, padx=20, pady=(10, 10))

    def openFichierExcel(self):
        result_folder_path = "resultRE"
        if os.path.exists(result_folder_path):
            if os.path.exists("resultRE\Recherche.xlsx"):
                os.startfile("resultRE\Recherche.xlsx")
            else:
                print("Le fichier 'Recherche.xlsx' n'existe pas dans le dossier 'resultRE'.")


    def openResultFolder(self):
        self.destroy()
        result_folder_path = "resultRE"
        if os.path.exists(result_folder_path):
            os.startfile(result_folder_path)
        else:
            os.makedirs(result_folder_path)
            os.startfile(result_folder_path)
        

if __name__ == "__main__":
    app = RE_Result()
    app.mainloop()