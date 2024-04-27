//#include "SearchTree.h"


using namespace std;
#include <iostream>
#include <fstream>
#include <string>
#include <sstream>
#include <algorithm>
#include <cctype>  
#include <unordered_set>

const int ALPHABET_SIZE = 26;

struct pair_hash {
    template <class T1, class T2>
    size_t operator() (const std::pair<T1, T2>& pair) const {
        return std::hash<T1>{}(pair.first);
    }
};

unordered_set<pair<string, vector<int>>, pair_hash> wordList;
unordered_set<string> dupecheck;

//Trie trie;

class Node {
public:
    Node* children[ALPHABET_SIZE];
    bool isWord;

    Node() {
        isWord = false;
        memset(children, 0, sizeof(children));
    }
};


class Trie {
public:
    Node* root;

    Trie() {
        root = new Node();
    }

    void insert(string word) {
        Node* curr = root;
        for (char c : word) {
            if (curr->children[c - 'a'] == nullptr) {
                curr->children[c - 'a'] = new Node();
            }
            curr = curr->children[c - 'a'];
        }
        curr->isWord = true;
        
    }

    bool search(string word) {
        Node* curr = root;
        for (char c : word) {
            if (curr->children[c - 'a'] == nullptr) {
                return false;
            }
            curr = curr->children[c - 'a'];
        }
        return curr->isWord;
    }

    bool prefixExists(string prefix) {
        Node* curr = root;
        for (char c : prefix) {
            if (curr->children[c - 'a'] == nullptr) {
                return false;
            }
            curr = curr->children[c - 'a'];
        }
        return true;
    }

};

Trie insertFile(string filePath) {
    Trie trie;
    ifstream file(filePath);
    if (!file.is_open()) {
        cerr << "Failed to open file: " << filePath << endl;
        return trie; 
    }
    string line;
    while (getline(file, line)) {
        line.erase(line.begin(), find_if(line.begin(), line.end(), [](unsigned char ch) { return !isspace(ch); }));
        line.erase(find_if(line.rbegin(), line.rend(), [](unsigned char ch) { return !isspace(ch); }).base(), line.end());

        if (!line.empty()) {
            trie.insert(line);
            //cout << "Added : " << line << endl;
        }
    }

    file.close();
    return trie;
}

void searchFrom(int row, int col, vector<vector<char>> &grid, string word, vector<vector<bool>> &traveled, Trie trie, vector<int> path, int size);

void stringToGrid(const string& str, vector<vector<char>> &grid, int size) {
    int index = 0;
    for (int i = 0; i < size; ++i) {
        for (int j = 0; j < size; ++j) {
            int index = i * size + j;
            grid[i][j] = str[index];
        }
    }

}

void searchGrid(Trie trie, string input) {
    int ROWS;
    int COLS;
    vector<vector<char>> grid;
    vector<vector<bool>> traveled;
    if (input.length() == 16) {
        ROWS = 4;
        COLS = 4;
        grid.resize(4, vector<char>(4));
        stringToGrid(input, grid, ROWS);
        traveled.resize(4, vector<bool>(4, false));
    }
    else if (input.length() == 25) {
        ROWS = 5;
        COLS = 5;
        grid.resize(5, vector<char>(5));
        stringToGrid(input, grid, ROWS);
        traveled.resize(5, vector<bool>(5, false));
    }
    else {
        cout << "Invalid size";
        return;
    }
    vector<int> path;
    
    for (int row = 0; row < ROWS; row++) {
        for (int col = 0; col < COLS; col++) {
            traveled[row][col] = 1;
            path.push_back(row);
            path.push_back(col);
            searchFrom(row, col, grid, string(1, grid[row][col]), traveled, trie, path, ROWS);
            traveled[row][col] = 0;
            path.pop_back();
            path.pop_back();
        }
    }

}

void searchFrom(int row, int col, vector<vector<char>> &grid, string word, vector<vector<bool>> &traveled, Trie trie, vector<int> path, int size) {
    if (!trie.prefixExists(word)) { return; }
    if (trie.search(word)) {
        vector<int> deepCopy(path.size());
        for (size_t i = 0; i < path.size(); ++i) {
            deepCopy[i] = path[i];
        }
        wordList.insert(make_pair(word,path)); 
    }
    //check all neighbors to make sure in bounds
    for (int rowOffset = -1; rowOffset <= 1; rowOffset += 1) {
        for (int colOffset = -1; colOffset <= 1; colOffset += 1) {
            if (rowOffset + row < size && rowOffset + row >= 0 && colOffset + col < size && colOffset + col >= 0 && !traveled[row + rowOffset][col + colOffset]) {
                traveled[row + rowOffset][col + colOffset] = 1;
                path.push_back(row + rowOffset);
                path.push_back(col + colOffset);
                searchFrom(row + rowOffset, col + colOffset, grid, word + grid[row + rowOffset][col + colOffset], traveled, trie, path, size);
                traveled[row + rowOffset][col + colOffset] = 0;
                path.pop_back();
                path.pop_back();
            }
        }
    }

    //This way is actually better since it doesn't check the [row][col] case but it's ugly
    /*if (row - 1 >= 0) {
        if (!traveled[row - 1][col]) {
            traveled[row - 1][col] = 1;
            searchFrom(row - 1, col, grid, word + grid[row - 1][col], traveled, trie);
            traveled[row - 1][col] = 0;
        }
    }
    if (row + 1 <= 3) {
        if (!traveled[row + 1][col]) {
            traveled[row + 1][col] = 1;
            searchFrom(row + 1, col, grid, word + grid[row + 1][col], traveled, trie);
            traveled[row + 1][col] = 0;
        }
    }
    if (col - 1 >= 0) {
        if (!traveled[row][col - 1]) {
            traveled[row][col - 1] = 1;
            searchFrom(row, col - 1, grid, word + grid[row][col - 1], traveled, trie);
            traveled[row][col - 1] = 0;
        }
    }
    if (col + 1 <= 3) {
        if (!traveled[row][col + 1]) {
            traveled[row][col + 1] = 1;
            searchFrom(row, col + 1, grid, word + grid[row][col + 1], traveled, trie);
            traveled[row][col + 1] = 0;
        }
    }
    if (row - 1 >= 0 && col - 1 >= 0) {
        if (!traveled[row - 1][col - 1]) {
            traveled[row - 1][col - 1] = 1;
            searchFrom(row - 1, col - 1, grid, word + grid[row - 1][col - 1], traveled, trie);
            traveled[row - 1][col - 1] = 0;
        }
    }
    if (row + 1 <= 3 && col - 1 >= 0) {
        if (!traveled[row + 1][col - 1]) {
            traveled[row + 1][col - 1] = 1;
            searchFrom(row + 1, col - 1, grid, word + grid[row + 1][col - 1], traveled, trie);
            traveled[row + 1][col - 1] = 0;
        }
    }
    if (row + 1 <= 3 && col + 1 <= 3) {
        if (!traveled[row + 1][col + 1]) {
            traveled[row + 1][col + 1] = 1;
            searchFrom(row + 1, col + 1, grid, word + grid[row + 1][col + 1], traveled, trie);
            traveled[row + 1][col + 1] = 0;
        }
    }
    if (row - 1 >= 0 && col + 1 <= 3) {
        if (!traveled[row - 1][col + 1]) {
            traveled[row - 1][col + 1] = 1;
            searchFrom(row - 1, col + 1, grid, word + grid[row - 1][col + 1], traveled, trie);
            traveled[row - 1][col + 1] = 0;
        }
    }*/
}

int main(int argc, char* argv[]) {
    string input = "";//"wdhdeiomltraypgi";

    if(argc >= 2) {
        input = argv[1];
    }
    else {
        getline(cin, input);
    }

    
    string filePath = "C:\\Users\\brend\\Desktop\\dads vid\\list.txt";
    Trie trie = insertFile(filePath);
    
    searchGrid(trie, input);

    vector<pair<string, vector<int>>> sortedPairs(wordList.begin(), wordList.end());

    //sort in descending order
    sort(sortedPairs.begin(), sortedPairs.end(),
        [](const auto& a, const auto& b) {
            return a.first.length() > b.first.length();
        });

    //Really jank way of checking for duplicates but I couldn't get my custom hash function working
    for (const auto& pair : sortedPairs) {
        if (dupecheck.count(pair.first) == 0) {
            for (int i = 0; i < pair.second.size(); i++) {
                cout << pair.second.at(i);
                if (i != pair.second.size() - 1) { cout << ","; }
            }
            cout << endl;
            cout << pair.first << endl;
            dupecheck.insert(pair.first);
        }       
    }
    cout << "END" << endl;
    cout << input.length() << endl;
    return 0;


}