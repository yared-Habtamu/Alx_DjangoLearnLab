from bookshelf.models import Book
book=Book.objects.get("Nineteen Eighty-Four")
book.delete()
#(1, {'bookshelf.Book': 1})
