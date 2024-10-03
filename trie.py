import json

class TrieNode:
    def __init__(self):
        self.children = {}
        self.emoji = None

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word, emoji):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.emoji = emoji

    def search(self, text):
        node = self.root
        matched_emojis = []
        for char in text:
            if char in node.children:
                node = node.children[char]
                if node.emoji:
                    matched_emojis.append(node.emoji)
            else:
                node = self.root

        if matched_emojis:
            return ''.join(matched_emojis)
        else:
            return "🤔..." 


    def load_from_json(self, file_path):
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
                for word, emoji in data.items():
                    self.insert(word, emoji)
        except Exception as e:
            print(f"An error occurred while loading the JSON file: {e}")


if __name__ == "__main__":
    trie = Trie()
    trie.load_from_json('./static/emojis.json')

    # Example searches
    print(trie.search("sick day"))    # Returns "🤢🤒 😷"
    print(trie.search("I don't know o"))  # Should return "🤔...""
