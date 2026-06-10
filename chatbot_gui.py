"""
CodeAlpha AI Internship - Task 2: Chatbot for FAQs
GUI Version using Tkinter
Author: [Your Name]
"""

import tkinter as tk
from tkinter import scrolledtext, ttk
import threading
from faq_chatbot import FAQChatbot, FAQ_DATA
import datetime


class ChatbotGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("CodeAlpha FAQ Chatbot")
        self.root.geometry("700x600")
        self.root.configure(bg="#f5f5f5")
        self.root.resizable(True, True)

        # Initialize chatbot
        self.chatbot = FAQChatbot(FAQ_DATA)

        self._build_ui()
        self._show_welcome()

    def _build_ui(self):
        """Build the GUI layout."""
        # ── Header ──
        header = tk.Frame(self.root, bg="#534AB7", pady=12)
        header.pack(fill=tk.X)
        tk.Label(header, text="🤖  CodeAlpha FAQ Assistant",
                 font=("Helvetica", 16, "bold"),
                 bg="#534AB7", fg="white").pack()
        tk.Label(header, text="AI Internship Helper Bot",
                 font=("Helvetica", 10),
                 bg="#534AB7", fg="#CCCCFF").pack()

        # ── Chat area ──
        chat_frame = tk.Frame(self.root, bg="#f5f5f5")
        chat_frame.pack(fill=tk.BOTH, expand=True, padx=12, pady=(10, 0))

        self.chat_display = scrolledtext.ScrolledText(
            chat_frame, wrap=tk.WORD, state=tk.DISABLED,
            font=("Helvetica", 11), bg="white", relief=tk.FLAT,
            borderwidth=1, cursor="arrow"
        )
        self.chat_display.pack(fill=tk.BOTH, expand=True)

        # Configure text tags for styling
        self.chat_display.tag_configure("user_name",
            foreground="#534AB7", font=("Helvetica", 10, "bold"))
        self.chat_display.tag_configure("user_msg",
            foreground="#333333", font=("Helvetica", 11),
            lmargin1=20, lmargin2=20)
        self.chat_display.tag_configure("bot_name",
            foreground="#1D9E75", font=("Helvetica", 10, "bold"))
        self.chat_display.tag_configure("bot_msg",
            foreground="#333333", font=("Helvetica", 11),
            lmargin1=20, lmargin2=20)
        self.chat_display.tag_configure("confidence",
            foreground="#888888", font=("Helvetica", 9, "italic"),
            lmargin1=20)
        self.chat_display.tag_configure("separator",
            foreground="#DDDDDD")

        # ── Quick topics ──
        topics_frame = tk.Frame(self.root, bg="#f0f0f0", pady=6)
        topics_frame.pack(fill=tk.X, padx=12)
        tk.Label(topics_frame, text="Quick Topics:",
                 font=("Helvetica", 9, "bold"),
                 bg="#f0f0f0", fg="#666").pack(side=tk.LEFT, padx=(0,6))

        quick_topics = [
            ("📋 Tasks", "What tasks are included in the AI internship?"),
            ("🎓 Certificate", "What certificate will I receive?"),
            ("📤 Submit", "How do I submit my project?"),
            ("📞 Contact", "What is the contact information for CodeAlpha?"),
        ]
        for label, query in quick_topics:
            btn = tk.Button(
                topics_frame, text=label,
                font=("Helvetica", 9),
                bg="white", fg="#534AB7",
                relief=tk.FLAT, bd=1,
                padx=8, pady=3, cursor="hand2",
                command=lambda q=query: self._send_quick(q)
            )
            btn.pack(side=tk.LEFT, padx=3)

        # ── Input row ──
        input_frame = tk.Frame(self.root, bg="#f5f5f5", pady=10)
        input_frame.pack(fill=tk.X, padx=12, pady=(4, 10))

        self.input_var = tk.StringVar()
        self.input_field = tk.Entry(
            input_frame, textvariable=self.input_var,
            font=("Helvetica", 12), relief=tk.FLAT,
            bg="white", insertbackground="#534AB7"
        )
        self.input_field.pack(side=tk.LEFT, fill=tk.X, expand=True,
                               ipady=8, padx=(0, 8))
        self.input_field.bind("<Return>", lambda e: self._send_message())

        self.send_btn = tk.Button(
            input_frame, text="Send ➤",
            font=("Helvetica", 11, "bold"),
            bg="#534AB7", fg="white",
            relief=tk.FLAT, padx=16, pady=6,
            cursor="hand2", command=self._send_message
        )
        self.send_btn.pack(side=tk.RIGHT)

        # ── Status bar ──
        self.status_var = tk.StringVar(value="Ready")
        status_bar = tk.Label(
            self.root, textvariable=self.status_var,
            font=("Helvetica", 9), bg="#534AB7", fg="white",
            anchor=tk.W, padx=10
        )
        status_bar.pack(fill=tk.X, side=tk.BOTTOM)

        self.input_field.focus()

    def _show_welcome(self):
        self._add_bot_message(
            "Hello! I'm your CodeAlpha FAQ Assistant 👋\n"
            "I can answer questions about the AI internship, tasks, "
            "submission process, certificates, and more.\n"
            "Type your question or click a quick topic above!"
        )

    def _add_user_message(self, text):
        self.chat_display.configure(state=tk.NORMAL)
        time_str = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\nYou  [{time_str}]\n", "user_name")
        self.chat_display.insert(tk.END, f"{text}\n", "user_msg")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _add_bot_message(self, text, confidence=None):
        self.chat_display.configure(state=tk.NORMAL)
        time_str = datetime.datetime.now().strftime("%H:%M")
        self.chat_display.insert(tk.END, f"\nBot  [{time_str}]\n", "bot_name")
        self.chat_display.insert(tk.END, f"{text}\n", "bot_msg")
        if confidence is not None:
            self.chat_display.insert(
                tk.END, f"  Match confidence: {confidence*100:.1f}%\n", "confidence")
        self.chat_display.insert(tk.END, "─" * 60 + "\n", "separator")
        self.chat_display.configure(state=tk.DISABLED)
        self.chat_display.see(tk.END)

    def _send_quick(self, query):
        self.input_var.set(query)
        self._send_message()

    def _send_message(self):
        user_text = self.input_var.get().strip()
        if not user_text:
            return
        self.input_var.set("")
        self._add_user_message(user_text)
        self.send_btn.configure(state=tk.DISABLED, text="...")
        self.status_var.set("Thinking...")
        threading.Thread(target=self._get_response,
                         args=(user_text,), daemon=True).start()

    def _get_response(self, query):
        response = self.chatbot.get_response(query)
        self.root.after(0, self._display_response, response)

    def _display_response(self, response):
        conf = response['confidence'] if response['found'] else None
        self._add_bot_message(response['answer'], confidence=conf)
        self.send_btn.configure(state=tk.NORMAL, text="Send ➤")
        self.status_var.set("Ready")


# ─────────────────────────────────────────────
#  MAIN
# ─────────────────────────────────────────────
if __name__ == "__main__":
    root = tk.Tk()
    app = ChatbotGUI(root)
    root.mainloop()
