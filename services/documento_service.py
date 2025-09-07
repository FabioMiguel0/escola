from models.documento import Documento

class DocumentoService:
    def __init__(self):
        self.documentos = []

    def emitir_documento(self, documento: Documento):
        self.documentos.append(documento)

    def editar_documento(self, id_documento, **kwargs):
        for doc in self.documentos:
            if doc.id_documento == id_documento:
                for chave, valor in kwargs.items():
                    setattr(doc, chave, valor)

    def excluir_documento(self, id_documento):
        self.documentos = [d for d in self.documentos if d.id_documento != id_documento]

    def listar_documentos_por_aluno(self, aluno_id):
        return [d for d in self.documentos if d.aluno_id == aluno_id]
