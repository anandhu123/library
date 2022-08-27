from library.models import BooksBookAuthors
from library.serializers import ListBooksSerializer
from rest_framework import viewsets, status
from rest_framework.response import Response
from django.db.models import Q
from library.pagination import CustomPageNumberPagination


class ListBookViewset(viewsets.ModelViewSet):
    """
    API to fetch books based on different criteria.

    """
    serializer_class = ListBooksSerializer
    queryset = BooksBookAuthors.objects.all()

    def list(self, request, *args, **kwargs):
        limit = self.request.GET.get('limit', 10)
        authors = self.request.GET.get('authors')
        title = self.request.GET.get('title')
        topic = self.request.GET.get('topic')
        language = self.request.GET.get('language')
        mime_type = self.request.GET.get('mime_type')
        gutenberg_id = self.request.GET.get('book_id')
        q = Q()
        queryset = self.queryset.order_by('-book__download_count')
        paginator = CustomPageNumberPagination()
        if limit:
            paginator.page_size = int(limit)
        # ---------------------------------------------------
        if authors:
            for item in authors.split(','):
                q = q | Q(author__name__icontains=item)

        if language:
            for item in language.split(','):
                q = q | Q(book__booksbooklanguages__language__code__iexact=item)

        if topic:
            for item in topic.split(','):
                q = q | Q(book__booksbookbookshelves__bookshelf__name__icontains=item) | \
                    Q(book__booksbooksubjects__subject__name__icontains=item)

        if mime_type:
            for item in mime_type.split(','):
                q = q | Q(book__booksformat__mime_type__icontains=item)

        if title:
            for item in title.split(','):
                q = q | Q(book__title__icontains=item)
            q = q | Q(q)

        if gutenberg_id:
            q = q | Q(book__gutenberg_id__in=gutenberg_id.split(','))

        queryset = queryset.filter(q)
        data = paginator.paginate_queryset(queryset, request)
        result_page = self.serializer_class(data, many=True).data
        # ---------------------------------------------------
        return Response({
            "code": status.HTTP_200_OK,
            "count": queryset.count(),
            "data": paginator.get_paginated_response(result_page).data
        },status=status.HTTP_200_OK)