import tkinter as tk
from tkinter import messagebox, simpledialog, ttk

class Locker:
    def __init__(self, locker_id, locker_ocupado=False, locker_usuario=None):
        self.__locker_id = locker_id
        self.__is_ocupado = locker_ocupado
        self.__usuario_id = locker_usuario

    def get_id_locker(self):
        return self.__locker_id

    def get_ocupado(self):
        return self.__is_ocupado

    def get_id_usuario(self):
        return self.__usuario_id

    def associar_usuario(self, usuario_id):
        if not self.__is_ocupado:
            self.__is_ocupado = True
            self.__usuario_id = usuario_id
            return True
        return False

    def liberar_usuario(self):
        if self.__is_ocupado:
            self.__is_ocupado = False
            self.__usuario_id = None
            return True
        return False

class Usuario:
    def __init__(self, usuario_id, nome):
        self.__usuario_id = usuario_id
        self.__nome = nome

    def get_id_usuario(self):
        return self.__usuario_id

    def get_nome(self):
        return self.__nome

class SistemaLocker:
    def __init__(self):
        self.__lockers = {}
        self.__usuarios = {}
        self.__locker_arq = 'lockers.txt'
        self.carregar_lockers()

    def existe_locker(self, id_locker):
        return id_locker in self.__lockers

    def adicionar_locker(self, locker_id):
        if locker_id not in self.__lockers:
            self.__lockers[locker_id] = Locker(locker_id)
            self.salvar_locker(self.__lockers[locker_id])


    def excluir_locker(self, locker_id):
        if locker_id in self.__lockers:
            del self.__lockers[locker_id]
            self.salvar_dados(self.__locker_arq)
            return True
        return False

    def adicionar_usuario(self, usuario_id, nome):
        if usuario_id not in self.__usuarios:
            self.__usuarios[usuario_id] = Usuario(usuario_id, nome)
            return True
        return False

    def excluir_usuario(self, usuario_id):
        if usuario_id in self.__usuarios:
            del self.__usuarios[usuario_id]
            return True
        return False

    def get_usuarios(self):
        return self.__usuarios

    def get_lockers(self):
        return self.__lockers

    def associar_locker_ao_usuario(self, locker_id, usuario_id):
        if locker_id in self.__lockers and usuario_id in self.__usuarios:
            return self.__lockers[locker_id].associar_usuario(usuario_id)
        return False

    def libera_locker(self, locker_id):
        if locker_id in self.__lockers:
            return self.__lockers[locker_id].liberar_usuario()
        return False

    def get_locker_status(self, locker_id):
        if locker_id in self.__lockers:
            return self.__lockers[locker_id].get_ocupado(), self.__lockers[locker_id].get_id_usuario()
        return None, None

    def is_locker_livre(self, locker_id):
        return locker_id in self.__lockers and not self.__lockers[locker_id].get_ocupado()

    def salvar_locker(self, locker):
        with open(self.__locker_arq, 'a') as arquivo:
            arquivo.write(f'{locker.get_id_locker()},{locker.get_ocupado()},{locker.get_id_usuario()}\n')

    def carregar_lockers(self):
        try:
            with open(self.__locker_arq, 'r') as arquivo:
                for linha in arquivo:
                    locker_id, locker_ocupado, locker_usuario = linha.strip().split(',')
                    self.__lockers[locker_id] = Locker(locker_id, locker_ocupado == 'True', locker_usuario if locker_usuario != 'None' else None)
        except FileNotFoundError:
            pass

    def salvar_dados(self, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:
            for locker_id, locker in self.__lockers.items():
                is_ocupado, usuario_id = locker.get_ocupado(), locker.get_id_usuario()
                arquivo.write(f'{locker_id},{is_ocupado},{usuario_id}\n')

    def carregar_dados(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as arquivo:
                for linha in arquivo:
                    locker_id, is_ocupado, usuario_id = linha.strip().split(',')
                    self.adicionar_locker(locker_id)
                    if is_ocupado == 'True':
                        self.associar_locker_ao_usuario(locker_id, usuario_id)
        except FileNotFoundError:
            pass

    def usuario_cadastrado(self, usuario_id):
        return usuario_id in self.__usuarios

    def get_usuario_unico(self, usuario_id):
        return self.__usuarios[usuario_id].get_nome()


class App:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Sistema de Lockers")
        self.sistema = SistemaLocker()

        # Menu
        menubar = tk.Menu(janela)
        janela.config(menu=menubar)

        # Menu de Opções
        menu_opcoes = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Opções", menu=menu_opcoes)
        menu_opcoes.add_command(label="Adicionar Locker", command=self.adicionar_lock)
        menu_opcoes.add_command(label="Excluir Locker", command=self.excluir_lock)
        menu_opcoes.add_command(label="Adicionar Usuário", command=self.adicionar_usuario)
        menu_opcoes.add_command(label="Excluir Usuário", command=self.excluir_usuario)
        menu_opcoes.add_command(label="Atribuir Locker a Usuário", command=self.atribuir_locker_usuario)
        menu_opcoes.add_command(label="Liberar Locker", command=self.liberar_locker)
        menu_opcoes.add_command(label="Verificar Status do Locker", command=self.verificar_status_locker)
        menu_opcoes.add_command(label="Salvar Dados", command=self.salvar_dados)
        menu_opcoes.add_command(label="Carregar Dados", command=self.carregar_dados)
        menu_opcoes.add_separator()
        menu_opcoes.add_command(label="Sair", command=janela.quit)

        # Frame para exibir lockers
        self.frame_lockers = tk.Frame(janela, highlightbackground="orange", highlightthickness=2)
        self.frame_lockers.pack(fill=tk.BOTH, expand=True)

        # Treeview para exibir os lockers
        self.tree_lockers = ttk.Treeview(self.frame_lockers, columns=("ID", "Status"), show="headings")
        self.tree_lockers.heading("ID", text="ID")
        self.tree_lockers.heading("Status", text="Status")
        self.tree_lockers.pack(fill=tk.BOTH, expand=True)

        # Frame para exibir usuarios
        self.frame_usuarios = tk.Frame(janela, highlightbackground="blue", highlightthickness=2)
        # self.frame_usuarios.pack(fill=tk.BOTH, expand=True)

        # Treeview para exibir os usuarios
        self.treeusuarios = ttk.Treeview(self.frame_usuarios, columns=("ID", "Nome"), show="headings")
        self.treeusuarios.heading("ID", text="ID")
        self.treeusuarios.heading("Nome", text="Nome")
        self.treeusuarios.pack(fill=tk.BOTH, expand=True)
        self.atualizar_lockers()

    def atualizar_lockers(self):
        for row in self.tree_lockers.get_children():
            self.tree_lockers.delete(row)

        lockers = self.sistema.get_lockers()
        if lockers:
            for locker_id, locker in lockers.items():
                status = "Ocupado" if locker.get_ocupado() else "Livre"
                usuario = locker.get_id_usuario() if locker.get_ocupado() else "N/A"
                self.tree_lockers.insert("", "end", values=(locker_id, status, usuario))
        else:
            self.tree_lockers.insert("", "end", values=("Nenhum locker cadastrado", "", ""))

    def adicionar_lock(self):
        locker_id = self.get_input("Digite o ID do Locker:")
        if locker_id and not self.sistema.existe_locker(locker_id):
            self.sistema.adicionar_locker(locker_id)
            messagebox.showinfo("Sucesso", f"Locker {locker_id} adicionado com sucesso.")
            self.atualizar_lockers()
        else:
            messagebox.showerror("Erro", "Locker já existe ou ID inválido.")

    def excluir_lock(self):
        locker_id = self.get_input("Digite o ID do Locker a ser excluído:")
        if locker_id and self.sistema.excluir_locker(locker_id):
            messagebox.showinfo("Sucesso", f"Locker {locker_id} excluído com sucesso.")
            self.atualizar_lockers()
        else:
            messagebox.showerror("Erro", "Locker não encontrado ou ID inválido.")

    def adicionar_usuario(self):
        # Mostra o frame
        self.frame_usuarios.pack(fill=tk.BOTH, expand=True)

        # self.atualizar_usuarios()
        usuario_id = self.get_input("Digite o ID do Usuário:")
        nome = self.get_input("Digite o Nome do Usuário:")
        if usuario_id and nome and self.sistema.adicionar_usuario(usuario_id, nome):
            self.atualizar_usuarios()
            messagebox.showinfo("Sucesso", "Usuário adicionado com sucesso.")
        else:
            messagebox.showerror("Erro", "ID já existe ou dados inválidos.")

        self.frame_usuarios.pack_forget()  # Esconde o Frame

    def atualizar_usuarios(self):
        for row in self.treeusuarios.get_children():
            self.treeusuarios.delete(row)

        usuarios = self.sistema.get_usuarios()
        for usuario in usuarios.values():
            self.treeusuarios.insert("", "end", values=(usuario.get_id_usuario(), usuario.get_nome()))

    def excluir_usuario(self):
        usuario_id = self.get_input("Digite o ID do Usuário a ser excluído:")
        if usuario_id and self.sistema.excluir_usuario(usuario_id):
            self.atualizar_usuarios()
            messagebox.showinfo("Sucesso", f"Usuário {usuario_id} excluído com sucesso.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado ou ID inválido.")




    def atribuir_locker_usuario(self):
        def on_user_select():
            selected_item = tree_users.selection()
            if selected_item:
                usuario_id = tree_users.item(selected_item, "values")[0]
                if self.sistema.associar_locker_ao_usuario(locker_id, usuario_id):
                    messagebox.showinfo("Sucesso", "Locker atribuído com sucesso.")
                    self.atualizar_lockers()
                    user_window.destroy()
                else:
                    messagebox.showerror("Erro", "Erro ao atribuir locker.")
            else:
                messagebox.showerror("Erro", "Nenhum usuário selecionado.")

        locker_id = self.get_input("Digite o ID do Locker:")
        if locker_id and self.sistema.is_locker_livre(locker_id):
            # Cria uma nova janela para selecionar o usuário
            user_window = tk.Toplevel(self.janela)
            user_window.title("Selecionar Usuário")

            # Treeview para exibir os usuários
            tree_users = ttk.Treeview(user_window, columns=("ID", "Nome"), show="headings")
            tree_users.heading("ID", text="ID")
            tree_users.heading("Nome", text="Nome")
            tree_users.pack(fill=tk.BOTH, expand=True)

            # Inserir dados dos usuários na Treeview
            for usuario_id, usuario in self.sistema.get_usuarios().items():
                tree_users.insert("", "end", values=(usuario_id, usuario.get_nome()))

            # Botão para confirmar a seleção do usuário
            btn_select_user = tk.Button(user_window, text="Selecionar", command=on_user_select)
            btn_select_user.pack()

        else:
            messagebox.showerror("Erro", "Locker não disponível.")


    def liberar_locker(self):
        locker_id = self.get_input("Digite o ID do Locker:")
        if locker_id and self.sistema.libera_locker(locker_id):
            messagebox.showinfo("Sucesso", "Locker liberado com sucesso.")
            self.atualizar_lockers()
        else:
            messagebox.showerror("Erro", "Erro ao liberar locker.")

    def verificar_status_locker(self):
        locker_id = self.get_input("Digite o ID do Locker:")
        if locker_id:
            esta_ocupado, usuario_id = self.sistema.get_locker_status(locker_id)
            if esta_ocupado:
                usuario = self.sistema.get_usuario_unico(usuario_id)
                messagebox.showinfo("Status do Locker", f"Locker {locker_id} - Ocupado por Usuário: {usuario_id} - {usuario}")
            else:
                messagebox.showinfo("Status do Locker", "Locker disponível.")
        else:
            messagebox.showerror("Erro", "ID inválido.")

    def salvar_dados(self):
        nome_arquivo = self.get_input("Digite o nome do arquivo para salvar os dados:")
        if nome_arquivo:
            self.sistema.salvar_dados(nome_arquivo)
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
        else:
            messagebox.showerror("Erro", "Nome de arquivo inválido.")

    def carregar_dados(self):
        nome_arquivo = self.get_input("Digite o nome do arquivo para carregar os dados:")
        if nome_arquivo:
            self.sistema.carregar_dados(nome_arquivo)
            messagebox.showinfo("Sucesso", "Dados carregados com sucesso.")
            self.atualizar_lockers()
        else:
            messagebox.showerror("Erro", "Nome de arquivo inválido.")

    def get_input(self, prompt):
        return simpledialog.askstring("Input", prompt)

if __name__ == "__main__":
    janela = tk.Tk()
    app = App(janela)
    janela.mainloop()