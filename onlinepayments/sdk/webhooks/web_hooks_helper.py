import hashlib
import hmac
from base64 import b64encode

from api_version_mismatch_exception import ApiVersionMismatchException
from onlinepayments.sdk.domain.web_hooks_event import WebhooksEvent
from signature_validation_exception import SignatureValidationException


class WebhooksHelper:
    """
    Online Payments platform webhooks helper.
    """

    def __init__(self, marshaller, secret_key_store):
        if marshaller is None:
            raise ValueError("marshaller is required")
        if secret_key_store is None:
            raise ValueError("secret_key_store is required")
        self.__marshaller = marshaller
        self.__secret_key_store = secret_key_store

    # body as InputStream

    def unmarshal(self, body, request_headers):
        """
        Unmarshals the given body, while also validating it using the given request headers.

        :raise: SignatureValidationException: If the body could not be validated successfully.
        :raise: ApiVersionMismatchException: If the resulting event has an API
         version that this version of the SDK does not support.
        :return: The body unmarshalled as a WebhooksEvent.
        """
        self._validate(body, request_headers)
        event = self.__marshaller.unmarshal(body, WebhooksEvent)
        self.__validate_api_version(event)
        return event

    def _validate(self, body, request_headers):
        """
        Validates the given body using the given request headers.

        :raise: SignatureValidationException: If the body could not be validated successfully.
        """
        self.__validate_body(body, request_headers)

    # validation utility methods

    def __validate_body(self, body, request_headers):
        signature = self.__get_header_value(request_headers, "X-GCS-Signature")
        key_id = self.__get_header_value(request_headers, "X-GCS-KeyId")
        secret_key = self.__secret_key_store.get_secret_key(key_id)
        unencoded_result = hmac.new(secret_key, body, hashlib.sha256)
        expected_signature = b64encode(unencoded_result.digest())
        is_valid = self.are_equal_signatures(signature, expected_signature)
        if is_valid is False:
            raise SignatureValidationException("failed to validate signature '"
                                               + signature + "'Expected: " + expected_signature)

    @staticmethod
    def are_equal_signatures(signature, expected_signature):
        # don't use a simple equals call, as that may leak timing information
        # (it fails fast)
        length = len(signature)
        expected_length = len(expected_signature)

        # always check at least 256 characters, to also not leak timing
        # information about the length of the expected signature
        limit = max(max(length, expected_length), 256)

        result = True

        # the loop below uses result &= false instead of result = false and
        # result &= true instead of nothing because those might leak timing
        # information
        for i in range(0, limit):
            if i < length and i < expected_length:
                # both within string boundaries
                result = result and (signature[i] == expected_signature[i])
            elif i >= length and i >= expected_length:
                # past both string boundaries
                result = result and True
            else:
                # i >= length || i >= expected_length but not both
                result = result and False

        return result

    # general utility methods

    @staticmethod
    def __validate_api_version(event):
        if not "v1" == event.api_version:
            raise ApiVersionMismatchException(event.api_version, "v1")

    @staticmethod
    def __get_header_value(request_headers, header_name):
        value = None
        for header in request_headers:
            if header_name.lower() == header.name.lower():
                if value is None:
                    value = header.value
                else:
                    raise SignatureValidationException(
                        "encountered multiple occurrences of header '" + header_name + "'")
        if value is None:
            raise SignatureValidationException(
                "could not find header '" + header_name + "'")
        return value

    # Used for unit tests
    @property
    def marshaller(self):
        return self.__marshaller

    @property
    def secret_key_store(self):
        return self.__secret_key_store
