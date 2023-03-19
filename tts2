import tkinter as tk

# create the main window
root = tk.Tk()

# set the window title
root.title("The Visualizer")

# set the window size
root.geometry("300x200")

# create a label with the welcome message
welcome_label = tk.Label(root, text="Welcome to The Visualizer")
welcome_label.pack(pady=20)

# create a frame to hold the buttons
button_frame = tk.Frame(root)
button_frame.pack(pady=10)

# function to open a new window for microphone prompt
def open_mic_window():
    # create a new window
    mic_window = tk.Toplevel(root)

    # set the window title
    mic_window.title("Microphone Visualizer")

    # set the window size
    mic_window.geometry("300x200")

    # create a label with the microphone prompt
    mic_label = tk.Label(mic_window, text="Speak into the microphone")
    mic_label.pack(pady=20)

    # function to click the "done" button
    def click_done():
        done_button.invoke()
        
        # create a "done" button to close the window and open a new window
    def done_button_click():
    
        def render_window():
            new_window = tk.Toplevel(root)
            new_window.title("Rendered Image")
            new_window.geometry("300x200")
            render_label = tk.Label(new_window, text="Here's a rendered image")
            render_label.pack(pady=20)
            done_button = tk.Button(new_window, text="Done", command=new_window.destroy)
            done_button.pack(pady=10)
        mic_window.withdraw()
        new_window = tk.Toplevel(root)
        new_window.title("Repeat Prompt")
        new_window.geometry("300x200")
        txt = "Penis enlargement pills"
        repeat_label = tk.Label(new_window, text="Here's what you said:\n" + txt + "\n\nDo you want to speak again?")
        repeat_label.pack(pady=20)
        repeat_button_frame = tk.Frame(new_window)
        repeat_button_frame.pack(pady=10)
        yes_button = tk.Button(repeat_button_frame, text="Yes", command=lambda: [new_window.destroy(), mic_window.deiconify()])
        yes_button.pack(side="left", padx=10)
        no_button = tk.Button(repeat_button_frame, text="No", command=lambda: [new_window.destroy(), render_window()])
        no_button.pack(side="left", padx=10)


    done_button = tk.Button(mic_window, text="Done", command=done_button_click)
    done_button.pack(pady=10)

    # schedule automatic click of "Done" button after 6 seconds
    mic_window.after(6000, click_done)

# create the "Run" button
run_button = tk.Button(button_frame, text="Run", command=open_mic_window)
run_button.pack(side="left", padx=10)

# create the "Quit" button
quit_button = tk.Button(button_frame, text="Quit", command=root.withdraw)
quit_button.pack(side="left", padx=10)

# run the main loop
root.mainloop()
