from django.test import Client, TestCase
from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from posts.forms import PostForm
from posts.models import Post
from django.urls import reverse

User = get_user_model()


class PostCreateFormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.form = PostForm()
        cls.user = User.objects.create_user(username='V.Pupkin')

    def setUp(self):
        self.user_author = get_object_or_404(User, username='V.Pupkin')
        self.author = Client()
        self.author.force_login(self.user_author)

    def test_create_post(self):
        """Валидная форма создает запись в Post."""
        tasks_count = Post.objects.count()
        form_data = {
            'text': 'Новый пост',
        }
        response = self.author.post(
            reverse('posts:create_post'),
            data=form_data
        )
        self.assertRedirects(response, reverse(
            'posts:profile', kwargs={'username': 'V.Pupkin'})
        )
        self.assertEqual(Post.objects.count(), tasks_count + 1)
        self.assertTrue(
            Post.objects.filter(
                text='Новый пост',
            ).exists()
        )

    def test_edit_post(self):
        """Происходит изменение поста с <post_id> в базе данных."""
        form_data = {
            'text': 'Редактируем пост',
        }
        self.author.post(
            reverse('posts:create_post'), args=('post_id',),
            data=form_data,
        )
        self.assertTrue(
            Post.objects.filter(
                text='Редактируем пост',
            ).exists()
        )
