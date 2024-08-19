from typing import List
from utils.sanitization import app_name_sanitization, model_name_sanitization, category_name_sanitization
from utils.definitions.application_component import ApplicationComponent
from utils.definitions.section_component import SectionComponent
from utils.definitions.page import Page
from utils.definitions.category import Category
import json
from uuid import uuid4


def get_apps(metadata: str) -> List[str]:
    """Returns a list of all application component names"""
    apps = []
    
    try:
        if metadata:
            for interface in json.loads(metadata)["interfaces"]:
                apps.append(app_name_sanitization(interface["value"]["name"]))
    except:
        raise Exception("Failed to retrieve names of interfaces")
    return " ".join(apps)


def find_model_by_id(metadata: str, class_id: str) -> str | None:
    for diagram in json.loads(metadata)["diagrams"]:
        if diagram["type"] != "classes":
            continue
        for node in diagram["nodes"]:
            if node["cls_ptr"] == class_id:
                return model_name_sanitization(node["cls"]["name"])
    return None


def find_category_by_id(metadata: str, category_id: str) -> str | None:
    for interface in json.loads(metadata)["interfaces"]:
        if "categories" not in interface["value"]["data"]:
            continue # Empty interface

        for category in interface["value"]["data"]["categories"]:
            if category["id"] == category_id:
                return category_name_sanitization(category["name"])
    return None


# TODO: redundant
def filter_section_components_by_application(section_components: List[SectionComponent], application: str) -> List[SectionComponent]:
    out = []
    for section_component in section_components:
        if section_component.application == application:
            out.append(section_component)
    return out


# TODO: redundant
def filter_pages_by_application(pages: List[Page], application: str) -> List[Page]:
    out = []
    for page in pages:
        if page.application == application:
            out.append(page)
    return out


def retrieve_section_components(application_name: str, page_name: str, metadata: str) -> List[SectionComponent]:
    '''Function that retrieves the section components corresponding to page_name from
    metadata and returns a list of SectionComponent objects.'''
    if metadata in ["", None]:
        raise Exception("Failed to retrieve section components from metadata: metadata is empty")
    
    out = []
    try:
        for application_component in json.loads(metadata)["interfaces"]:
            if application_component["label"] != application_name:
                continue
            
            if "pages" not in application_component["value"]["data"]: # no pages in interface
                return []

            for page in application_component["value"]["data"]["pages"]:
                if page["name"] != page_name:
                    continue

                for section in page["sections"]:
                    sec = SectionComponent(
                        id = section["id"],
                        name = section["name"],
                        application = application_name,
                        page = page_name,
                        primary_model = find_model_by_id(metadata, section["class"]), # TODO: there might be a quicker method than this
                        parent_models = [], # TODO
                        attributes = [], # TODO
                        updatable_attributes = [], # TODO
                        has_create_operation = section["operations"]["create"],
                        has_delete_operation = section["operations"]["delete"],
                        has_update_operation = section["operations"]["update"],

                    )
                    out.append(sec)
            return out
    except:
        raise Exception("Failed to retrieve section components from metadata: parsing error")

    return out


def retrieve_pages(application_name: str, metadata: str) -> List[Page]:
    '''Function that retrieves the pages corresponding to application_name from
    metadata and returns a list of Page objects.'''
    
    if metadata in ["", None]:
        raise Exception("Failed to retrieve pages from metadata: metadata is empty")
    
    out = []

    try:
        for application_component in json.loads(metadata)["interfaces"]:
            if "pages" not in application_component["value"]["data"]: # empty interface
                continue
            if application_component["label"] != application_name:
                continue

            for page in application_component["value"]["data"]["pages"]:
                pg = Page(
                    id = page["id"],
                    name = page["name"],
                    application = application_component["label"],
                    category = find_category_by_id(metadata, page["category"]), # TODO: there might be a quicker method than this
                    section_components = retrieve_section_components(application_name=application_name, page_name=page["name"], metadata=metadata)
                )
            out.append(pg)
    except:
        raise Exception("Failed to retrieve pages from metadata: parsing error")

    return out

def get_application_component(project_name: str, application_name: str, metadata: str) -> ApplicationComponent:
    '''Function that builds an ApplicationComponent object for application_name
    from metadata.'''
    pages = retrieve_pages(application_name=application_name, metadata=metadata)
    return ApplicationComponent(
        id = uuid4(), # TODO: retrieve frontend id from metadata
        project=project_name,
        name=application_name,
        pages=pages
    )