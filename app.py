from PIL import Image
from customtkinter import *
from tkinter import END
from bs4 import BeautifulSoup
import requests
import platform
import threading

class Sync:
    '''
    It simplifies a command from the threading module.\n
    '''
    def __init__(self, func):
        threading.Thread(target=func).start()


# IMPORTANTE
# https://rule34.xxx/index.php?page=post&s=view&id=10384664

class Sparrow:
    '''
    An UI that allows the user to extract HTML data in an easy-peasy way
    Made by @jurihanpadaria
    '''
    def __init__(self, master=None):
        pass

        set_appearance_mode('dark')
        root.resizable(False, False)
        root.title('Sparrow')
        root.grid_columnconfigure((0, 1), weight=1)

        # Imagens
        consolebtnimage = CTkImage(light_image=Image.open('write.png'),
                                   dark_image=Image.open('write.png'))

        # For some reason, the icon isn't working for linux so it will only work in windows
        # I promise I will find a way to fix this
        if platform.system() == 'Windows':
            root.iconbitmap('./sparrow.ico')

        # Containeres
        self.containeresquerda = CTkFrame(master)
        self.containeresquerda.grid(row=0, column=0, padx=(0, 10), pady=0, sticky='nw')

        self.containerdireita = CTkFrame(master)
        self.containerdireita.grid(row=0, column=1, padx=(10, 0), pady=0, sticky='ne')

        self.containerconsole = CTkFrame(self.containeresquerda)
        self.containerconsole.grid(row=0, column=0, padx=10, pady=10, sticky='nw')

        self.containerhtmllog = CTkFrame(self.containeresquerda)
        self.containerhtmllog.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

        self.containertitulo = CTkFrame(self.containerdireita)
        self.containertitulo.grid(row=0, column=0, padx=20, pady=10, sticky='n')

        self.containerbusca = CTkFrame(self.containerdireita)
        self.containerbusca.grid(row=1, column=0, padx=20, pady=5, sticky='nw')

        self.containerdownload = CTkFrame(self.containerdireita)
        self.containerdownload.grid(row=2, column=0, padx=20, pady=5, sticky='nw')

        self.containertags = CTkFrame(self.containerdireita)
        self.containertags.grid(row=3, column=0, padx=20, pady=5, sticky='nw')

        # Widgets
        self.console = CTkTextbox(self.containerconsole, width=500)
        self.console.insert(0.0, text='The Sparrow Project Console\n')
        self.console.configure(state='disabled')
        self.console.grid(row=0, column=0, padx=10, pady=10, columnspan=2)

        self.consoleentry = CTkEntry(self.containerconsole,placeholder_text='Type a command', width=350)
        self.consoleentry.grid(row=1, column=0, padx=10, pady=10, sticky='nw')

        self.consolebtn = CTkButton(self.containerconsole, text='Send', image=consolebtnimage, command=self.sendcommand)
        self.consolebtn.grid(row=1, column=1, padx=(0, 10), pady=10)

        self.htmltitle = CTkLabel(self.containerhtmllog, text='HTML Log')
        self.htmltitle.grid(row=0, column=0, padx=10, pady=5, sticky='nw')

        self.htmllog = CTkTextbox(self.containerhtmllog, width=500)
        self.htmllog.configure(state='disabled')
        self.htmllog.grid(row=1, column=0, padx=10, pady=(0, 10), sticky='nw')

        self.titulo = CTkLabel(self.containertitulo, text='Welcome to the Sparrow Project')
        self.titulo.grid(row=0, column=1, padx=20, pady=10, sticky='n')

        # Url search
        self.urllbl = CTkLabel(self.containerbusca, text='Type the website here')
        self.urllbl.grid(row=0, column=1, padx=20, pady=5)

        self.urlentry = CTkEntry(self.containerbusca, placeholder_text='Website url', width=250)
        self.urlentry.grid(row=1, column=1, padx=20, pady=10)

        self.buscarbtn = CTkButton(self.containerbusca, text='Buscar', command=self.search)
        self.buscarbtn.grid(row=2, column=1, padx=20, pady=(0, 10))

        # Archive download options
        self.arquivolbl = CTkLabel(self.containerdownload, text='Type the archive name')
        self.arquivolbl.grid(row=0, column=1, padx=20, pady=5)

        self.imgentry = CTkEntry(self.containerdownload,
                                 placeholder_text='Image link here',
                                 border_color='#4EC4DA',
                                 border_width=2,
                                 width=250)
        self.imgentry.grid(row=1, column=1, padx=20, pady=(10, 0))

        self.arquivoentry = CTkEntry(self.containerdownload,
                                     placeholder_text='Name, e.g: archive.jpg',
                                     border_color='#4EC4DA',
                                     border_width=2,
                                     width=250)
        self.arquivoentry.grid(row=2, column=1, padx=20, pady=10)

        self.downloadbtn = CTkButton(self.containerdownload, text='Download',
                                     fg_color='#02B126', corner_radius=32)
        self.downloadbtn.grid(row=3, column=1, padx=20, pady=(0, 10))

        # Filter options
        self.tagtitulo = CTkLabel(self.containertags, text='Select an option')
        self.tagtitulo.grid(row=0, column=0, padx=20, pady=5, sticky='n')

        self.tags = CTkOptionMenu(self.containertags, values=[' ', 'Links', 'Images'])
        self.tags.grid(row=1, column=0, padx=20, pady=10, sticky='n')

    def search(self):
        def exec():
            link = self.urlentry.get()
            cons = self.console
            log = self.htmllog

            cons.configure(state='normal')
            log.configure(state='normal')

            headers = {'User-Agent':
                       'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:128.0) Gecko/20100101 Firefox/128.0'}
            
            try:
                req = requests.get(link, headers=headers)
                if req.status_code == 200:
                    cons.insert(END, text=f'{req.status_code} - REQUEST SUCCESSFUL!\n')

                    html = req.text
                    soup = BeautifulSoup(html, 'html.parser')
                    res = soup.prettify()

                    log.insert(END, text=res)
                else:
                    cons.insert(END, text=f'{req.status_code} - REQUEST DENIED\n')

            # Exceptions
            except requests.exceptions.ConnectionError:
                cons.insert(END, text='ERROR - A connection error occurred.\n')
            except requests.exceptions.MissingSchema:
                cons.insert(END, text='ERROR - http/https is missing.\n')
            except requests.exceptions.InvalidURL:
                cons.insert(END, text='ERROR - The URL is invalid.\n')
            except requests.exceptions.InvalidSchema:
                cons.insert(END, text='ERROR - There is no https or domain.\n')
            finally:
                log.configure(state='disabled')
                cons.configure(state='disabled')
                cons.see(END)
        Sync(func=exec)

    def sendcommand(self):
        cmd = self.consoleentry.get()
        cons = self.console
        htmllog = self.htmllog

        cons.configure(state='normal')
        cons.insert(END, text=f'>{cmd}\n')

        match cmd:
            case 'version':
                cons.insert(END, text='"Wyrm"\n')

            case 'sweet':
                cons.insert(END, text=f'Foo Fighters - Learn to fly\n')
                
            case 'clear':
                cons.delete(0.0, END)
                cons.insert(END, text='The Sparrow Project Console\n')

            case 'clearhtml':
                htmllog.configure(state='normal')
                htmllog.delete(0.0, END)
                htmllog.configure(state='disabled')

            case 'clearall':
                cons.delete(0.0, END)
                cons.insert(END, text='The Sparrow Project Console\n')
                htmllog.configure(state='normal')
                htmllog.delete(0.0, END)
                htmllog.configure(state='disabled')

            case 'help':
                command_list = ['version - shows the project version',
                                'clear - clean the console interface',
                                'clearhtml - clean the HTML log',
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
