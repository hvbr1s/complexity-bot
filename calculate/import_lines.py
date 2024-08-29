import re

async def count_import_lines_solidity(content):
    # Regular expression to match import statements in Solidity
    import_pattern = re.compile(r'^\s*import\s+.*?;', re.MULTILINE)
    imports = import_pattern.findall(content)
    return len(imports)

async def count_import_lines_rust(content):
    # Regular expression to match Rust import statements
    import_pattern = re.compile(r'^\s*(use|extern crate)\s.*?;', re.MULTILINE)
    import_matches = import_pattern.findall(content)
    return len(import_matches)