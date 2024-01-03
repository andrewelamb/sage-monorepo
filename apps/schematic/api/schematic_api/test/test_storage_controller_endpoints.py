"""Tests for endpoints"""
# pylint: disable=duplicate-code

import unittest
from unittest.mock import patch
import pandas as pd

from synapseclient.core.exceptions import SynapseNoCredentialsError  # type: ignore
from schematic.exceptions import AccessCredentialsError  # type: ignore

import schematic_api.controllers.storage_controller_impl
from schematic_api.test import BaseTestCase
from schematic_api.models.file_metadata import FileMetadata
from schematic_api.models.dataset_metadata import DatasetMetadata
from .conftest import EXAMPLE_MANIFEST_METADATA, MANIFEST_METADATA_KEYS

HEADERS = {
    "Accept": "application/json",
    "Authorization": "Bearer xxx",
}

ASSET_VIEW_JSON_URL = "/api/v1/assetTypes/synapse/assetViews/syn1/json"
DATASET_FILE_METADATA_ARRAY_URL = (
    "/api/v1/assetTypes/synapse/datasets/syn2/fileMetadataArray?assetViewId=syn1"
)
DATASET_FILE_METADATA_PAGE_URL = (
    "/api/v1/assetTypes/synapse/datasets/syn2/fileMetadataPage?assetViewId=syn1"
)
DATASET_MANIFEST_JSON_URL = (
    "/api/v1/assetTypes/synapse/datasets/syn2/manifestJson?assetViewId=syn1"
)
MANIFEST_JSON_URL = "/api/v1/assetTypes/synapse/manifests/syn1/json"
PROJECTS_URL = "/api/v1/assetTypes/synapse/assetViews/syn1/projects"
PROJECT_DATASET_METATDATA_ARRRAY_URL = (
    "/api/v1/assetTypes/synapse/projects/syn2/datasetMetadataArray?assetViewId=syn1"
)
PROJECT_DATASET_METATDATA_PAGE_URL = (
    "/api/v1/assetTypes/synapse/projects/syn2/datasetMetadataPage?assetViewId=syn1"
)
PROJECT_MANIFEST_METADATA_ARRAY_URL = (
    "/api/v1/assetTypes/synapse/projects/syn2/manifestMetadataArray?assetViewId=syn1"
)
PROJECT_MANIFEST_METADATA_PAGE_URL = (
    "/api/v1/assetTypes/synapse/projects/syn2/manifestMetadataPage?assetViewId=syn1"
)


class TestGetAssetViewJson(BaseTestCase):
    """Test case for asset view json endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_asset_view_from_schematic",
            return_value=pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
        ):
            response = self.client.open(
                ASSET_VIEW_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            assert response.json == '{"col1":{"0":1,"1":2},"col2":{"0":3,"1":4}}'

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_asset_view_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                ASSET_VIEW_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_asset_view_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                ASSET_VIEW_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_asset_view_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                ASSET_VIEW_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetDatasetFileMetadataArray(BaseTestCase):
    """Test case for files endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            return_value=[FileMetadata("syn1", "name1"), FileMetadata("syn2", "name2")],
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            result = response.json
            assert isinstance(result, dict)
            assert isinstance(result["files"], list)
            for item in result["files"]:
                assert isinstance(item, dict)
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)

    def test_file_names(self) -> None:
        """Test with file_names parameter"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            return_value=[FileMetadata("syn1", "name1"), FileMetadata("syn2", "name2")],
        ) as mock_function:
            response = self.client.open(
                DATASET_FILE_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", None, False)

            url = f"{DATASET_FILE_METADATA_ARRAY_URL}&fileNames=file.text"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", ["file.text"], False)

            url = f"{DATASET_FILE_METADATA_ARRAY_URL}&fileNames=file.text&fileNames=file2.text"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with(
                "syn2", "synapse", ["file.text", "file2.text"], False
            )

    def test_use_full_file_path(self) -> None:
        """Test with use_full_file_path parameter"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            return_value=[FileMetadata("syn1", "name1"), FileMetadata("syn2", "name2")],
        ) as mock_function:
            url = f"{DATASET_FILE_METADATA_ARRAY_URL}&useFullFilePath=true"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", None, True)

            url = f"{DATASET_FILE_METADATA_ARRAY_URL}&useFullFilePath=false"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", None, False)

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetDatasetFileMetadataPage(BaseTestCase):
    """Test case for files endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            return_value=[FileMetadata("syn1", "name1"), FileMetadata("syn2", "name2")],
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            result = response.json
            assert isinstance(result, dict)
            assert result["number"] == 1
            assert result["size"] == 100000
            assert not result["hasNext"]
            assert not result["hasPrevious"]
            assert result["totalPages"] == 1
            assert isinstance(result["totalElements"], int)
            assert isinstance(result["files"], list)
            for item in result["files"]:
                assert isinstance(item, dict)
                assert list(item.keys()) == ["id", "name"]
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)

    def test_file_names(self) -> None:
        """Test with file_names parameter"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            return_value=[FileMetadata("syn1", "name1"), FileMetadata("syn2", "name2")],
        ) as mock_function:
            response = self.client.open(
                DATASET_FILE_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", None, False)

            url = f"{DATASET_FILE_METADATA_PAGE_URL}&fileNames=file.text"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", ["file.text"], False)

            url = f"{DATASET_FILE_METADATA_PAGE_URL}&fileNames=file.text&fileNames=file2.text"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with(
                "syn2", "synapse", ["file.text", "file2.text"], False
            )

    def test_use_full_file_path(self) -> None:
        """Test with use_full_file_path parameter"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            return_value=[FileMetadata("syn1", "name1"), FileMetadata("syn2", "name2")],
        ) as mock_function:
            url = f"{DATASET_FILE_METADATA_PAGE_URL}&useFullFilePath=true"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", None, True)

            url = f"{DATASET_FILE_METADATA_PAGE_URL}&useFullFilePath=false"
            response = self.client.open(url, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            mock_function.assert_called_with("syn2", "synapse", None, False)

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_file_metadata_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                DATASET_FILE_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetDatasetManifestJson(BaseTestCase):
    """Test case for manifest json endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_manifest_from_schematic",
            return_value=pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
        ):
            response = self.client.open(
                DATASET_MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            assert response.json == '{"col1":{"0":1,"1":2},"col2":{"0":3,"1":4}}'

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_manifest_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                DATASET_MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_manifest_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                DATASET_MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_dataset_manifest_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                DATASET_MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetManifestJson(BaseTestCase):
    """Test case for manifest json endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_manifest_from_schematic",
            return_value=pd.DataFrame({"col1": [1, 2], "col2": [3, 4]}),
        ):
            response = self.client.open(
                MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            assert response.json == '{"col1":{"0":1,"1":2},"col2":{"0":3,"1":4}}'

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_manifest_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_manifest_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_manifest_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                MANIFEST_JSON_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetProjects(BaseTestCase):
    """Test case for projects endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_projects_from_schematic",
            return_value=[("syn1", "name1"), ("syn2", "name2")],
        ):
            response = self.client.open(PROJECTS_URL, method="GET", headers=HEADERS)
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

            assert not response.json["hasNext"]
            assert not response.json["hasPrevious"]
            assert response.json["number"] == 0
            assert response.json["size"] == 100
            assert response.json["totalElements"] == 2
            assert response.json["totalPages"] == 1
            projects = response.json["projects"]
            assert len(projects) == 2
            project = projects[0]
            assert list(project.keys()) == ["id", "name"]
            assert project["name"] == "name1"
            assert project["id"] == "syn1"

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_projects_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(PROJECTS_URL, method="GET", headers=HEADERS)
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_projects_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(PROJECTS_URL, method="GET", headers=HEADERS)
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_projects_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(PROJECTS_URL, method="GET", headers=HEADERS)
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetProjectDatasetMetadataArray(BaseTestCase):
    """Test case for dataset metadat endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            return_value=[
                DatasetMetadata("syn1", "name1"),
                DatasetMetadata("syn2", "name2"),
            ],
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_ARRRAY_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            result = response.json
            assert isinstance(result, dict)
            assert isinstance(result["datasets"], list)
            for item in result["datasets"]:
                assert isinstance(item, dict)
                assert list(item.keys()) == ["id", "name"]
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_ARRRAY_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_ARRRAY_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_ARRRAY_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetProjectDatasetMetadataPage(BaseTestCase):
    """Test case for dataset metadat endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            return_value=[
                DatasetMetadata("syn1", "name1"),
                DatasetMetadata("syn2", "name2"),
            ],
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            result = response.json
            assert isinstance(result, dict)
            assert result["number"] == 1
            assert result["size"] == 100000
            assert not result["hasNext"]
            assert not result["hasPrevious"]
            assert result["totalPages"] == 1
            assert isinstance(result["totalElements"], int)
            assert isinstance(result["datasets"], list)
            for item in result["datasets"]:
                assert isinstance(item, dict)
                assert list(item.keys()) == ["id", "name"]
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_dataset_metadata_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                PROJECT_DATASET_METATDATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetProjectManifestMetadataArray(BaseTestCase):
    """Test case for manifests endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            return_value=EXAMPLE_MANIFEST_METADATA,
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            result = response.json
            assert isinstance(result, dict)
            assert isinstance(result["manifests"], list)
            for item in result["manifests"]:
                assert isinstance(item, dict)
                assert list(item.keys()) == MANIFEST_METADATA_KEYS
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)
                assert isinstance(item["datasetName"], str)
                assert isinstance(item["datasetId"], str)
                assert isinstance(item["componentName"], str)

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_ARRAY_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


class TestGetProjectManifestMetadataPage(BaseTestCase):
    """Test case for manifests endpoint"""

    def test_success(self) -> None:
        """Test for successful result"""

        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            return_value=EXAMPLE_MANIFEST_METADATA,
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert200(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )
            result = response.json
            assert isinstance(result, dict)
            assert result["number"] == 1
            assert result["size"] == 100000
            assert not result["hasNext"]
            assert not result["hasPrevious"]
            assert result["totalPages"] == 1
            assert isinstance(result["totalElements"], int)
            assert isinstance(result["manifests"], list)
            for item in result["manifests"]:
                assert isinstance(item, dict)
                assert list(item.keys()) == MANIFEST_METADATA_KEYS
                assert isinstance(item["id"], str)
                assert isinstance(item["name"], str)
                assert isinstance(item["datasetName"], str)
                assert isinstance(item["datasetId"], str)
                assert isinstance(item["componentName"], str)

    def test_401(self) -> None:
        """Test for 401 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            side_effect=SynapseNoCredentialsError,
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert401(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_403(self) -> None:
        """Test for 403 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            side_effect=AccessCredentialsError("project"),
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert403(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )

    def test_500(self) -> None:
        """Test for 500 result"""
        with patch.object(
            schematic_api.controllers.storage_controller_impl,
            "get_project_manifest_metadata_from_schematic",
            side_effect=TypeError,
        ):
            response = self.client.open(
                PROJECT_MANIFEST_METADATA_PAGE_URL, method="GET", headers=HEADERS
            )
            self.assert500(
                response, f"Response body is : {response.data.decode('utf-8')}"
            )


if __name__ == "__main__":
    unittest.main()
