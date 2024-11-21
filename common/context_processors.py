from .models import SiteParameters

def settings(request):
    return { 'settings': SiteParameters.load() }