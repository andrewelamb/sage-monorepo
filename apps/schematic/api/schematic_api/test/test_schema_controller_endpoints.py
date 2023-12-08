"""Tests for schema endpoints"""

# pylint: disable=duplicate-code
import unittest

from schematic_api.test import BaseTestCase
from .conftest import TEST_SCHEMA_URL

HEADERS = {
    "Accept": "application/json",
    "Authorization": "Bearer xxx",
}

COMPONENT_URL = "/api/v1/components/Patient/?schemaUrl="
CONNECTED_NODES_URL = "/api/v1/connectedNodes?schemaUrl="
NODE_IS_REQUIRED_URL = "/api/v1/nodes/FamilyHistory/isRequired?schemaUrl="
PROPERTY_LABEL_URL = "/api/v1/nodes/node_label/propertyLabel?schemaUrl="
SCHEMA_ATTRIBUTES_URL = "/api/v1/schemaAttributes?schemaUrl="
NODE_PROPERTIES_URL = "/api/v1/nodes/MolecularEntity/nodeProperties?schemaUrl="
NODE_VALIDATION_RULES_URL = "/api/v1/nodes/CheckRegexList/validationRules?schemaUrl="
NODE_DEPENDENCIES_URL = "/api/v1/nodes/Patient/dependencies?schemaUrl="


class TestGetComponent(BaseTestCase):
    """Test case for component endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{COMPONENT_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert isinstance(response.json, str)

    def test_parameters(self) -> None:
        """Test for successful result"""
        url = f"{COMPONENT_URL}{TEST_SCHEMA_URL}&includeIndex=True"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert isinstance(response.json, str)

    def test_404(self) -> None:
        """Test for 404 result"""
        url = f"{COMPONENT_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert404(response, f"Response body is : {response.data.decode('utf-8')}")


class TestGetConnectedNodes(BaseTestCase):
    """Tests for connected nodes endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{CONNECTED_NODES_URL}{TEST_SCHEMA_URL}&relationshipType=requiresDependency"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert not response.json["hasNext"]
        assert not response.json["hasPrevious"]
        assert response.json["number"] == 0
        assert response.json["size"] == 100
        assert response.json["totalPages"] == 1
        connected_nodes = response.json["connected_nodes"]
        assert connected_nodes
        assert isinstance(connected_nodes, list)

    def test_500(self) -> None:
        """Test for 500 result"""
        url = f"{CONNECTED_NODES_URL}not_a_url&relationshipType=requiresDependency"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert500(response, f"Response body is : {response.data.decode('utf-8')}")


class TestGetNodeIsRequired(BaseTestCase):
    """Test case for node is required endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{NODE_IS_REQUIRED_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert response.json

    def test_500(self) -> None:
        """Test for 500 result"""
        url = f"{NODE_IS_REQUIRED_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert500(response, f"Response body is : {response.data.decode('utf-8')}")


class TestGetPropertyLabel(BaseTestCase):
    """Test case for property label endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{PROPERTY_LABEL_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert response.json == "nodeLabel"

    def test_500(self) -> None:
        """Test for 500 result"""
        url = f"{PROPERTY_LABEL_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert500(response, f"Response body is : {response.data.decode('utf-8')}")


class TestGetSchemaAttributes(BaseTestCase):
    """Test case for schema attributes endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{SCHEMA_ATTRIBUTES_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert isinstance(response.json, str)

    def test_404(self) -> None:
        """Test for 404 result"""
        url = f"{SCHEMA_ATTRIBUTES_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert404(response, f"Response body is : {response.data.decode('utf-8')}")


class TestGetNodeProperties(BaseTestCase):
    """Test case for node attributes endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{NODE_PROPERTIES_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert not response.json["hasNext"]
        assert not response.json["hasPrevious"]
        assert response.json["number"] == 0
        assert response.json["size"] == 100
        assert response.json["totalPages"] == 1
        node_properties = response.json["node_properties"]
        assert isinstance(node_properties, list)

    def test_500(self) -> None:
        """Test for 500 result"""
        url = f"{NODE_PROPERTIES_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert500(response, f"Response body is : {response.data.decode('utf-8')}")


class TestNodeValidationRules(BaseTestCase):
    """Test case for node validation rules endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{NODE_VALIDATION_RULES_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")

        assert not response.json["hasNext"]
        assert not response.json["hasPrevious"]
        assert response.json["number"] == 0
        assert response.json["size"] == 100
        assert response.json["totalPages"] == 1
        validation_rules = response.json["validation_rules"]
        assert validation_rules

    def test_500(self) -> None:
        """Test for 500 result"""
        url = f"{NODE_VALIDATION_RULES_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert500(response, f"Response body is : {response.data.decode('utf-8')}")


class TestNodeDependencies(BaseTestCase):
    """Test case for node depencencies endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        url = f"{NODE_DEPENDENCIES_URL}{TEST_SCHEMA_URL}"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")
        assert not response.json["hasNext"]
        assert not response.json["hasPrevious"]
        assert response.json["number"] == 0
        assert response.json["size"] == 100
        assert response.json["totalPages"] == 1
        dependencies = response.json["nodes"]
        assert dependencies

    def test_return_display_names(self) -> None:
        """Test for returnDisplayNames parameter"""
        url = f"{NODE_DEPENDENCIES_URL}{TEST_SCHEMA_URL}&returnDisplayNames=true"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")

        url = f"{NODE_DEPENDENCIES_URL}{TEST_SCHEMA_URL}&returnDisplayNames=false"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")

    def test_return_ordered_by_schema(self) -> None:
        """Test for returnOrderedBySchema parameter"""
        url = f"{NODE_DEPENDENCIES_URL}{TEST_SCHEMA_URL}&returnOrderedBySchema=true"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")

        url = f"{NODE_DEPENDENCIES_URL}{TEST_SCHEMA_URL}&returnOrderedBySchema=false"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert200(response, f"Response body is : {response.data.decode('utf-8')}")

    def test_500(self) -> None:
        """Test for 500 result"""
        url = f"{NODE_DEPENDENCIES_URL}not_a_url"
        response = self.client.open(url, method="GET", headers=HEADERS)
        self.assert500(response, f"Response body is : {response.data.decode('utf-8')}")


if __name__ == "__main__":
    unittest.main()
