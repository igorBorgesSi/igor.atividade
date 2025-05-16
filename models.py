import sqlite3
import os
from werkzeug.security import generate_password_hash, check_password_hash

# Caminho para o banco de dados
DB_PATH = 'data/laticinios.db'

# Função para garantir que a pasta 'data' exista
def ensure_data_dir():
    os.makedirs('data', exist_ok=True)  # Cria a pasta 'data' se não existir

# Função para obter uma conexão com o banco de dados
def get_db_connection():
    ensure_data_dir()  # Garante que a pasta 'data' existe
    conn = sqlite3.connect(DB_PATH)  # Conecta ao banco de dados SQLite
    conn.row_factory = sqlite3.Row  # Permite acessar colunas por nome
    return conn

# Função para inicializar o banco de dados
def init_db():
    ensure_data_dir()  # Garante que a pasta 'data' existe
    db_exists = os.path.exists(DB_PATH)  # Verifica se o banco de dados já existe
    conn = get_db_connection()  # Obtém uma conexão com o banco

    # Lê o arquivo schema.sql com codificação UTF-8
    try:
        with open('schema.sql', 'r', encoding='utf-8') as f:
            schema = f.read()  # Lê o conteúdo do arquivo
        conn.executescript(schema)  # Executa o script SQL para criar as tabelas
    except FileNotFoundError:
        raise Exception("Erro: schema.sql não encontrado no diretório do projeto")
    except sqlite3.DatabaseError as e:
        raise Exception(f"Erro ao executar schema.sql: {str(e)}")

    if not db_exists:
        popular_dados_iniciais()  # Popula dados iniciais se o banco for novo

    conn.commit()  # Confirma as alterações
    conn.close()  # Fecha a conexão

# Função para popular o banco com dados iniciais
def popular_dados_iniciais():
    # Cria um usuário administrador padrão
    Usuario.criar("admin", "admin123", "admin", "Administrador do Sistema")

# Classe para representar um usuário
class Usuario:
    def __init__(self, id_usuario, username, password_hash, funcao, nome):
        self.id_usuario = id_usuario  # ID do usuário
        self.username = username  # Nome de usuário
        self.password_hash = password_hash  # Hash da senha
        self.funcao = funcao  # Função do usuário (ex.: admin, gerente)
        self.nome = nome  # Nome completo do usuário

    # Método estático para criar um novo usuário
    @staticmethod
    def criar(username, senha, funcao, nome):
        password_hash = generate_password_hash(senha)  # Gera o hash da senha
        conn = get_db_connection()  # Obtém uma conexão com o banco
        cursor = conn.execute(
            'INSERT INTO usuarios (username, password_hash, funcao, nome) VALUES (?, ?, ?, ?)',
            (username, password_hash, funcao, nome)
        )  # Insere o usuário na tabela
        conn.commit()  # Confirma a inserção
        conn.close()  # Fecha a conexão
        return cursor.lastrowid  # Retorna o ID do usuário criado

    # Método estático para autenticar um usuário
    @staticmethod
    def autenticar(username, senha):
        conn = get_db_connection()  # Obtém uma conexão com o banco
        user = conn.execute(
            'SELECT id_usuario, username, password_hash, funcao, nome FROM usuarios WHERE username = ?',
            (username,)
        ).fetchone()  # Busca o usuário pelo username
        conn.close()  # Fecha a conexão
        # Verifica se o usuário existe e se a senha está correta
        if user and check_password_hash(user['password_hash'], senha):
            return Usuario(
                user['id_usuario'], user['username'], user['password_hash'], user['funcao'], user['nome']
            )  # Retorna um objeto Usuario se autenticado
        return None  # Retorna None se a autenticação falhar

    # Método estático para obter um usuário pelo username
    @staticmethod
    def obter_por_username(username):
        conn = get_db_connection()  # Obtém uma conexão com o banco
        user = conn.execute(
            'SELECT id_usuario, username, password_hash, funcao, nome FROM usuarios WHERE username = ?',
            (username,)
        ).fetchone()  # Busca o usuário pelo username
        conn.close()  # Fecha a conexão
        if user:
            return Usuario(
                user['id_usuario'], user['username'], user['password_hash'], user['funcao'], user['nome']
            )  # Retorna um objeto Usuario se encontrado
        return None  # Retorna None se o usuário não for encontrado
    #classe para representar uma area de armazenamento
    class Area:
         def __init__(self, id_area, nome, descricao):
        self.id_area = id_area  # ID do area
        self.nome = nome  # Nome de area
        self.descricao = descricao  # descricao da area
    
    # Método estático para criar um novo usuário
    @staticmethod
    def criar(id_area, nome, descricao:
        conn = get_db_connection()  # Obtém uma conexão com o banco
        try:
            cursor = conn.execute(
            'INSERT INTO areas_armazen (id_area, nome, descricao) VALUES (?, ?, ?, ?)',
            (id_area, nome, descricao)
            )  # Insere o usuário na tabela
            conn.commit()  # Confirma a inserção
            return True
        except sqlite3.IntegrityError:
            return False
        finally:
            conn.close()  # Fecha a conexão
    @staticmethod
    def listar_todas():
         conn = get_db_connection()
         areas = conn.excute(
             'SELECT * FROM area_armazen ORDER BY nome',).fetchall()
            conn.close()
            return [Area(a['id_area'], a['descricao']) 
            for a in areas]
        @staticmethod
        def obter_por_id(id_area):
             conn = get_db_connection()
             area = conn.excute('SELECT FROM areas.armazem WERE id_area = ?', (id_areas,)).fetchome()
             conn.close()

             if area:
                 return Area(area['id_area'], area[nome], area['descricao'])
            return Nome 

    @staticmethod
        def atualizar(id_area, nome, descricao):
             conn = get_db_connection()
             conn.execute('UPDATE areas.armazem SET nome = ?, descricao = ? WERE id_area = ?', (nome, descricao, id_area))
             conn.commit()
             conn.close()

    @staticmethod
    def excluir(id_area):
            conn = get_db_connection()
            # verificar se há produtos nesta área
            produtos = conn.execute('SELECT COUNT(*)as count FROM produtos_areas WERE area_id = ?'
                                    (id_area,)).fetchome()
                                    if produtos['count'] > 0:
                                        conn.close 
                                        return False
                                    
                                    conn.execute('DELE FROM area_armazen WERE id_area = ?', (id_area,))
                                    conn.commit()
                                    conn.close()
                                    return true
                                    

            

        
