import tkinter as tk
import tkinter.scrolledtext as tkst
import csv

class VideoManager:
    def __init__(self, window):
        # Set up the main window
        window.geometry("850x500")
        window.title("Video Manager")

        # Input Fields and Labels
        self.create_input_fields(window)

        # Buttons
        self.create_buttons(window)

        # Scrolled Text Box for Video List
        self.video_list_text = tkst.ScrolledText(window, width=80, height=12, wrap="none")
        self.video_list_text.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

        # Status Label
        self.status_label = tk.Label(window, text="", font=("Helvetica", 10))
        self.status_label.grid(row=6, column=0, columnspan=4, padx=10, pady=10)

        # File name for CSV storage
        self.csv_file = "videos.csv"

        # Load existing videos from CSV
        self.video_list = self.load_videos_from_csv()
        self.playlist = []

        # Refresh video list display
        self.refresh_video_list()

    def create_input_fields(self, window):
        """Create input fields and their labels."""
        tk.Label(window, text="Enter Video Number:").grid(row=0, column=0, padx=10, pady=10)
        self.video_number_entry = tk.Entry(window, width=5)
        self.video_number_entry.grid(row=0, column=1, padx=10, pady=10)

        tk.Label(window, text="Video Name:").grid(row=1, column=0, padx=10, pady=10)
        self.video_name_entry = tk.Entry(window, width=30)
        self.video_name_entry.grid(row=1, column=1, columnspan=2, padx=10, pady=10)

        tk.Label(window, text="Director Name:").grid(row=2, column=0, padx=10, pady=10)
        self.director_name_entry = tk.Entry(window, width=30)
        self.director_name_entry.grid(row=2, column=1, columnspan=2, padx=10, pady=10)

        tk.Label(window, text="Rating:").grid(row=3, column=0, padx=10, pady=10)
        self.rating_entry = tk.Entry(window, width=5)
        self.rating_entry.grid(row=3, column=1, padx=10, pady=10)

    def create_buttons(self, window):
        """Create buttons for various functionalities."""
        tk.Button(window, text="Add Video", command=self.add_video).grid(row=0, column=2, padx=10, pady=10)
        tk.Button(window, text="Update Video", command=self.update_video).grid(row=0, column=3, padx=10, pady=10)
        tk.Button(window, text="Play Playlist", command=self.play_playlist).grid(row=4, column=0, padx=10, pady=10)
        tk.Button(window, text="Reset Playlist", command=self.reset_playlist).grid(row=4, column=1, padx=10, pady=10)

    def load_videos_from_csv(self):
        """Load videos from a CSV file."""
        video_list = []
        try:
            with open(self.csv_file, mode='r', newline='') as file:
                reader = csv.DictReader(file)
                for row in reader:
                    row['rating'] = float(row['rating'])  # Convert rating to float
                    row['play_count'] = int(row.get('play_count', 0))  # Convert play_count to int
                    video_list.append(row)
        except FileNotFoundError:
            # If the file doesn't exist, we start with an empty list
            self.status_label.configure(text="No previous data found. Starting fresh.", fg="blue")
        return video_list

    def save_videos_to_csv(self):
        """Save the current video list to a CSV file."""
        with open(self.csv_file, mode='w', newline='') as file:
            fieldnames = ['number', 'name', 'director', 'rating', 'play_count']
            writer = csv.DictWriter(file, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(self.video_list)

    def add_video(self):
        """Add a new video to the list."""
        video_info = self.get_video_info()
        if video_info:
            self.video_list.append(video_info)
            self.status_label.configure(text=f"Video {video_info['number']} added successfully!", fg="green")
            self.clear_inputs()
            self.save_videos_to_csv()  # Save to CSV after adding
            self.refresh_video_list()

    def update_video(self):
        """Update an existing video's details."""
        video_info = self.get_video_info()
        if video_info:
            for video in self.video_list:
                if video['number'] == video_info['number']:
                    video.update(video_info)
                    self.status_label.configure(text=f"Video {video_info['number']} updated successfully!", fg="green")
                    self.save_videos_to_csv()  # Save to CSV after updating
                    self.refresh_video_list()
                    return
            self.status_label.configure(text=f"Video {video_info['number']} not found.", fg="red")

    def get_video_info(self):
        """Retrieve video information from input fields and validate it."""
        video_number = self.video_number_entry.get()
        video_name = self.video_name_entry.get()
        director_name = self.director_name_entry.get()
        rating = self.rating_entry.get()

        if video_number and video_name and director_name and rating:
            try:
                return {
                    "number": video_number,
                    "name": video_name,
                    "director": director_name,
                    "rating": float(rating),
                    "play_count": 0
                }
            except ValueError:
                self.status_label.configure(text="Invalid rating. Please enter a numeric value.", fg="red")
        else:
            self.status_label.configure(text="All fields are required.", fg="red")
        return None

    def play_playlist(self):
        """Simulate playing the playlist."""
        if self.playlist:
            for video in self.playlist:
                video['play_count'] += 1
            self.status_label.configure(text="Playlist played successfully!", fg="green")
            self.save_videos_to_csv()  # Save to CSV after playing playlist
            self.refresh_video_list()
        else:
            self.status_label.configure(text="Playlist is empty.", fg="red")

    def reset_playlist(self):
        """Reset the playlist."""
        self.playlist = []
        self.status_label.configure(text="Playlist reset successfully!", fg="green")

    def refresh_video_list(self):
        """Refresh the displayed video list."""
        self.video_list_text.delete(1.0, tk.END)
        for video in self.video_list:
            video_info = (f"Video Number: {video['number']}, Name: {video['name']}, "
                          f"Director: {video['director']}, Rating: {video['rating']}, "
                          f"Play Count: {video.get('play_count', 0)}")
            self.video_list_text.insert(tk.END, video_info + "\n")

    def clear_inputs(self):
        """Clear all input fields."""
        self.video_number_entry.delete(0, tk.END)
        self.video_name_entry.delete(0, tk.END)
        self.director_name_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

if __name__ == "__main__":
    root = tk.Tk()
    app = VideoManager(root)
    root.mainloop()
