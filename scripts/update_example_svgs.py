import os
import re
import subprocess
from pathlib import Path

rst_file = 'docs/examples.rst'
static_dir = 'docs/_static'

with open(rst_file, 'r') as f:
    content = f.read()

# Replace image references in RST
pattern = re.compile(r'\.\.\s+image::\s+_static/([a-zA-Z0-9_-]+)\.svg\n\s+:alt:\s+(.+?)\n\s+:align:\s+center')

def replacer(match):
    filename = match.group(1)
    alt = match.group(2)
    
    if filename.endswith('-dark') or filename == 'example-dark' or filename == 'example-sw-dark':
        return match.group(0)
        
    return f""".. image:: _static/{filename}.svg
   :alt: {alt}
   :align: center
   :class: only-light

.. image:: _static/{filename}-dark.svg
   :alt: {alt}
   :align: center
   :class: only-dark"""

content = pattern.sub(replacer, content)

with open(rst_file, 'w') as f:
    f.write(content)

print("examples.rst updated. Now finding snippets to generate dark SVGs...")

# Find code blocks
code_blocks = re.findall(r'code = """(.*?)"""\n.*?d2\.compile\(code,\s*library="(adi|sw)"(?:\s*,\s*theme="([^"]+)")?\).*?with open\("?([^"]+\.svg)"?,\s*"w"\)', content, flags=re.DOTALL)

# Handle basic explicitly
basic_content = "x -> y -> z"

def run_d2(code_str, lib, theme, output_name):
    # build the D2 concatenated str
    deps = []
    if lib:
        deps.append(f"lib/{lib}/{lib}-components.d2")
        if theme == "dark":
            deps.append(f"lib/{lib}/{lib}-theme-dark.d2")
        else:
            deps.append(f"lib/{lib}/{lib}-theme.d2")
    
    cat_content = ""
    for d in deps:
        if os.path.exists(d):
            with open(d, 'r') as f:
                cat_content += f.read() + "\n"
    
    full_code = cat_content + "\n" + code_str
    
    with open("temp.d2", "w") as f:
        f.write(full_code)
    
    subprocess.run([os.path.expanduser("~/.local/bin/d2"), "--layout", "elk", "temp.d2", output_name])

# generate dark versions for all found
for match in code_blocks:
    code_str = match[0]
    lib = match[1]
    is_dark = match[2]
    filename = match[3]
    
    if is_dark:
        continue # Already dark inside the code block logic
        
    # The output filename in RST is like signal-chain.svg
    # The actual image in RST uses example-signal-chain.svg!
    # Wait, looking at examples.rst, "signal-chain.svg" translates to "_static/example-signal-chain.svg" via the author's copy.
    # Let's just lookup the corresponding "-dark" filename we need to output to.
    
    expected_img_name = f"example-{os.path.splitext(filename)[0]}-dark.svg"
    output_path = f"docs/_static/{expected_img_name}"
    print(f"Generating {output_path}...")
    run_d2(code_str, lib, "dark", output_path)

# Handle basic
print("Generating docs/_static/example-basic-dark.svg...")
run_d2("x -> y -> z\n", None, "dark", "docs/_static/example-basic-dark.svg")

print("Done generating dark SVGs.")
