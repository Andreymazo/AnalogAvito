from django.core.management import BaseCommand

#"Программа, которая выводит n первых элементов последовательности 122333444455555… (число повторяется столько раз, чему оно равно)"
def num_repeated(x):
    # print(str(x)*x)
    return str(x)*x

def string_num(num_in):
    num_in = int(num_in)# Мало ли строку введут
    str_gen = [str(num_repeated(i)) for i in range(1, num_in+1)]
    str_gen="".join(str_gen)
    print(str_gen[:num_in])

class Command(BaseCommand):

    def handle(self, *args, **options):
        string_num(7)#"122333444455555"