import pathlib

import django_micro
from django.http import HttpResponse
from django.db import models

django_micro.configure({
    'DEBUG': True,
    'DATABASES': {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': ':memory:'
        },
    },
})

@django_micro.route('', name='homepage')
def homepage(request):
    name = request.GET.get('name', 'World')
    return HttpResponse('Hello, {}!'.format(name))


class Post(models.Model):
    title = models.CharField(max_length=255)
    parent = models.ForeignKey('self', null=True, on_delete=models.CASCADE)

    class Meta:
        app_label = django_micro.get_app_label()


from django.core import management

@django_micro.command('print_hello')
class PrintHelloCommand(management.BaseCommand):
    def handle(self, *args, **options):
        management.call_command('makemigrations', django_micro.get_app_label())
        management.call_command('migrate', run_syncdb=True)
        p = Post.objects.create(title='foo')
        Post.objects.create(parent=p, title='ham')
        print(
            Post
            .objects
            .values_list('parent__title', 'title')
        )


application = django_micro.run()
