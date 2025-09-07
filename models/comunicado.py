class Comunicado:
    def __init__(self, id_comunicado, titulo, mensagem, data_envio, destinatarios):
        self.id_comunicado = id_comunicado
        self.titulo = titulo
        self.mensagem = mensagem
        self.data_envio = data_envio
        self.destinatarios = destinatarios  # lista de IDs de alunos/pais
