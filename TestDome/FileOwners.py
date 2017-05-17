class FileOwners:

    @staticmethod
    def group_by_owners(files):
        r = {}
        for file_name in files:
            r.setdefault(files[file_name], [])
            r[files[file_name]].append(file_name)
        return r

files = {
    'Input.txt': 'Randy',
    'Code.py': 'Stan',
    'Output.txt': 'Randy'
}
print(FileOwners.group_by_owners(files))