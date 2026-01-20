import customtkinter as ctk
from PIL import Image
import threading
import ai_engine  # Ensure this file is in the same folder

ctk.set_appearance_mode("Dark")

class CobraStudio(ctk.CTk):
    def __init__(self):
        super().__init__()

        # --- Window Config ---
        self.title("Cobra AI Studio")
        self.geometry("1100x850")
        self.configure(fg_color="#1a1a1a")

        # --- Sidebar ---
        self.sidebar = ctk.CTkFrame(self, width=250, corner_radius=0, fg_color="#111111")
        self.sidebar.pack(side="left", fill="y")
        
        self.new_btn = ctk.CTkButton(self.sidebar, text="+ New chat", height=42, 
                                     fg_color="#222222", hover_color="#333333",
                                     font=("Segoe UI", 14), command=self.reset_ui)
        self.new_btn.pack(padx=20, pady=25, fill="x")

        # --- Main Workspace ---
        self.main_view = ctk.CTkFrame(self, fg_color="transparent")
        self.main_view.pack(side="right", fill="both", expand=True)

        # 1. THE WATERMARK (Created after main_view so it's visible)
        self.watermark = ctk.CTkLabel(self.main_view, text="IMAGINE & GENERATE", 
                                      font=("Helvetica", 50, "bold"), text_color="#262626")
        self.watermark.place(relx=0.5, rely=0.45, anchor="center")

        # 2. THE CHAT FEED
        self.chat_feed = ctk.CTkScrollableFrame(self.main_view, fg_color="transparent")
        self.chat_feed.pack(fill="both", expand=True, padx=85, pady=(20, 110))

        # --- Bottom Input Bar ---
        self.dock = ctk.CTkFrame(self.main_view, fg_color="transparent")
        self.dock.place(relx=0.5, rely=0.92, anchor="center", relwidth=0.85)

        self.prompt_entry = ctk.CTkEntry(self.dock, placeholder_text="Describe your vision...",
                                         height=56, corner_radius=28, fg_color="#262626",
                                         border_color="#3a3a3a", font=("Segoe UI", 15))
        self.prompt_entry.pack(side="left", fill="x", expand=True)
        self.prompt_entry.bind("<Return>", lambda e: self.generate())

        # PRO ICON BUTTON (Circular Send)
        self.send_btn = ctk.CTkButton(self.dock, text="↑", width=40, height=40,
                                      corner_radius=20, fg_color="white", text_color="black",
                                      hover_color="#cccccc", font=("Arial", 22, "bold"),
                                      command=self.generate)
        self.send_btn.place(relx=0.993, rely=0.5, anchor="e", x=-8)

    def reset_ui(self):
        for widget in self.chat_feed.winfo_children():
            widget.destroy()
        self.watermark.place(relx=0.5, rely=0.45, anchor="center")

    def generate(self):
        prompt = self.prompt_entry.get().strip()
        if not prompt: return
        
        self.watermark.place_forget() # Removes watermark on first prompt
        self.prompt_entry.delete(0, 'end')
        self.add_bubble("You", prompt, is_user=True)
        
        # Disable button during work
        self.send_btn.configure(state="disabled")
        threading.Thread(target=self.run_ai, args=(prompt,), daemon=True).start()

    def add_bubble(self, sender, content, is_img=False, is_user=False):
        bubble = ctk.CTkFrame(self.chat_feed, fg_color="transparent")
        bubble.pack(fill="x", pady=18)
        
        name_color = "#10a37f" if is_user else "#d1d1d1"
        header = ctk.CTkLabel(bubble, text=sender.upper(), font=("Helvetica", 11, "bold"), text_color=name_color)
        header.pack(anchor="w", padx=10)

        if is_img:
            img_lbl = ctk.CTkLabel(bubble, image=content, text="", corner_radius=15)
            img_lbl.pack(anchor="w", padx=10, pady=8)
        else:
            txt_lbl = ctk.CTkLabel(bubble, text=content, wraplength=650, justify="left", font=("Segoe UI", 15))
            txt_lbl.pack(anchor="w", padx=10)

    def run_ai(self, prompt):
        try:
            pil_img = ai_engine.generate_ai_image(prompt)
            ctk_img = ctk.CTkImage(light_image=pil_img, dark_image=pil_img, size=(512, 512))
            self.after(0, lambda: self.add_bubble("Cobra AI", ctk_img, is_img=True))
        except Exception as e:
            self.after(0, lambda: self.add_bubble("System", f"Notice: {str(e)[:50]}"))
        finally:
            self.after(0, lambda: self.send_btn.configure(state="normal"))

if __name__ == "__main__":
    try:
        app = CobraStudio()
        app.mainloop()
    except Exception as e:
        print(f"Critical Startup Error: {e}")