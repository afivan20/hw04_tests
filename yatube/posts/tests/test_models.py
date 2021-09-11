from django.contrib.auth import get_user_model
from django.test import TestCase
from ..models import Group, Post

User = get_user_model()


class PostModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )
        cls.post = Post.objects.create(
            author=cls.user,
            text='Тестовая группа123',
        )

    def test_post_model_have_correct_object_name(self):
        """Проверяем, что у модели Post корректно работает __str__."""
        post = PostModelTest.post
        post_obj_name = post.text[:15]
        self.assertEqual(post_obj_name, str(post))

    def test_post_verbose_name(self):
        """verbose_name модели Post совпадает с ожидаемыми."""
        post = PostModelTest.post
        verbose_text = post._meta.get_field('text').verbose_name
        verbose_date = post._meta.get_field('pub_date').verbose_name
        verbose_author = post._meta.get_field('author').verbose_name
        verbose_group = post._meta.get_field('group').verbose_name
        self.assertEqual(verbose_text, 'Текст')
        self.assertEqual(verbose_date, 'Дата публикации')
        self.assertEqual(verbose_author, 'автор')
        self.assertEqual(verbose_group, 'Группа')

    def test_post_help_text(self):
        """help_text модели Post совпадает с ожидаемыми."""
        post = PostModelTest.post
        help_text = post._meta.get_field('text').help_text
        help_author = post._meta.get_field('author').help_text
        help_group = post._meta.get_field('group').help_text
        self.assertEqual(help_text, 'Введите текст')
        self.assertEqual(help_author, 'Изменить авторство')
        self.assertEqual(help_group, 'Выберите группу')


class GroupModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.user = User.objects.create_user(username='auth')
        cls.group = Group.objects.create(
            title='Тестовая группа',
            slug='Тестовый слаг',
            description='Тестовое описание',
        )

    def test_group_model_have_correct_object_name(self):
        """Проверяем, что у модели Group корректно работает __str__."""
        group = GroupModelTest.group
        expected_object_name = group.title
        self.assertEqual(expected_object_name, str(group))

    def test_group_verbose_name(self):
        """verbose_name модели Group совпадает с ожидаемыми."""
        group = GroupModelTest.group
        verbose_title = group._meta.get_field('title').verbose_name
        verbose_slug = group._meta.get_field('slug').verbose_name
        verbose_description = group._meta.get_field('description').verbose_name
        self.assertEqual(verbose_title, 'Название')
        self.assertEqual(verbose_slug, 'slug')
        self.assertEqual(verbose_description, 'Описание')

    def test_group_help_text(self):
        """help_text модели Group совпадает с ожидаемыми."""
        group = GroupModelTest.group
        help_texts = {
            'title': 'Введите название группы',
            'slug': 'Имя группы',
            'description': 'Краткое описание для кого эта группа'
        }
        for field, help_text in help_texts.items():
            with self.subTest(help_text=help_text, field=field):
                help_text = group._meta.get_field(field).help_text
                self.assertEqual(help_text, help_text)
