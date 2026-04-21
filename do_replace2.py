import re

with open('build_html.py', 'r') as f:
    lines = f.readlines()

# buildHeavenChart is at line 2323 (1-indexed) = index 2322 (0-indexed)
# It ends at line 2469 (1-indexed) = index 2468 (0-indexed) which is the `}}`
# Lines 2323 to 2469 inclusive (1-indexed) = indices 2322 to 2468 inclusive

start_idx = 2322  # 0-indexed, line 2323
end_idx = 2469    # 0-indexed exclusive, so we replace up to but NOT including line 2470

print(f"Start line: {start_idx+1}: {lines[start_idx].rstrip()}")
print(f"End line: {end_idx}: {lines[end_idx-1].rstrip()}")
print(f"Total lines before: {len(lines)}")

# Read the new function
with open('heaven_chart_new.py', 'r') as f:
    new_py = f.read()

match = re.search(r"NEW_HEAVEN = '''(.+?)'''", new_py, re.DOTALL)
if not match:
    print("ERROR: could not extract NEW_HEAVEN")
    exit(1)

new_func = match.group(1)
if not new_func.endswith('\n'):
    new_func += '\n'

new_func_lines = new_func.splitlines(keepends=True)
print(f"New function: {len(new_func_lines)} lines")

# Replace lines[start_idx:end_idx] with new_func_lines
new_lines = lines[:start_idx] + new_func_lines + lines[end_idx:]
print(f"Total lines after: {len(new_lines)}")

with open('build_html.py', 'w') as f:
    f.writelines(new_lines)

print("Done!")
