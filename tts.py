import tkinter as tk
from PIL import ImageTk, Image
import speech as sp
import description as ds
import process as ps

# Create a new Tkinter window
window = tk.Tk()

# Set the window title and size
window.title("My Simple UI")
window.geometry("400x200")

# Create a label widget to display text
label = tk.Label(window, text="Welcome to The Visualiser", font=("Arial", 16))
label.pack(pady=20)

# Create a function to handle button clicks
def handle_button_click():
    # # Hide the main window
    # window.withdraw()

    # Create a new Tkinter window
    speak_window = tk.Toplevel()

    # Set the window title and size
    speak_window.title("Speak Window")
    speak_window.geometry("400x200")

    # Create a label widget to display text
    speak_label = tk.Label(speak_window, text="Speak into the microphone", font=("Arial", 16))
    speak_label.pack(pady=20)

    # Take input as speech
    ip_text = sp.speech_to_text()

    # Give use that to get input for the other file
    input_text = ds.generate_description(ip_text)
    sentiments = ds.get_sentiments(ip_text)

    # Create a function to handle "Done" button clicks
    def handle_done_button_click():
        # Close the speak window
        window.withdraw()
        speak_window.withdraw()

        # Create a new Tkinter window
        image_window = tk.Toplevel()

        # Set the window title and size
        image_window.title("Image Window")
        image_window.geometry("400x400")

        # Create a label widget to display text
        image_label = tk.Label(image_window, text="Here's a rendered image\n(You spoke: " + ip_text + ")", font=("Arial", 16))
        image_label.pack(pady=20)

        # Generate image
        ps.generate_image(input_text, sentiments)

        img = Image.open('image.png')
        img = img.resize((350, 350))
        # convert the image to a PhotoImage object
        photo = ImageTk.PhotoImage(img)

        # create a label with the image
        render_label = tk.Label(image_window, image=photo)
        render_label.image = photo
        render_label.pack(pady=20)

        # Create a function to handle "Quit" button clicks
        def handle_image_quit_button_click():
            # Close the image window
            image_window.destroy()

            # Show the main window again
            window.deiconify()

        # Create a quit button widget
        image_quit_button = tk.Button(image_window, text="Quit", font=("Arial", 14), command=handle_image_quit_button_click)
        image_quit_button.pack(pady=10)

    # Create a function to handle "Quit" button clicks
    def handle_speak_quit_button_click():
        # Close the speak window
        speak_window.destroy()

        # Show the main window again
        window.deiconify()

    # Create a button widget to quit the current UI window and open the image window
    done_button = tk.Button(speak_window, text="Done", font=("Arial", 14), command=handle_done_button_click)
    done_button.pack(pady=10)

    # Create a quit button widget to go back to the main window
    speak_quit_button = tk.Button(speak_window, text="Quit", font=("Arial", 14), command=handle_speak_quit_button_click)
    speak_quit_button.pack(pady=10)

# Create a button widget
button = tk.Button(window, text="Run", font=("Arial", 14), command=handle_button_click)
button.pack(pady=10)

# Create a quit button widget
quit_button = tk.Button(window, text="Quit", font=("Arial", 14), command=window.withdraw)
quit_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
