from datetime import date

from django.urls import reverse
from django.db import models
from django.contrib.auth.models import User


class Genre(models.Model):
    name = models.CharField(max_length=200,
                            help_text=" Введіть жанр книги",
                            verbose_name="Жанр книги")

    def __str__(self):
        return self.name


class Language(models.Model):
    name = models.CharField(max_length=20,
                            help_text=" Введіть мову книги",
                            verbose_name="Мова книги")

    def __str__(self):
        return self.name


class Author(models.Model):
    first_name = models.CharField(max_length=100,
                                  help_text="Введіть ім'я автора",
                                  verbose_name="Ім'я автора")
    last_name = models.CharField(max_length=100,
                                 help_text="Введіть прізвище автора",
                                 verbose_name="Прізвище автора")
    date_of_birth = models.DateField(
        help_text="Введіт дату народження",
        verbose_name="Дата народження",
        null=True,
        blank=True
    )
    date_of_death = models.DateField(
        help_text="Введіть дату смерті",
        verbose_name="Дата смерті",
        null=True,
        blank=True
    )

    def __str__(self):
        return self.last_name


class Book(models.Model):
    title = models.CharField(max_length=200,
                             help_text=" Введіть назву книги",
                             verbose_name="Назва книги")
    genre = models.ForeignKey('Genre', on_delete=models.CASCADE,
                              help_text=" Оберіть жанр книги",
                              verbose_name="Жанр книги",
                              null=True)
    language = models.ForeignKey('Language',
                                 on_delete=models.CASCADE,
                                 help_text=" Оберіть мову книги",
                                 verbose_name="Мова книги",
                                 null=True)
    author = models.ManyToManyField('Author',
                                    help_text=" Оберіть автора книги",
                                    verbose_name="Автор книги",
                                    )
    summary = models.TextField(max_length=1000,
                               help_text="Введіть аннотацію книги",
                               verbose_name="Аннотація книги")
    isbn = models.CharField(max_length=13,
                            help_text="Повинно містити 13 символів",
                            verbose_name=" ISBN книги", )

    def display_author(self):
        return ', '.join([author.last_name for author in self.author.all()])

    display_author.short_description = 'Автори'

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('book-detail',
                       args=[str(self.id)])


class Status(models.Model):
    name = models.CharField(max_length=20,
                            help_text="Введіть статус екземпляра книги",
                            verbose_name="Статус екземпляра книги")

    def __str__(self):
        return self.name


class BookInstance(models.Model):
    book = models.ForeignKey('Book', on_delete=models.CASCADE
                             , null=True)
    inv_nom = models.CharField(max_length=20,
                               help_text="Введіть інвентерезаційний номер",
                               verbose_name="інвентерезаційний номер")
    imprint = models.CharField(max_length=200,
                               help_text="Введіть назву видавництва і рік",
                               verbose_name="Видавництво")
    status = models.ForeignKey('Status', on_delete=models.CASCADE,
                               help_text="Змінити стан екземпляра",
                               verbose_name="Стан екземпляра",
                               null=True)
    due_back = models.DateField(null=True,
                                help_text="Введіть кінець строку стану",
                                verbose_name="Дата закцінчення статусу")
    borrower = models.ForeignKey(User, on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name="Замовник",
                                 help_text="Оберіть замовника книги")

    @property
    def is_overdue(self):
        if self.due_back and date.today() > self.due_back:
            return True
        return False

    def __str__(self):
        return '%s  %s %s' % (self.inv_nom, self.book, self.status)
