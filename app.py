from PIL import Image
from customtkinter import *
from tkinter import END
from bs4 import BeautifulSoup
import requests
import winsound
import threading

# COMANDOS IMPORTANTES
# threading.Thread(target=nomedafuncao).start() - Permite que você rode funções dentro do app sem travar


class Sparrow:
    def __init__(self, master=None):
        pass

        set_appearance_mode('dark')
        root.resizable(False, False)
        root.title('Sparrow')
        root.iconbitmap('./images/sparrow.ico')

        root.grid_columnconfigure((0, 1), weight=1)

        # Imagens
        consolebtnimage = CTkImage(light_image=Image.open('./images/write.png'),
                                   dark_image=Image.open('./images/write.png'))

        # Containeres
        self.containeresquerda = CTkFrame(master)
        self.containeresquerda.grid(row=0, column=0, padx=(0, 10), pady=0, sticky='nw')

        self.containerdireita = CTkFrame(master)
        self.containerdireita.grid(row=0, column=1, padx=(10, 0), pady=0, sticky='ne')

        self.containerconsole = CTkFrame(self.containeresquerda)
        self.containerconsole.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        self.containerhtmllog = CTkFrame(self.containeresquerda)
        self.containerhtmllog.grid(row=2, column=0, padx=10, pady=10, sticky='nw')

        self.containertitulo = CTkFrame(self.containerdireita)
        self.containertitulo.grid(row=0, column=0, padx=20, pady=10, sticky='n')

        self.containerwidgets = CTkFrame(self.containerdireita)
        self.containerwidgets.grid(row=1, column=0, padx=20, pady=10, sticky='n')

        self.containercheckboxes = CTkFrame(self.containerdireita)
        self.containercheckboxes.grid(row=2, column=0, padx=20, pady=10, sticky='nw')

        # Widgets
        self.console = CTkTextbox(self.containerconsole, width=500)
        self.console.insert(0.0, text='The Sparrow Project Console - <WYRM> Edition\n')
        self.console.configure(state='disabled')
        self.console.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.consoleentry = CTkEntry(self.containerconsole,placeholder_text='Type a command', width=350)
        self.consoleentry.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

        self.consolebtn = CTkButton(self.containerconsole, text='Send',
                                    image=consolebtnimage,
                                    command=self.sendcommand)
        self.consolebtn.grid(row=1, column=1, padx=(0, 10), pady=10)

        self.htmltitle = CTkLabel(self.containerhtmllog, text='HTML Log')
        self.htmltitle.grid(row=0, column=0, padx=10, pady=5, sticky='nw')

        self.htmllog = CTkTextbox(self.containerhtmllog, width=500)
        self.htmllog.configure(state='disabled')
        self.htmllog.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nw')

        self.titulo = CTkLabel(self.containertitulo, text='Welcome to the Sparrow Project')
        self.titulo.grid(row=0, column=1, padx=20, pady=10, sticky='n')

        self.urlentry = CTkEntry(self.containerwidgets, placeholder_text='Type the website url', width=250)
        self.urlentry.grid(row=1, column=1, padx=20, pady=10)

        self.nomearquivoentry = CTkEntry(self.containerwidgets, placeholder_text='Name, e.g: archive.jpg', width=250)
        self.nomearquivoentry.grid(row=2, column=1, padx=20, pady=(0, 10))

        self.buscarbtn = CTkButton(self.containerwidgets, text='Buscar', command=self.search)
        self.buscarbtn.grid(row=3, column=1, padx=20, pady=(0, 10))

        self.downloadbtn = CTkButton(self.containerwidgets,text='Download', fg_color='#02B126')
        self.downloadbtn.grid(row=4, column=1, padx=20, pady=(0, 10))


    def search(self):
        link = self.urlentry.get()
        cons = self.console
        log = self.htmllog

        def main():
            
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'}
            req = requests.get(link, headers=headers)
            html = req.text
            soup = BeautifulSoup(html, 'html.parser')
            res = soup.prettify()

            cons.configure(state='normal')
            log.configure(state='normal')

            if req.status_code == 200:
                cons.insert(END, text=f'{req.status_code} - REQUEST SUCCESSFUL!\n')
                log.insert(END, text=res)

            else:
                cons.insert(END, text=f'{req.status_code} - REQUEST FAILED!\n')

            log.configure(state='disabled')
            cons.configure(state='disabled')
            cons.see(END)

            # Permite que o app rode a função sem travar
            threading.Thread(target=main).start()

    def sendcommand(self):
        cmd = self.consoleentry.get()
        cons = self.console
        htmllog = self.htmllog

        cons.configure(state='normal')
        cons.insert(END, text=f'>{cmd}\n')

        match cmd:
            case 'sweet':
                cons.insert(END, text=f'Foo Fighters - Learn to fly\n')
                
            case 'clear':
                cons.delete(0.0, END)
                cons.insert(END, text='The Sparrow Project Console - <WYRM> Edition\n')

            case 'clearall':
                cons.delete(0.0, END)
                cons.insert(END, text='The Sparrow Project Console - <WYRM> Edition\n')
                htmllog.configure(state='normal')
                htmllog.delete(0.0, END)
                htmllog.configure(state='disabled')

            # A ser testado (SUCESSO)
            case 'help':
                command_list = ['clear - clean the console interface',
                                'clearall - clean the console interface and the HTML log',
                                'sweet - shows the song of the day',
                                'help - shows the help menu, duh!']
                
                # printa todos os comandos dentro da lista
                cont = 0
                while cont != len(command_list):
                    cons.insert(END, text=f'{command_list[cont]}\n')
                    cont += 1

            case _:
                cons.insert(END, text=f'"{cmd}" is not recognized as a command.\n')

        cons.configure(state='disabled')
        cons.see(END)


root = CTk()
Sparrow(root)
root.mainloop()
