from django.contrib import admin
from django.core.exceptions import ValidationError
from django.forms import BaseInlineFormSet
from .models import Article, Scope


class ScopeInlineFormset(BaseInlineFormSet):
    def clean(self):
        main_tag_counter = 0
        tags_all = (list(map(lambda x: x.cleaned_data.get('tag'), self.forms)))
        for form in self.forms:
            if form.cleaned_data.get('is_main'):  # исправлено обращение по ключу. использован get
                main_tag_counter += 1
            tag_current = form.cleaned_data.get('tag')
            if tags_all.count(tag_current) > 1:
                raise ValidationError(f'Должен быть выбран один Тэг/раздел: {tag_current}')
        if main_tag_counter < 1:
            raise ValidationError('Должен быть выбран основной Тэг/раздел')
        if main_tag_counter > 1:
            raise ValidationError('Основной Тэг/раздел должен быть один')
        return super().clean()


class ScopeInline(admin.TabularInline):
    model = Scope
    formset = ScopeInlineFormset
    extra = 1


@admin.register(Article)
class ArticleAdmin(admin.ModelAdmin):
    inlines = [ScopeInline]
