from typing import Type, Tuple, Any
import inspect
from flask import request, current_app, jsonify, abort, Response
from flask.views import MethodView
from pydantic import ValidationError, BaseModel
from app.extensions import logging


logger = logging.get_logger(__name__)

def format_error(e: ValidationError) -> list[dict]:
    errors = []
    for error in e.errors():
        new_error = {
            "loc": ".".join(error["loc"]),
            "message": error["msg"],
            "input": str(error["input"]),
        }
        errors.append(new_error)

    return errors


class RestAPI(MethodView):
    def dispatch_request(self, *args, **kwargs):
        meth = getattr(self, request.method.lower(), None)

        # If the request method is HEAD and we don't have a handler for it
        # retry with GET.
        if meth is None and request.method == "HEAD":
            meth = getattr(self, "get", None)

        assert meth is not None, f"Unimplemented method {request.method!r}"

        annotations = inspect.get_annotations(meth)        

        if not kwargs:
            kwargs = dict()

        body_schema = annotations.get("body")
        if body_schema:
            body, errors = self.validate_data(body_schema, request.get_data())
            if errors:
                return jsonify(errors=errors), 400
            kwargs.update({"body": body})
        
        args_schema = annotations.get("args")
        if args_schema:
            args, errors = self.validate_data(args_schema, request.args.to_dict())
            if errors:
                return jsonify(errors=errors), 400
            kwargs.update({"args": args}) 

        return current_app.ensure_sync(meth)(**kwargs)
    
    def validate_data(self, schema: Type[BaseModel], data: bytes | str | dict) -> Tuple[Any | None, list | None]:
        try:
            obj = None
            if isinstance(data, (bytes, str)):
                obj = schema.model_validate_json(data)

            elif isinstance(data, dict):
                obj = schema.model_validate(data)

        except ValidationError as e:
            errors = format_error(e)
            return None, errors
        else:
            return obj, None
