import random
from django.test import TestCase, Client
from django.contrib.auth import get_user_model
from django.urls import reverse
from leads.models import Agent
from agents.forms import AgentModelForm


class AgentListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            is_organisor=True
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_agent_list_view(self):
        url = reverse('agents:agent-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_list.html')


class AgentCreateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            is_organisor=True
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_agent_create_view(self):
        url = reverse('agents:agent-create')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_create.html')

        data = {
            'email': 'agent@example.com',
            'username': 'agentuser',
            'first_name': 'Agent',
            'last_name': 'User',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.assertTrue(get_user_model().objects.filter(email='agent@example.com').exists())
        self.assertTrue(Agent.objects.filter(user__email='agent@example.com').exists())


class AgentDetailViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            is_organisor=True
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

        self.agent = Agent.objects.create(
            user=self.user,
            organisation=self.user.userprofile
        )

    def test_agent_detail_view(self):
        url = reverse('agents:agent-detail', kwargs={'pk': self.agent.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_detail.html')
        self.assertEqual(response.context['agent'], self.agent)


class AgentUpdateViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            is_organisor=True
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

        self.agent = Agent.objects.create(
            user=self.user,
            organisation=self.user.userprofile
        )

    def test_agent_update_view(self):
        url = reverse('agents:agent-update', kwargs={'pk': self.agent.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_update.html')

        data = {
            'email': 'updated_agent@example.com',
            'username': 'updated_agentuser',
            'first_name': 'Updated',
            'last_name': 'Agent',
        }
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, 302)

        self.agent.refresh_from_db()
        self.assertEqual(self.agent.user.email, 'updated_agent@example.com')


class AgentDeleteViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            is_organisor=True
        )
        self.client = Client()
        self.client.login(username='admin', password='adminpass')

        self.agent = Agent.objects.create(
            user=self.user,
            organisation=self.user.userprofile
        )

    def test_agent_delete_view(self):
        url = reverse('agents:agent-delete', kwargs={'pk': self.agent.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_delete.html')

        response = self.client.post(url, {})
        self.assertEqual(response.status_code, 302)

        self.assertFalse(Agent.objects.filter(user=self.agent.user).exists())
