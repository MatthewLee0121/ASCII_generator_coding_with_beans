from PIL import Image
import tkinter as tk
from tkinter import filedialog, ttk, font

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
#'function to generate the are
def get_ascii_art(image_path):
    # Load the image
    img = Image.open(image_path)

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
        if y % 1 == 0:  #can be modified to exclude data not recommended unless you need to try reduce the minimum and maximum values some fucking with the dynamic brightness index will be a more optimised version
            for x in range(width):
                if x % 1 == 0: #can be modified to exclude data not recommended unless you need to try reduce the minimum and maximum values some fucking with the dynamic brightness index will be a more optimised version
                    brightness = pixels[x, y]
                    min_brightness = min(brightness, min_brightness)#This for loop will get me minimum and max brightness values from the range of data within the pixels
                    max_brightness = max(brightness, max_brightness)# can then utalise this information in the next for loop to dynamically set ASCII characters

    for y in range(height):
        if y % 1 == 0: #if i change this it will exclude the height row % 3 will take every 3rd row ETC
            ascii_art += "\n" #adds a new line to the string whenever we hit a new Y coordinate char
            for x in range(width):
                if x % 1 == 0: #if i change this it will exclude the width row % 3 will take every 3rd row ETC
                    # converted image to greyscale with (img = img.convert("L")) this means we no longer have to work on RGB channels and only work on brightness values
                    brightness = pixels[x, y]
                    # Calculate the brightness index in a dynamic way so every image has different brightness values, this calculates the range and gets us representative values convert to int to get approimation we can only have 155 values as a max
                    brightness_index = int(((brightness - min_brightness) / (max_brightness - min_brightness)) * (len(ascii_characters_by_density) - 1))
                    # Append the corresponding ASCII character to the ASCII art string
                    ascii_art += ascii_characters_by_density[brightness_index]
    #returns completed string
    return ascii_art
#function for GUI to open the file
def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.jpg;*.jpeg;*.gif")])
    if file_path: #if theres a file path then execute
        # Create a themed Tkinter window for displaying ASCII art
        ascii_window = tk.Tk() #creates the window
        ascii_window.title("ASCII Art") #sets new window title
        
        # Set window size and background color
        ascii_window.geometry("500x300")
        ascii_window.configure(bg="#f0f0f0") #white cos we in testing
        
        # Get ASCII art from the selected image
        ascii_art = get_ascii_art(file_path)
        
        # Create a label for displaying the ASCII art
        ascii_label = tk.Label(
            ascii_window,
            text=ascii_art,
            font=("Courier New", 2),  # Adjust font size and font family as needed #make this into a setting so i dont need to keep re running app to modify
            bg="#f0f0f0",
            justify="left"  # Adjust justification as needed
        )
        ascii_label.pack(pady=5, padx =5) # gives us 5 pixels
        
        ascii_window.mainloop()

# Create a themed Tkinter window for selecting an image file
main_window = tk.Tk()
main_window.title("Settings for your generation!")

# Set window size and background color
main_window.geometry("200x100")
main_window.configure(bg="#f0f0f0")

# Create a button for selecting an image file
get_art_button = tk.Button(
    main_window,
    text="Generate image",
    font=("Rockabilly", 10),
    command=open_file,
    width=20,  
    height=2
)
get_art_button.pack(pady=10)

#starts the main loop of the main GUI window
main_window.mainloop()








































# file_path_button.pack(pady=10)
# # def change_font():
#     selected_font = font_var.get()
#     text_label.config(font=(selected_font, font_size_var.get()))
#     font_preview_label.config(text=f"Font Preview: {selected_font}")

# # Tkinter UI setup
# main_window = tk.Tk()
# main_window.title("Font Example")

# # Create a variable to store the selected font
# font_var = tk.StringVar()
# font_var.set("Arial")

# # Create a variable to store the font size
# font_size_var = tk.IntVar()
# font_size_var.set(12)

# # Updated list of fonts
# font_list = ["System", "Terminal", "Fixedsys", "Modern", "Roman", "Script", "Courier", "MS Serif", "MS Sans Serif",
#              "Small Fonts", "Marlett", "Arial", "Arabic Transparent", "Arial Baltic", "Arial CE", "Arial CYR",
#              "Arial Greek", "Arial TUR", "Arial Black", "Bahnschrift Light", "Bahnschrift SemiLight", "Bahnschrift",
#              "Bahnschrift SemiBold", "Bahnschrift Light SemiCondensed", "Bahnschrift SemiLight SemiConde", "Bahnschrift SemiCondensed",
#              "Bahnschrift SemiBold SemiConden", "Bahnschrift Light Condensed", "Bahnschrift SemiLight Condensed",
#              "Bahnschrift Condensed", "Bahnschrift SemiBold Condensed", "Calibri", "Calibri Light", "Cambria", "Cambria Math",
#              "Candara", "Candara Light", "Comic Sans MS", "Consolas", "Constantia", "Corbel", "Corbel Light", "Courier New",
#              "Courier New Baltic", "Courier New CE", "Courier New CYR", "Courier New Greek", "Courier New TUR", "Ebrima",
#              "Franklin Gothic Medium", "Gabriola", "Gadugi", "Georgia", "Impact", "Ink Free", "Javanese Text", "Leelawadee UI",
#              "Leelawadee UI Semilight", "Lucida Console", "Lucida Sans Unicode", "Malgun Gothic", "Malgun Gothic Semilight",
#              "Microsoft Himalaya", "Microsoft JhengHei", "Microsoft JhengHei UI", "Microsoft JhengHei Light",
#              "Microsoft JhengHei UI Light", "Microsoft New Tai Lue", "Microsoft PhagsPa", "Microsoft Sans Serif",
#              "Microsoft Tai Le", "Microsoft YaHei", "Microsoft YaHei UI", "Microsoft YaHei Light", "Microsoft YaHei UI Light",
#              "Microsoft Yi Baiti", "MingLiU-ExtB", "PMingLiU-ExtB", "MingLiU_HKSCS-ExtB", "Mongolian Baiti", "MS Gothic",
#              "MS UI Gothic", "MS PGothic", "MV Boli", "Myanmar Text", "Nirmala UI", "Nirmala UI Semilight", "Palatino Linotype",
#              "Sans Serif Collection", "Segoe Fluent Icons", "Segoe MDL2 Assets", "Segoe Print", "Segoe Script", "Segoe UI",
#              "Segoe UI Black", "Segoe UI Emoji", "Segoe UI Historic", "Segoe UI Light", "Segoe UI Semibold", "Segoe UI Semilight",
#              "Segoe UI Symbol", "Segoe UI Variable Small Light", "Segoe UI Variable Small Semilig", "Segoe UI Variable Small",
#              "Segoe UI Variable Small Semibold", "Segoe UI Variable Text Light", "Segoe UI Variable Text Semiligh",
#              "Segoe UI Variable Text", "Segoe UI Variable Text Semibold", "Segoe UI Variable Display Light",
#              "Segoe UI Variable Display Semil", "Segoe UI Variable Display", "Segoe UI Variable Display Semibold", "SimSun",
#              "NSimSun", "SimSun-ExtB", "Sitka Small", "Sitka Small Semibold", "Sitka Text", "Sitka Text Semibold",
#              "Sitka Subheading", "Sitka Subheading Semibold", "Sitka Heading", "Sitka Heading Semibold", "Sitka Display",
#              "Sitka Display Semibold", "Sitka Banner", "Sitka Banner Semibold", "Sylfaen", "Symbol", "Tahoma", "Times New Roman",
#              "Times New Roman Baltic", "Times New Roman CE", "Times New Roman CYR", "Times New Roman Greek", "Times New Roman TUR",
#              "Trebuchet MS", "Verdana", "Webdings", "Wingdings", "Yu Gothic", "Yu Gothic UI", "Yu Gothic UI Semibold",
#              "Yu Gothic Light", "Yu Gothic UI Light", "Rockybilly"]  # Add your new fonts here

# # Create a style for the font menu to set the item font
# font_menu_style = ttk.Style()
# font_menu_style.configure("FontMenu.TMenubutton", font=("Arial", 12))

# # Option menu for font selection with a scrollbar
# font_menu = ttk.Combobox(main_window, textvariable=font_var, values=font_list, style="FontMenu.TMenubutton", state="readonly")
# font_menu.pack(pady=10)

# # Font preview label
# font_preview_label = tk.Label(main_window, text="Font Preview: Arial", font=("Arial", 12))
# font_preview_label.pack(pady=10)

# # Scale widget for font size
# font_size_scale = tk.Scale(main_window, from_=8, to=24, orient=tk.HORIZONTAL, variable=font_size_var, label="Font Size")
# font_size_scale.pack(pady=10)

# # Button to apply font changes
# apply_button = tk.Button(main_window, text="Apply Font", command=change_font, font=("Rockybilly", 5))
# apply_button.pack(pady=10)

# # Label to demonstrate the selected font
# text_label = tk.Label(main_window, text="ABCDEFGHIKLMNOPQRSTUVWXYZ \n abcdefghijklmnopqrstwxyz", font=("Arial", 12))
# text_label.pack(pady=10)

main_window.mainloop()

    