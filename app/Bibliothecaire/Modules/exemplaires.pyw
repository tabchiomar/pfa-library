from customtkinter import *
import customtkinter
import sqlite3
import os
from PIL import Image
from CTkMessagebox import CTkMessagebox
import subprocess
import sys
from datetime import datetime
now = datetime.now()
dash_path = os.path.join(os.path.dirname(__file__), '..', 'dashboard.pyw')
db_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'db', 'app.db')

current_dir = os.path.dirname(os.path.abspath(__file__))

if len(sys.argv) > 1:
    valeur = sys.argv[1]
    print("Valeur reçue :", valeur)
else:
    valeur="omar"

def callpage(script_path, user): 
    app.destroy()
    subprocess.call(["pythonw", script_path, user], bufsize=0)

def godashboard():
    callpage(dash_path, str(valeur))




class ScrollableLabelButtonFrame(customtkinter.CTkScrollableFrame):


    def __init__(self, master, command=None, **kwargs):
        super().__init__(master, **kwargs)
        self.grid_columnconfigure(0, weight=1)

        self.command = command
        self.radiobutton_variable = customtkinter.StringVar()
        self.label_list = []
        self.button_list = []

    def add_item(self, item, image=None):
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        button = customtkinter.CTkButton(self, text="Traiter", width=50, height=24, fg_color='green')
        if self.command is not None:
            button.configure(command=lambda: self.command(item))
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        button.grid(row=len(self.button_list), column=1, pady=(0, 10), padx=5)
        self.label_list.append(label)
        self.button_list.append(button)

    def show_item(self, item, image=None):
        label = customtkinter.CTkLabel(self, text=item, image=image, compound="left", padx=5, anchor="w")
        label.grid(row=len(self.label_list), column=0, pady=(0, 10), sticky="w")
        self.label_list.append(label)


    def remove_item_nobutton(self, item):
        for label in self.label_list:
            if item == label.cget("text"):
                label.destroy()
                self.label_list.remove(label)
                return    

    def clean(self):
        for i in range(10):
                for label in self.label_list:
                    label.destroy()
                    self.label_list.remove(label)

    

def chercher():
    app.scrollable_label_button_frame.clean()
    search=app.entrylist.get()
    print(search)
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    query="SELECT COUNT(*), titre FROM EXEMPLAIRE E, Livre L where titre = '"+search+"' and E.idlivre = L.idlivre GROUP BY titre"
    cursor.execute(query)
    result=cursor.fetchone()
    print(result)
    titre=result[1]
    count=result[0]
    app.scrollable_label_button_frame.show_item(f"{titre} | {count} Exemplaires", image=app.book_image)
    conn.close()

class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        self.title("Gestion d'exemplaires - Bibliothécaire")
        self.geometry("1100x450")

        # set grid layout 1x2
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)


        #images navigation
        image_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), r"..\..\..\pics")
        self.delete_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "delete_light.png")), dark_image=Image.open(os.path.join(image_path, "delete_dark.png")), size=(20, 20))
        self.edit_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "edit_light.png")), dark_image=Image.open(os.path.join(image_path, "edit_dark.png")), size=(20, 20))
        self.add_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "add_light.png")), dark_image=Image.open(os.path.join(image_path, "add_dark.png")), size=(20, 20))
        self.list_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "list_light.png")), dark_image=Image.open(os.path.join(image_path, "list_dark.png")), size=(20, 20))
        self.dashboard_image = customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "dashboard.png")), dark_image=Image.open(os.path.join(image_path, "dashboard_dark.png")), size=(30, 30))
        self.book_image= customtkinter.CTkImage(light_image=Image.open(os.path.join(image_path, "open_book.png")), dark_image=Image.open(os.path.join(image_path, "open_book_dark.png")))
        # create navigation frame
        self.navigation_frame = customtkinter.CTkFrame(self, corner_radius=0)
        self.navigation_frame.grid(row=0, column=0, sticky="nsew")
        self.navigation_frame.grid_rowconfigure(5, weight=1)

        self.navigation_frame_label = customtkinter.CTkLabel(self.navigation_frame, text="  Gestion d'examplaires", 
                                                             compound="left", font=customtkinter.CTkFont(size=15, weight="bold"))
        self.navigation_frame_label.grid(row=0, column=0, padx=20, pady=20)

        self.list_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Lister", image=self.list_image,
                                                   fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                    anchor="w", command=self.list_button_event)
        self.list_button.grid(row=1, column=0, sticky="ew")

        # self.add_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ajouter", image=self.add_image,
        #                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                                anchor="w", command=self.add_button_event)
        # self.add_button.grid(row=2, column=0, sticky="ew")

        # self.edit_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Modifier", image=self.edit_image,
        #                                               fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
        #                                                anchor="w", command=self.edit_button_event)
        # self.edit_button.grid(row=3, column=0, sticky="ew")

        self.archive_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Ajout / Suppression", image=self.edit_image,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=self.archive_button_event)
        self.archive_button.grid(row=2, column=0, sticky="ew")

        self.dashboard_button = customtkinter.CTkButton(self.navigation_frame, corner_radius=0, height=40, border_spacing=10, text="Tableau de bord", image=self.dashboard_image,
                                                      fg_color="transparent", text_color=("gray10", "gray90"), hover_color=("gray70", "gray30"),
                                                       anchor="w", command=godashboard)
        self.dashboard_button.grid(row=5, column=0, sticky="ew")

        self.appearance_mode_menu = customtkinter.CTkOptionMenu(self.navigation_frame, values=["Dark", "Light", "System"],
                                                                command=self.change_appearance_mode_event)
        self.appearance_mode_menu.grid(row=6, column=0, padx=20, pady=20, sticky="s")

        # create list frame

        # create second frame
        self.add_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.edit_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # create third frame
        self.archive_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        # select default frame
        self.select_frame_by_name("list")

    def select_frame_by_name(self, name):
        # set button color for selected button
        self.list_button.configure(fg_color=("gray75", "gray25") if name == "list" else "transparent")
        # self.add_button.configure(fg_color=("gray75", "gray25") if name == "add" else "transparent")
        #self.edit_button.configure(fg_color=("gray75", "gray25") if name == "edit" else "transparent")
        self.archive_button.configure(fg_color=("gray75", "gray25") if name == "archive" else "transparent")
    

        #LIST FRAME----------------------------------------------------------------------------------------------------------------
        self.list_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.entrylist = customtkinter.CTkEntry(self, placeholder_text='Chercher par nom du livre', width=650)
        self.entrylist.place(x=250,y=20)

        self.main_button_1 = customtkinter.CTkButton(master=self, fg_color="transparent", border_width=2, text_color=("gray10", "#DCE4EE"), text='Chercher', command=chercher)
        self.main_button_1.place(y=20,x=925)

        self.scrollable_label_button_frame = ScrollableLabelButtonFrame(master=self, width=800, height=360, corner_radius=0)
        self.scrollable_label_button_frame.place(x=250,y=60)
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        sql="SELECT COUNT(*), titre FROM EXEMPLAIRE E, Livre L where E.idlivre = L.idlivre GROUP BY titre"
        cursor.execute(sql)
        result=cursor.fetchall()
        i=0
        for row in result:
            titre=result[i][1]
            count=result[i][0]
            i=i+1
            self.scrollable_label_button_frame.show_item(f"{titre} | {count} Exemplaires", image=self.book_image)

        cursor.close()
        conn.close()
        

        #create fourth frame----------------------------------------------------------------------------------------------------------------
        def ajout():
            try:
                valeur=entryexemplaire.get()
                titre=entrytitle.get()

                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                sql="SELECT idlivre from Livre where titre='"+titre+"'"
                cursor.execute(sql)
                id=cursor.fetchone()[0]
                for i in range(int(valeur)):
                    sql2="INSERT INTO EXEMPLAIRE VALUES(NULL, ?, 1)"
                    cursor.execute(sql2, (str(id)))

                conn.commit()
                CTkMessagebox(title='Erreur',message='Les exemplaires sont ajoutés avec succès!', icon="warning")
            except:
                CTkMessagebox(title='Erreur',message='Erreur de saisie', icon="warning")

        def suppression():
            try:
                valeur=entryexemplaire.get()
                titre=entrytitle.get()
                conn = sqlite3.connect(db_path)
                cursor = conn.cursor()
                sql="SELECT COUNT(*) from exemplaire where idlivre='"+valeur+"'"
                cursor.execute(sql)
                result=cursor.fetchone()[0]
                if(int(result)<int(valeur)):
                    CTkMessagebox(title='Erreur',message="Le nombre saisie est inférieur au nombre d'exemplaire présents", icon="warning")
                else:
                    sql3="SELECT idlivre from Livre where titre='"+titre+"'"
                    cursor.execute(sql3)
                    idlivre=cursor.fetchone()[0]
                    sql2="DELETE FROM EXEMPLAIRE WHERE idlivre='"+str(idlivre)+"' and idexemplaire in (SELECT idexemplaire FROM EXEMPLAIRE WHERE idlivre='"+str(idlivre)+"' LIMIT "+str(valeur)+")"
                    cursor.execute(sql2)
                    CTkMessagebox(title='Erreur',message="Supprimé", icon="warning")
                conn.commit()
            except:
                CTkMessagebox(title='Erreur',message='Erreur de saisie', icon="warning")


            

        self.archive_frame = customtkinter.CTkFrame(self, corner_radius=0, fg_color="transparent")

        labeltitle = customtkinter.CTkLabel(self.archive_frame, text="Titre du livre", fg_color="transparent")
        entrytitle = customtkinter.CTkEntry(self.archive_frame, placeholder_text="Titre", width=300)

        labeltitle.place(x=75, y=50)
        entrytitle.place(x=150, y=50)

        labelexemplaire = customtkinter.CTkLabel(self.archive_frame, text="Nombre d'exemplaire", fg_color="transparent")
        entryexemplaire = customtkinter.CTkEntry(self.archive_frame, placeholder_text="Nombre", width=100)

        labelexemplaire.place(x=75, y=100)
        entryexemplaire.place(x=200, y=100)

        add = customtkinter.CTkButton(self.archive_frame, text= "Ajouter" , command=ajout)
        supp = customtkinter.CTkButton(self.archive_frame, text= "Supprimer" , command=suppression)

        add.place(x=100, y=150)
        supp.place(x=250, y=150)





        # select default frame



# show selected frame
        if name == "list":
            self.list_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.list_frame.grid_forget()

        if name == "add":
            self.add_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.add_frame.grid_forget()

        if name == "edit":
            self.edit_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.edit_frame.grid_forget()

        if name == "archive":
            self.archive_frame.grid(row=0, column=1, sticky="nsew")
        else:
            self.archive_frame.grid_forget()

    def list_button_event(self):
        self.select_frame_by_name("list")

    def add_button_event(self):
        self.select_frame_by_name("add")

    def edit_button_event(self):
        self.select_frame_by_name("edit")

    def archive_button_event(self):
        self.select_frame_by_name("archive")

    def change_appearance_mode_event(self, new_appearance_mode):
        customtkinter.set_appearance_mode(new_appearance_mode)
    
def ListerContact():
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql="SELECT * FROM contact where etat=0"
    cursor.execute(sql)
    result=cursor.fetchall()
    i=0
    for row in result:
        idcontact=result[i][0]
        username=result[i][2]
        contact=result[i][3]
        sujet=result[i][4]
        dateenvoi=result[i][6]
        app.scrollable_label_button_frame.show_item(f"{idcontact}| Username :{username} | Contact :{contact} | Sujet: {sujet} | Envoyé le :{dateenvoi}", image=app.book_image)
        i=i+1

        cursor.close()

if __name__ == "__main__":
    app = App()
    app.mainloop()

