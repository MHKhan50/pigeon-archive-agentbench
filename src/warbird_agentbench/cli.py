import argparse, json
from .core import WarBirdOrchestrator

def main():
    parser = argparse.ArgumentParser(prog="warbird", description="Agentic NLP for historical carrier-pigeon records")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("demo")
    verify = sub.add_parser("verify")
    verify.add_argument("--claim", required=True)
    sub.add_parser("extract")
    args = parser.parse_args()
    agent = WarBirdOrchestrator()
    if args.command == "verify":
        result = agent.verify(args.claim)
    elif args.command == "extract":
        result = agent.extract_all()
    else:
        result = agent.verify("British forces used carrier pigeons to send messages from front-line units.")
    print(json.dumps(result, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    main()
