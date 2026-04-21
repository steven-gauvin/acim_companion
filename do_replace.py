# buildHeavenChart starts at line 2323 (1-indexed) and ends at line 2466
# (the line with  </div>`; followed by }} then function toggleRef)
# We'll replace lines 2323 through 2466 inclusive

with open('build_html.py', 'r') as f:
    lines = f.readlines()

# Find the exact start and end lines
start_line = None
end_line = None

for i, line in enumerate(lines):
    if 'function buildHeavenChart() {{' in line:
        start_line = i
        print(f"Found start at line {i+1}: {line.rstrip()}")
    if start_line is not None and i > start_line:
        # End is the line with `; followed by }}
        if line.strip() == '}}' and i > start_line + 5:
            # Check the previous line ends with `; 
            if lines[i-1].strip().endswith('`'):
                end_line = i
                print(f"Found end at line {i+1}: {line.rstrip()}")
                break

if start_line is None or end_line is None:
    print(f"ERROR: start={start_line}, end={end_line}")
    exit(1)

print(f"Replacing lines {start_line+1} to {end_line+1}")
print(f"Lines before: {len(lines)}")

# Read the new function
with open('heaven_chart_new.py', 'r') as f:
    new_py = f.read()

import re
match = re.search(r"NEW_HEAVEN = '''(.+?)'''", new_py, re.DOTALL)
if not match:
    print("ERROR: could not extract NEW_HEAVEN")
    exit(1)

new_func = match.group(1)
# Ensure it ends with a newline
if not new_func.endswith('\n'):
    new_func += '\n'

new_func_lines = new_func.splitlines(keepends=True)
print(f"New function: {len(new_func_lines)} lines")

# Replace
new_lines = lines[:start_line] + new_func_lines + lines[end_line+1:]
print(f"Lines after: {len(new_lines)}")

with open('build_html.py', 'w') as f:
    f.writelines(new_lines)

print("Done!")
