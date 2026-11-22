import argparse
import json
import sys
from pathlib import Path

from jsonschema import Draft202012Validator

from .annotation import validate_jsonl
from .core import WarBirdOrchestrator


def main():
    parser = argparse.ArgumentParser(
        prog="warbird",
        description="Agentic NLP for historical carrier-pigeon records",
    )
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("demo")

    verify = sub.add_parser("verify")
    verify.add_argument("--claim", required=True)

    sub.add_parser("extract")

    validate = sub.add_parser(
        "validate-annotations",
        help="Validate annotation JSONL against the schema and seed corpus",
    )
    validate.add_argument("path", help="Path to the annotation JSONL file")

    args = parser.parse_args()

    if args.command == "validate-annotations":
        try:
            records = validate_jsonl(args.path)

            schema_path = (
                Path(__file__).resolve().parent
                / "schemas"
                / "annotation.schema.json"
            )
            with schema_path.open("r", encoding="utf-8") as handle:
                schema = json.load(handle)

            Draft202012Validator.check_schema(schema)
            validator = Draft202012Validator(schema)

            errors = []
            for index, record in enumerate(records, start=1):
                for error in validator.iter_errors(record):
                    errors.append(
                        "Record {}: {}".format(index, error.message)
                    )

            if errors:
                print(
                    json.dumps(
                        {"valid": False, "records": len(records), "errors": errors},
                        indent=2,
                    )
                )
                return 1

            print(
                json.dumps(
                    {
                        "valid": True,
                        "records": len(records),
                        "checks": [
                            "Python annotation validation",
                            "Source evidence validation",
                            "JSON Schema Draft 2020-12",
                        ],
                    },
                    indent=2,
                )
            )
            return 0

        except (OSError, ValueError, json.JSONDecodeError) as exc:
            print("Annotation validation failed: {}".format(exc), file=sys.stderr)
            return 1

    agent = WarBirdOrchestrator()

    if args.command == "verify":
        result = agent.verify(args.claim)
    elif args.command == "extract":
        result = agent.extract_all()
    else:
        result = agent.verify(
            "British forces used carrier pigeons to send messages from front-line units."
        )

    print(json.dumps(result, indent=2, ensure_ascii=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
