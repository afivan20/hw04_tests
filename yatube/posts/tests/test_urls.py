from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.test import TestCase, Client


from posts.models import Group, Post

User = get_user_model()


class StaticURLTests(TestCase):
    def setUp(self):
        self.guest_client = Client()

    def test_index(self):
        """Домашняя страница доступна(smoke test)."""
        response = self.guest_client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_author(self):
        """Статичесекая страница об авторе."""
        response = self.guest_client.get('/about/author/')
        self.assertEqual(response.status_code, 200)

    def test_tech(self):
        """Статичесекая страница о технологиях."""
        response = self.guest_client.get('/about/tech/')
        self.assertEqual(response.status_code, 200)


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
                self.assertEqual(response.status_code, 200)

    def test_unexisitng_page_exists_at_desired_location_authorized(self):
        """Страница /unexisting_page/ не существует."""
        response = self.guest_client.get('/unexisitng_page')
        self.assertEqual(response.status_code, 404)

    def test_create_url_exists_at_desired_location(self):
        """Страница /create/ доступна авторизованному пользователю."""
        response = self.authorized_client.get('/create/')
        self.assertEqual(response.status_code, 200)

    def test_create_url_redirect_anonymous(self):
        """Страница /create/ перенаправляет анонимного пользователя."""
        response = self.client.get('/create/')
        self.assertEqual(response.status_code, 302)

    def test_posts_edit_available(self):
        """Страница /posts/<post_id>/edit доступна автору."""
        response = self.author.get('/posts/999/edit/')
        self.assertEqual(response.status_code, 200)

    def test_posts_edit_available(self):
        """Страница /posts/<post_id>/edit перенаправляет НЕ автора."""
        response = self.authorized_client.get('/posts/999/edit/')
        self.assertEqual(response.status_code, 302)

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
