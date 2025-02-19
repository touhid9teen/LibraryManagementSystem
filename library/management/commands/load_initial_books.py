import os
import random
from tqdm import tqdm
from django.conf import settings
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from library.models import Book, Category

class Command(BaseCommand):
    help = 'Load initial data into the database'

    def handle(self, *args, **options):
        total_iterations = 20

        self.stdout.write(self.style.NOTICE('Clearing media directory'))
        media_root = settings.MEDIA_ROOT
        book_covers_path = os.path.join(media_root, 'book_covers')

        # Initialize tqdm progress bar
        progress_bar = tqdm(total=total_iterations, desc='Processing', unit='iteration', dynamic_ncols=True)

        cc = 0
        for filename in os.listdir(book_covers_path):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                try:
                    cover_image_path = os.path.join(book_covers_path, filename)
                    with open(cover_image_path, 'rb') as f:
                        cover_image_data = f.read()
                        cover_image = ContentFile(cover_image_data, name=filename)
                        category, _ = Category.objects.get_or_create(name='Default Category')
                        Book.objects.create(
                            name=f'Book {cc + 1}',
                            author='Unknown Author',
                            category=category,
                            isbn=f'ISBN{cc + 1}',
                            format='Paperback',
                            price=random.uniform(10.0, 100.0),
                            cover_image=cover_image
                        )
                except Exception as e:
                    self.stdout.write(self.style.ERROR(f'Error processing book cover: {e}'))
                    progress_bar.update(1)
                    continue
                progress_bar.update(1)
                cc += 1
                if cc == total_iterations:
                    break
        progress_bar.close()
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {cc} Books'))
# import os
# import random
# from tqdm import tqdm
# from django.conf import settings
# from django.core.files.base import ContentFile
# from django.core.management.base import BaseCommand

# from core.utils import load_book_data
# from library.models import Book, Category

# class Command(BaseCommand):
#     help = 'Load initial data into the database'

#     def handle(self, *args, **options):
#         total_iterations = 20

#         self.stdout.write(self.style.NOTICE('Clearing media directory'))
#         media_root = settings.MEDIA_ROOT
#         for dirpath, dirnames, filenames in os.walk(media_root):
#             for file in filenames:
#                 # Construct full file path
#                 file_path = os.path.join(dirpath, file)

#                 # Remove the file
#                 os.remove(file_path)
#         self.stdout.write(self.style.SUCCESS('Successfully cleared media directory'))
        
#         # Initialize tqdm progress bar
#         progress_bar = tqdm(total=total_iterations, desc='Processing', unit='iteration', dynamic_ncols=True)

#         cc = 0
#         books = load_book_data()
#         # for i, book in enumerate(load_book_data()):
#         for i in range(len(books)):
#             random_index = random.randint(0, len(books) - 1)
#             book = books[random_index]
#             try:
#                 with open(book['book_covers_directory'], 'rb') as f:
#                     cover_image_data = f.read()
#                     cover_image = ContentFile(cover_image_data, name='book_cover.jpg')
#                     category,_ = Category.objects.get_or_create(name = book['category'])
#                     book = Book.objects.create(
#                         name=book['name'],
#                         author=book['author'],
#                         category=category,
#                         isbn=book['isbn'],
#                         format=book['format'],
#                         price=book['price'],
#                         cover_image= cover_image 
#                     )
#             except Exception as e:
#                 progress_bar.update(1)
#                 continue
#             progress_bar.update(1)
#             cc+=1
#             if cc == total_iterations:
#                 break
#         progress_bar.close()
#         self.stdout.write(self.style.SUCCESS(f'Successfully loaded {cc} Books'))
#         # self.stdout.write(self.style.SUCCESS(load_category_data()))



