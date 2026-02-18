import customtkinter as ctk
import pyshorteners
import os

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

class EncurtadorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Link Shortener Pro") 
        self.geometry("600x450")
        
        try:
            if os.path.exists("icon.ico"):
                self.iconbitmap("icon.ico")
        except:
            pass 

        self.idioma_atual = "en" 
        
        self.textos = {
            "en": {
                "titulo": "URL Shortener",
                "placeholder_entrada": "Paste your long link here...",
                "btn_encurtar": "Shorten Link",
                "placeholder_saida": "Short link will appear here...",
                "erro": "Error: Invalid link or no internet",
                "sucesso": "Success!",
                "btn_lang": "Mudar para PT-BR 🇧🇷"
            },
            "pt": {
                "titulo": "Encurtador de URL",
                "placeholder_entrada": "Cole seu link longo aqui...",
                "btn_encurtar": "Encurtar Link",
                "placeholder_saida": "O link curto aparecerá aqui...",
                "erro": "Erro: Link inválido ou sem internet",
                "sucesso": "Sucesso!",
                "btn_lang": "Switch to English 🇺🇸"
            }
        }

        self.btn_idioma = ctk.CTkButton(self, text=self.textos["en"]["btn_lang"], width=120, height=30, 
                                        fg_color="transparent", border_width=1, command=self.mudar_idioma)
        self.btn_idioma.place(relx=0.95, rely=0.05, anchor="ne")

        self.label_titulo = ctk.CTkLabel(self, text=self.textos["en"]["titulo"], font=("Arial", 24, "bold"))
        self.label_titulo.pack(pady=(50, 20))

        self.frame_entrada = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_entrada.pack(pady=10)

        self.entry_url = ctk.CTkEntry(self.frame_entrada, placeholder_text=self.textos["en"]["placeholder_entrada"], width=400, height=40)
        self.entry_url.pack(side="left", padx=(0, 10))

        self.btn_colar = ctk.CTkButton(self.frame_entrada, text="Paste 📋", width=80, height=40, fg_color="orange", hover_color="darkorange", command=self.colar_link)
        self.btn_colar.pack(side="left")

        self.btn_encurtar = ctk.CTkButton(self, text=self.textos["en"]["btn_encurtar"], width=200, height=50, font=("Arial", 16, "bold"), command=self.encurtar_link)
        self.btn_encurtar.pack(pady=30)

        self.frame_saida = ctk.CTkFrame(self, fg_color="transparent")
        self.frame_saida.pack(pady=10)

        self.entry_resultado = ctk.CTkEntry(self.frame_saida, placeholder_text=self.textos["en"]["placeholder_saida"], width=400, height=40)
        self.entry_resultado.pack(side="left", padx=(0, 10))

        self.btn_copiar = ctk.CTkButton(self.frame_saida, text="Copy 📑", width=80, height=40, fg_color="green", hover_color="darkgreen", command=self.copiar_link)
        self.btn_copiar.pack(side="left")

        self.label_status = ctk.CTkLabel(self, text="", text_color="green")
        self.label_status.pack(pady=5)


    def mudar_idioma(self):
        if self.idioma_atual == "en":
            self.idioma_atual = "pt"
        else:
            self.idioma_atual = "en"
        
        t = self.textos[self.idioma_atual]
        self.label_titulo.configure(text=t["titulo"])
        self.entry_url.configure(placeholder_text=t["placeholder_entrada"])
        self.btn_encurtar.configure(text=t["btn_encurtar"])
        self.entry_resultado.configure(placeholder_text=t["placeholder_saida"])
        self.btn_idioma.configure(text=t["btn_lang"])
        
        if self.idioma_atual == "pt":
            self.btn_colar.configure(text="Colar 📋")
            self.btn_copiar.configure(text="Copiar 📑")
        else:
            self.btn_colar.configure(text="Paste 📋")
            self.btn_copiar.configure(text="Copy 📑")

    def colar_link(self):
        try:
            texto_clipboard = self.clipboard_get()
            self.entry_url.delete(0, "end")
            self.entry_url.insert(0, texto_clipboard)
        except:
            self.label_status.configure(text="Clipboard empty", text_color="red")

    def copiar_link(self):
        link = self.entry_resultado.get()
        if link:
            self.clipboard_clear()
            self.clipboard_append(link)
            self.update()
            
            msg = "Copiado!" if self.idioma_atual == "pt" else "Copied!"
            self.label_status.configure(text=msg, text_color="#2CC985")
            self.after(3000, lambda: self.label_status.configure(text=""))

    def encurtar_link(self):
        url_original = self.entry_url.get()
        t = self.textos[self.idioma_atual]
        
        if url_original:
            try:
                self.entry_resultado.delete(0, "end")
                self.entry_resultado.insert(0, "..." if self.idioma_atual == "en" else "Aguarde...")
                self.update()

                s = pyshorteners.Shortener()
                link_curto = s.tinyurl.short(url_original)
                
                self.entry_resultado.delete(0, "end")
                self.entry_resultado.insert(0, link_curto)
                self.label_status.configure(text=t["sucesso"], text_color="#2CC985")
            except:
                self.entry_resultado.delete(0, "end")
                self.entry_resultado.insert(0, t["erro"])
        else:
            self.label_status.configure(text="URL Empty", text_color="red")

if __name__ == "__main__":
    app = EncurtadorApp()
    app.mainloop()