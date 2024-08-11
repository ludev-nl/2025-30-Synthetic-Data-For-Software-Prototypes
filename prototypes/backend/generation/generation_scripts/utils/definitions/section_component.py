from typing import List
from utils.definitions.model import Model, Attribute

class SectionComponent():
    """Definition of a Section Component. A Section Component is a component
    on a page on which the end user can act on the attributes of a model."""
    def __init__(
            self,
            id: str,
            name: str,
            application: str, # TODO: reference
            primary_model: Model, # TODO: reference
            parent_models: List[Model], # TODO: implement
            attributes: List[Attribute],
            updatable_attributes: List[Attribute], # TODO: implement
            has_create_operation: bool = False,
            has_delete_operation: bool = False,
            has_update_operation: bool = False
    ):
        self.name = name
        self.id = id
        self.application = application
        self.primary_model = primary_model
        self.parent_models = parent_models
        self.attributes = attributes
        self.updatable_attributes = updatable_attributes
        self.has_create_operation = has_create_operation
        self.has_delete_operation = has_delete_operation
        self.has_update_operation = has_update_operation