from typing import Any, Dict, List, Type, TypeVar, Union

from attrs import define as _attrs_define
from attrs import field as _attrs_field

from ..models.error_code import ErrorCode
from ..types import UNSET, Unset

T = TypeVar("T", bound="UserAlreadyExistsResponse")


@_attrs_define
class UserAlreadyExistsResponse:
    """
    Attributes:
        error_code (Union[Unset, ErrorCode]):
        error_message (Union[Unset, str]):  Default: 'User with given username already exists'.
    """

    error_code: Union[Unset, ErrorCode] = UNSET
    error_message: Union[Unset, str] = "User with given username already exists"
    additional_properties: Dict[str, Any] = _attrs_field(init=False, factory=dict)

    def to_dict(self) -> Dict[str, Any]:
        error_code: Union[Unset, int] = UNSET
        if not isinstance(self.error_code, Unset):
            error_code = self.error_code.value

        error_message = self.error_message

        field_dict: Dict[str, Any] = {}
        field_dict.update(self.additional_properties)
        field_dict.update({})
        if error_code is not UNSET:
            field_dict["error_code"] = error_code
        if error_message is not UNSET:
            field_dict["error_message"] = error_message

        return field_dict

    @classmethod
    def from_dict(cls: Type[T], src_dict: Dict[str, Any]) -> T:
        d = src_dict.copy()
        _error_code = d.pop("error_code", UNSET)
        error_code: Union[Unset, ErrorCode]
        if isinstance(_error_code, Unset):
            error_code = UNSET
        else:
            error_code = ErrorCode(_error_code)

        error_message = d.pop("error_message", UNSET)

        user_already_exists_response = cls(
            error_code=error_code,
            error_message=error_message,
        )

        user_already_exists_response.additional_properties = d
        return user_already_exists_response

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
