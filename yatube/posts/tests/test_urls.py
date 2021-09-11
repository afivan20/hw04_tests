from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client
from http import HTTPStatus


from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_static_pages(self):
        """Smoke-test главной страницы и статических страниц."""
        adress_names = {
            'index': '/',
            'about_author': '/about/author/',
            'about_tech': '/about/tech/'}
        for key in adress_names.keys():
            adress = adress_names[key]
            with self.subTest(adress=adress):
                response = self.guest_client.get(adress)
                self.assertEqual(response.status_code, HTTPStatus.OK)


class PostURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Group.objects.create(
            title='Тестовый заголовок',
            slug='test-slug',
        )
        cls.user = User.objects.create_user(username='test_user')
        cls.group = get_object_or_404(Group, slug='test-slug')
        Post.objects.create(
            author=cls.user,
            pk=999,
            group=cls.group
        )

    def setUp(self):
        self.guest_client = Client()
        self.user = User.objects.create_user(username='HasNoName')
        self.authorized_client = Client()
        self.authorized_client.force_login(self.user)
        self.user_author = get_object_or_404(User, username='test_user')
        self.author = Client()
        self.author.force_login(self.user_author)

    def test_page_exists_at_desired_location_authorized(self):
        """Страница доступна любому пользователю."""
        urls = {
            'group_list': '/group/test-slug/',
            'profile': '/profile/HasNoName/',
            'post_detail': '/posts/999/',
        }
        for url in urls.values():
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_unexisitng_page_exists_at_desired_location_authorized(self):
        """Страница /unexisting_page/ не существует."""
        response = self.guest_client.get('/unexisitng_page')
        self.assertEqual(response.status_code, HTTPStatus.NOT_FOUND)

    def test_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_posts_edit_available(self):
        """Страница /posts/<post_id>/edit доступна автору."""
        response = self.author.get('/posts/999/edit/')
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_posts_edit_available(self):
        """Страница /posts/<post_id>/edit перенаправляет НЕ автора."""
        response = self.authorized_client.get('/posts/999/edit/')
        self.assertEqual(response.status_code, HTTPStatus.FOUND)

    def test_urls_uses_correct_template(self):
        """URL-адрес использует соответствующий шаблон."""
        templates_url_names = {
            '/': (
                '/',
                'posts/index.html'
            ),
            '/group/<slug>/': (
                '/group/test-slug/',
                'posts/group_list.html'
            ),
            'profile/<username>/': (
                '/profile/HasNoName/',
                'posts/profile.html'
            ),
            'posts/<post_id>/': (
                '/posts/999/',
                'posts/post_detail.html'
            ),
            'posts/<post_id>/edit': (
                '/posts/999/edit/',
                'posts/create_post.html'
            ),
            'create/': (
                '/create/',
                'posts/create_post.html'
            ),
        }
        for key in templates_url_names.keys():
            adress, template = templates_url_names[key]
            with self.subTest(adress=adress):
                response = self.author.get(adress)
                self.assertTemplateUsed(response, template)
