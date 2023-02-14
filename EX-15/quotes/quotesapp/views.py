from django.db.models import Count
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Quotes, Authors, Tags
from .forms import AuthorForm, TagForm, QuoteForm


def get_top_tags():
    popular_tags = Tags.objects.annotate(ctags=Count('quotes')).order_by('-ctags', 'name')[:10]
    return [{'id': popular_tags[i].id, 'name': popular_tags[i].name} for i in range(len(popular_tags))]


def main(request, page=1):
    cnt_quotes = 3
    quotes_list = []
    len_q = Quotes.objects.count()
    cnt_pages = 0
    if len_q % cnt_quotes == 0:
        cnt_pages = len_q // cnt_quotes
    else:
        cnt_pages = len_q // cnt_quotes + 1
    previos = page - 1
    next = page + 1 if page < cnt_pages else 0
    start_q = (page - 1) * cnt_quotes
    end_q = (page - 1) * cnt_quotes + cnt_quotes

    for el in Quotes.objects.all()[start_q:end_q]:
        tags = el.tags.all()
        quotes_list.append({
            'id': el.id,
            'quote': el.quote[:200] + '....' if len(el.quote) > 200 else el.quote,
            'tags': [{'id': el.id, 'name': el.name} for el in tags],
            'author': el.author.fullname,
            'author_id': el.author.id
        })

    return render(request, 'quotesapp/quotes.html', {'quotes_list': quotes_list, 'previous': previos,
                                                     'next': next, 'top_tag': get_top_tags()})


def author(request, author_id):
    author = get_object_or_404(Authors, pk=author_id)
    return render(request, 'quotesapp/author.html', {'author': author})


def tag(request, tag_id, page=1):
    tag = get_object_or_404(Tags, pk=tag_id)
    cnt_quotes = 3
    quotes_list = []
    len_t = Quotes.objects.filter(tags=tag_id).count()
    cnt_pages = 0
    if len_t % cnt_quotes == 0:
        cnt_pages = len_t // cnt_quotes
    else:
        cnt_pages = len_t // cnt_quotes + 1
    previos = page - 1
    next = page + 1 if page < cnt_pages else 0
    start_q = (page - 1) * cnt_quotes
    end_q = (page - 1) * cnt_quotes + cnt_quotes

    for el in Quotes.objects.filter(tags=tag_id)[start_q:end_q]:
        tags = el.tags.all()
        quotes_list.append({
            'id': el.id,
            'quote': el.quote[:200] + '....' if len(el.quote) > 200 else el.quote,
            'tags': [{'id': el.id, 'name': el.name} for el in tags],
            'author': el.author.fullname,
            'author_id': el.author.id
        })
    return render(request, 'quotesapp/quotes_by_tag.html', {'quotes_list': quotes_list, 'previous': previos,
                                                            'next': next, 'tag_id': tag_id, 'tag_name': tag.name,
                                                            'top_tag': get_top_tags()})


def detail(request, quote_id):
    quote = get_object_or_404(Quotes, pk=quote_id)
    return render(request, 'quotesapp/detail.html', {'quote': quote})


@login_required
def addauthor(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to='quotesapp:authors')
        else:
            return render(request, 'quotesapp/form_author.html', {'form': form})
    return render(request, 'quotesapp/form_author.html', {'form': AuthorForm()})


@login_required
def addtag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='quotesapp:tags')
        else:
            return render(request, 'quotesapp/form_tags.html', {'form': form})
    return render(request, 'quotesapp/form_tags.html', {'form': TagForm()})


@login_required
def addquote(request):
    tags = Tags.objects.all().order_by('name')
    authors = Authors.objects.all().order_by('fullname')
    if request.method == 'POST':
        form = QuoteForm(request.POST)
        if form.is_valid():
            new_quote = form.save(commit=False)
            new_quote.user = request.user
            new_quote.save()
            choice_tags = Tags.objects.filter(name__in=request.POST.getlist('tags'))
            for tag in choice_tags.iterator():
                new_quote.tags.add(tag)
            return redirect(to='quotesapp:main')
        else:
            return render(request, 'quotesapp/form_quote.html', {'tags': tags, 'authors': authors, 'form': form})
    return render(request, 'quotesapp/form_quote.html', {'tags': tags, 'authors': authors, 'form': QuoteForm})


def get_authors(request, page=1):
    cnt_authors = 12
    len_a = Authors.objects.count()
    cnt_pages = 0
    if len_a % cnt_authors == 0:
        cnt_pages = len_a // cnt_authors
    else:
        cnt_pages = len_a // cnt_authors + 1
    previos = page - 1
    next = page + 1 if page < cnt_pages else 0
    start_a = (page - 1) * cnt_authors
    end_a = (page - 1) * cnt_authors + cnt_authors

    return render(request, 'quotesapp/get_authors.html',
                  {'authors': Authors.objects.order_by('fullname')[start_a:end_a], 'previous': previos, 'next': next})


def get_tags(request, page=1):
    cnt_tags = 12
    len_tags = Tags.objects.count()
    cnt_pages = 0
    if len_tags % cnt_tags == 0:
        cnt_pages = len_tags // cnt_tags
    else:
        cnt_pages = len_tags // cnt_tags + 1
    previos = page - 1
    next = page + 1 if page < cnt_pages else 0
    start_tag = (page - 1) * cnt_tags
    end_tag = (page - 1) * cnt_tags + cnt_tags

    return render(request, 'quotesapp/get_tags.html',
                  {'tags': Tags.objects.order_by('name')[start_tag:end_tag], 'previous': previos, 'next': next})


@login_required
def remove_quote(request, quote_id):
    Quotes.objects.filter(id=quote_id).delete()
    return redirect(to='quotesapp:main')


@login_required
def remove_tag(request, tag_id):
    Tags.objects.filter(id=tag_id).delete()
    return redirect(to='quotesapp:tags')


@login_required
def remove_author(request, author_id):
    Authors.objects.filter(id=author_id).delete()
    return redirect(to='quotesapp:authors')


@login_required
def edit_author(request, author_id):
    author = get_object_or_404(Authors, pk=author_id)
    form = AuthorForm({
        'id': author.id,
        'fullname': author.fullname,
        'born_date': author.born_date,
        'born_location': author.born_location,
        'description': author.description
    })
    return render(request, 'quotesapp/form_author.html', {'form': form})