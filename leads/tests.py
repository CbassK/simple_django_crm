from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from leads.models import Lead, Agent
from leads.forms import AssignAgentForm


class LandingPageViewTest(TestCase):
    def test_landing_page_view(self):
        url = reverse('landing-page')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'landing.html')


class SignUpViewTest(TestCase):
    def test_signup_view(self):
        url = reverse('signup')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'registration/signup.html')

    def test_signup_form_submission(self):
        url = reverse('signup')
        data = {
            'username': 'testuser',
            'password1': 'testpass!123',
            'password2': 'testpass!123',
        }

        response = self.client.post(url, data, follow=True)
        self.assertRedirects(response, reverse('login'), status_code=302, target_status_code=200)
        self.assertTrue(get_user_model().objects.filter(username='testuser').exists())


class LeadViewsTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            is_organisor=True
        )
        self.lead = Lead.objects.create(
            first_name='John',
            last_name='Doe',
            age=30,
            email='john@example.com',
            phone_number='123456789',
            description='Example lead description',
            agent=None,
            organisation=self.user.userprofile
        )

    def test_lead_list_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('leads:lead-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/lead_list.html')

    def test_lead_create_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('leads:lead-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/lead_create.html')

    def test_lead_detail_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('leads:lead-detail', kwargs={'pk': self.lead.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/lead_detail.html')

    def test_lead_update_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('leads:lead-update', kwargs={'pk': self.lead.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/lead_update.html')

    def test_lead_delete_view(self):
        self.client.login(username='testuser', password='testpass')
        url = reverse('leads:lead-delete', kwargs={'pk': self.lead.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'leads/lead_delete.html')


class AssignAgentViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
            is_organisor=True
        )

        self.client.login(username='testuser', password='testpass')

        lead_data = {
            'first_name': 'Test',
            'last_name': 'Lead',
            'age': 30,
            'email': 'test@example.com',
            'phone_number': '123-456-7890',
            'description': 'Test lead description',
            'organisation': self.user.userprofile,
        }

        self.lead = Lead.objects.create(**lead_data)

        agent_data = {
            'user': self.user,
            'organisation': self.user.userprofile,
        }

        self.agent = Agent.objects.create(**agent_data)

    def test_assign_agent_form_submission(self):
        redirect_url = reverse('leads:lead-list')

        data = {
            'agent': self.agent.pk,
        }

        response = self.client.post(reverse('leads:assign-agent', kwargs={'pk': self.lead.pk}), data)
        self.assertRedirects(response, redirect_url)

        self.lead.refresh_from_db()

        self.assertEqual(self.lead.agent, self.agent)
