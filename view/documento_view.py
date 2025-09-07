import os
import shutil
import datetime
import json
import flet as ft

UPLOAD_DIR = os.path.join(os.path.dirname(__file__), "..", "uploads", "documentos")
os.makedirs(UPLOAD_DIR, exist_ok=True)
METADATA_FILE = os.path.join(UPLOAD_DIR, "metadata.json")


def _load_metadata():
    try:
        with open(METADATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []


def _save_metadata(md):
    try:
        with open(METADATA_FILE, "w", encoding="utf-8") as f:
            json.dump(md, f, ensure_ascii=False, indent=2)
    except Exception:
        pass


def DocumentoView(page: ft.Page, user: str = None, role: str = None, user_id: int = None):
    page.auto_scroll = True

    msg = ft.Text("")
    desc_field = ft.TextField(label="Descrição", multiline=True, width=600)
    files_column = ft.Column()
    recipient_dropdown = None
    recipients = []  # list of dicts: {"value": id, "label": name, "type": "turma"|"admin"}
    info = ft.Text("")

    # staged attachments (antes de enviar)
    staged_attachments = []
    staged_column = ft.Column()

    # --- obter todas as turmas (fallbacks para nomes de função possíveis) ---
    all_turmas = []
    try:
        from services.turma_service import list_turmas
        all_turmas = list_turmas()
    except Exception:
        try:
            from services.turma_service import get_all_turmas
            all_turmas = get_all_turmas()
        except Exception:
            try:
                from services.turma_service import turmas_all
                all_turmas = turmas_all()
            except Exception:
                all_turmas = []

    # normaliza lista de turmas -> dicts (id,label)
    normalized_turmas = []
    for t in all_turmas:
        if isinstance(t, dict):
            tid = t.get("id") or t.get("turma_id")
            name = t.get("nome") or t.get("name") or t.get("label") or str(tid)
        elif isinstance(t, (list, tuple)) and len(t) >= 2:
            tid, name = t[0], t[1]
        else:
            tid, name = getattr(t, "id", None), str(t)
        if tid is not None:
            normalized_turmas.append({"id": str(tid), "label": str(name)})

    # --- obter turmas do professor (ids) para validar permissões ---
    prof_turma_ids = []
    if role == "professor":
        try:
            from services.turma_service import turmas_por_professor
            turmas_prof = turmas_por_professor(user_id)
            for t in turmas_prof:
                if isinstance(t, dict):
                    tid = t.get("id") or t.get("turma_id")
                elif isinstance(t, (list, tuple)) and len(t) >= 1:
                    tid = t[0]
                else:
                    tid = getattr(t, "id", None)
                if tid is not None:
                    prof_turma_ids.append(str(tid))
        except Exception:
            # se falhar, deixamos prof_turma_ids vazio (nenhuma turma autorizada)
            prof_turma_ids = []

    # --- construir recipients conforme role ---
    if role == "admin":
        # admin pode enviar para qualquer turma — lista todas as turmas
        for t in normalized_turmas:
            recipients.append({"value": t["id"], "label": t["label"], "type": "turma"})
        if not recipients:
            info.value = "Aviso: não foi possível carregar turmas."
        recipient_dropdown = ft.Dropdown(label="Enviar para Turma", options=[ft.dropdown.Option(r["value"], r["label"]) for r in recipients]) if recipients else None

    elif role == "professor":
        # professor: oferecer apenas suas turmas + opção 'Administração'
        for t in normalized_turmas:
            if str(t["id"]) in prof_turma_ids:
                recipients.append({"value": t["id"], "label": t["label"], "type": "turma"})
        # adicionar opção para enviar ao admin
        recipients.append({"value": "admin", "label": "Administração", "type": "admin"})
        if not recipients:
            info.value = "Aviso: não foi possível carregar as suas turmas. Só Administração disponível."
        recipient_dropdown = ft.Dropdown(label="Destinatário", options=[ft.dropdown.Option(r["value"], r["label"]) for r in recipients]) if recipients else None
        # auto selecionar se apenas 1 real opção de turma + admin => deixar professor escolher, não auto-select
        if recipient_dropdown and len(recipients) == 1:
            recipient_dropdown.value = recipients[0]["value"]

    else:
        # outros papéis: não permitem envio (apenas visualização)
        recipient_dropdown = None

    # helpers para filtragem por visualização
    def _get_aluno_turma_id():
        try:
            from services.aluno_service import turma_por_aluno
            tid = turma_por_aluno(user_id)
            return str(tid) if tid is not None else None
        except Exception:
            return None

    def _allowed_entries():
        all_entries = _load_metadata()
        if role == "admin":
            return all_entries  # admin vê tudo
        if role == "professor":
            allowed = []
            for e in all_entries:
                rtype = e.get("recipient_type")
                rid = str(e.get("recipient_id")) if e.get("recipient_id") is not None else None
                if rtype == "professor" and rid == str(user_id):
                    allowed.append(e)
                elif rtype == "turma" and rid in prof_turma_ids:
                    allowed.append(e)
                elif rtype == "admin" and e.get("recipient_id") == "admin":
                    # docs sent to admin are visible to professors? skip by default
                    pass
            return allowed
        if role == "aluno":
            allowed = []
            aluno_tid = _get_aluno_turma_id()
            for e in all_entries:
                if e.get("recipient_type") == "turma" and str(e.get("recipient_id")) == aluno_tid:
                    allowed.append(e)
            return allowed
        return []

    def _refresh_files():
        files_column.controls.clear()
        entries = list(reversed(_allowed_entries()))
        if not entries:
            files_column.controls.append(ft.Text("Nenhum documento disponível.", italic=True))
        for entry in entries:
            orig = entry.get("original_name")
            desc = entry.get("description", "")
            ts = entry.get("timestamp", "")
            author = entry.get("author", "Anonimo")
            rtype = entry.get("recipient_type", "")
            rname = entry.get("recipient_name", "")
            stored = entry.get("stored_name")
            path = os.path.join(UPLOAD_DIR, stored) if stored else None
            open_btn = ft.TextButton("Abrir", on_click=lambda e, p=path: _open_file(p) if p else None)
            files_column.controls.append(
                ft.Column(
                    [
                        ft.Row([ft.Text(orig or stored, expand=True), ft.Text(f"{author} — {ts}", size=10)], alignment="spaceBetween"),
                        ft.Row([ft.Text(f"Para: {rname} ({rtype})", size=12), open_btn]),
                        ft.Text(desc, selectable=True, size=12),
                        ft.Divider()
                    ],
                    spacing=6
                )
            )
        page.update()

    def _refresh_staged():
        staged_column.controls.clear()
        for s in staged_attachments:
            staged_column.controls.append(
                ft.Row([ft.Text(s["original_name"], expand=True), ft.Text(str(s.get("size", "")), size=10), ft.TextButton("Remover", on_click=lambda e, s=s: _remove_staged(s))])
            )
        page.update()

    def _remove_staged(item):
        try:
            staged_attachments.remove(item)
        except Exception:
            pass
        _refresh_staged()

    # ao escolher ficheiros, só faz stage (a cópia só acontece ao enviar)
    def on_pick_result(e: ft.FilePickerResultEvent):
        if not e.files:
            return
        for f in e.files:
            try:
                staged_attachments.append({"path": f.path, "original_name": os.path.basename(f.path), "size": f.size})
            except Exception as ex:
                msg.value = f"Erro ao adicionar {os.path.basename(getattr(f,'path',str(f)))}: {ex}"
        _refresh_staged()

    # envia os ficheiros staged: copia e grava metadados
    def _send_staged(e):
        if not staged_attachments:
            msg.value = "Nenhum ficheiro selecionado para envio."
            page.update()
            return
        if role not in ("admin", "professor"):
            msg.value = "Só administradores e professores podem enviar documentos."
            page.update()
            return
        if not recipients:
            msg.value = "Nenhum destinatário disponível."
            page.update()
            return
        selected_option = None
        if recipient_dropdown and recipient_dropdown.value:
            selected_option = next((r for r in recipients if r["value"] == recipient_dropdown.value), None)
        if not selected_option:
            msg.value = "Selecione um destinatário antes de enviar."
            page.update()
            return

        # valida professor: só permite suas turmas ou admin
        if role == "professor" and selected_option["type"] == "turma" and str(selected_option["value"]) not in prof_turma_ids:
            msg.value = "Não autorizado: só pode enviar para as turmas que leciona."
            page.update()
            return

        md = _load_metadata()
        saved = []
        for s in staged_attachments:
            try:
                ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                stored_name = f"{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{s['original_name']}"
                dest_path = os.path.join(UPLOAD_DIR, stored_name)
                shutil.copyfile(s["path"], dest_path)
                entry = {
                    "stored_name": stored_name,
                    "original_name": s["original_name"],
                    "description": desc_field.value or "",
                    "timestamp": ts,
                    "author": user or "Anonimo",
                    "recipient_type": selected_option["type"],
                    "recipient_id": selected_option["value"],
                    "recipient_name": selected_option["label"],
                }
                md.append(entry)
                saved.append(stored_name)
            except Exception as ex:
                msg.value = f"Erro ao salvar {s['original_name']}: {ex}"
        if saved:
            _save_metadata(md)
            msg.value = f"Ficheiros enviados: {', '.join(saved)}"
            desc_field.value = ""
            staged_attachments.clear()
            _refresh_staged()
            _refresh_files()
        page.update()

    file_picker = ft.FilePicker(on_result=on_pick_result)
    page.overlay.append(file_picker)

    def _open_file(path):
        try:
            if path:
                os.startfile(path)
        except Exception as ex:
            msg.value = f"Não foi possível abrir: {ex}"
            page.update()

    pick_btn = ft.ElevatedButton("Escolher ficheiros...", on_click=lambda e: file_picker.pick_files(allow_multiple=True))
    send_btn = ft.ElevatedButton("Enviar documentos", on_click=_send_staged)

    controls = [ft.Text("Documentos", size=18, weight="bold"), ft.Divider(), ft.Row([desc_field])]
    if recipient_dropdown:
        controls.append(ft.Row([recipient_dropdown]))
    else:
        if role in ("admin", "professor"):
            controls.append(ft.Text("Nenhum destinatário disponível.", color=ft.Colors.RED))
        else:
            controls.append(ft.Text("Só administradores e professores podem enviar documentos.", color=ft.Colors.GREY))
    controls += [ft.Row([pick_btn, send_btn, msg]), info, ft.Divider(), ft.Text("Ficheiros seleccionados para envio:", weight="bold"), staged_column, ft.Divider(), ft.Text("Ficheiros carregados:", weight="bold"), files_column]

    container = ft.Container(content=ft.Column(controls, spacing=12), padding=16, expand=True)

    _refresh_staged()
    _refresh_files()
    return container


