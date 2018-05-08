import unittest
import os
import sys
from steembase.account import PrivateKey


class Testcases(unittest.TestCase):
    def test_encrypt(self):
        if 'SCRYPT_MODULE' in os.environ:
            del os.environ['SCRYPT_MODULE']
        try:
            del sys.modules['steembase.bip38']
        except KeyError:
            pass
        import steembase.bip38
        self.assertEqual([
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd"),
                    "TestingOneTwoThree"), "encwif"),
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR"),
                    "TestingOneTwoThree"), "encwif"),
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"),
                    "Satoshi"), "encwif")
        ], [
            "6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi",
            "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg",
            "6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq"
        ])

    def test_decrypt(self):
        if 'SCRYPT_MODULE' in os.environ:
            del os.environ['SCRYPT_MODULE']
        try:
            del sys.modules['steembase.bip38']
        except KeyError:
            pass
        import steembase.bip38
        self.assertEqual([
            format(
                steembase.bip38.decrypt(
                    "6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxTh"
                    "xsUW8epQi", "TestingOneTwoThree"), "wif"),
            format(
                steembase.bip38.decrypt(
                    "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEb"
                    "n2Nh2ZoGg", "TestingOneTwoThree"), "wif"),
            format(
                steembase.bip38.decrypt(
                    "6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTe"
                    "PPX1dWByq", "Satoshi"), "wif")
        ], [
            "5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd",
            "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR",
            "5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"
        ])

    def test_encrypt_scrypt(self):
        os.environ['SCRYPT_MODULE'] = 'scrypt'
        try:
            del sys.modules['steembase.bip38']
        except KeyError:
            pass
        import steembase.bip38
        assert steembase.bip38.SCRYPT_MODULE == 'scrypt'
        self.assertEqual([
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd"),
                    "TestingOneTwoThree"), "encwif"),
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR"),
                    "TestingOneTwoThree"), "encwif"),
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"),
                    "Satoshi"), "encwif")
        ], [
            "6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi",
            "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg",
            "6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq"
        ])
        del os.environ['SCRYPT_MODULE']

    def test_decrypt_scrypt(self):
        os.environ['SCRYPT_MODULE'] = 'scrypt'
        try:
            del sys.modules['steembase.bip38']
        except KeyError:
            pass
        import steembase.bip38
        assert steembase.bip38.SCRYPT_MODULE == 'scrypt'
        self.assertEqual([
            format(
                steembase.bip38.decrypt(
                    "6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxTh"
                    "xsUW8epQi", "TestingOneTwoThree"), "wif"),
            format(
                steembase.bip38.decrypt(
                    "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEb"
                    "n2Nh2ZoGg", "TestingOneTwoThree"), "wif"),
            format(
                steembase.bip38.decrypt(
                    "6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTe"
                    "PPX1dWByq", "Satoshi"), "wif")
        ], [
            "5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd",
            "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR",
            "5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"
        ])
        del os.environ['SCRYPT_MODULE']

    def test_encrypt_pylibscrypt(self):
        os.environ['SCRYPT_MODULE'] = 'pylibscrypt'
        try:
            del sys.modules['steembase.bip38']
        except KeyError:
            pass
        import steembase.bip38
        assert steembase.bip38.SCRYPT_MODULE == 'pylibscrypt'
        self.assertEqual([
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd"),
                    "TestingOneTwoThree"), "encwif"),
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR"),
                    "TestingOneTwoThree"), "encwif"),
            format(
                steembase.bip38.encrypt(
                    PrivateKey(
                        "5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"),
                    "Satoshi"), "encwif")
        ], [
            "6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxThxsUW8epQi",
            "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEbn2Nh2ZoGg",
            "6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTePPX1dWByq"
        ])
        del os.environ['SCRYPT_MODULE']

    def test_decrypt_pylibscrypt(self):
        os.environ['SCRYPT_MODULE'] = 'pylibscrypt'
        try:
            del sys.modules['steembase.bip38']
        except KeyError:
            pass
        import steembase.bip38
        assert steembase.bip38.SCRYPT_MODULE == 'pylibscrypt'
        self.assertEqual([
            format(
                steembase.bip38.decrypt(
                    "6PRN5mjUTtud6fUXbJXezfn6oABoSr6GSLjMbrGXRZxSUcxTh"
                    "xsUW8epQi", "TestingOneTwoThree"), "wif"),
            format(
                steembase.bip38.decrypt(
                    "6PRVWUbkzzsbcVac2qwfssoUJAN1Xhrg6bNk8J7Nzm5H7kxEb"
                    "n2Nh2ZoGg", "TestingOneTwoThree"), "wif"),
            format(
                steembase.bip38.decrypt(
                    "6PRNFFkZc2NZ6dJqFfhRoFNMR9Lnyj7dYGrzdgXXVMXcxoKTe"
                    "PPX1dWByq", "Satoshi"), "wif")
        ], [
            "5HqUkGuo62BfcJU5vNhTXKJRXuUi9QSE6jp8C3uBJ2BVHtB8WSd",
            "5KN7MzqK5wt2TP1fQCYyHBtDrXdJuXbUzm4A9rKAteGu3Qi5CVR",
            "5HtasZ6ofTHP6HCwTqTkLDuLQisYPah7aUnSKfC7h4hMUVw2gi5"
        ])
        del os.environ['SCRYPT_MODULE']


if __name__ == '__main__':
    unittest.main()
