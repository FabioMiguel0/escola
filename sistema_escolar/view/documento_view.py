# filepath: sistema_escolar/view/documento_view.py
import flet as ft

class DocumentoView:
    def __init__(self, page: ft.Page):
        self.page = page
        self.content = self.build_view()

    def build_view(self):
        return ft.Column(
            controls=[
                ft.Text("Documentos", size=24, weight="bold"),
                ft.Divider(),
                # Add controls for document management here
                ft.Text("Aqui você pode gerenciar documentos."),
                ft.ElevatedButton("Adicionar Documento", on_click=self.add_document),
                ft.ElevatedButton("Visualizar Documentos", on_click=self.view_documents),
            ]
        )

    def add_document(self, e):
        # Logic to add a document
        pass

    def view_documents(self, e):
        # Logic to view documents
        pass

    def get_view(self):
        return self.content