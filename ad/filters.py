import django_filters
from django_filters import OrderingFilter
from ad.models import Advertisement


class AdvertisementFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='icontains')#iexact
    # name = django_filters.CharFilter(lookup_expr='iexact')

    # name = django_filters.CharFilter(lookup_expr='gt')
    # name = django_filters.CharFilter(field_name='name')
    created__gt = django_filters.DateTimeFilter(field_name='creted', lookup_expr='gt')
    # data__gt = django_filters.NumberFilter(field_name='data', lookup_expr='gt')
    # quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt')

    # name__name = django_filters.CharFilter(lookup_expr='icontains')
    # order_by('name')

    def filter_queryset(self, queryset):
       
        queryset=Advertisement.objects.all().order_by('title')
        return queryset

    class Meta:
        model = Advertisement
        # ordering = ('title',)
        fields = ['title', 'created']
        

