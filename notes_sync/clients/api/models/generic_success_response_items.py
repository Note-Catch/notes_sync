from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.generic_success_response_items_items_item import (
        GenericSuccessResponseItemsItemsItem,
    )


T = TypeVar("T", bound="GenericSuccessResponseItems")


@_attrs_define
class GenericSuccessResponseItems:
    """
    Attributes:
        count (int):
        items (List['GenericSuccessResponseItemsItemsItem']):
    """

    count: int
    items: List["GenericSuccessResponseItemsItemsItem"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        count = self.count

        items = []
        for items_item_data in self.items:
            items_item = items_item_data.to_dict()
            items.append(items_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "count": count,
                "items": items,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.generic_success_response_items_items_item import (
            GenericSuccessResponseItemsItemsItem,
        )

        d = src_dict.copy()
        count = d.pop("count")

        items = []
        _items = d.pop("items")
        for items_item_data in _items:
            items_item = GenericSuccessResponseItemsItemsItem.from_dict(items_item_data)

            items.append(items_item)

        generic_success_response_items = cls(
            count=count,
            items=items,
        )

        generic_success_response_items.additional_properties = d
        return generic_success_response_items

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
