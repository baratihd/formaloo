from drf_spectacular.utils import OpenApiRequest, OpenApiResponse, extend_schema
from drf_spectacular.extensions import OpenApiViewExtension


class AppCreateViewSchema(OpenApiViewExtension):
    target_class = 'apps.store.views.AppCreateView'
    request_body = {
        'type': 'object',
        'properties': {
            'title': {'type': 'string', 'example': 'Test App'},
            'description': {'type': 'string', 'example': 'Test description for the app'},
            'price': {'type': 'number', 'example': 9.99},
        },
        'required': ['title', 'description', 'price'],
        'description': 'The owner field is automatically set to the authenticated user and should not be provided.',
    }
    response_body = {
        'type': 'object',
        'properties': {
            'id': {'type': 'integer', 'example': 1},
            'title': {'type': 'string', 'example': 'Test App'},
            'description': {'type': 'string', 'example': 'Test description for the app'},
            'price': {'type': 'number', 'example': 9.99},
            'owner': {'type': 'integer', 'example': 1},
            'is_verified': {'type': 'boolean', 'example': False},
            'created_at': {'type': 'string', 'format': 'date-time', 'example': '2025-02-28T12:34:56Z'},
            'updated_at': {'type': 'string', 'format': 'date-time', 'example': '2025-02-28T12:34:56Z'},
        },
    }
    error_responses = {
        400: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'field_name': {'type': 'string', 'example': 'This field is required.'},
                },
            },
            description='Bad Request',
        ),
        401: OpenApiResponse(
            response={
                'type': 'object',
                'properties': {
                    'detail': {'type': 'string', 'example': 'Authentication credentials were not provided.'},
                },
            },
            description='Unauthorized',
        ),
    }

    def view_replacement(self):
        return extend_schema(
            tags=['store'],
            description=(
                'Endpoint to create a new app. Returns the created app details on success or error details otherwise.'
            ),
            request=OpenApiRequest(request=self.request_body),
            responses={
                201: OpenApiResponse(response=self.response_body),
                **self.error_responses,
            },
        )(self.target_class)
