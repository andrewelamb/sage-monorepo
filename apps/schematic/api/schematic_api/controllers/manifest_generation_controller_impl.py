"""Manifest generation functions"""
# pylint: disable=too-many-arguments

from typing import Union, BinaryIO, Optional
from schematic import CONFIG  # type: ignore
from schematic.manifest.generator import ManifestGenerator  # type: ignore

from schematic_api.models.basic_error import BasicError
from schematic_api.models.google_sheet_links import GoogleSheetLinks
from schematic_api.controllers.utils import (
    handle_exceptions,
    get_access_token,
    download_schema_file_as_jsonld,
    InvalidValueError,
)


@handle_exceptions
def generate_excel_manifest(
    schema_url: str,
    asset_view_id: str,
    node_label: str,
    add_annotations: bool,
    manifest_title: str,
    dataset_id: Optional[str],
) -> tuple[Union[BinaryIO, BasicError], int]:
    """Generates a manifest in excel form

    Args:
        schema_url (str): The URL of the schema
        dataset_id (Optional[str]): Use this to get the existing manifest in the dataset.
          Must be of same type as the node_label
        asset_view_id (str): ID of the asset view
        node_label (str): The datatype of the manifest to generate
        add_annotations (bool): Whether or not annotatiosn get added to the manifest
        manifest_title (str): Title of the manifest

    Returns:
        tuple[Union[BinaryIO, BasicError], int]: A tuple
           The first item is either manifest in Excel form or an error object
           The second item is the response status
    """
    access_token = get_access_token()
    CONFIG.load_config("schematic_api/config.yml")
    CONFIG.synapse_master_fileview_id = asset_view_id
    schema_path = download_schema_file_as_jsonld(schema_url)
    manifest = ManifestGenerator.create_single_manifest(
        jsonld=schema_path,
        output_format="excel",
        data_type=node_label,
        title=manifest_title,
        access_token=access_token,
        dataset_id=dataset_id,
        use_annotations=add_annotations,
    )
    result: Union[BinaryIO, BasicError] = manifest
    status = 200
    return result, status


@handle_exceptions
def generate_google_sheet_manifests(
    schema_url: str,
    asset_view_id: str,
    add_annotations: bool,
    dataset_id_array: Optional[list[str]],
    manifest_title: str,
    node_label_array: Optional[list[str]],
    use_strict_validation: bool,
    generate_all_manifests: bool,
) -> tuple[Union[GoogleSheetLinks, BasicError], int]:
    """Generates a list of links to manifets in google sheet form

    Args:
        schema_url (str): The URL of the schema
        dataset_id_array (Optional[list[str]]): Use this to get the existing manifests in the
          datasets. Must be of same type as the node_label_array, same order, and same length
        asset_view_id (str): ID of the asset view
        node_label_array (Optional[list[str]]): The datatypes of the manifests to generate
        add_annotations (bool): Whether or not annotatiosn get added to the manifest
        manifest_title (str): Title of the manifest
        use_strict_validation (bool): Whether or not to use google sheet strict validation
        generate_all_manifests (bool): Will generate a manifest for all data types

    Raises:
        ValueError: When generate_all_manifests is true and either dataset_id_array or
          node_label_array are provided
        ValueError: When generate_all_manifests is false and node_label_array is not provided
        ValueError: When generate_all_manifests is false and dataset_id_arrayy is provided,
          but it doesn't match the length of node_label_array

    Returns:
        tuple[Union[GoogleSheetLinks, BasicError], int]: A tuple
           The first item is either the google sheet links of the manifests or an error object
           The second item is the response status
    """

    if generate_all_manifests:
        if dataset_id_array:
            raise InvalidValueError(
                "When generate_all_manifests is True dataset_id_array must be None",
                {"dataset_id_array": dataset_id_array},
            )
        if node_label_array:
            raise InvalidValueError(
                "When generate_all_manifests is True node_label_array must be None",
                {"node_label_array": node_label_array},
            )
        node_label_array = ["all_manifests"]

    else:
        if not node_label_array:
            raise InvalidValueError(
                (
                    "When generate_all_manifests is False node_label_array must be a list with "
                    "atleast one item"
                ),
                {"node_label_array": node_label_array},
            )
        if dataset_id_array and len(dataset_id_array) != len(node_label_array):
            raise InvalidValueError(
                (
                    "When generate_all_manifests is False node_label_array and dataset_id_array "
                    "must both lists with the same length"
                ),
                {
                    "node_label_array": node_label_array,
                    "dataset_id_array": dataset_id_array,
                },
            )

    access_token = get_access_token()
    CONFIG.load_config("schematic_api/config.yml")
    CONFIG.synapse_master_fileview_id = asset_view_id
    schema_path = download_schema_file_as_jsonld(schema_url)
    links = ManifestGenerator.create_manifests(
        jsonld=schema_path,
        output_format="google_sheet",
        data_types=node_label_array,
        title=manifest_title,
        access_token=access_token,
        dataset_ids=dataset_id_array,
        strict=use_strict_validation,
        use_annotations=add_annotations,
    )
    result: Union[GoogleSheetLinks, BasicError] = GoogleSheetLinks(links)
    status = 200
    return result, status