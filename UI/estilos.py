import flet as ft

# Paleta de cores moderna
PRIMARY_COLOR = "#6366F1"  # Indigo moderno
PRIMARY_COLOR_DARK = "#4F46E5"
PRIMARY_COLOR_LIGHT = "#A5B4FC"
SECONDARY_COLOR = "#10B981"  # Verde esmeralda
ACCENT_COLOR = "#F59E0B"  # Âmbar
ERROR_COLOR = "#EF4444"  # Vermelho
WARNING_COLOR = "#F59E0B"  # Âmbar
SUCCESS_COLOR = "#10B981"  # Verde

# Cores de fundo
BACKGROUND_COLOR = "#F8FAFC"  # Cinza muito claro
SURFACE_COLOR = "#FFFFFF"  # Branco puro
CARD_COLOR = "#FFFFFF"
SIDEBAR_COLOR = "#1E293B"  # Cinza escuro para sidebar
SIDEBAR_HOVER = "#334155"  # Cinza médio para hover

# Cores de texto
TEXT_PRIMARY = "#0F172A"  # Preto suave
TEXT_SECONDARY = "#64748B"  # Cinza médio
TEXT_MUTED = "#94A3B8"  # Cinza claro
TEXT_WHITE = "#FFFFFF"

# Sombras modernas
SHADOW_SM = ft.BoxShadow(blur_radius=4, color="#00000008", offset=ft.Offset(0, 1))
SHADOW_MD = ft.BoxShadow(blur_radius=8, color="#00000012", offset=ft.Offset(0, 4))
SHADOW_LG = ft.BoxShadow(blur_radius=16, color="#00000016", offset=ft.Offset(0, 8))
SHADOW_XL = ft.BoxShadow(blur_radius=24, color="#00000020", offset=ft.Offset(0, 12))

# Bordas arredondadas
RADIUS_SM = 6
RADIUS_MD = 12
RADIUS_LG = 16
RADIUS_XL = 24

# Espaçamentos
SPACING_XS = 4
SPACING_SM = 8
SPACING_MD = 16
SPACING_LG = 24
SPACING_XL = 32

def titulo(texto): 
    return ft.Text(
        texto, 
        size=28, 
        weight="w700", 
        color=TEXT_PRIMARY,
        font_family="Inter, system-ui, sans-serif"
    )

def subtitulo(texto): 
    return ft.Text(
        texto, 
        size=16, 
        color=TEXT_SECONDARY,
        weight="w500",
        font_family="Inter, system-ui, sans-serif"
    )

def texto_pequeno(texto):
    return ft.Text(
        texto,
        size=12,
        color=TEXT_MUTED,
        font_family="Inter, system-ui, sans-serif"
    )

def card_metric(titulo: str, valor: str, icon, color=PRIMARY_COLOR):
    return ft.Container(
        bgcolor=SURFACE_COLOR,
        border_radius=RADIUS_LG,
        padding=SPACING_LG,
        shadow=SHADOW_MD,
        border=ft.border.all(1, "#E2E8F0"),
        content=ft.Column([
            ft.Row([
                ft.Container(
                    content=ft.Icon(icon, size=24, color=color),
                    bgcolor=f"{color}15",
                    border_radius=RADIUS_MD,
                    padding=SPACING_SM,
                ),
                ft.Text(titulo, size=14, color=TEXT_SECONDARY, weight="w500"),
            ], alignment="spaceBetween"),
            ft.Text(valor, size=32, weight="w800", color=TEXT_PRIMARY),
        ], spacing=SPACING_SM, tight=True),
        width=280,
        height=120,
    )

def card_moderno(titulo: str, conteudo, icon=None, cor=PRIMARY_COLOR):
    """Cria um card moderno com sombra e bordas arredondadas"""
    header = None
    if icon and titulo:
        header = ft.Row([
            ft.Icon(icon, size=20, color=cor),
            ft.Text(titulo, size=18, weight="w600", color=TEXT_PRIMARY),
        ], spacing=SPACING_SM)
    
    return ft.Container(
        bgcolor=SURFACE_COLOR,
        border_radius=RADIUS_LG,
        padding=SPACING_LG,
        shadow=SHADOW_MD,
        border=ft.border.all(1, "#E2E8F0"),
        content=ft.Column([
            header,
            ft.Divider(height=1, color="#E2E8F0") if header else None,
            conteudo,
        ], spacing=SPACING_MD, tight=True) if header else ft.Container(content=conteudo),
    )

def botao_primario(texto, on_click=None, icon=None, width=None):
    """Botão primário moderno"""
    content = []
    if icon:
        content.append(ft.Icon(icon, size=16))
    content.append(ft.Text(texto, weight="w600"))
    
    return ft.ElevatedButton(
        content=ft.Row(content, alignment="center", spacing=SPACING_SM),
        on_click=on_click,
        bgcolor=PRIMARY_COLOR,
        color=TEXT_WHITE,
        elevation=0,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
            padding=ft.padding.symmetric(horizontal=SPACING_LG, vertical=SPACING_MD),
        ),
        width=width,
    )

def botao_secundario(texto, on_click=None, icon=None, width=None):
    """Botão secundário moderno"""
    content = []
    if icon:
        content.append(ft.Icon(icon, size=16))
    content.append(ft.Text(texto, weight="w500"))
    
    return ft.OutlinedButton(
        content=ft.Row(content, alignment="center", spacing=SPACING_SM),
        on_click=on_click,
        color=PRIMARY_COLOR,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=RADIUS_MD),
            padding=ft.padding.symmetric(horizontal=SPACING_LG, vertical=SPACING_MD),
        ),
        width=width,
    )

def input_moderno(label, width=None, **kwargs):
    """Campo de entrada moderno"""
    return ft.TextField(
        label=label,
        width=width,
        border_radius=RADIUS_MD,
        border_color="#D1D5DB",
        focused_border_color=PRIMARY_COLOR,
        label_style=ft.TextStyle(color=TEXT_SECONDARY, weight="w500"),
        text_style=ft.TextStyle(font_family="Inter, system-ui, sans-serif"),
        **kwargs
    )

def sidebar_item(texto, icon, route, current_route, on_click):
    """Item do menu lateral moderno"""
    is_active = route == current_route
    bg_color = PRIMARY_COLOR if is_active else "transparent"
    text_color = TEXT_WHITE if is_active else TEXT_MUTED
    icon_color = TEXT_WHITE if is_active else TEXT_MUTED
    
    return ft.Container(
        content=ft.Row([
            ft.Icon(icon, size=20, color=icon_color),
            ft.Text(texto, color=text_color, weight="w500" if is_active else "w400"),
        ], spacing=SPACING_MD),
        padding=ft.padding.symmetric(horizontal=SPACING_MD, vertical=SPACING_SM),
        border_radius=RADIUS_MD,
        bgcolor=bg_color,
        on_click=lambda e: on_click(route),
        animate=ft.animation.Animation(200, ft.AnimationCurve.EASE_IN_OUT),
    )

def aplicar_tema_moderno(page: ft.Page):
    """Aplica o tema moderno à página"""
    page.theme = ft.Theme(
        color_scheme=ft.ColorScheme(
            primary=PRIMARY_COLOR,
            secondary=SECONDARY_COLOR,
            surface=SURFACE_COLOR,
            background=BACKGROUND_COLOR,
            on_primary=TEXT_WHITE,
            on_secondary=TEXT_WHITE,
            on_surface=TEXT_PRIMARY,
            on_background=TEXT_PRIMARY,
        ),
        text_theme=ft.TextTheme(
            body_large=ft.TextStyle(font_family="Inter, system-ui, sans-serif"),
            body_medium=ft.TextStyle(font_family="Inter, system-ui, sans-serif"),
            title_large=ft.TextStyle(font_family="Inter, system-ui, sans-serif", weight="w700"),
        ),
    )
