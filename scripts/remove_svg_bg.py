import re
import glob

svgs = glob.glob("docs/_static/*.svg") + glob.glob("test/visual-tests/*.svg")

count = 0
for filepath in svgs:
    with open(filepath, 'r') as f:
        content = f.read()
        
    # In D2 v0.7.1, the background is the first <rect> in the inner <svg>, usually having class=" fill-N..." 
    # and fill="#FFFFFF" or similar. It is exactly the size of the viewBox.
    # We can match `<rect ... width="X" height="Y" ... fill="#FFFFFF" ... />`
    # Or generically, just replace the first `<rect ... />` right after `<svg ...>` 
    # But replacing `fill=\"#[0-9A-Fa-f]+\"` with `fill=\"transparent\"` where `class=\" fill-N` is present works well.
    
    # D2 0.7.1 pattern: <rect x="..." y="..." width="..." height="..." rx="0.000000" fill="#FFFFFF" class=" fill-N7" stroke-width="0" />
    # D2 0.6.6 pattern: <rect x="..." y="..." width="..." height="..." rx="0.000000" class=" fill-N7" stroke-width="0" />
    
    # Let's target the exact first <rect> element right after the secondary <svg> tag.
    # Example snippet: <svg class="d2-..." width="..." height="..." viewBox="..."><rect x="..."
    
    # The safest way is to change any 'fill="#FFFFFF"' on a tag that has `stroke-width="0"` and is the first rect.
    # Actually, we can use `re.sub` to replace the very first `<rect` that comes immediately after `<svg class="[^\"]*" width=...>`
    
    # Replace the first rect's fill to transparent and remove class-based
    # fill tokens (e.g. `fill-N7`) which can override `fill="transparent"`
    # via embedded CSS.
    def replacer(match):
        rect_inner = match.group(2)
        # replace any fill with transparent
        if 'fill="' in rect_inner:
            rect_inner = re.sub(r'fill="[^"]+"', 'fill="transparent"', rect_inner)
        else:
            rect_inner += ' fill="transparent"'
        # remove class attribute from canvas rect to avoid CSS override
        rect_inner = re.sub(r'\sclass="[^"]*"', '', rect_inner)
        # enforce a style fill to outrank class rules if any remain
        if 'style="' in rect_inner:
            if 'fill:' in rect_inner:
                rect_inner = re.sub(
                    r'style="([^"]*?)fill\s*:[^;"\']+;?([^"]*)"',
                    r'style="\1fill:transparent;\2"',
                    rect_inner,
                )
            else:
                rect_inner = rect_inner.replace('style="', 'style="fill:transparent;')
        else:
            rect_inner += ' style="fill:transparent;"'
        return match.group(1) + rect_inner + "/>"
        
    new_content = re.sub(r'(<svg[^>]*class="d2-[^>]*>\s*<rect)([^>]+)/>', replacer, content, count=1)
    
    if new_content != content:
        with open(filepath, 'w') as f:
            f.write(new_content)
        count += 1

print(f"Fixed background in {count} SVGs.")
