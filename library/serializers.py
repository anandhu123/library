from rest_framework import serializers
from library.models import BooksBookAuthors, BooksBookLanguages, BooksFormat, BooksBookBookshelves, BooksBookSubjects


class ListBooksSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()
    mime_type = serializers.SerializerMethodField()
    bookshelf = serializers.SerializerMethodField()
    subject = serializers.SerializerMethodField()
    author = serializers.SerializerMethodField()
    download_count = serializers.ReadOnlyField(source='book.download_count')
    gutenberg_id = serializers.ReadOnlyField(source='book.gutenberg_id')
    media_type = serializers.ReadOnlyField(source='book.media_type')
    title = serializers.ReadOnlyField(source='book.title')
    genre = serializers.SerializerMethodField()

    def get_language(self, obj):
        return list(BooksBookLanguages.objects.filter(book=obj.book).values_list('language__code', flat=True))

    def get_mime_type(self, obj):
        queryset = BooksFormat.objects.filter(book=obj.book)
        data = [{'mime_type': item.mime_type, 'url': item.url} for item in queryset]
        return data

    def get_bookshelf(self, obj):
        return list(BooksBookBookshelves.objects.filter(book=obj.book).values_list('bookshelf__name', flat=True))

    def get_subject(self, obj):
        return list(BooksBookSubjects.objects.filter(book=obj.book).values_list('subject__name', flat=True))

    def get_author(self, obj):
        return {
            'birth_year': obj.author.birth_year,
            'death_year': obj.author.death_year,
            "name": obj.author.name,
        }


    def get_genre(self, obj):
        sub_list = list(BooksBookSubjects.objects.filter(
            book=obj.book).values_list('subject__name', flat=True))
        genre_list = []
        for item in sub_list:
            split_item = item.split("--")
            if len(split_item) > 1:
                genre_list.append(split_item[-1].strip().lower())
            else:
                genre_list.append(split_item[0])
        return [item.capitalize() for item in list(set(genre_list))] if genre_list else []

    class Meta:
        model = BooksBookAuthors
        fields = ('title', 'gutenberg_id', 'media_type', 'download_count', 'language', 'mime_type', 'bookshelf',
                  'subject', 'author', 'genre')
