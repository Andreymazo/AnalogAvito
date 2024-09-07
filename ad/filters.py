import django_filters
from django_filters import OrderingFilter
from ad.models import Advertisement, BagsKnapsacks, Car, Category, ChildClothesShoes, MenClothes, MenShoes, WemenClothes, WemenShoes

# """MenClothes Filter"""
# class MenClothesFilter(django_filters.FilterSet):
#     # name = django_filters.CharFilter(lookup_expr='icontains')#iexact
#     # name = django_filters.CharFilter(lookup_expr='iexact')

#     # name = django_filters.CharFilter(lookup_expr='gt')
#     # name = django_filters.CharFilter(field_name='name')
#     created__gt = django_filters.DateTimeFilter(field_name='created', lookup_expr='gt')
#     # data__gt = django_filters.NumberFilter(field_name='data', lookup_expr='gt')
#     # quantity__lt = django_filters.NumberFilter(field_name='quantity', lookup_expr='lt')

#     # name__name = django_filters.CharFilter(lookup_expr='icontains')
#     # order_by('name')

#     def filter_queryset(self, queryset):
       
#         queryset=Advertisement.objects.all().order_by('title')
#         return queryset

#     class Meta:
#         model = MenClothes
#         # ordering = ('title',)
#         fields = ['title', 'created',]



class MenClothesFilter(django_filters.FilterSet):

    def filter_queryset(self, queryset):
        queryset=MenClothes.objects.all().order_by('title')
        return queryset

    class Meta:
        model = MenClothes
        # ordering = ('title',)
        fields = "__all__"

class MenClothesFilter(django_filters.FilterSet):

    class Meta:
        model = MenClothes
        fields = "__all__"


class MenShoesFilter(django_filters.FilterSet):

    class Meta:
        model = MenShoes
        fields = "__all__"

class WemenClothesFilter(django_filters.FilterSet):

    class Meta:
        model = WemenClothes
        fields = "__all__"


class WemenShoesFilter(django_filters.FilterSet):

    class Meta:
        model = WemenShoes
        fields = "__all__"


class BagsKnapsacksFilter(django_filters.FilterSet):
    # title__gt = django_filters.CharFilter(field_name='title', lookup_expr='gt')

    class Meta:
        model = BagsKnapsacks
        fields = "__all__"# ['title',]



class ChildClothesShoesFilter(django_filters.FilterSet):

    class Meta:
        model = ChildClothesShoes
        fields = "__all__"


class CategoryFilter(django_filters.FilterSet):
    # name = django_filters.CharFilter(lookup_expr='iexact')
    
    class Meta:
        model = Category
        fields = ['name',]


class CarFilter(django_filters.FilterSet):
    
    class Meta:
        model = Car
        fields = ['id',]

class CustomFilterSet(django_filters.FilterSet):
    
    def __init__(self, *args, content_type, **kwargs):
        self.content_type = content_type
        
        super().__init__(*args, **kwargs)
    
    def is_valid(self):
        print('self is_valid', self)
        return super().is_valid()
#     @classmethod
#     def get_model_fm_kwargs(self, **kwargs):
#         filters_list = [CarFilter,]
#         print('kwargs=========000000000', kwargs)
#         # contetn_type = kwargs['content_type']
#         # for i in filters_list:
#         #     if kwargs["content_type"]:
#         #         print('kwargs contrtnt type', kwargs["content_type"])
#         #         return i
#         print('default filter .... ')
#         return CarFilter
# CustomFilterSet.get_model_fm_kwargs()


class CategoryFilterByName(django_filters.FilterSet):
    """Фильтр для поиска категории по названию"""

    name = django_filters.CharFilter(method='filter_by_name', label='Категория')

    class Meta:
        model = Category
        fields = ['name',]

    def filter_by_name(self, queryset, name, value):
        """Метод расширения QuerySet для поиска категорий как в parent, так и в children"""

        extend_queryset = Category.objects.prefetch_related('children').filter(name__icontains=value)
        return extend_queryset

