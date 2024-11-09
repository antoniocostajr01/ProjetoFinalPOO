# Classe-> Locker: Representa um Armário individual.
# Atributos: __locker_id, __is_ocupado, __usuario_id.
# Métodos: associar_usuario(usuario_id), liberar_usuario(), get_status(), get_locker_id().

class Locker:
     """
     Essa classe vai receber como paramêtro o ID do Locker.
     Ela possui métodos os seguintes métodos:
     - associar_usuário: Associa o ID Usuário ao Locker livre
     - liberar_usuario: Libera o Locker e reseta o ID do Usuário do Locker
     - get_status: Retorna o status de ocupação do Locker e o ID do usuário
     - get_locker_id: Retorna o ID do Locker
     """
     def __init__(self,locker_id):
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
          id, livre = [self.__usuario_id, self.__is_livre]
          return id, livre

     def get_locker_id(self):
          return self.__locker_id
     
     def get_locker_livre(self):
          return self.__is_livre
     
     def get_usuario_id(self):
          return self.__usuario_id


# Classe-> Usuario: Representa um usuário do sistema.
# Atributos: __usuario_id, __nome.
# Métodos: get_usuario_id(), get_nome().
class Usuario:
     """
     Esta classe vai receber dois paramêtros, sendo eles nome do usuário e ID
     Possui os seguintes métodos:
     - get_usuario_id: Retorna o ID do usuário
     - get_nome: Retorna o nome do usuário
     """

     def __init__(self, nome, id_usuario):
          self.__usuario_id = id_usuario
          self.__nome = nome

     def get_usuario_id(self):
          return self.__usuario_id 

     def get_nome(self):
          return self.__nome 

#   Classe-> SistemaLocker: Gerencia os lockers e os usuários.
# Atributos: __lockers, __usuarios, __locker_arq.
# Métodos: adicionar_locker(locker_id), adicionar_usuario(usuario_id, nome), 
# associar_locker_ao_usuario(locker_id, usuario_id), liberar_locker(locker_id), 
# get_locker_status(locker_id), salvar_locker(locker_id), carregar_lockers(), 
# salvar_dado(nome_arquivo), carregar_dados(nome_arquivo).
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


#Programa Principal
sistemaLocker = SistemaLocker()
sistemaLocker.adicionar_locker(50)
sistemaLocker.adicionar_usuario(1, "Antonio")
sistemaLocker.associar_locker_ao_usuario(50, 1)
sistemaLocker.salvar_dados("teste.txt")

