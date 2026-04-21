import re

with open('build_html.py', 'r') as f:
    lines = f.readlines()

# Find start of buildHeavenChart
start_idx = None
for i, line in enumerate(lines):
    if 'function buildHeavenChart() {{' in line:
        start_idx = i
        break

if start_idx is None:
    print("ERROR: could not find buildHeavenChart")
    exit(1)

print(f"Found buildHeavenChart at line {start_idx+1}: {lines[start_idx].rstrip()}")

# Find end: the `}}` line that closes the function
# Look for the pattern: a line with just `}}` after a line ending with `;`
end_idx = None
for i in range(start_idx + 5, len(lines)):
    stripped = lines[i].strip()
    if stripped == '}}' and i > start_idx:
        # Check if previous non-empty line ends with `; or just `
        for j in range(i-1, start_idx, -1):
            prev = lines[j].strip()
            if prev:
                if prev.endswith('`;') or prev.endswith('`'):
                    end_idx = i
                break
        if end_idx is not None:
            break

if end_idx is None:
    print("ERROR: could not find end of buildHeavenChart")
    exit(1)

print(f"Found end at line {end_idx+1}: {lines[end_idx].rstrip()}")
print(f"Next line: {lines[end_idx+1].rstrip()}")

# Read the new function
with open('heaven_chart_v2.py', 'r') as f:
    new_py = f.read()

match = re.search(r"NEW_HEAVEN = '''(.+?)'''", new_py, re.DOTALL)
if not match:
    print("ERROR: could not extract NEW_HEAVEN")
    exit(1)

new_func = match.group(1)
if not new_func.endswith('\n'):
    new_func += '\n'

new_func_lines = new_func.splitlines(keepends=True)
print(f"Old function: lines {start_idx+1} to {end_idx+1} ({end_idx - start_idx + 1} lines)")
print(f"New function: {len(new_func_lines)} lines")

# Replace lines[start_idx:end_idx+1] with new_func_lines
new_lines = lines[:start_idx] + new_func_lines + lines[end_idx+1:]
print(f"Total lines before: {len(lines)}, after: {len(new_lines)}")

with open('build_html.py', 'w') as f:
    f.writelines(new_lines)

print("Done!")
