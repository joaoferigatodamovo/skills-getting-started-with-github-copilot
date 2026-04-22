import pytest
from httpx import AsyncClient, ASGITransport
from src.app import app

@pytest.mark.asyncio
async def test_get_activities():
    # Arrange
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Act
        response = await ac.get("/activities")
    # Assert
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

@pytest.mark.asyncio
async def test_signup_for_activity():
    # Arrange
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        # Act
        response = await ac.post(f"/activities/{activity}/signup?email={test_email}")
    # Assert
    assert response.status_code in (200, 400)  # 400 if already signed up
    if response.status_code == 200:
        assert f"Signed up {test_email}" in response.json()["message"]
    else:
        assert response.json()["detail"] == "Student already signed up"
