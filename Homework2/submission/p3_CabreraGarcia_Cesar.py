# Author Cesar Cabrera Garcia
# Course COP 4045-042 Python Programming
# Term Fall 2026
# Description Manage mutual friendships and save a social network as CSV

import csv
import os
import tempfile
from testif import testif

student_name = "Cesar Cabrera Garcia"
network_filename = os.path.join(os.path.dirname(__file__), "social_network.csv")


def add_user(sn: dict, username: str, fullname: str) -> bool:
    """Add a user with no friends; return False for an existing username."""
    try:
        if username in sn:
            return False
        sn[username] = (fullname, [])
        return True
    except (TypeError, ValueError) as error:
        print("[ERROR] Could not add the user:", error)
        raise


def add_friend(sn: dict, user1: str, user2: str) -> bool:
    """Add a mutual link; reject missing users and self-friendship."""
    try:
        if user1 not in sn or user2 not in sn or user1 == user2:
            return False
        if user2 not in sn[user1][1]:
            sn[user1][1].append(user2)
        if user1 not in sn[user2][1]:
            sn[user2][1].append(user1)
        return True
    except (TypeError, KeyError, IndexError, AttributeError) as error:
        print("[ERROR] Could not add the friendship:", error)
        raise


def get_friends(sn: dict, user1: str, distance: int) -> list:
    """Return unique friends within the given link distance, excluding user1."""
    found_friends = []
    visited_users = [user1]
    current_level = [user1]
    current_distance = 0

    try:
        if user1 not in sn or distance <= 0:
            return []
        # Search one level at a time so each person is reached by a shortest path.
        while current_distance < distance and current_level:
            next_level = []
            for current_user in current_level:
                for friend in sn[current_user][1]:
                    if friend not in visited_users:
                        visited_users.append(friend)
                        found_friends.append(friend)
                        next_level.append(friend)
            current_level = next_level
            current_distance = current_distance + 1
        return found_friends
    except (TypeError, KeyError, IndexError) as error:
        print("[ERROR] Could not look up friends:", error)
        raise


def save_network(filename: str, sn: dict) -> None:
    """Save headerless CSV rows: username, full name, then zero or more friends."""
    try:
        with open(filename, "w", newline="", encoding="utf-8") as network_file:
            writer = csv.writer(network_file)
            for username in sn:
                writer.writerow([username, sn[username][0]] + sn[username][1])
    except (OSError, UnicodeError, csv.Error, TypeError, IndexError) as error:
        print("[ERROR] Could not save the network:", error)
        raise


def load_network(filename: str) -> dict:
    """Read a network saved by save_network and reject broken friend links."""
    network = {}
    try:
        with open(filename, "r", newline="", encoding="utf-8") as network_file:
            reader = csv.reader(network_file, strict=True)
            for row in reader:
                if len(row) < 2 or row[0] in network:
                    raise ValueError("A network row is incomplete or duplicated.")
                network[row[0]] = (row[1], row[2:])
        for username in network:
            checked_friends = []
            for friend in network[username][1]:
                if friend not in network or friend == username or friend in checked_friends:
                    raise ValueError("A friend link is missing, repeated, or self-referencing.")
                if username not in network[friend][1]:
                    raise ValueError("Friend links must be mutual.")
                checked_friends.append(friend)
        return network
    except (OSError, UnicodeError, csv.Error, ValueError) as error:
        print("[ERROR] Could not load the network:", error)
        raise


def test() -> bool:
    """Use the supplied testif helper to check all five network operations."""
    network = {}
    passed = True

    try:
        passed = testif(add_user(network, "Cash", "Cash"), "add user") and passed
        passed = testif(not add_user(network, "Cash", "Cash"), "duplicate user") and passed
        add_user(network, "Ubuntu", "Ubuntu")
        add_user(network, "Mint", "Mint")
        add_user(network, "Zorin OS", "Zorin OS")
        passed = testif(add_friend(network, "Cash", "Ubuntu"), "add friendship") and passed
        passed = testif("Cash" in network["Ubuntu"][1], "mutual friendship") and passed
        add_friend(network, "Ubuntu", "Mint")
        add_friend(network, "Mint", "Zorin OS")
        passed = testif(get_friends(network, "Cash", 2) == ["Ubuntu", "Mint"], "distance two") and passed
        add_friend(network, "Mint", "Cash")
        passed = testif(get_friends(network, "Cash", 10) == ["Ubuntu", "Mint", "Zorin OS"], "cycle handling") and passed
        passed = testif(not add_friend(network, "Cash", "Cash"), "reject self link") and passed
        passed = testif(get_friends({}, "Cash", 1) == [], "unknown user") and passed
        passed = testif(not add_friend({}, "Cash", "Ubuntu"), "missing friends") and passed
        # Temporary storage keeps the extra-credit tests separate from the demo.
        with tempfile.TemporaryDirectory() as directory:
            filename = os.path.join(directory, "Cash.csv")
            save_network(filename, network)
            passed = testif(load_network(filename) == network, "CSV round trip") and passed
        return passed
    except (OSError, UnicodeError, csv.Error, ValueError, TypeError) as error:
        print("[ERROR] Could not complete network tests:", error)
        raise


def main() -> None:
    """Demonstrate each network operation and run the extra-credit tests."""
    network = {}
    try:
        print(student_name)
        print("[STATUS] Creating social network...")
        add_user(network, "Cash", "Cash")
        add_user(network, "Ubuntu", "Ubuntu")
        add_user(network, "Mint", "Mint")
        add_friend(network, "Cash", "Ubuntu")
        add_friend(network, "Ubuntu", "Mint")
        print("Network:", network)
        print("Cash friends at distance 1:", get_friends(network, "Cash", 1))
        print("Cash friends at distance 2:", get_friends(network, "Cash", 2))
        save_network(network_filename, network)
        print("Reloaded network:", load_network(network_filename))
        print("[STATUS] All extra-credit tests passed:", test())
    except (OSError, UnicodeError, csv.Error, ValueError, TypeError) as error:
        print("[ERROR] The network demonstration failed:", error)
        raise


if __name__ == "__main__":
    main()
