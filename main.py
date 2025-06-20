from alice.main import main as alice_main
from bob.main import main as bob_main


def run_demo():
    """Run a simple Alice/Bob encryption demo."""
    bob_main()


if __name__ == "__main__":
    run_demo()