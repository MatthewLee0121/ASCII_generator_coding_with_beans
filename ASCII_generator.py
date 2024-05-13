###ASCII Image Generator ######
###############################

from PIL import Image  ##used to read Jpeg
import tkinter as tk   #Used for GUI
from tkinter import filedialog #makes selecting files easier
import cv2, os, time  #used in the MP4 conversion
import numpy as np

if __name__ == '__main__':


    ###### Globals and other Variables we can use
    selected_file_path = "" #Globals are bad
    selected_output_path = ""
    
    # ASCII characters arranged by rough density
    ascii_characters_by_density = [
        " ", ".", ",", ":", ";", "i", "!", "|", "1", "t", "f", "L", "I", "(", ")", "[", "]", "{", "}", "r", "c",
        "*", "+", "=", "7", "?", "v", "x", "J", "3", "n", "o", "s", "z", "5", "2", "S", "F", "C", "Z", "U", "O",
        "0", "Q", "8", "9", "V", "Y", "X", "G", "q", "m", "w", "p", "d", "A", "D", "H", "#", "M", "B", "&", "W",
        "E", "%", "6", "k", "R", "P", "N", "T", "4", "K", "E", "U", "h", "y", "b", "g", "j", "@", "^", "a", "u",
        "e", "l", "I", "T", "q", "H", "D", "W", "M", "B", "Q", "G", "N", "O", "Z", "S", "C", "V", "X", "Y", "K",
        "A", "0", "9", "8", "Q", "O", "Z", "C", "V", "S", "X", "Y", "N", "K", "M", "G", "B", "W", "H", "D", "Q",
        "E", "U", "T", "l", "y", "u", "a", "^", "@", "j", "g", "b", "y", "h", "U", "K", "4", "T", "N", "P", "R",
        "k", "6", "%", "E", "W", "B", "M", "#"
    ]

    # Function to get the Mp4 video path
    def get_video_path():
        """Gets a Mp4 File Path When Button Pressed \n
        -----------------------------------------------------------------------------\n
        Keyword Arguments: \n
        None \n
        -----------------------------------------------------------------------------\n
        Variables: \n
        selected_file_path -- Imports the global empty string so we can assign a value \n
        selected_output_path -- Imports the global empty string so we can assign a value \n
        -----------------------------------------------------------------------------\n
        Overview: \n
        Function opens x2 file browsers windows using filedialog 1st to be displayed is to get the video path, \n
        second will get a Jpeg Dump folder
        """
        global selected_file_path, selected_output_path#i know globals are bad but i am sick of trying to work out how to call it in the function without filepath name error
        selected_file_path = filedialog.askopenfilename(filetypes=[("Mp4 Files", "*.mp4;")]) #selects a mp4
        selected_output_path = filedialog.askdirectory() # selects a output jpeg dump folder

    # Function to set the file path
    def get_image_path():
        """Gets the Jpeg image path \n
            -----------------------------------------------------------------------------\n
            Keyword Arguments: \n
            None \n
            -----------------------------------------------------------------------------\n
            Variables: \n
            selected_file_path -- Imports the global empty string so we can assign a value \n
            -----------------------------------------------------------------------------\n
            Overview: \n
            Function opens a file browser using filedialog \n
        """
        global selected_file_path#i know globals are bad but i am sick of trying to work out how to call it in the function without filepath name error
        selected_file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")]) #i honestly dont know how this works thank you internet u the real MPV
        
    # Function to open the file and display ASCII art
    def open_file(font_size_var):
        """Brief overview \n
            -----------------------------------------------------------------------------\n
            Keyword Arguments: \n
            font_size_var -- used within the ASCII label to use the font size selected within the slider. \n
            -----------------------------------------------------------------------------\n
            Variables: \n
            selected_file_path -- Imports the global empty string so we can assign a value \n
            rows -- within this function the global TK variable rows (if y % 1 == 0:) is used to send data to the get ascii_art function \n
            columns -- within this function the global TK variable columns (if x % 1 == 0:) is used to send data to the get ascii_art function \n
            ascii_window -- used to create a window object within tkinter \n
            ascii_label -- creates a label object within tkinter \n
            ascii_art -- stores a string variable returned from get_ascii_art \n
            -----------------------------------------------------------------------------\n
            Overview: \n
            Function first imports the global variables (selected_file_path, rows, columns) \n
            It then enters a if loop for the selected_file_path and creates a new TKinter window titled ASCII Art \n
            Then it sets ascii_art = to the return of get_ascii_art with selected file_path, rows.get() and columns.get() as arguments \n
            .get() is used to use the values returned from the scale slider in the main GUI window \n
            Function then creates a new TKinter label to display the string variable (displaying the art) in the new window \n

        """
        global selected_file_path, rows, columns #i know globals are bad but i am sick of trying to work out how to call it in the function without filepath name error
        if selected_file_path:  # Check if a file path is selected
            # Create a themed Tkinter window for displaying ASCII art
            ascii_window = tk.Tk() #creates the window
            ascii_window.title("ASCII Art") #sets new window title
            
            # Set window size and background color
            ascii_window.geometry("500x300")
            ascii_window.configure(bg="#f0f0f0") #white cos we in testing
            
            # Get ASCII art from the selected image
            ascii_art = get_ascii_art(selected_file_path, rows.get(), columns.get(), line_detection.get())
            
            # Create a label for displaying the ASCII art
            ascii_label = tk.Label(
                ascii_window,
                text=ascii_art,
                font=("Courier New", font_size_var),  # Adjust font size and font family as needed #make this into a setting so i dont need to keep re running app to modify
                bg="#f0f0f0",
                justify="left"  # Adjust justification as needed
            )
            ascii_label.pack(pady=5, padx =5) # gives us 5 pixels

            ascii_window.mainloop()

    def edge_detection(image):
        # Convert the image to grayscale
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Apply Gaussian blur to reduce noise
        blurred_image = cv2.GaussianBlur(gray_image, (3, 3), 0)

        # Apply Sobel operator for edge detection
        sobel_x = cv2.Sobel(blurred_image, cv2.CV_64F, 1, 0, ksize=3)
        sobel_y = cv2.Sobel(blurred_image, cv2.CV_64F, 0, 1, ksize=3)

        # Compute the gradient magnitude
        gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

        # Normalize the gradient magnitude to 0-255
        gradient_magnitude *= 255.0 / gradient_magnitude.max()

        # Convert the gradient magnitude to uint8
        gradient_magnitude = np.uint8(gradient_magnitude)

        return gradient_magnitude

    # Function to generate art
    def get_ascii_art(image_path, rows, columns, line_detection):
        """Reads a Jpeg and converts it to ASCII art \n
        ----------------------------------------------------------------------------- \n
        Keyword Arguments: \n
        image_path -- the path to the file we are going to convert \n
        rows -- Sets how many rows we should read using x % rows to vary \n
        columns -- Sets how many columns we should read using y % columns to vary \n
        ----------------------------------------------------------------------------- \n
        Variables: \n
        img -- The image \n
        Pixels -- pixel data from img.load() \n
        Width -- The amount of pixels in each row \n
        height -- The amount of pixels in each column \n
        ascii_art -- variable to store the converted image \n
        min_brightness -- sets the minimum brightness value in our range \n
        max_brightness -- sets the maximum brightness value in our range \n
        ----------------------------------------------------------------------------- \n
        Overview: \n
        Function takes an image, stores it as img variable. \n
        Function then converts image to greyscale and loads pixel data. \n
        Function then gets the Image width and height and creates an empty string variable and 2 integers variables \n
        Set the min the to height value and the max to the lowest value as when we iterate though we will call min() and max() on them \n
        \n
        Function now begins to create the Art the For loop first says every time we encounter a new Y value the string needs to print a new line \n
        Next for loop takes the value for brightness and maps each value to a index value inbetween the Len() of how every many characters we are using \n
        Finally the loop append the ASCII character to the ascii_art variable and returns the string after the loop.
        """
        if line_detection == True:
            image = cv2.imread(image_path)
            img = edge_detection(image)
            img = Image.fromarray(img)

        else:
            img = Image.open(image_path)

        # Load the image
        #img = Image.open(image_path)

        # Convert the image to grayscale mode
        img = img.convert("L")

        # Get pixel data
        pixels = img.load()

        # Get the size of the image
        width, height = img.size
        #sets empty string variable
        ascii_art = ""
        min_brightness = 256 #max brighness for jpeg is 255
        max_brightness = 0 #min brightness on jpeg is 0
        #had to make 2 forloops for dynamic brightness values 
        for y in range(height):
            if y % 1 == 0:  #can be modified to exclude data not recommended unless you need to try reduce the minimum and maximum values some with the dynamic brightness index will be a more optimised version
                for x in range(width):
                    if x % 1 == 0: #can be modified to exclude data not recommended unless you need to try reduce the minimum and maximum values some with the dynamic brightness index will be a more optimised version
                        brightness = pixels[x, y]
                        min_brightness = min(brightness, min_brightness)#This for loop will get me minimum and max brightness values from the range of data within the pixels
                        max_brightness = max(brightness, max_brightness)# can then utalise this information in the next for loop to dynamically set ASCII characters
        
        for y in range(height):
            if y % rows == 0: #if i change this it will exclude the height row % 3 will take every 3rd row ETC
                ascii_art += "\n" #adds a new line to the string whenever we hit a new Y coordinate char
                for x in range(width):
                    if x % columns == 0: #if i change this it will exclude the width row % 3 will take every 3rd row ETC
                        # converted image to greyscale with (img = img.convert("L")) this means we no longer have to work on RGB channels and only work on brightness values
                        brightness = pixels[x, y]
                        # Calculate the brightness index in a dynamic way so every image has different brightness values, this calculates the range and gets us representative values convert to int to get approimation we can only have 155 values as a max
                        brightness_index = int(((brightness - min_brightness) / (max_brightness - min_brightness)) * (len(ascii_characters_by_density) - 1))
                        # Append the corresponding ASCII character to the ASCII art string
                        ascii_art += ascii_characters_by_density[brightness_index]
        #returns completed string
        return ascii_art
    
    #Function to swap Mp4 into Jpegs and convert
    def mp4_to_jpeg():
        """Read the mp4 convert each frame into a jpeg and then ASCII, deletes the jpeg and stores the ascii \n
        -----------------------------------------------------------------------------\n
        Keyword Arguments: \n
         None \n
        -----------------------------------------------------------------------------\n
        Variables: \n
         selected_file_path -- Imports the global empty string so we can assign a value \n
         selected_output_path -- Imports the global empty string so we can assign a value \n
         variable -- explination \n
         variable -- explination \n
         variable -- explination \n
         variable -- explination \n
         variable -- explination \n
         variable -- explination \n
         variable -- explination \n
        -----------------------------------------------------------------------------\n
        Overview: \n
         Detail function behaviour \n
        """
        global selected_file_path, selected_output_path 
        cap = cv2.VideoCapture(selected_file_path)
        frame_count = 0
        ascii_art_list = []  # List to store ASCII art for each frame

        while True:
            try:
                ret, frame = cap.read() #if ret is true then frame was successful if its false we have an error or end of video

                if not ret: # ends loop on error or end of video
                    print("End of video or error has occurred")
                    break

                jpeg_filename = f"{selected_output_path}/frame_{frame_count:044}.jpg"
                cv2.imwrite(jpeg_filename, frame) #sets a new jpeg file in the dump folder for the frame

                # Get ASCII art for the saved frame and append it to the list
                ascii_art = get_ascii_art(jpeg_filename, rows.get(), columns.get(), line_detection.get())
                ascii_art_list.append(ascii_art)

                # Delete the file after obtaining ASCII art
                os.remove(jpeg_filename)

                frame_count += 1

            except Exception as e:
                print("Error:", e)

        cap.release()
        
        jpeg_to_string(ascii_art_list)

    

    def play_video(ascii_label, ascii_art_list):
        i = 0
        while True:  # Loop indefinitely
            time.sleep(0.03334)
            ascii_label.config(text=ascii_art_list[i])
            ascii_label.update()
            i = (i + 1) % len(ascii_art_list)  # Loop back to the beginning if end is reached

    def jpeg_to_string(ascii_art_list):
        ascii_video_window = tk.Tk()  # creates the window
        ascii_video_window.title("ASCII Art")  # sets new window title

        # Set window size and background color
        ascii_video_window.geometry("1000x600")
        ascii_video_window.configure(bg="#f0f0f0")  # white because we are testing

        # Get ASCII art from the selected image
        font_size = font_size_var.get()

        # Create a label for displaying the ASCII art
        ascii_label = tk.Label(
            ascii_video_window,
            text=ascii_art_list[0],
            font=("Courier New", font_size),  # Adjust font size and font family as needed
            bg="#f0f0f0",
            justify="left"  # Adjust justification as needed
        )
        ascii_label.grid(row=0, column=9, pady=5, padx=5)  # Place label in the first row, first column

        play_video_button = tk.Button(
            ascii_video_window,
            text="Play Video",
            font=("Rockabilly", 10),
            command=lambda: play_video(ascii_label, ascii_art_list),  # Pass the function reference
            width=20,
            height=2
        )
        play_video_button.grid(row=0, column=10, pady=20, padx=10) # Place button in the first row, second column

        ascii_video_window.mainloop()


         

    def create_main(open_file_command, mp4_to_jpeg_command, get_image_path_command, get_video_path_command):
        """Brief overview \n
            -----------------------------------------------------------------------------\n
            Keyword Arguments: \n
            keyword -- explination \n
            -----------------------------------------------------------------------------\n
            Variables: \n
            variable -- explination \n
            -----------------------------------------------------------------------------\n
            Overview: \n
            Detail function behaviour \n
        """
        #create the main window of the GUI
        main_window = tk.Tk()
        main_window.title("Settings for your generation!")
        main_window.geometry("400x600")
        main_window.configure(bg="#f0f0f0")

        # Create the generate artwork button
        get_art_button = tk.Button(
            main_window,
            text="Generate artwork",
            font=("Rockabilly", 10),
            command=lambda: open_file_command(font_size_var.get()),
            width=20,
            height=2
        )
        get_art_button.pack(pady=10)

        # Create the generate ASCII video button
        get_video_button = tk.Button(
            main_window,
            text="Generate ASCII video",
            font=("Rockabilly", 10),
            command=mp4_to_jpeg_command,
            width=20,
            height=2
        )
        get_video_button.pack(pady=20)

        # Create the select image button
        get_image_path_button = tk.Button(
            main_window,
            text="Select image",
            font=("Rockabilly", 10),
            command=get_image_path_command,
            width=20,
            height=2
        )
        get_image_path_button.pack(pady=10)

        # Create the select mp4 button
        get_video_path_button = tk.Button(
            main_window,
            text="Select Mp4",
            font=("Rockabilly", 10),
            command=get_video_path_command,
            width=20,
            height=2
        )
        get_video_path_button.pack(pady=20)

        # GUI variables
        font_size_var = tk.IntVar(value=1)
        rows = tk.IntVar(value=1)
        columns = tk.IntVar(value=1)
        line_detection = tk.IntVar()

        # Create font size scale
        font_size_scale = tk.Scale(
            main_window,
            from_=1,
            to=20,
            orient=tk.HORIZONTAL,
            variable=font_size_var,
            label="Font Size"
        )
        font_size_scale.pack(pady=10)

        # Create rows scale
        rows_scale = tk.Scale(
            main_window,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=rows,
            label="Adjust Y Scaling"
        )
        rows_scale.pack(pady=10)

        # Create columns scale
        columns_scale = tk.Scale(
            main_window,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            variable=columns,
            label="Adjust X Scaling"
        )
        columns_scale.pack(pady=10)

        LineDetection_box = tk.Checkbutton(
            main_window,
            text= 'Line Detection?(untick for mp4)',
            variable= line_detection,
            onvalue= True,
            offvalue= False,
        )
        LineDetection_box.pack(pady=10)

        # Return the main window
        return main_window, font_size_var, columns, rows, line_detection

    #creates the main window
    main_window, font_size_var, columns, rows, line_detection = create_main(open_file, mp4_to_jpeg, get_image_path, get_video_path)

    # Start the Tkinter event loop
    main_window.mainloop()
