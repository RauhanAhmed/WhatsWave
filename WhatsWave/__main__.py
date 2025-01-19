from tkinter import filedialog, messagebox
from ai_rewrite import rewrite_message
import customtkinter as ctk
import pywhatkit as pwk
from PIL import Image
import tkinter as tk
import pandas as pd
import phonenumbers
import keyboard
import os
import sys

# Get the application directory
def resource_path(relative_path):
    # For PyInstaller
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

# Use the resource path for the icon
class Theme:
    COLORS = {
        'bg': '#1E293B',          # Cool dark blue-gray for the background
        'card': '#334155',        # Soft slate blue for cards
        'accent': '#4F46E5',      # Vibrant indigo for accents
        'text': '#F8FAFC',        # Very light gray for primary text
        'text_secondary': '#CBD5E1', # Muted gray for secondary text
        'border': '#475569',      # Subtle gray for borders
        'hover': '#3B82F6',       # Soft blue for hover states
        'success': '#10B981',     # Lush green for success
        'error': '#F43F5E',       # Warm red for errors
        'tab_active': '#1E40AF',  # Deep blue for active tabs
        'tab_inactive': '#64748B' # Neutral slate for inactive tabs
    }
    
    FONTS = {
        'heading': ('Inter', 23, 'bold'),     # Slightly larger for headings
        'subheading': ('Inter', 19, 'bold'),
        'body': ('Inter', 17),                # Increased body font for better readability
        'small': ('Inter', 15),
        'label': ('Inter', 17, 'bold')        # Clear font for form labels
    }
class WhatsWave:
    def __init__(self):
        self.root = ctk.CTk()
        self.root.title("WhatsWave")
        self.root.geometry("800x750")
        self.root.iconbitmap(resource_path("logo.ico"))
        self.root.configure(bg=Theme.COLORS['bg'])
        
        # Appearance Mode and Color Theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_widgets()

    def create_widgets(self):
        # Main Frame
        main_frame = ctk.CTkFrame(
            self.root,
            fg_color=Theme.COLORS['bg'],
            corner_radius=12
        )
        main_frame.pack(padx=30, pady=30, fill='both', expand=True)

        # Title Label
        title_label = ctk.CTkLabel(
            main_frame,
            text="WhatsWave: Connect Smarter, Not Harder.",
            font=Theme.FONTS['heading'],
            text_color=Theme.COLORS['text']
        )
        title_label.pack(pady=(0, 30))

        # Tab View
        self.tabview = ctk.CTkTabview(
            main_frame,
            fg_color=Theme.COLORS['card'],
            segmented_button_fg_color=Theme.COLORS['tab_inactive'],
            segmented_button_selected_color=Theme.COLORS['tab_active'],
            segmented_button_unselected_color=Theme.COLORS['tab_inactive'],
        )
        self.tabview.pack(fill='both', expand=True, padx=15, pady=10)

        # Add Tabs
        self.tab_text = self.tabview.add("Text Message")
        self.tab_image = self.tabview.add("Message with Image")
        self.tab_ai_rewrite = self.tabview.add("AI Message Generator")
        self.tab_tool_usage = self.tabview.add("Tool Usage Points")
        
        # Create Tab Content
        self.create_tool_usage_tab()
        self.create_text_tab()
        self.create_image_tab()
        self.create_ai_rewrite_tab()


    def create_text_tab(self):
        # Create a scrollable frame for the tab
        scroll_frame = ctk.CTkScrollableFrame(
            self.tab_text,
            fg_color=Theme.COLORS['bg'],
            corner_radius=12,
            scrollbar_button_hover_color=Theme.COLORS['hover'],
            scrollbar_button_color=Theme.COLORS['card']
        )
        scroll_frame.pack(fill='both', expand=True, padx=15, pady=10)
        
        # Message Card
        message_card = ctk.CTkFrame(
            scroll_frame,
            fg_color=Theme.COLORS['card'],
            corner_radius=12
        )
        message_card.pack(fill='x', expand=True, padx=15, pady=15)

        # Message Label
        message_label = ctk.CTkLabel(
            message_card,
            text="Message Content",
            font=Theme.FONTS['label'],
            text_color=Theme.COLORS['text']
        )
        message_label.pack(padx=15, pady=(15, 5), anchor='w')
        
        # Message Input
        self.text_message_input = ctk.CTkTextbox(
            message_card,
            height=150,
            corner_radius=8,
            border_width=1,
            border_color=Theme.COLORS['border'],
            fg_color=Theme.COLORS['card']
        )
        self.text_message_input.pack(padx=15, pady=(0, 15), fill='x')

        # Personalization Tip
        tip_label = ctk.CTkLabel(
            message_card,
            text="Use {name} to personalize messages with names from your data",
            font=Theme.FONTS['small'],
            text_color=Theme.COLORS['text_secondary']
        )
        tip_label.pack(padx=15, pady=(0, 20))
        
        # Default Name Label
        name_label = ctk.CTkLabel(
            message_card,
            text="Default Name",
            font=Theme.FONTS['label'],
            text_color=Theme.COLORS['text']
        )
        name_label.pack(padx=15, pady=(0, 5), anchor='w')

        # Default Name Input
        self.text_default_name = ctk.CTkEntry(
            message_card,
            placeholder_text="Enter default name",
            corner_radius=6,
            border_width=1,
            border_color=Theme.COLORS['border'],
            fg_color=Theme.COLORS['card'],
            height=35  
        )
        self.text_default_name.pack(padx=15, pady=(0, 20), fill='x')
        self.text_default_name.insert(0, "Customer")

        # CSV File Label
        csv_label = ctk.CTkLabel(
            message_card,
            text="CSV File",
            font=Theme.FONTS['label'],
            text_color=Theme.COLORS['text']
        )
        csv_label.pack(padx=15, pady=(0, 5), anchor='w')
        
        # CSV Upload Frame
        self.text_csv_path_var = tk.StringVar()
        csv_frame = ctk.CTkFrame(
            message_card,
            fg_color="transparent"
        )
        csv_frame.pack(padx=15, pady=(0, 20), fill='x')
        
        csv_entry = ctk.CTkEntry(
            csv_frame,
            textvariable=self.text_csv_path_var,
            corner_radius=6,
            border_width=1,
            border_color=Theme.COLORS['border'],
            fg_color=Theme.COLORS['card'],
            height=35
        )
        csv_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
        
        csv_button = ctk.CTkButton(
            csv_frame,
            text="Browse",
            font = Theme.FONTS["body"],
            width=100,
            corner_radius=6,
            command=lambda: self.browse_file(
                self.text_csv_path_var,
                [("CSV files", "*.csv")]
            ),
            fg_color=Theme.COLORS['accent'],
            hover_color=Theme.COLORS['hover']
        )
        csv_button.pack(side='right')
        
        # Send Button
        send_button = ctk.CTkButton(
            message_card,
            text="Send Messages",
            font=Theme.FONTS['body'],
            corner_radius=6,
            command=lambda: self.send_messages(with_image=False),
            fg_color="#D50032",
            hover_color=Theme.COLORS['hover'],
            height=40
        )
        send_button.pack(pady=(0, 20))

    def create_image_tab(self):
            # Create a scrollable frame container
            scrollable_frame = ctk.CTkScrollableFrame(
                self.tab_image,
                fg_color=Theme.COLORS['bg'],
                corner_radius=12
            )
            scrollable_frame.pack(fill='both', expand=True)
            
            # Create message card inside scrollable frame
            message_card = self.create_card(scrollable_frame, "Compose Message with Image")
            message_card.pack(padx=15, pady=15, fill='both', expand=True)
            
            # Message Label
            message_label = ctk.CTkLabel(
                message_card,
                text="Message Content",
                font=Theme.FONTS['label'],
                text_color=Theme.COLORS['text']
            )
            message_label.pack(padx=15, pady=(15, 5), anchor='w')
            
            # Message Input
            self.image_message_input = ctk.CTkTextbox(
                message_card,
                height=150,
                corner_radius=8,
                border_width=1,
                border_color=Theme.COLORS['border'],
                fg_color=Theme.COLORS['card']
            )
            self.image_message_input.pack(padx=15, pady=(0, 20), fill='x')

            # Personalization Tip
            tip_label = ctk.CTkLabel(
                message_card,
                text="Use {name} to personalize messages with names from your data",
                font=Theme.FONTS['small'],
                text_color=Theme.COLORS['text_secondary']
            )
            tip_label.pack(padx=15, pady=(0, 20))
        
            
            # Default Name Label
            name_label = ctk.CTkLabel(
                message_card,
                text="Default Name",
                font=Theme.FONTS['label'],
                text_color=Theme.COLORS['text']
            )
            name_label.pack(padx=15, pady=(0, 5), anchor='w')
            
            # Default Name Input
            self.image_default_name = ctk.CTkEntry(
                message_card,
                placeholder_text="Enter default name",
                corner_radius=6,
                border_width=1,
                border_color=Theme.COLORS['border'],
                fg_color=Theme.COLORS['card'],
                height=35
            )
            self.image_default_name.pack(padx=15, pady=(0, 20), fill='x')
            self.image_default_name.insert(0, "Customer")
            
            # Image Upload Label
            image_label = ctk.CTkLabel(
                message_card,
                text="Image File",
                font=Theme.FONTS['label'],
                text_color=Theme.COLORS['text']
            )
            image_label.pack(padx=15, pady=(0, 5), anchor='w')
            
            # Image Upload Frame
            self.image_path_var = tk.StringVar()
            image_frame = ctk.CTkFrame(
                message_card,
                fg_color="transparent"
            )
            image_frame.pack(padx=15, pady=(0, 20), fill='x')
            
            image_entry = ctk.CTkEntry(
                image_frame,
                textvariable=self.image_path_var,
                corner_radius=6,
                border_width=1,
                border_color=Theme.COLORS['border'],
                fg_color=Theme.COLORS['card'],
                height=35
            )
            image_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            image_button = ctk.CTkButton(
                image_frame,
                text="Browse",
                width=100,
                font = Theme.FONTS["body"],
                corner_radius=6,
                command=lambda: self.browse_file(
                    self.image_path_var,
                    [("Image files", "*.png *.jpg *.jpeg *.gif *.bmp")]
                ),
                fg_color=Theme.COLORS['accent'],
                hover_color=Theme.COLORS['hover']
            )
            image_button.pack(side='right')
            
            # Image Preview Section
            preview_label = ctk.CTkLabel(
                message_card,
                text="Image Preview",
                font=Theme.FONTS['label'],
                text_color=Theme.COLORS['text']
            )
            preview_label.pack(padx=15, pady=(0, 5), anchor='w')
            
            self.image_preview_label = ctk.CTkLabel(
                message_card,
                text="No image selected",
                font=Theme.FONTS['body'],
                text_color=Theme.COLORS['text_secondary']
            )
            self.image_preview_label.pack(pady=(0, 20))
            
            # CSV File Label
            csv_label = ctk.CTkLabel(
                message_card,
                text="CSV File",
                font=Theme.FONTS['label'],
                text_color=Theme.COLORS['text']
            )
            csv_label.pack(padx=15, pady=(0, 5), anchor='w')
            
            # CSV Upload Frame
            self.image_csv_path_var = tk.StringVar()
            csv_frame = ctk.CTkFrame(
                message_card,
                fg_color="transparent"
            )
            csv_frame.pack(padx=15, pady=(0, 20), fill='x')
            
            csv_entry = ctk.CTkEntry(
                csv_frame,
                textvariable=self.image_csv_path_var,
                corner_radius=6,
                border_width=1,
                border_color=Theme.COLORS['border'],
                fg_color=Theme.COLORS['card'],
                height=35
            )
            csv_entry.pack(side='left', fill='x', expand=True, padx=(0, 10))
            
            csv_button = ctk.CTkButton(
                csv_frame,
                text="Browse",
                font = Theme.FONTS["body"],
                width=100,
                corner_radius=6,
                command=lambda: self.browse_file(
                    self.image_csv_path_var,
                    [("CSV files", "*.csv")]
                ),
                fg_color=Theme.COLORS['accent'],
                hover_color=Theme.COLORS['hover']
            )
            csv_button.pack(side='right')
            
            # Send Button
            send_button = ctk.CTkButton(
                message_card,
                text="Send Messages",
                font=Theme.FONTS['body'],
                corner_radius=6,
                command=lambda: self.send_messages(with_image=True),
                fg_color="#D50032",
                hover_color=Theme.COLORS['hover'],
                height=40
            )
            send_button.pack(pady=(0, 20))

    def create_ai_rewrite_tab(self):
        # Create message card for AI Rewrite
        rewrite_card = self.create_card(self.tab_ai_rewrite, "Rewrite Your Message")
        
        # Input text box for the base message
        base_message_label = ctk.CTkLabel(
            rewrite_card,
            text="Base Message:",
            font=Theme.FONTS['body'],
            text_color=Theme.COLORS['text']
        )
        base_message_label.pack(anchor='w', padx=15, pady=(10, 5))
        
        self.base_message_input = ctk.CTkTextbox(
            rewrite_card,
            height=100,
            corner_radius=8,
            border_width=1,
            border_color=Theme.COLORS['border'],
            fg_color=Theme.COLORS['card']
        )
        self.base_message_input.pack(padx=15, pady=(0, 15), fill='x')
        
        # Input text field for use case description
        use_case_label = ctk.CTkLabel(
            rewrite_card,
            text="Use Case (Describe the audience, tone, purpose, etc.):",
            font=Theme.FONTS['body'],
            text_color=Theme.COLORS['text']
        )
        use_case_label.pack(anchor='w', padx=15, pady=(0, 5))
        
        self.use_case_input = ctk.CTkEntry(
            rewrite_card,
            placeholder_text="E.g.: Send a personalized greeting message to clients for the New Year.",
            corner_radius=8,
            border_width=1,
            border_color=Theme.COLORS['border'],
            fg_color=Theme.COLORS['card']
        )
        self.use_case_input.pack(padx=15, pady=(0, 15), fill='x')
        
        # Output text box for the rewritten message
        output_message_label = ctk.CTkLabel(
            rewrite_card,
            text="Rewritten Message:",
            font=Theme.FONTS['body'],
            text_color=Theme.COLORS['text']
        )
        output_message_label.pack(anchor='w', padx=15, pady=(0, 5))
        
        self.output_message_display = ctk.CTkTextbox(
            rewrite_card,
            height=100,
            corner_radius=8,
            border_width=1,
            border_color=Theme.COLORS['border'],
            fg_color=Theme.COLORS['card'],
            state='disabled'
        )
        self.output_message_display.pack(padx=15, pady=(0, 20), fill='x')
        
        # Generate button for AI message rewrite
        generate_button = ctk.CTkButton(
            rewrite_card,
            text="Generate",
            font=Theme.FONTS['body'],
            corner_radius=6,
            command=self.generate_ai_rewrite,
            fg_color="#D50032",
            hover_color=Theme.COLORS['hover']
        )
        generate_button.pack(pady=(10, 15))

    def create_tool_usage_tab(self):
        info_card = self.create_card(self.tab_tool_usage, "CSV File Format and Usage Instructions")

        # Information Content
        instructions = (
            "Instructions for Using the Tool:\n"
            "- Only files with the '.csv' extension are supported.\n"
            "- Ensure your CSV file follows this format:\n\n"
            "  Column 1: Phone Number without country code\n"
            "  Column 2: Name\n"
            "  Column 3: Country Code (e.g., 'IN' for India)\n\n"
            "Example:\n"
            "  1234567890,John Doe,IN\n"
            "  2071838750,Jane Smith,GB\n\n"
            "Please ensure the data is clean and formatted correctly for optimal performance.\n\n"
            "\n\n\n~ An application by "
        )

        # Creating label for instructions
        info_label = ctk.CTkLabel(
            info_card,
            text=instructions,
            font=Theme.FONTS['body'],
            text_color=Theme.COLORS['text'],
            justify='left',
            wraplength=700  # Adjust wrap length for better readability
        )
        info_label.pack(padx=15, pady=10, anchor='w')

        # Adding hyperlink
        def open_link(event=None):
            import webbrowser
            webbrowser.open("https://rauhanahmed.org")

        # Hyperlink label
        hyperlink_label = ctk.CTkLabel(
            info_card,
            text="Rauhan Ahmed Siddiqui",
            font=("Inter", 17, "underline"),
            cursor="hand2"
        )
        hyperlink_label.pack(padx=15, pady=5, anchor='w')
        hyperlink_label.bind("<Button-1>", open_link)


    def create_card(self, parent, title):
        card = ctk.CTkFrame(
            parent,
            corner_radius=12,
            fg_color=Theme.COLORS['card'],
            border_width=1,
            border_color=Theme.COLORS['border']
        )
        card.pack(padx=20, pady=10, fill='x')
        
        title_label = ctk.CTkLabel(
            card,
            text=title,
            font=Theme.FONTS['subheading'],
            text_color=Theme.COLORS['text']
        )
        title_label.pack(padx=15, pady=(15, 10), anchor='w')
        
        return card
        
    def browse_file(self, path_var, file_types):
        """
        Open a file dialog to browse for files and update the path variable.
        
        Args:
            path_var: StringVar to store the selected file path
            file_types: List of tuples containing file type descriptions and extensions
        """
        file_path = filedialog.askopenfilename(
            filetypes=file_types,
            initialdir=".",  # Start in current directory
            title="Select File"
        )
        if file_path:
            path_var.set(file_path)
            # If this is an image file, update the preview
            if any(file_path.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg', '.gif', '.bmp']):
                self.show_image_preview(file_path)

    def show_image_preview(self, image_path):
        try:
            img = Image.open(image_path)            
            max_size = 200             
            aspect_ratio = img.width / img.height
            if img.width > img.height:
                new_width = max_size
                new_height = int(max_size / aspect_ratio)
            else:
                new_height = max_size
                new_width = int(max_size * aspect_ratio)            
            img = img.resize((new_width, new_height))            
            ctk_image = ctk.CTkImage(light_image=img, size=(new_width, new_height))            
            self.image_preview_label.configure(image=ctk_image, text="")  
            self.image_preview_label.image = ctk_image
        except Exception as e:
            self.image_preview_label.configure(text="Image Preview - Error loading image", image=None)
            print(f"Error loading image: {e}")


    def send_messages(self, with_image=False):
        if with_image:
            message_input = self.image_message_input
            csv_path_var = self.image_csv_path_var
            default_name = self.image_default_name
        else:
            message_input = self.text_message_input
            csv_path_var = self.text_csv_path_var
            default_name = self.text_default_name
            
        # Validate inputs
        if not csv_path_var.get():
            messagebox.showerror("Error", "Please upload a CSV file first!")
            return
            
        message = message_input.get("1.0", tk.END).strip()
        if not message:
            messagebox.showerror("Error", "Please enter a message!")
            return
            
        if with_image and not self.image_path_var.get():
            messagebox.showerror("Error", "Please upload an image!")
            return
        
        try:
            df = pd.read_csv(csv_path_var.get())
            
            if with_image:
                self.send_messages_with_image(
                    message=message,
                    default_name=default_name.get(),
                    image_path=self.image_path_var.get(),
                    df=df
                )
            else:
                self.send_messages_without_image(
                    message=message,
                    default_name=default_name.get(),
                    df=df
                )
            
            messagebox.showinfo("Success", "Done sending the messages")
            
            # Remove log files after sending messages
            self.cleanup_logs()

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")

    def send_messages_with_image(self, message, default_name, image_path, df):
        for _, row in df.iterrows():
            try:
                name = row.iloc[1]
                if pd.isna(name):
                    name = default_name   
                
                number = str(row.iloc[0])
                country_code = row.iloc[2]
                phone_number = phonenumbers.parse(number, country_code)
                phone_number = "".join(["+", str(phone_number.country_code), str(phone_number.national_number)])
                
                # Send message with image
                pwk.sendwhats_image(
                receiver = phone_number,
                img_path = image_path,
                tab_close=True,
                caption = message.format(name=name)
                )
                keyboard.send("ctrl+w")
            except Exception as e:
                continue

    def send_messages_without_image(self, message, default_name, df):
        for _, row in df.iterrows():
            try:
                name = row.iloc[1]
                if pd.isna(name):
                    name = default_name   
                
                number = str(row.iloc[0])
                country_code = row.iloc[2]
                phone_number = phonenumbers.parse(number, country_code)
                phone_number = "".join(["+", str(phone_number.country_code), str(phone_number.national_number)])
                
                pwk.sendwhatmsg_instantly(
                    phone_no=phone_number,
                    message=message.format(name=name),
                    tab_close=True,
                    close_time=3
                )
                keyboard.send("ctrl+w")
            except Exception as e:
                continue

    def generate_ai_rewrite(self):
        # Placeholder function for AI rewrite logic
        base_message = self.base_message_input.get("1.0", tk.END).strip()
        use_case = self.use_case_input.get().strip()
        
        if base_message == "" and use_case == "":
            messagebox.showerror("Error", "Please enter either a base message or a use case description.")
            return
        
        # Here you can call your AI rewrite logic
        # Example: rewritten_message = some_ai_model.rewrite_message(base_message, use_case)
        rewritten_message = rewrite_message(base_message = base_message, use_case = use_case)  # Placeholder
        
        self.output_message_display.configure(state='normal')
        self.output_message_display.delete("1.0", tk.END)
        self.output_message_display.insert("1.0", rewritten_message)
        self.output_message_display.configure(state='disabled')

    def cleanup_logs(self):
        log_files = ['whatsapp_messenger.log', 'PyWhatKit_DB.txt']
        for log_file in log_files:
            if os.path.exists(log_file):
                os.remove(log_file)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = WhatsWave()
    app.run()
