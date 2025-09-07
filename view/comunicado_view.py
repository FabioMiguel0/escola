import os
import shutil
import datetime
import json
import flet as ft

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads", "comunicados")
os.makedirs(UPLOAD_DIR, exist_ok=True)
METADATA_FILE = os.path.join(UPLOAD_DIR, "comunicados.json")


def _load_comunicados():
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_comunicados(md):
    try:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(md, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def ComunicadoView(page: ft.Page, user: str = None):
    page.auto_scroll = True

    subject_field = ft.TextField(label="Assunto", width=600)
    message_field = ft.TextField(label="Mensagem", multiline=True, width=600, height=160)
    attach_msg = ft.Text("")
    attached_files_column = ft.Column()
    published_column = ft.Column()

    # attachments staged before publishing
    staged_attachments = []

    def _refresh_attachments():
        attached_files_column.controls.clear()
        for a in staged_attachments:
            attached_files_column.controls.append(
                ft.Row([ft.Text(a["original_name"], expand=True),
                        ft.TextButton("Remover", on_click=lambda e, a=a: _remove_staged(a))])
            )
        page.update()

    def _refresh_published():
        published_column.controls.clear()
        for rec in reversed(_load_comunicados()):
            ts = rec.get("timestamp")
            subj = rec.get("subject")
            msg = rec.get("message")
            author = rec.get("author", "Anonimo")
            atts = rec.get("attachments", [])
            published_column.controls.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Row([ft.Text(subj, weight="bold"), ft.Text(f"{author} — {ts}", size=10)], alignment="spaceBetween"),
                            ft.Text(msg, selectable=True),
                            ft.Column([
                                ft.Row([ft.Text(a, expand=True),
                                        ft.TextButton("Abrir", on_click=lambda e, p=os.path.join(UPLOAD_DIR, a): _open_file(p))])
                                for a in atts
                            ])
                        ],
                        spacing=6
                    ),
                    padding=8,
                    border=ft.border.all(1, ft.Colors.GREY_200)
                )
            )
        page.update()

    def _remove_staged(a):
        try:
            staged_attachments.remove(a)
        except Exception:
            pass
        _refresh_attachments()

    def on_pick_result(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        for f in e.files:
            try:
                stored_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{os.path.basename(f.path)}"
                dest_path = os.path.join(UPLOAD_DIR, stored_name)
                shutil.copyfile(f.path, dest_path)
                staged_attachments.append({"stored_name": stored_name, "original_name": os.path.basename(f.path)})
            except Exception as ex:
                attach_msg.value = f"Erro ao anexar {os.path.basename(f.path)}: {ex}"
        _refresh_attachments()

    file_picker = ft.FilePicker(on_result=on_pick_result)
    page.overlay.append(file_picker)

    def _publish(e):
        subject = (subject_field.value or "").strip()
        message = (message_field.value or "").strip()
        if not subject or not message:
            attach_msg.value = "Assunto e mensagem são obrigatórios."
            page.update()
            return
        recs = _load_comunicados()
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        attachments = [a["stored_name"] for a in staged_attachments]
        rec = {"timestamp": ts, "subject": subject, "message": message, "attachments": attachments, "author": user or "Anonimo"}
        recs.append(rec)
        _save_comunicados(recs)
        subject_field.value = ""
        message_field.value = ""
        staged_attachments.clear()
        attach_msg.value = "Comunicado publicado."
        _refresh_attachments()
        _refresh_published()

    def _open_file(p):
        try:
            os.startfile(p)
        except Exception as ex:
            attach_msg.value = f"Erro: {ex}"
            page.update()

    pick_btn = ft.ElevatedButton("Anexar ficheiros...", on_click=lambda e: file_picker.pick_files(allow_multiple=True))
    publish_btn = ft.ElevatedButton("Publicar comunicado", on_click=_publish)

    header = [ft.Text("Comunicados", size=18, weight="bold"), ft.Divider()]
    if user:
        header.append(ft.Text(f"Usuário: {user}", size=12))

    body = ft.Column(
        header + [
            ft.Row([subject_field]),
            ft.Row([message_field]),
            ft.Row([pick_btn, attach_msg]),
            ft.Row([ft.Text("Ficheiros a anexar:", weight="bold")]),
            attached_files_column,
            ft.Divider(),
            ft.Row([publish_btn]),
            ft.Divider(),
            ft.Text("Comunicados publicados:", weight="bold"),
            published_column,
        ],
        spacing=12,
    )

    _refresh_attachments()
    _refresh_published()
    return ft.Container(content=body, expand=True, padding=16)
