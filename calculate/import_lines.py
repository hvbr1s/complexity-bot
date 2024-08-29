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

async def count_import_lines_go(content):
    # Regular expression to match import statements in Go
    import_pattern = re.compile(r'^\s*import\s*(\([\s\S]*?\)|\S+\s+"[^"]+"\s*)', re.MULTILINE)
    imports = import_pattern.findall(content)
    
    # Count lines in grouped imports
    total_import_lines = 0
    for imp in imports:
        if imp.startswith('('):
            # Count lines in grouped import
            total_import_lines += len(imp.strip().split('\n'))
        else:
            # Single import
            total_import_lines += 1
    
    return total_import_lines