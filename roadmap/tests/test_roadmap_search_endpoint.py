from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from roadmap.models import Roadmap, Vertex, InfoCard, MetaDomain, LocalDomain, KnowledgeType, EntryLevel, Tag
from roadmap.serializers import RoadmapSerializer
from user.models import User


class UserForTests(APITestCase):
    def setUp(self):
        self.url = "/api/roadmaps/search/"
        self.user_data = {
            "username": "test_user",
            "email": "testuser@gmail.com",
            "password": "test_user",
            "avatar": None,
        }
        self.user = User.objects.create(**self.user_data)
        self.client.force_authenticate(self.user)


class RoadmapSearchApiViewTests(UserForTests):

    def setUp(self):
        super().setUp()

        self.meta_domain = MetaDomain.objects.create(name="Test Meta Domain")
        self.local_domain = LocalDomain.objects.create(name="Test Local Domain")
        self.knowledge_type = KnowledgeType.objects.create(name="Test Knowledge Type")
        self.entry_level = EntryLevel.objects.create(name="Test Entry Level")
        self.tag1 = Tag.objects.create(name="Tag 1")
        self.tag2 = Tag.objects.create(name="Tag 2")
        self.tag3 = Tag.objects.create(name="Tag 3")

        self.roadmap1 = Roadmap.objects.create(published=True, title="Roadmap 1")
        self.roadmap2 = Roadmap.objects.create(published=True, title="Roadmap 2")
        self.unpublished_roadmap = Roadmap.objects.create(published=False, title="Unpublished Roadmap")

        self.info_card1 = InfoCard.objects.create(
            meta_domain=self.meta_domain,
            local_domain=self.local_domain,
            knowledge_type=self.knowledge_type,
            entry_level=self.entry_level,
            title="Info Card 1"
        )
        self.info_card1.tags.add(self.tag1, self.tag2)
        self.vertex1 = Vertex.objects.create(roadmap=self.roadmap1, info_card=self.info_card1)

        self.info_card2 = InfoCard.objects.create(
            meta_domain=self.meta_domain,
            local_domain=self.local_domain,
            knowledge_type=self.knowledge_type,
            entry_level=self.entry_level,
            title="Info Card 2"
        )
        self.info_card2.tags.add(self.tag2, self.tag3)
        self.vertex2 = Vertex.objects.create(roadmap=self.roadmap2, info_card=self.info_card2)

    def test_search_by_entry_level(self):
        response = self.client.get(self.url, {'entry_level': 'Test Entry Level'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_by_meta_domain(self):
        response = self.client.get(self.url, {'meta_domain': 'Test Meta Domain'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_by_local_domain(self):
        response = self.client.get(self.url, {'local_domain': 'Test Local Domain'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_full_text_search(self):
        response = self.client.get(self.url, {'search': 'road'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_search_all_parameters_together(self):
        response = self.client.get(self.url, {
            'search': 'Roadmap',
            'page': 1,
            'meta_domain': 'Test Meta Domain',
            'local_domain': 'Test Local Domain',
            'entry_level': 'Test Entry Level',
            'ordering': 'asc'
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 2)

    def test_unpublished_roadmap_not_displayed(self):
        response = self.client.get(self.url, {'search': 'Roadmap', 'page': 1})
        self.assertEqual(response.status_code, 200)
        titles = [roadmap['title'] for roadmap in response.data['results']]
        self.assertNotIn(self.unpublished_roadmap.title, titles)


class TestPagination(UserForTests):
    def setUp(self):
        super().setUp()
        for i in range(6):
            Roadmap.objects.create(published=True, title=f"Roadmap {i + 1}")

    def test_pagination_default(self):
        response = self.client.get(self.url, {'search': 'Roadmap', 'page': 1})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 5)

    def test_pagination_custom(self):
        response = self.client.get(self.url, {'search': 'Roadmap', 'page': 1, 'page_size': 3})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.data['results']), 3)
