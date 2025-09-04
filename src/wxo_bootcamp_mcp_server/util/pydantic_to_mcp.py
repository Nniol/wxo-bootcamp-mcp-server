from typing import Any


def pydantic_to_mcp_schema(model_class) -> dict[str, Any]:
    json_schema = model_class.model_json_schema()

    def resolve_refs(obj, defs):
        """Recursively resolve $ref references."""
        if isinstance(obj, dict):
            if "$ref" in obj:
                # Extract reference name
                ref_path = obj["$ref"]
                if ref_path.startswith("#/$defs/"):
                    ref_name = ref_path.split("/")[-1]
                    if ref_name in defs:
                        # Return the resolved definition
                        return resolve_refs(defs[ref_name], defs)
                # If we can't resolve, return the original
                return obj
            else:
                # Recursively process all keys
                return {k: resolve_refs(v, defs) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [resolve_refs(item, defs) for item in obj]
        else:
            return obj

    # Get definitions
    defs = json_schema.get("$defs", {})

    # Start with base schema
    schema = {
        "type": "object",
        "properties": json_schema.get("properties", {}),
    }

    if "required" in json_schema:
        schema["required"] = json_schema["required"]

    # Resolve all references
    schema = resolve_refs(schema, defs)

    return schema  # type: ignore
