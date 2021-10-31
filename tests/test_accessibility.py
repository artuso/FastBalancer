from schemas.serialize import serialize_list, serialize_dict
from bson import ObjectId
import pytest


class TestAccessibilityRoutes:

    @pytest.mark.asyncio
    async def test_get_available_stand(self, api_client, db_client) -> None:
        params = {"platform": "ios"}
        res = await api_client.get(url="/get_available_stand", params=params)
        await api_client.aclose()
        assert res.status_code == 200
        stand = serialize_dict(db_client.connection.appium.stand.find_one({"_id": ObjectId(res.json()["_id"])}))
        assert res.json()["name"] == stand["name"]
        assert res.json()["address"] == stand["address"]
        assert res.json()["platform"] == params["platform"]
        assert res.json()["available"] is False
        other_stands = serialize_list(db_client.connection.appium.stand.find({"platform": params["platform"],
                                                                              "available": True}))
        assert len(other_stands) == 1

    @pytest.mark.dependency(name="all_busy")
    @pytest.mark.asyncio
    async def test_get_take_over_all_stands(self, api_client, db_client) -> None:
        params = {"platform": "ios"}
        res = await api_client.get(url="/take_over_all_stands", params=params)
        await api_client.aclose()
        assert res.status_code == 200
        stands = serialize_list(db_client.connection.appium.stand.find({"platform": params["platform"]}))
        assert len(stands) == 2
        for stand in stands:
            assert stand["available"] is False

    @pytest.mark.dependency(depends=["all_busy"])
    @pytest.mark.asyncio
    async def test_get_take_over_all_stands_all_busy(self, api_client, db_client) -> None:
        params = {"platform": "ios"}
        res = await api_client.get(url="/take_over_all_stands", params=params)
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()["message"] == "All the stands are busy"
        assert res.json()["no_stands_available"] is True

    @pytest.mark.dependency(depends=["all_busy"])
    @pytest.mark.asyncio
    async def test_get_available_stand_all_busy(self, api_client, db_client) -> None:
        params = {"platform": "ios"}
        res = await api_client.get(url="/get_available_stand", params=params)
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()["message"] == "All the stands are busy"
        assert res.json()["no_stands_available"] is True

    @pytest.mark.dependency(name="all_available")
    @pytest.mark.asyncio
    async def test_get_vacate_all_stands(self, api_client, db_client) -> None:
        params = {"platform": "ios"}
        res = await api_client.get(url="/vacate_all_stands", params=params)
        await api_client.aclose()
        assert res.status_code == 200
        stands = serialize_list(db_client.connection.appium.stand.find({"platform": params["platform"]}))
        assert len(stands) == 2
        for stand in stands:
            assert stand["available"] is True

    @pytest.mark.dependency(depends=["all_available"])
    @pytest.mark.asyncio
    async def test_get_vacate_all_stands_all_available(self, api_client, db_client) -> None:
        params = {"platform": "ios"}
        res = await api_client.get(url="/vacate_all_stands", params=params)
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()["message"] == "All the stands are available"
        assert res.json()["no_stands_available"] is False
