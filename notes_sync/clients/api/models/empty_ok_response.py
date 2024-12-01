from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.generic_success_response_items import GenericSuccessResponseItems


T = TypeVar("T", bound="EmptyOkResponse")


@_attrs_define
class EmptyOkResponse:
    """
    Attributes:
        response (GenericSuccessResponseItems):
    """

    response: "GenericSuccessResponseItems"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        response = self.response.to_dict()

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "response": response,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.generic_success_response_items import GenericSuccessResponseItems

        d = src_dict.copy()
        response = GenericSuccessResponseItems.from_dict(d.pop("response"))

        empty_ok_response = cls(
            response=response,
        )

        empty_ok_response.additional_properties = d
        return empty_ok_response

    @property
    def additional_keys(self) -> List[str]:
        return list(self.additional_properties.keys())

    def __getitem__(self, key: str) -> Any:
        return self.additional_properties[key]

    def __setitem__(self, key: str, value: Any) -> None:
        self.additional_properties[key] = value

    def __delitem__(self, key: str) -> None:
        del self.additional_properties[key]

    def __contains__(self, key: str) -> bool:
        return key in self.additional_properties
