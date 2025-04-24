from typing import List, Tuple, Iterable, Optional
import json

Board = List[List[str]]
Path = List[Tuple[int, int]]


def all_board_coordinates(board):
    """
    :param board: list of strings lists
    :return: list of all cells of the board
    """
    return [(i, j) for i in range(len(board)) for j in range(len(board[0]))]


def find_neighbors(path, all_cells):
    """
    :param path: list of coordinates
    :param all_cells: all board cells
    :return: all neighbors of last coordinate if was, all_cells if wasn't
    """
    if len(path) == 0:
        return all_cells
    neighbors = []
    for i in range(-1, 2):
        for j in range(-1, 2):
            if (path[-1][0] + i, path[-1][1] + j) in all_cells and (path[-1][0] + i, path[-1][1] + j) not in path:
                neighbors.append((path[-1][0] + i, path[-1][1] + j))
    return neighbors


def path_to_word(path, board):
    """
    convert path to word according board
    :param path: list of coordinates
    :param board: list of strings lists
    :return: word represents the path
    """
    word = ""
    for i, j in path:
        word += board[i][j]
    return word


def is_valid_path(board: Board, path: Path, words: Iterable[str]) -> Optional[str]:
    """
    this function checks if the path is valid.
    :param board: list of strings lists
    :param path: list of coordinates
    :param words: data structure of words
    :return: word represents the path when path is valid, None otherwise
    """
    all_cells = all_board_coordinates(board)
    for i in range(len(path)):
        if path[i] not in all_cells:
            return
        if path.count(path[i]) != 1:
            return
        if path[i] not in find_neighbors(path[:i], all_cells):
            return
    word = path_to_word(path, board)
    if word in words:
        return word


def find_words_accord_path(path_word, words):
    """
    filters the words according the path
    :param path_word: list of coordinates
    :param words: data structure of words
    :return: set of filtered words
    """
    new_words = set()
    for word in words:
        if path_word == word[:len(path_word)]:
            new_words.add(word)
    return new_words


def find_moves(path, board, word, all_cells, words):
    """
    :param path: list of coordinates
    :param board: list of strings lists
    :param word: current word
    :param all_cells: all board cells
    :param words: data structure of words
    :return: list of legal moves according last chosen coordinate, and matches path with words
    """
    if len(path) == 0:
        return all_cells
    neighbors = find_neighbors(path, all_cells)
    moves = []
    for x, y in neighbors:
        for word_ in words:
            if word + board[x][y] in word_:
                moves.append((x, y))
    return set(moves)


def find_length_n_paths_helper(n, board, words, path, all_paths, word, all_cells):
    """
    this function is a find_length_n_paths helper that fills paths in all_paths list
    :param n: integer number
    :param board: list of strings lists
    :param words: data structure of words
    :param path: list of coordinates
    :param all_paths: list of all paths
    :param word: current word
    :param all_cells: all board cells
    """
    if len(path) == n:
        if word in words:
            all_paths.append(path)
        return
    for x, y in find_moves(path, board, word, all_cells, words):
        find_length_n_paths_helper(n, board, find_words_accord_path(word + board[x][y], words), path + [(x, y)],
                                   all_paths,
                                   word + board[x][y], all_cells)


def find_length_n_paths(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    this function finds all paths that represent a word in board and in words argument according paths with n length
    :param n: integer number
    :param board: list of strings lists
    :param words: data structure of words
    :return: all paths that represent a word in board and in words argument with length n
    """
    all_paths = []
    find_length_n_paths_helper(n, board, set(words), [], all_paths, "", all_board_coordinates(board))
    return all_paths


def find_length_n_words_helper(n, board, words, path, all_paths, word, all_cells):
    """
    this function is a find_length_n_paths helper that fills paths in all_paths list
    :param n: integer number
    :param board: list of strings lists
    :param words: data structure of words
    :param path: list of coordinates
    :param all_paths: list of all paths
    :param word: current word
    :param all_cells: all board cells
    """
    if len(word) > n:
        return
    if len(word) == n:
        if word in words:
            all_paths.append(path)
        return
    for x, y in find_moves(path, board, word, all_cells, words):
        find_length_n_words_helper(n, board, find_words_accord_path(word + board[x][y], words), path + [(x, y)],
                                   all_paths,
                                   word + board[x][y], all_cells)


def find_length_n_words(n: int, board: Board, words: Iterable[str]) -> List[Path]:
    """
    this function finds all paths that represent a word in board and in words argument according words with n length
    :param n: integer number
    :param board: list of strings lists
    :param words: data structure of words
    :return: all paths that represent a word in board and in words argument according words with n length
    """
    all_paths = []
    find_length_n_words_helper(n, board, set(words), [], all_paths, "", all_board_coordinates(board))
    return all_paths


def max_score_paths(board: Board, words: Iterable[str]) -> List[Path]:
    """
    finds the max score paths can reach by finds words in board
    :param board: list of strings lists
    :param words: data structure of words
    :return: the max score paths can reach by finds words in board
    """
    max_paths = []
    for word in words:
        all_paths = find_length_n_words(len(word), board, [word])
        if all_paths:
            max_paths.append(max(all_paths, key=lambda path: len(path)))
    return max_paths


# ---------------------------- utils functions of boggle game -------------------------------

def load_json(file_name):
    """
    reads a json file
    :param file_name: name of json file
    :return: dictionary of json data (names with details)
    """
    with open(file_name) as json_file:
        data = json.load(json_file)
    return data


def dump_json(file_name, data):
    """
    writes to json file
    :param file_name: name of json file
    :param data: dictionary (username is key and details as value)
    """
    origin_data = load_json(file_name)
    with open(file_name, 'w') as f:
        origin_data.update(data)
        json.dump(origin_data, f)


def read_words_file(file_name):
    """
    reads words file
    :param file_name:
    :return:
    """
    with open(file_name) as file:
        lines = {line.rstrip(): False for line in file}
    return lines
