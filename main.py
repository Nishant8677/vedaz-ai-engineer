import argparse

def main():
    parser = argparse.ArgumentParser(description="Vedaz AI Engineer Pipeline")
    subparsers = parser.add_subparsers(dest="command")

    # Check command
    parser_check = subparsers.add_parser("check", help="Run the chat checker")
    
    # Generate command
    parser_generate = subparsers.add_parser("generate", help="Run the chat generator")
    
    # Evaluate command
    parser_evaluate = subparsers.add_parser("evaluate", help="Run the quality evaluator")
    
    args = parser.parse_args()

    if args.command == "check":
        print("Running checker...")
        from checker.checker import run_checker
        from utils.config import ORIGINAL_DATA_PATH
        run_checker(ORIGINAL_DATA_PATH)
    elif args.command == "generate":
        print("Running generator...")
        from generator.generator import run_generator
        run_generator(num_chats=10)
    elif args.command == "evaluate":
        print("Running evaluator...")
        # TODO: call evaluator logic
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
