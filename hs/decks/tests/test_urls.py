from django.urls import reverse, resolve

from decks.views import logout, DeckView, DecksView, signup, activation_email_sent, activate


class TestUrls:

    def test_account_activation_url(self):
        path = reverse('email')
        assert resolve(path).view_name == 'email'
        assert resolve(path).func == activation_email_sent

    def test_activate_url(self):
        path = reverse('activate', kwargs={'uidb64': 'Njc', 'token': '5gg-0cb3b3b4f111ed7029fa'})
        assert resolve(path).view_name == 'activate'
        assert resolve(path).func == activate

    def test_signup_url(self):
        path = reverse('signup')
        assert resolve(path).view_name == 'signup'
        assert resolve(path).func == signup

    # def test_logout_url(self):
    #     path = reverse('logout')
    #     assert resolve(path).view_name == 'logout'
    #     assert resolve(path).func == logout

    def test_home_url(self):
        path = reverse('home')
        assert resolve(path).view_name == 'home'
        assert resolve(path).func.view_class == DeckView

    def test_decks_views_url(self):
        path = reverse('choose', args=['some-slug'])
        assert resolve(path).view_name == 'choose'
        assert resolve(path).func.view_class == DecksView

