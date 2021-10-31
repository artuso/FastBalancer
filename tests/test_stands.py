from schemas.serialize import serialize_list
import pytest


class TestStandsRoutes:

    @pytest.mark.asyncio
    async def test_get_stands(self, api_client) -> None:
        res = await api_client.get(url="/stands")
        await api_client.aclose()
        assert res.status_code == 200
        assert len(res.json()) == 10

    @pytest.mark.asyncio
    async def test_get_stand_by_id(self, api_client, db_client) -> None:
        stands = serialize_list(db_client.connection.appium.stand.find())
        res = await api_client.get(url=f"/stand/{stands[0]['_id']}")
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()['_id'] == stands[0]['_id']

    @pytest.mark.dependency(name="post_stand")
    @pytest.mark.asyncio
    async def test_post_stand(self, api_client) -> None:
        payload = {"name": "stand_11", "address": "0.0.0.10", "platform": "ios", "available": True}
        res = await api_client.post(url="/stand", json=payload)
        await api_client.aclose()
        assert res.status_code == 200
        assert len(res.json()) == 11
        assert res.json()[10]["name"] == payload["name"]
        assert res.json()[10]["address"] == payload["address"]
        assert res.json()[10]["platform"] == payload["platform"]
        assert res.json()[10]["available"] == payload["available"]

    @pytest.mark.dependency(depends=["post_stand"])
    @pytest.mark.asyncio
    async def test_put_stand(self, api_client, db_client) -> None:
        stand = serialize_list(db_client.connection.appium.stand.find())[10]
        payload = {"name": "stand_12", "address": "0.0.0.11", "platform": "ios", "available": True}
        res = await api_client.put(url=f"/stand/{stand['_id']}", json=payload)
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()["name"] == payload["name"]
        assert res.json()["address"] == payload["address"]
        assert res.json()["platform"] == payload["platform"]
        assert res.json()["available"] == payload["available"]

    @pytest.mark.dependency(depends=["post_stand"])
    @pytest.mark.asyncio
    async def test_patch_stand(self, api_client, db_client) -> None:
        stand = serialize_list(db_client.connection.appium.stand.find())[10]
        payload = {"available": False}
        res = await api_client.patch(url=f"/stand/{stand['_id']}", json=payload)
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()["name"] == stand["name"]
        assert res.json()["address"] == stand["address"]
        assert res.json()["platform"] == stand["platform"]
        assert res.json()["available"] == payload["available"]

    @pytest.mark.dependency(depends=["post_stand"])
    @pytest.mark.asyncio
    async def test_delete_stand(self, api_client, db_client) -> None:
        stand = serialize_list(db_client.connection.appium.stand.find())[10]
        res = await api_client.delete(url=f"/stand/{stand['_id']}")
        await api_client.aclose()
        assert res.status_code == 200
        assert res.json()["_id"] == stand['_id']
        assert len(serialize_list(db_client.connection.appium.stand.find())) == 10
