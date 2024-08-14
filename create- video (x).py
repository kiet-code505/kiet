import tkinter as tk
import tkinter.scrolledtext as tkst

class CreateVideoList():
    def __init__(self, window):
        window.geometry("750x350")
        window.title("Create Video List")

        # Video Name Input
        tk.Label(window, text="Video Name:").grid(row=0, column=0, padx=10, pady=10)
        self.video_name_txt = tk.Entry(window, width=30)
        self.video_name_txt.grid(row=0, column=1, padx=10, pady=10)

        # Director Name Input
        tk.Label(window, text="Director Name:").grid(row=1, column=0, padx=10, pady=10)
        self.director_name_txt = tk.Entry(window, width=30)
        self.director_name_txt.grid(row=1, column=1, padx=10, pady=10)

        # Rating Input
        tk.Label(window, text="Rating:").grid(row=2, column=0, padx=10, pady=10)
        self.rating_txt = tk.Entry(window, width=30)
        self.rating_txt.grid(row=2, column=1, padx=10, pady=10)

        # Add Video Button
        add_video_btn = tk.Button(window, text="Add Video", command=self.add_video_clicked)
        add_video_btn.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

        # Scrolled Text Box for Video List
        self.list_txt = tkst.ScrolledText(window, width=60, height=12, wrap="none")
        self.list_txt.grid(row=4, column=0, columnspan=2, padx=10, pady=10)

        # Status Label
        self.status_lbl = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_lbl.grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        # List to store videos
        self.video_list = []

    def add_video_clicked(self):
        video_name = self.video_name_txt.get()
        director_name = self.director_name_txt.get()
        rating = self.rating_txt.get()

        if video_name and director_name and rating:
            try:
                rating = float(rating)
                video_info = f"Video Name: {video_name}, Director: {director_name}, Rating: {rating}"
                self.video_list.append(video_info)
                self.list_txt.insert(tk.END, video_info + "\n")
                self.status_lbl.configure(text="Video added successfully!")
                self.clear_inputs()
            except ValueError:
                self.status_lbl.configure(text="Invalid rating. Please enter a number.")
        else:
            self.status_lbl.configure(text="All fields are required.")

    def clear_inputs(self):
        self.video_name_txt.delete(0, tk.END)
        self.director_name_txt.delete(0, tk.END)
        self.rating_txt.delete(0, tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    CreateVideoList(window)
    window.mainloop()
