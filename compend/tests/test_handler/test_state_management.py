import pytest


from handler.state_management import UnsavedObjectException
from handler import state_management

@pytest.mark.asyncio
class TestStateManager:
    
    @pytest.fixture(scope="function", autouse=True)
    def setup_fixtures(
        self, fake_redis_client
    ):
        self.manager = state_management.StateManager(client=fake_redis_client)

    def test_save_page(self, fake_redis_client, fake_notion_page_object):
        fake_notion_page_object.id = 1234
        self.manager.save_page("0000", "test", fake_notion_page_object)

        expected = {
            "0000": {
                "test": fake_notion_page_object
            }
        }
        
        assert expected.items() <= self.manager.states.items()
        fake_redis_client.set.assert_called_once_with("0000:test", 1234)
        
        
    def test_get_from_state(self, fake_notion_page_object):
        fake_notion_page_object.id = 1337
        self.manager.save_page("0000", "foo", fake_notion_page_object)
        obj = self.manager.get_from_state("0000", "foo")
        assert obj == fake_notion_page_object
        with pytest.raises(UnsavedObjectException):
            _obj = self.manager.get_from_state("1111", "foo")


        
        
      