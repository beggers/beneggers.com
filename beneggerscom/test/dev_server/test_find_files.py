from beneggerscom.dev_server import find_file

import os
import tempfile


def _set_up_test_files(files: list[str]) -> tempfile.TemporaryDirectory:
    tmpdir = tempfile.TemporaryDirectory()
    for filename in files:
        fullpath = os.path.join(tmpdir.name, filename)
        os.makedirs(os.path.dirname(fullpath), exist_ok=True)
        with open(fullpath, "w") as f:
            f.write(filename)
    return tmpdir


def _set_up_and_test_files(files_and_routes: dict):
    tmpdir = _set_up_test_files(list(files_and_routes.keys()))
    for filename in files_and_routes:
        b, t = find_file(files_and_routes[filename], tmpdir.name)
        assert b == filename.encode()
        expected_ext = filename.split(".")[-1]
        assert t == expected_ext


def test_find_index_implicit():
    files = {"index.html": "localhost"}
    _set_up_and_test_files(files)


def test_find_index_explicit():
    files = {"index.html": "index.localhost"}
    _set_up_and_test_files(files)


def test_find_top_level_file():
    files = {"file.html": "file.localhost"}
    _set_up_and_test_files(files)


def test_find_subdirectory_index_implicit():
    files = {"subdir/index.html": "subdir.localhost"}
    _set_up_and_test_files(files)


def test_find_subdirectory_index_explicit():
    files = {"subdir/index.html": "index.subdir.localhost"}
    _set_up_and_test_files(files)


def test_find_subdirectory_index_subsubdirectory():
    files = {"subdir/index/index.html": "index.subdir.localhost"}
    _set_up_and_test_files(files)


def test_find_favicon():
    files = {"favicon.ico": "favicon.localhost"}
    _set_up_and_test_files(files)


def test_find_file_in_subdirectory():
    files = {"subdir/file.html": "file.subdir.localhost"}
    _set_up_and_test_files(files)


def test_find_file_in_subsubdirectory():
    files = {"subdir/subsubdir/file.html": "file.subsubdir.subdir.localhost"}
    _set_up_and_test_files(files)


def test_find_file_with_same_named_sibling_directory():
    files = {
        "subdir/test.html": "test.subdir.localhost",
        "subdir.html": "subdir.localhost",
    }
    _set_up_and_test_files(files)
