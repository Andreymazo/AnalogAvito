import json
from django.shortcuts import render
from django.core.serializers import serialize

from users.models import Profile


def MarkersMap(request):
    
    # queryset = Marker.objects.all()
    queryset = Profile.objects.all()
    # queryset={}
    context = {'queryset':queryset}
    context['queryset'] = json.loads(serialize('geojson', queryset))
    return render(request, "map/templates/map/home_map.html", context)


from django.views.generic.base import TemplateView
from map.models import Marker

# from map.models import ModelGis
# class MarkersMapView(TemplateView):
#     """Markers map view."""

#     template_name = "map/templates/map/home_map.html"

class MarkersMapView(TemplateView):
    model = Marker
    template_name = 'map/templates/map/home_map.html'
    

    def get_context_data(self, **kwargs):
#         # Call the base implementation first to get a context
        context = super().get_context_data(**kwargs)
        modelgis = Marker.objects.all()
        context['markers'] = json.loads(serialize('geojson', modelgis))
        return context
    
    def get(self, request, *args, **kwargs):
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)
    


