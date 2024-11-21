import customtkinter as ctk
from tkinter import messagebox, ttk

class Locker:
     """
     Essa classe vai receber como paramêtro o ID do Locker.
     Ela possui métodos os seguintes métodos:
     - associar_usuário: Associa o ID Usuário ao Locker livre
     - liberar_usuario: Libera o Locker e reseta o ID do Usuário do Locker
     - get_status: Retorna o status de ocupação do Locker e o ID do usuário
     - get_locker_id: Retorna o ID do Locker
     """
     def __init__(self,locker_id, is_livre = True, usuario_id = None):
          self.__locker_id = locker_id
          self.__is_livre = is_livre
          self.__usuario_id = usuario_id
     
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
          id, livre = [self.__usuario_id, self.__is_livre]
          return id, livre

     def get_locker_id(self):
          return self.__locker_id
     
     def get_locker_livre(self):
          return self.__is_livre
     
     def get_usuario_id(self):
          return self.__usuario_id

class pessoa:
    def __init__(self,nome):
        self.__nome = nome 

    def get_nome(self):
        return self.__nome 

class Usuario(pessoa):
    def __init__(self, nome, id_usuario):
        self.__usuario_id = id_usuario
        super().__init__(nome)

    def get_usuario_id(self):
        return self.__usuario_id 

class SistemaLocker:
     def __init__(self, locker_arq = 'lockers.txt'):
          self.__lockers = {}
          self.__usuarios = {}
          self.__locker_arq = locker_arq

     def adicionar_locker(self, locker_id):
          """
          Este método adiciona um locker, mas antes ele verifica se 
          o locker adicionado já não está na lista, caso não esteja
          executa o método e retorna True, caso esteja não executa e
          retorna False
          """
          if locker_id not in self.__lockers:
               self.__lockers[locker_id] = Locker(locker_id)
               self.salvar_locker(self.__lockers[locker_id])
               return True
          return False
     
     def excluir_locker(self, locker_id):
        """
        Este método verifica se o usuario_id existe na lista de
        locker, se sim ele exclui e atualiza o arquivo e retorna 
        True, se não retorna False.
        """
        if locker_id in self.__lockers:
            del self.__lockers[locker_id]
            self.atualizar_dados()
            return True
        return False

     def adicionar_usuario(self, usuario_id, nome):
        """
        Este método verifica se o usuario_id já existe na lista de
        usuário, se não ele adiciona e retorna True, se não retorna 
        False.
        """
        if usuario_id not in self.__usuarios:
            self.__usuarios[usuario_id] = Usuario(nome, usuario_id)
            return True
        return False

     def excluir_usuario(self, usuario_id):
        """
        Este método verifica se o usuario_id existe na lista de
        usuário, se sim ele exclui e atualiza o arquivo e retorna 
        True, se não retorna False.
        """
        if usuario_id in self.__usuarios:
            del self.__usuarios[usuario_id]
            self.atualizar_dados()
            return True
        return False

     def associar_locker_ao_usuario(self, locker_id, usuario_id):
          """
          Esta função associa locker a usuário, apenas se o id do locker
          e o id de usuário forem encontrados na lista. Se não forem
          encontrados, retorna False.
          """
          if locker_id in self.__lockers and usuario_id in self.__usuarios:
               if self.__lockers[locker_id].associar_usuario(usuario_id):
                    self.atualizar_dados()
                    return True
          return False

     def liberar_locker(self, locker_id):
          if locker_id in self.__lockers:
               resultado = self.__lockers[locker_id].liberar_usuario()
               self.atualizar_dados()
               return resultado
          return False

     def get_locker_status(self, locker_id):
          if locker_id in self.__lockers:
               return self.__lockers[locker_id].get_status()
          return None
     
     def is_locker_livre(self, locker_id):
          return locker_id in self.__lockers and not self.__lockers[locker_id].get_locker_livre()

     def salvar_locker(self, locker):
          with open(self.__locker_arq, 'a') as arquivo:
               arquivo.write(f'{locker.get_locker_id()},{locker.get_locker_livre()},{locker.get_usuario_id()}\n')

     def carregar_lockers(self):
          try:
               with open(self.__locker_arq, 'r') as arquivo:
                    for linha in arquivo:
                         locker_id, locker_livre, locker_usuario = linha.strip().split(',')
                         self.__lockers[locker_id] = Locker(locker_id, locker_livre == 'True', locker_usuario if locker_usuario != 'None' else None)
          except FileNotFoundError:
               pass
     
     def atualizar_dados(self):
          with open(self.__locker_arq, 'w') as arquivo:
               for locker_id, locker in self.__lockers.items():
                    is_livre, usuario_id = locker.get_locker_livre(), locker.get_usuario_id()
                    arquivo.write(f'{locker_id},{is_livre},{usuario_id}\n')

     def salvar_dados(self, nome_arquivo):
          with open(nome_arquivo, 'w') as arquivo:
               for locker_id, locker in self.__lockers.items():
                    is_livre, usuario_id = locker.get_locker_livre(), locker.get_usuario_id()
                    arquivo.write(f'{locker_id},{is_livre},{usuario_id}\n')

     def carregar_dados(self, nome_arquivo): 
          try:
               with open(nome_arquivo, 'r') as arquivo:
                    for linha in arquivo:
                         locker_id, is_livre, usuario_id = linha.strip().split(',')
                         self.adicionar_locker(locker_id)
                    if is_livre == 'False':
                         self.associar_locker_ao_usuario(locker_id, usuario_id)
          except FileNotFoundError:
               pass

     def usuario_cadastrado(self, usuario_id):
          return usuario_id in self.__usuarios

     def get_usuario_unico(self, usuario_id):
          if(usuario_id in self.__usuarios):  
            return self.__usuarios[usuario_id].get_nome()
          return "N/A"
     
     def get_lockers(self):
          return self.__lockers

# Função para criar a interface gráfica
class LockerApp(ctk.CTk):
    def __init__(self, sistema_locker):
        super().__init__()

        self.sistema_locker = sistema_locker
        self.title("Sistema de Lockers")
        self.geometry("400x600")

        # Criação do menu
        self.menu_frame = ctk.CTkFrame(self)
        self.menu_frame.pack(pady=20)

        self.add_locker_button = ctk.CTkButton(self.menu_frame, text="Adicionar Locker", command=self.adicionar_locker)
        self.add_locker_button.grid(row=0, column=0, padx=10, pady=10)

        self.del_locker_button = ctk.CTkButton(self.menu_frame, text="Excluir Locker", command=self.excluir_locker)
        self.del_locker_button.grid(row=1, column=0, padx=10, pady=10)

        self.add_user_button = ctk.CTkButton(self.menu_frame, text="Adicionar Usuário", command=self.adicionar_usuario)
        self.add_user_button.grid(row=2, column=0, padx=10, pady=10)

        self.del_user_button = ctk.CTkButton(self.menu_frame, text="Excluir Usuário", command=self.excluir_usuario)
        self.del_user_button.grid(row=3, column=0, padx=10, pady=10)

        self.associar_button = ctk.CTkButton(self.menu_frame, text="Associar Locker", command=self.associar_locker)
        self.associar_button.grid(row=4, column=0, padx=10, pady=10)

        self.liberar_button = ctk.CTkButton(self.menu_frame, text="Liberar Locker", command=self.liberar_locker)
        self.liberar_button.grid(row=5, column=0, padx=10, pady=10)

        self.salvar_button = ctk.CTkButton(self.menu_frame, text="Salvar dados", command=self.salvar_dados)
        self.salvar_button.grid(row=6, column=0, padx=10, pady=10)

        self.carregar_button = ctk.CTkButton(self.menu_frame, text="Carregar Dados", command=self.carregar_dados)
        self.carregar_button.grid(row=7, column=0, padx=10, pady=10)

        self.check_status_button = ctk.CTkButton(self.menu_frame, text="Ver Status Locker", command=self.check_status)
        self.check_status_button.grid(row=8, column=0, padx=10, pady=10)

        #Espaço de exibição dos lockers e usuários
        self.frame_lockers = ctk.CTkFrame(self, corner_radius=10)
        self.frame_lockers.pack(fill=ctk.BOTH, expand=True)

        # Treeview para exibição dos lockers
        self.tree_lockers = ttk.Treeview(self.frame_lockers, columns=("ID", "Status"), show="headings")
        self.tree_lockers.heading("ID", text="ID")
        self.tree_lockers.heading("Status", text="Status")
        self.tree_lockers.pack(fill=ctk.BOTH, expand=True)

        #Frame para users
        self.frame_usuarios = ctk.CTkFrame(self, border_color="blue", border_width=2, corner_radius=10)

     #Treeview para exibir os usuários
        self.treeusuarios = ttk.Treeview(self.frame_usuarios, columns=("ID", "Nome"), show="headings")
        self.treeusuarios.heading("ID", text="ID")
        self.treeusuarios.heading("Nome", text="Nome")
        self.treeusuarios.pack(fill=ctk.BOTH, expand=True)
        self.atualizar_lockers()
     
    def atualizar_lockers(self):
        for row in self.tree_lockers.get_children():
            self.tree_lockers.delete(row)
        lockers = self.sistema_locker.get_lockers()
        if lockers:
            for locker_id, locker in lockers.items():
                status = "Livre" if locker.get_locker_livre() else "Ocupado"
                usuario = "N/A" if locker.get_locker_livre() else locker.get_usuario_id()
                self.tree_lockers.insert("", "end", values=(locker_id, status, usuario))
        else:
            self.tree_lockers.insert("", "end", values=("Nenhum locker cadastrado", "", ""))
    

    def adicionar_locker(self):
        locker_id = self.prompt_input("Digite o ID do Locker:")
        if locker_id:
            success = self.sistema_locker.adicionar_locker(locker_id)
            if success:
                self.atualizar_lockers() # atualiza a tabela do app
                messagebox.showinfo("Sucesso", f"Locker {locker_id} adicionado com sucesso!")
            else:
                messagebox.showerror("Erro", f"Locker {locker_id} já existe.")
        else:
            messagebox.showerror("Erro", "ID do Locker inválido.")

    def excluir_locker(self):
        locker_id = self.prompt_input("Digite o ID do Locker a ser excluído:")
        if locker_id and self.sistema_locker.excluir_locker(locker_id):
            self.atualizar_lockers() # atualiza a tabela do app
            messagebox.showinfo("Sucesso", f"Locker {locker_id} excluído com sucesso.")
        else:
            messagebox.showerror("Erro", "Locker não encontrado ou ID inválido.")

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

    def excluir_usuario(self):
        usuario_id = self.prompt_input("Digite o ID do Usuário a ser excluído:")
        if usuario_id and self.sistema_locker.excluir_usuario(usuario_id):
            messagebox.showinfo("Sucesso", f"Usuário {usuario_id} excluído com sucesso.")
        else:
            messagebox.showerror("Erro", "Usuário não encontrado ou ID inválido.")

    def associar_locker(self):
        locker_id = self.prompt_input("Digite o ID do Locker:")
        usuario_id = self.prompt_input("Digite o ID do Usuário:")
        if locker_id and usuario_id:
            success = self.sistema_locker.associar_locker_ao_usuario(locker_id, usuario_id)
            if success:
                self.atualizar_lockers() # atualiza a tabela do app
                messagebox.showinfo("Sucesso", f"Locker {locker_id} associado ao Usuário {usuario_id} com sucesso!")
            else:
                messagebox.showerror("Erro", "Falha ao associar Locker ao Usuário.")
        else:
            messagebox.showerror("Erro", "ID do Locker ou Usuário inválido.")

    def liberar_locker(self):
        locker_id = self.prompt_input("Digite o ID do Locker a ser liberado:")
        if locker_id and self.sistema_locker.liberar_locker(locker_id):
            self.atualizar_lockers() # atualiza a tabela do app
            messagebox.showinfo("Sucesso", f"Locker {locker_id} liberado com sucesso.")
        else:
            messagebox.showerror("Erro", "Locker não encontrado ou ID inválido.")

    def check_status(self):
        locker_id = self.prompt_input("Digite o ID do Locker:")
        if locker_id:
            status = self.sistema_locker.get_locker_status(locker_id)
            if status:
                usuario_id, is_livre = status
                if is_livre:
                    messagebox.showinfo("Status do Locker", f"Locker {locker_id} está livre.")
                else:
                    usuario_nome = self.sistema_locker.get_usuario_unico(usuario_id)
                    messagebox.showinfo("Status do Locker", f"Locker {locker_id} está ocupado por {usuario_nome}.")
            else:
                messagebox.showerror("Erro", "Locker não encontrado.")
        else:
            messagebox.showerror("Erro", "ID do Locker inválido.")

    def prompt_input(self, prompt):
        input_window = ctk.CTkToplevel(self)
        input_window.title("Entrada de Dados")
        input_window.geometry("300x150")

        label = ctk.CTkLabel(input_window, text=prompt)
        label.pack(pady=10)

        entry = ctk.CTkEntry(input_window)
        entry.pack(pady=5)
        botao_clicado = ctk.BooleanVar()


        def submit():
            # mudar a variável para o .wait_variable executar o resto do código
            botao_clicado.set(True)

        submit_button = ctk.CTkButton(input_window, text="Submeter", command=submit)
        submit_button.pack(pady=5)

        self.wait_variable(botao_clicado)  # Aguarda a entrada do usuário
        # Depois que o botão foi clicado, executar código abaixo

        resultado = entry.get() # recuperar valor do input
        input_window.destroy() # destruir janela

        return resultado

    def salvar_dados(self):
        nome_arquivo = self.prompt_input("Digite o nome do arquivo para salvar os dados:")
        if nome_arquivo:
            self.sistema_locker.salvar_dados(nome_arquivo)
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
        else:
            messagebox.showerror("Erro", "Nome de arquivo inválido.")

    def carregar_dados(self):
        nome_arquivo = self.prompt_input("Digite o nome do arquivo para salvar os dados:")
        if nome_arquivo:
            self.sistema_locker.carregar_dados(nome_arquivo)
            self.atualizar_lockers()
            messagebox.showinfo("Sucesso", "Dados salvos com sucesso.")
        else:
            messagebox.showerror("Erro", "Nome de arquivo inválido.")

# Programa principal
if __name__ == "__main__":
    sistema_locker = SistemaLocker()
    sistema_locker.carregar_lockers()
    app = LockerApp(sistema_locker)
    app.mainloop()