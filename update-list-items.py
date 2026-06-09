"""
update-list-items.py — Upgrade article list items on paginated pages.
- Adds onclick (full item clickable)
- Adds "Read article →" link at bottom of each item
- Replaces featured card "Read the full guide" plain link with btn-primary class
"""
import os, re

ROOT = os.path.dirname(os.path.abspath(__file__))

FEATURED_OLD = '<a href="articles/how-much-car-insurance-do-i-need.html" class="read-link">Read the full guide &rarr;</a>'
FEATURED_NEW = '<a href="articles/how-much-car-insurance-do-i-need.html" class="btn-primary">Read the full guide &rarr;</a>'


def extract_and_update_list_items(html):
    result = []
    pos = 0
    while True:
        i0 = html.find('<div class="list-item"', pos)
        if i0 == -1:
            result.append(html[pos:])
            break
        result.append(html[pos:i0])

        # Balanced div counter to find closing tag of this list-item
        depth, i = 0, i0
        while i < len(html):
            if html[i:i+4] == '<div':
                depth += 1; i += 4
            elif html[i:i+6] == '</div>':
                depth -= 1
                if depth == 0:
                    item_end = i + 6
                    break
                i += 6
            else:
                i += 1
        else:
            result.append(html[i0:])
            break

        item = html[i0:item_end]

        # Extract article href from h3 link
        m = re.search(r'<h3><a href="([^"]+)"', item)
        if m:
            href = m.group(1)

            # Add onclick to opening div (skip if already present)
            if 'onclick' not in item[:item.index('>')+1]:
                item = re.sub(
                    r'(<div class="list-item"[^>]*?)>',
                    lambda x: x.group(1) + f' onclick="location.href=\'{href}\';">',
                    item, count=1
                )

            # Add "Read article →" after list-meta, before the two closing </div>s
            if 'Read article' not in item:
                item = re.sub(
                    r'(<div class="list-meta">.*?</div>)([ \t]*\n[ \t]*</div>[ \t]*\n[ \t]*</div>)',
                    lambda x: x.group(1) + '\n        <a href="' + href + '" class="read-link">Read article &rarr;</a>' + x.group(2),
                    item, count=1, flags=re.DOTALL
                )

        result.append(item)
        pos = item_end

    return ''.join(result)


def process(fp):
    with open(fp, 'r', encoding='utf-8') as f:
        content = f.read()

    if os.path.basename(fp) == 'index.html':
        content = content.replace(FEATURED_OLD, FEATURED_NEW, 1)

    content = extract_and_update_list_items(content)

    with open(fp, 'w', encoding='utf-8') as f:
        f.write(content)
    print(f'  OK: {os.path.basename(fp)}')


def main():
    for fname in ['index.html', 'page2.html', 'page3.html', 'page4.html']:
        fp = os.path.join(ROOT, fname)
        if os.path.exists(fp):
            process(fp)
    print('Done.')

if __name__ == '__main__':
    main()
