from django.http import HttpResponse
from django.shortcuts import render
from articles.models import Article, Tag


def articles_list(request):
    """Функция формирует сгруппированный по дате публикации список статей и возвращает рендер"""
    template = 'articles/news.html'
    # ordering = '-published_at'
    articles = Article.objects.all()  # order_by(ordering)
    context = {'object_list': articles}
    return render(request, template, context)


def add_tags(request):
    """Функция добавляет список тэгов в БД и возвращает уведомление."""
    tag_list = [
        'Наука',
        'Здоровье',
        'Культура',
        'Город',
        'Космос',
        'Международные отношения',
        'Музыка'
    ]
    tag_str = []
    errors_str = []
    for tag in tag_list:
        try:
            Tag.objects.create(name=tag)
            tag_str.append(tag)
        except:
            errors_str.append(tag)
    result = f'Успешно добавлен в БД следующий список: {", ".join(tag_str)}.<br>'\
             f'Уже были ранее добавлены в БД: {", ".join(errors_str)}.'
    return HttpResponse(result)
