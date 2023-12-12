class AgentListViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username='admin',
            password='adminpass',
            is_organisor=True
        )

        self.user_profile = self.user.userprofile

        permission = Permission.objects.get(codename='view_agent')
        self.user.user_permissions.set([permission])

        self.agent = Agent.objects.create(
            user=self.user,
            organisation=self.user_profile
        )

        self.client = Client()
        self.client.login(username='admin', password='adminpass')

    def test_agent_list_view(self):
        url = reverse('agents:agent-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'agents/agent_list.html')

        self.assertContains(response, self.agent.user.email)