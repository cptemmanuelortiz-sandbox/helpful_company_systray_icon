import sys
import os
import webbrowser
import urllib.parse
import socket
import tempfile
from datetime import datetime
import threading
import tkinter as tk
from tkinter import messagebox
import pyautogui
import config


class CompanyFloatingButton:
    def __init__(self):
        self.config = config.COMPANY_CONFIG
        self.screenshot_path = None
        self.tray_icon = None
        self.visible = False
        self.hover_zone_size = 60      # pixels from bottom-right corner to trigger
        self.hover_delay_ms = 1000     # how long mouse must stay before showing

        self.create_floating_button()
        self.create_tray_icon()
        self.start_hover_watcher()

    def get_resource_path(self, filename):
        if getattr(sys, 'frozen', False):
            return os.path.join(sys._MEIPASS, filename)
        return filename

    def create_floating_button(self):
        self.root = tk.Tk()
        self.root.title("Company Tools")
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.wm_attributes('-transparentcolor', 'white')
        self.root.configure(bg='white')

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.btn_w = 175
        self.btn_h = 175
        x = screen_width - self.btn_w - 20
        y = screen_height - self.btn_h - 50
        self.root.geometry(f"{self.btn_w}x{self.btn_h}+{x}+{y}")
        self.screen_w = screen_width
        self.screen_h = screen_height

        self.create_button()
        self.make_draggable()
        self.root.withdraw()
        self.root.bind('<Leave>', self.on_mouse_leave)

    def create_button(self):
        try:
            from PIL import Image, ImageTk
            logo_path = self.get_resource_path("logo.png")
            if os.path.exists(logo_path):
                logo_image = Image.open(logo_path).resize((140, 140), Image.Resampling.LANCZOS)
                self.logo_photo = ImageTk.PhotoImage(logo_image)
                self.button = tk.Button(
                    self.root, image=self.logo_photo, bg='white', activebackground='white',
                    relief='flat', borderwidth=0, highlightthickness=0,
                    cursor='hand2', command=self.show_menu
                )
            else:
                raise Exception("No logo")
        except Exception:
            self.button = tk.Button(
                self.root, text=self.config.get('icon_text', 'C'), font=('Segoe UI', 36, 'bold'),
                bg='white', activebackground='white', relief='flat',
                borderwidth=0, highlightthickness=0, cursor='hand2',
                command=self.show_menu
            )
        self.button.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

    def make_draggable(self):
        def start_drag(event):
            self.drag_data = {'x': event.x, 'y': event.y}
        def drag(event):
            x = self.root.winfo_x() + (event.x - self.drag_data['x'])
            y = self.root.winfo_y() + (event.y - self.drag_data['y'])
            self.root.geometry(f"+{x}+{y}")
        self.button.bind('<Button-1>', start_drag)
        self.button.bind('<B1-Motion>', drag)

    def start_hover_watcher(self):
        threading.Thread(target=self._hover_loop, daemon=True).start()

    def _hover_loop(self):
        in_zone_since = None
        while True:
            try:
                mx, my = pyautogui.position()
                in_zone = (mx >= self.screen_w - self.hover_zone_size and
                           my >= self.screen_h - self.hover_zone_size)

                if in_zone and not self.visible:
                    if in_zone_since is None:
                        in_zone_since = datetime.now()
                    elif (datetime.now() - in_zone_since).total_seconds() * 1000 >= self.hover_delay_ms:
                        self.show_logo()
                        in_zone_since = None
                elif not in_zone:
                    in_zone_since = None
            except Exception:
                pass
            threading.Event().wait(0.2)

    def show_logo(self):
        def _show():
            self.root.deiconify()
            self.root.lift()
            self.root.attributes('-topmost', True)
            self.visible = True
        self.root.after(0, _show)

    def hide_logo(self):
        def _hide():
            if self.visible:
                self.root.withdraw()
                self.visible = False
        self.root.after(0, _hide)

    def on_mouse_leave(self, event):
        self.root.after(800, self._maybe_hide)

    def _maybe_hide(self):
        try:
            mx, my = pyautogui.position()
            win_x, win_y = self.root.winfo_x(), self.root.winfo_y()
            if not (win_x <= mx <= win_x + self.btn_w and win_y <= my <= win_y + self.btn_h):
                self.hide_logo()
        except Exception:
            self.hide_logo()

    def show_menu(self):
        menu = tk.Menu(self.root, tearoff=0)
        menu.add_command(label="📧 IT Support", command=self.open_support)
        menu.add_command(label="🔗 Quick Links", command=self.open_quick_links)
        menu.add_command(label="🌐 Caminantes", command=self.open_caminantes)
        menu.add_separator()
        menu.add_command(label="❌ Exit", command=self.exit_app)
        menu.post(self.root.winfo_x() + 10, self.root.winfo_y() + self.button.winfo_height())

    def capture_screenshot(self):
        try:
            temp_dir = tempfile.mkdtemp(prefix="company_support_")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(temp_dir, f"screenshot_{timestamp}.png")
            pyautogui.screenshot().save(filepath)
            self.screenshot_path = filepath
            return filepath
        except Exception as e:
            print(f"❌ Screenshot failed: {e}")
            return None

    def open_support(self):
        try:
            prompt_window = tk.Toplevel(self.root)
            prompt_window.title("IT Support Request")
            prompt_window.geometry("400x250")
            prompt_window.attributes('-topmost', True)
            
            prompt_window.update_idletasks()
            x = (prompt_window.winfo_screenwidth() // 2) - 200
            y = (prompt_window.winfo_screenheight() // 2) - 125
            prompt_window.geometry(f"+{x}+{y}")

            tk.Label(prompt_window, text="Please briefly describe the issue you are experiencing:", font=('Segoe UI', 10), wraplength=380).pack(pady=10)
            issue_text = tk.Text(prompt_window, height=5, width=45, font=('Segoe UI', 10))
            issue_text.pack(pady=5)
            user_issue = [""]

            def submit_issue():
                user_issue[0] = issue_text.get("1.0", tk.END).strip()
                if not user_issue[0]:
                    messagebox.showwarning("Input Required", "Please describe your issue before submitting.", parent=prompt_window)
                    return
                prompt_window.destroy()

            def cancel_issue():
                prompt_window.destroy()

            btn_frame = tk.Frame(prompt_window)
            btn_frame.pack(pady=10)
            tk.Button(btn_frame, text="Submit", command=submit_issue, width=10, bg="#0078D4", fg="white").pack(side=tk.LEFT, padx=10)
            tk.Button(btn_frame, text="Cancel", command=cancel_issue, width=10).pack(side=tk.LEFT, padx=10)

            self.root.wait_window(prompt_window)
            if not user_issue[0]:
                return

            device_name = socket.gethostname()
            import getpass
            username = getpass.getuser()
            screenshot_path = self.capture_screenshot()

            subject = f"IT Support Request - {device_name}"
            body = f"""Dear IT Support Team,\n\nI need assistance with my device.\n\nIssue Description:\n{user_issue[0]}\n\nDevice Information:\n- Device Name: {device_name}\n- User: {username}\n- Date/Time: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}\n\nScreenshot Information:\n- Screenshot saved at: {screenshot_path if screenshot_path else "Screenshot capture failed"}\n- Please attach this file to your email\n\nThank you for your help.\n\nBest regards,\n{username}"""
            
            encoded_subject = urllib.parse.quote(subject)
            encoded_body = urllib.parse.quote(body)
            gmail_url = f"https://mail.google.com/mail/?view=cm&fs=1&to={self.config['support_email']}&su={encoded_subject}&body={encoded_body}"
            webbrowser.open(gmail_url)
        except Exception as e:
            print(f"❌ Error: {e}")

    def open_quick_links(self):
        webbrowser.open(self.config['quick_links_url'])

    def open_caminantes(self):
        webbrowser.open(self.config['caminantes_url'])

    def create_tray_icon(self):
        try:
            import pystray
            from PIL import Image, ImageDraw
            try:
                logo_path = self.get_resource_path("logo.png")
                tray_image = Image.open(logo_path).resize((64, 64))
            except Exception:
                tray_image = Image.new('RGB', (64, 64), color='white')
                draw = ImageDraw.Draw(tray_image)
                draw.ellipse((8, 8, 56, 56), fill=self.config.get('icon_color', (0, 100, 200)))
                draw.text((20, 15), self.config.get('icon_text', 'C'), fill='white')

            menu = (
                pystray.MenuItem('👀 Show Logo', lambda: self.show_logo()),
                pystray.MenuItem('📧 IT Support', lambda: self.open_support()),
                pystray.MenuItem('🔗 Quick Links', lambda: self.open_quick_links()),
                pystray.MenuItem('🌐 Caminantes', lambda: self.open_caminantes()),
                pystray.MenuItem('---', None, enabled=False),
                pystray.MenuItem('❌ Exit', lambda: self.exit_app()),
            )
            self.tray_icon = pystray.Icon("company_tray", tray_image, self.config['name'], menu)
            self.start_tray_icon()
        except Exception as e:
            print(f"⚠️ Tray icon not available: {e}")
            self.tray_icon = None

    def start_tray_icon(self):
        if self.tray_icon:
            threading.Thread(target=self.tray_icon.run, daemon=True).start()

    def exit_app(self):
        if self.tray_icon:
            try: self.tray_icon.stop()
            except: pass
        self.root.quit()
        self.root.destroy()
        sys.exit(0)

    def run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = CompanyFloatingButton()
    app.run()
