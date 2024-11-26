from http import HTTPStatus
from typing import Any, Dict, Optional, Union

import httpx

from ... import errors
from ...client import AuthenticatedClient, Client
from ...models.http_validation_error import HTTPValidationError
from ...models.signup_request import SignupRequest
from ...models.signup_response import SignupResponse
from ...models.user_already_exists_response import UserAlreadyExistsResponse
from ...types import Response


def _get_kwargs(
    *,
    body: SignupRequest,
) -> Dict[str, Any]:
    headers: Dict[str, Any] = {}

    _kwargs: Dict[str, Any] = {
        "method": "post",
        "url": "/api/v1/oauth2/signup",
    }

    _body = body.to_dict()

    _kwargs["json"] = _body
    headers["Content-Type"] = "application/json"

    _kwargs["headers"] = headers
    return _kwargs


def _parse_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Optional[
    Union[
        HTTPValidationError,
        Union["SignupResponse", "UserAlreadyExistsResponse"],
        UserAlreadyExistsResponse,
    ]
]:
    if response.status_code == 200:

        def _parse_response_200(
            data: object,
        ) -> Union["SignupResponse", "UserAlreadyExistsResponse"]:
            try:
                if not isinstance(data, dict):
                    raise TypeError()
                response_200_type_0 = SignupResponse.from_dict(data)

                return response_200_type_0
            except:  # noqa: E722
                pass
            if not isinstance(data, dict):
                raise TypeError()
            response_200_type_1 = UserAlreadyExistsResponse.from_dict(data)

            return response_200_type_1

        response_200 = _parse_response_200(response.json())

        return response_200
    if response.status_code == 400:
        response_400 = UserAlreadyExistsResponse.from_dict(response.json())

        return response_400
    if response.status_code == 422:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(response.status_code, response.content)
    else:
        return None


def _build_response(
    *, client: Union[AuthenticatedClient, Client], response: httpx.Response
) -> Response[
    Union[
        HTTPValidationError,
        Union["SignupResponse", "UserAlreadyExistsResponse"],
        UserAlreadyExistsResponse,
    ]
]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: AuthenticatedClient,
    body: SignupRequest,
) -> Response[
    Union[
        HTTPValidationError,
        Union["SignupResponse", "UserAlreadyExistsResponse"],
        UserAlreadyExistsResponse,
    ]
]:
    """Signup

    Args:
        body (SignupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['SignupResponse', 'UserAlreadyExistsResponse'], UserAlreadyExistsResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = client.get_httpx_client().request(
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: AuthenticatedClient,
    body: SignupRequest,
) -> Optional[
    Union[
        HTTPValidationError,
        Union["SignupResponse", "UserAlreadyExistsResponse"],
        UserAlreadyExistsResponse,
    ]
]:
    """Signup

    Args:
        body (SignupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['SignupResponse', 'UserAlreadyExistsResponse'], UserAlreadyExistsResponse]
    """

    return sync_detailed(
        client=client,
        body=body,
    ).parsed


async def asyncio_detailed(
    *,
    client: AuthenticatedClient,
    body: SignupRequest,
) -> Response[
    Union[
        HTTPValidationError,
        Union["SignupResponse", "UserAlreadyExistsResponse"],
        UserAlreadyExistsResponse,
    ]
]:
    """Signup

    Args:
        body (SignupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[HTTPValidationError, Union['SignupResponse', 'UserAlreadyExistsResponse'], UserAlreadyExistsResponse]]
    """

    kwargs = _get_kwargs(
        body=body,
    )

    response = await client.get_async_httpx_client().request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: AuthenticatedClient,
    body: SignupRequest,
) -> Optional[
    Union[
        HTTPValidationError,
        Union["SignupResponse", "UserAlreadyExistsResponse"],
        UserAlreadyExistsResponse,
    ]
]:
    """Signup

    Args:
        body (SignupRequest):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Union[HTTPValidationError, Union['SignupResponse', 'UserAlreadyExistsResponse'], UserAlreadyExistsResponse]
    """

    return (
        await asyncio_detailed(
            client=client,
            body=body,
        )
    ).parsed
