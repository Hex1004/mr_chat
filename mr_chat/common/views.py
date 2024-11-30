from django.views.generic import TemplateView

# Simplified view for rendering a basic HTML template
class HomeView(TemplateView):
    template_name = 'base.html'

class HomePageView(TemplateView):
    template_name = 'home.html'

