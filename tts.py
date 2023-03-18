import tkinter as tk
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
    # Create a new Tkinter window
    speak_window = tk.Toplevel()

    # Set the window title and size
    speak_window.title("Speak Window")
    speak_window.geometry("400x200")

    # Create a label widget to display text
    speak_label = tk.Label(speak_window, text="Speak into the microphone", font=("Arial", 16))
    speak_label.pack(pady=20)
    
    # Take input as speech
    text = sp.speech_to_text()
    
    # Give use that to get input for the other file
    input_text = ds.generate_description(text)
    sentiments = ds.get_sentiments(text)
    
    # Create a function to handle "Done" button clicks
    def handle_done_button_click():
        # Close the speak window
        speak_window.withdraw()

        # Create a new Tkinter window
        image_window = tk.Toplevel()

        # Set the window title and size
        image_window.title("Image Window")
        image_window.geometry("400x200")

        # Create a label widget to display text
        image_label = tk.Label(image_window, text="Here's a rendered image", font=("Arial", 16))
        image_label.pack(pady=20)
        
        # Generate image
        ps.generate_image(input_text, sentiments)

        # Create a quit button widget
        image_quit_button = tk.Button(image_window, text="Quit", font=("Arial", 14), command=image_window.withdraw)
        image_quit_button.pack(pady=10)

    # Create a button widget to quit the current UI window and open the image window
    done_button = tk.Button(speak_window, text="Done", font=("Arial", 14), command=handle_done_button_click)
    done_button.pack(pady=10)

# Create a button widget
button = tk.Button(window, text="Run", font=("Arial", 14), command=handle_button_click)
button.pack(pady=10)

# Create a quit button widget
quit_button = tk.Button(window, text="Quit", font=("Arial", 14), command=window.withdraw)
quit_button.pack(pady=10)

# Start the Tkinter event loop
window.mainloop()
