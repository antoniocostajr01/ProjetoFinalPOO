import customtkinter as ctk
from tkinter import messagebox

# Classe Locker
class Locker:
    def __init__(self, locker_id):
        self.__locker_id = locker_id
        self.__is_livre = True
        self.__usuario_id = None
    
    def associar_usuario(self, id_usuario):
        if self.__is_livre:
            self.__is_livre = False
            self.__usuario_id = id_usuario
            return True
        return False

    def liberar_usuario(self):
        if not self.__is_livre:
            self.__is_livre = True
            self.__usuario_id = None
            return True
        return False

    def get_status(self):
        return self.__usuario_id, self.__is_livre

    def get_locker_id(self):
        return self.__locker_id
    
    def get_locker_livre(self):
        return self.__is_livre

# Classe Usuario
class Usuario:
    def __init__(self, nome, id_usuario):
        self.__usuario_id = id_usuario
        self.__nome = nome

    def get_usuario_id(self):
        return self.__usuario_id 

    def get_nome(self):
        return self.__nome 

# Classe SistemaLocker
class SistemaLocker:
    def __init__(self):
        self.__lockers = {}
        self.__usuarios = {}

    def adicionar_locker(self, locker_id):
        if locker_id not in self.__lockers:
            self.__lockers[locker_id] = Locker(locker_id)
            return True
        return False

    def adicionar_usuario(self, usuario_id, nome):
        if usuario_id not in self.__usuarios:
            self.__usuarios[usuario_id] = Usuario(nome, usuario_id)
            return True
        return False

    def associar_locker_ao_usuario(self, locker_id, usuario_id):
        if locker_id in self.__lockers and usuario_id in self.__usuarios:
            if self.__lockers[locker_id].associar_usuario(usuario_id):
                return True
        return False

    def liberar_locker(self, locker_id):
        if locker_id in self.__lockers:
            return self.__lockers[locker_id].liberar_usuario()
        return False

    def get_locker_status(self, locker_id):
        if locker_id in self.__lockers:
            return self.__lockers[locker_id].get_status()
        return None

    def get_usuario_nome(self, usuario_id):
        if usuario_id in self.__usuarios:
            return self.__usuarios[usuario_id].get_nome()
        return None

# Função para criar a interface gráfica
class LockerApp(ctk.CTk):
    def __init__(self, sistema_locker):
        super().__init__()

        self.sistema_locker = sistema_locker
        self.title("Sistema de Lockers")
        self.geometry("400x400")

        # Criação do menu
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(pady=20)

        self.add_locker_button = ctk.CTkButton(self.menu_frame, text="Adicionar Locker", command=self.adicionar_locker)
        self.add_locker_button.grid(row=0, column=0, padx=10, pady=10)

        self.add_user_button = ctk.CTkButton(self.menu_frame, text="Adicionar Usuário", command=self.adicionar_usuario)
        self.add_user_button.grid(row=1, column=0, padx=10, pady=10)

        self.associar_button = ctk.CTkButton(self.menu_frame, text="Associar Locker", command=self.associar_locker)
        self.associar_button.grid(row=2, column=0, padx=10, pady=10)

        self.check_status_button = ctk.CTkButton(self.menu_frame, text="Ver Status Locker", command=self.check_status)
        self.check_status_button.grid(row=3, column=0, padx=10, pady=10)

        self.status_label = ctk.CTkLabel(self, text="Status: Nenhuma operação realizada")
        self.status_label.pack(pady=20)

    def adicionar_locker(self):
        locker_id = self.prompt_input("Digite o ID do Locker:")
        if locker_id:
            success = self.sistema_locker.adicionar_locker(locker_id)
            if success:
                messagebox.showinfo("Sucesso", f"Locker {locker_id} adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", f"Locker {locker_id} já existe.")
        else:
            messagebox.showerror("Erro", "ID do Locker inválido.")

    def adicionar_usuario(self):
        usuario_id = self.prompt_input("Digite o ID do Usuário:")
        nome = self.prompt_input("Digite o nome do Usuário:")
        if usuario_id and nome:
            success = self.sistema_locker.adicionar_usuario(usuario_id, nome)
            if success:
                messagebox.showinfo("Sucesso", f"Usuário {nome} adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", f"Usuário {nome} já existe.")
        else:
            messagebox.showerror("Erro", "ID ou Nome do Usuário inválido.")

    def associar_locker(self):
        locker_id = self.prompt_input("Digite o ID do Locker:")
        usuario_id = self.prompt_input("Digite o ID do Usuário:")
        if locker_id and usuario_id:
            success = self.sistema_locker.associar_locker_ao_usuario(locker_id, usuario_id)
            if success:
                messagebox.showinfo("Sucesso", f"Locker {locker_id} associado ao Usuário {usuario_id} com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao associar Locker ao Usuário.")
        else:
            messagebox.showerror("Erro", "ID do Locker ou Usuário inválido.")

    def check_status(self):
        locker_id = self.prompt_input("Digite o ID do Locker:")
        if locker_id:
            status = self.sistema_locker.get_locker_status(locker_id)
            if status:
                usuario_id, is_livre = status
                if is_livre:
                    self.status_label.config(text=f"Locker {locker_id} está livre.")
                else:
                    usuario_nome = self.sistema_locker.get_usuario_nome(usuario_id)
                    self.status_label.config(text=f"Locker {locker_id} está ocupado por {usuario_nome}.")
            else:
                self.status_label.config(text="Locker não encontrado.")
        else:
            self.status_label.config(text="ID do Locker inválido.")

    def prompt_input(self, prompt):
        input_window = ctk.CTkToplevel(self)
        input_window.title("Entrada de Dados")
        input_window.geometry("300x100")

        label = ctk.CTkLabel(input_window, text=prompt)
        label.pack(pady=10)

        entry = ctk.CTkEntry(input_window)
        entry.pack(pady=5)

        def submit():
            input_window.destroy()
            return entry.get()

        submit_button = ctk.CTkButton(input_window, text="Submeter", command=submit)
        submit_button.pack(pady=5)

        self.wait_window(input_window)  # Aguarda a entrada do usuário
        return entry.get()

# Programa principal
if __name__ == "__main__":
    sistema_locker = SistemaLocker()
    app = LockerApp(sistema_locker)
    app.mainloop()
