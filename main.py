import pathlib

import django_micro
from django.http import HttpResponse
from django.db import models
from django.core.files.base import ContentFile, File

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
    file = models.FileField()

    class Meta:
        app_label = django_micro.get_app_label()


from django.core import management

@django_micro.command('print_hello')
class PrintHelloCommand(management.BaseCommand):
    def handle(self, *args, **options):
        management.call_command('makemigrations', django_micro.get_app_label())
        management.call_command('migrate', run_syncdb=True)
        with ContentFile('foo', name='foo') as f:
            p = Post.objects.create(title='foo', file=f)

        print('cf closed?', f.closed)
        print('same?', f is p.file)
        print('closed?', p.file.closed)
        print('content', p.file.read())
        print('closed?', p.file.closed)
        print('cf closed?', f.closed)
        print('#######################')
        """
        c = Post.objects.create(parent=p, title='ham')
        c.file.save('foo', ContentFile('foo'))

        vl = (
            Post
            .objects
            .values_list('parent__title', 'title', 'file')
        )
        print(Post.objects.get(title='ham').file.read())
        f = Post.objects.get(title='ham').file
        with f.open('r+') as ff:
            ff.write('hello')
            print(ff)
            print(f)
            import pdb; pdb.set_trace()
        print(ff)
        print(f)
        """


application = django_micro.run()
