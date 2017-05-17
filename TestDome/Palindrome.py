class Palindrome:

    @staticmethod
    def is_palindrome(word):
        for i, ch in enumerate(word, 1):
            if ch.lower() != word[-i].lower():
                return False
        return True

print(Palindrome.is_palindrome('Deleveled'))