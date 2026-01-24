import pytest
from starlette.testclient import TestClient

from invoices.domain.models.invoice import Invoice


@pytest.mark.asyncio
async def test_empty(client: TestClient):
    """Test that the endpoint returns an empty list when no invoices are present."""
    response = client.get("/invoices")

    assert response.status_code == 200, response.text
    assert response.json() == []


@pytest.mark.asyncio
async def test_not_empty(client: TestClient, invoice: Invoice):
    """Test that the endpoint returns a list with one invoice when an invoice is present."""
    response = client.get("/invoices")

    assert response.status_code == 200, response.text
    assert response.json() == [{"id": str(invoice.id)}]
