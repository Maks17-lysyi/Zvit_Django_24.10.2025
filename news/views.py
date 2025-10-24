from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from .models import News


def news_list(request):
	q = request.GET.get('q', '').strip()
	qs = News.objects.all()
	if q:
		qs = qs.filter(Q(title__icontains=q) | Q(summary__icontains=q))
	return render(request, 'news_list.html', {'news': qs, 'q': q})


def news_detail(request, slug: str):
	item = get_object_or_404(News, slug=slug)
	return render(request, 'news_detail.html', {'item': item})
