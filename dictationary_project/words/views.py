from django.core.paginator import Paginator
from django.http import JsonResponse
from .models import Word, Category
from django.db.models import Q
from datetime import datetime
import os

def word_list(request):
    query = request.GET.get('search')
    category = request.GET.get('category')
    sort = request.GET.get('sort', 'word')
    page_number = request.GET.get('page', 1)

    words = Word.objects.all()

    if query:
        words = words.filter(word__icontains=query)
        if not words.exists():
            week = datetime.now().strftime("%Y-%U")
            file_path = f'missed_words_{week}.txt'
            with open(file_path, 'a', encoding='utf-8') as f:
                f.write(f"{query}\n")
            return JsonResponse({"message": "So'z topilmadi!", "suggestion_file": file_path})

    if category:
        words = words.filter(category__id=category)

    words = words.order_by(sort)
    paginator = Paginator(words, 10)
    page = paginator.get_page(page_number)

    data = []
    for word in page:
        data.append({
            'id': word.id,
            'word': word.word,
            'definition': word.definition,
            'category': word.category.name,
            'synonyms': [syn.word for syn in word.synonyms.all()]
        })

    return JsonResponse({
        'results': data,
        'total': paginator.count,
        'pages': paginator.num_pages,
        'current_page': page.number
    })

def word_detail(request, pk):
    try:
        word = Word.objects.get(pk=pk)
        related_words = Word.objects.filter(category=word.category).exclude(pk=word.pk)[:20]
        return JsonResponse({
            'word': word.word,
            'definition': word.definition,
            'category': word.category.name,
            'synonyms': [syn.word for syn in word.synonyms.all()],
            'related_words': [
                {'id': w.id, 'word': w.word} for w in related_words
            ]
        })
    except Word.DoesNotExist:
        return JsonResponse({'error': 'So’z topilmadi!'}, status=404)

def category_list(request):
    categories = Category.objects.all()
    return JsonResponse({
        'categories': [{'id': cat.id, 'name': cat.name} for cat in categories]
    })