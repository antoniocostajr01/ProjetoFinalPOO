import customtkinter as ctk
from tkinter import messagebox

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


class Usuario:
    def __init__(self, nome, id_usuario):
        self.__usuario_id = id_usuario
        self.__nome = nome

    def get_usuario_id(self):
        return self.__usuario_id 

    def get_nome(self):
        return self.__nome 


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

     def adicionar_usuario(self, usuario_id, nome):
          if usuario_id not in self.__usuarios:
               self.__usuarios[usuario_id] = Usuario(nome, usuario_id)
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

     def libera_locker(self, locker_id):
          if locker_id in self.__lockers:
               return self.__lockers[locker_id].liberar_usuario()
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

     def carregar_dados(self,nome_arquivo): 
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
          return self.__usuarios[usuario_id].get_nome()

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
                    self.status_label.configure(text=f"Locker {locker_id} está livre.")
                else:
                    usuario_nome = self.sistema_locker.get_usuario_unico(usuario_id)
                    self.status_label.configure(text=f"Locker {locker_id} está ocupado por {usuario_nome}.")
            else:
                self.status_label.configure(text="Locker não encontrado.")
        else:
            self.status_label.configure(text="ID do Locker inválido.")

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

# Programa principal
if __name__ == "__main__":
    sistema_locker = SistemaLocker()
    sistema_locker.carregar_lockers()
    # sistema_locker.adicionar_locker(100)
    print(sistema_locker.get_locker_status(100))
    app = LockerApp(sistema_locker)
    app.mainloop()
