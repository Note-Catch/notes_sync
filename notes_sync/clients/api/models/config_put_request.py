from typing import TYPE_CHECKING, Any, Dict, List, Type, TypeVar

from attrs import define as _attrs_define
from attrs import field as _attrs_field

if TYPE_CHECKING:
    from ..models.config_logsequence_enable import ConfigLogsequenceEnable


T = TypeVar("T", bound="ConfigPutRequest")


@_attrs_define
class ConfigPutRequest:
    """
    Attributes:
        config (List['ConfigLogsequenceEnable']):
    """

    config: List["ConfigLogsequenceEnable"]
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        config = []
        for config_item_data in self.config:
            config_item = config_item_data.to_dict()
            config.append(config_item)

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update(
            {
                "config": config,
            }
        )

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        from ..models.config_logsequence_enable import ConfigLogsequenceEnable

        d = src_dict.copy()
        config = []
        _config = d.pop("config")
        for config_item_data in _config:
            config_item = ConfigLogsequenceEnable.from_dict(config_item_data)

            config.append(config_item)

        config_put_request = cls(
            config=config,
        )

        config_put_request.additional_properties = d
        return config_put_request

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
