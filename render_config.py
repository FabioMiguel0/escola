import os
import sys

# Configurações específicas para Render.com
def configure_for_render():
    """Configurações específicas para o ambiente Render.com"""
    
    # Configurações de ambiente
    os.environ.setdefault('RENDER', 'true')
    os.environ.setdefault('FLET_WEB', 'true')
    
    # Configurações de performance
    os.environ.setdefault('PYTHONUNBUFFERED', '1')
    os.environ.setdefault('PYTHONDONTWRITEBYTECODE', '1')
    
    # Configurações de segurança
    os.environ.setdefault('SECURE_SSL_REDIRECT', 'true')
    
    # Configurações de CORS
    os.environ.setdefault('CORS_ALLOW_ALL_ORIGINS', 'true')
    os.environ.setdefault('CORS_ALLOW_CREDENTIALS', 'true')
    
    # Configurações de logging
    os.environ.setdefault('LOG_LEVEL', 'INFO')
    
    print("Configurações do Render aplicadas:")
    print(f"- RENDER: {os.environ.get('RENDER')}")
    print(f"- FLET_WEB: {os.environ.get('FLET_WEB')}")
    print(f"- PYTHONUNBUFFERED: {os.environ.get('PYTHONUNBUFFERED')}")
    print(f"- CORS_ALLOW_ALL_ORIGINS: {os.environ.get('CORS_ALLOW_ALL_ORIGINS')}")

def get_render_config():
    """Retorna configurações específicas para Render"""
    return {
        'host': '0.0.0.0',
        'port': int(os.environ.get('PORT', 8000)),
        'debug': False,
        'ssl_context': None,
        'cors_enabled': True,
        'max_upload_size': 10 * 1024 * 1024,  # 10MB
        'allowed_origins': ['*'],
        'health_check_path': '/',
        'static_files': True,
        'assets_dir': 'assets',
        'uploads_dir': 'uploads'
    }

# Configurações de compatibilidade com diferentes dispositivos
DEVICE_CONFIGS = {
    'mobile': {
        'viewport': 'width=device-width, initial-scale=1.0, user-scalable=no',
        'theme_color': '#3B82F6',
        'apple_mobile_web_app_capable': 'yes',
        'apple_mobile_web_app_status_bar_style': 'default'
    },
    'tablet': {
        'viewport': 'width=device-width, initial-scale=1.0',
        'theme_color': '#3B82F6',
        'apple_mobile_web_app_capable': 'yes'
    },
    'desktop': {
        'viewport': 'width=device-width, initial-scale=1.0',
        'theme_color': '#3B82F6'
    }
}

# Configurações de fallback para navegadores antigos
FALLBACK_CONFIGS = {
    'ie_support': True,
    'safari_support': True,
    'chrome_support': True,
    'firefox_support': True,
    'edge_support': True,
    'mobile_safari_support': True,
    'chrome_mobile_support': True
}

if __name__ == "__main__":
    # Aplicar configurações quando executado diretamente
    configure_for_render()
    config = get_render_config()
    print(f"Configuração final: {config}")
