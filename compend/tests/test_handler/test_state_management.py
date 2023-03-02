import pytest
from unittest.mock import patch

from handler.state_management import UnsavedObjectException
from handler import state_management


@pytest.mark.asyncio
class TestStateManager:
    @pytest.fixture(scope="function", autouse=True)
    def setup_fixtures(self, fake_redis_client):
        self.manager = state_management.StateManager(client=fake_redis_client)

    def test_save_page(self, fake_redis_client, fake_notion_page_object):
        fake_notion_page_object.id = 1234
        self.manager.save_page("0000", "test", fake_notion_page_object)
        expected = {"0000": {"test": fake_notion_page_object}}
        assert expected.items() <= self.manager.states.items()
        fake_redis_client.set.assert_called_once_with("0000:test", 1234)
        
    def test_get_from_state_unsaved(self):
        with pytest.raises(UnsavedObjectException):
            _obj = self.manager.get_from_state("1111", "foo")        
    
    def test_get_from_state_success(self, fake_notion_page_object):
        fake_notion_page_object.id = 1337
        self.manager.save_page("0000", "foo", fake_notion_page_object)
        obj = self.manager.get_from_state("0000", "foo")
        assert obj == fake_notion_page_object
        
    async def test_get_page_unsaved_page(self, fake_redis_client):
        fake_redis_client.get.return_value = None
        obj = await self.manager.get_page("0000", "foo")
        assert obj is None
        fake_redis_client.get.assert_called_once_with("0000:foo")

  
    @patch("handler.state_management.StateManager.save_page")    
    @patch("handler.state_management.get_page_object_for_id")
    async def test_get_page_unsaved_object(self, mock_api_get_page, mock_save_page, fake_notion_page_object, fake_redis_client):
        fake_redis_client.get.return_value = 1000
        mock_api_get_page.return_value = fake_notion_page_object
        obj = await self.manager.get_page("0000", "foo")
        
        assert obj == fake_notion_page_object
        fake_redis_client.get.assert_called_once_with("0000:foo")
        mock_save_page.assert_called_once_with("0000", "foo", fake_notion_page_object)
        
        
        
        
        
    