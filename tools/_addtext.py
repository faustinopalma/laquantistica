"""Insert an SVG snippet (read from a file) just before the final </svg> of each target SVG.
Usage: python tools/_addtext.py <snippet.txt> <target1.svg> [<target2.svg> ...]
Idempotency: if a target already contains the marker comment in the snippet, it is skipped.
"""
import sys

snippet = open(sys.argv[1], encoding="utf-8").read()
marker = "<!--labels-->"
for t in sys.argv[2:]:
    s = open(t, encoding="utf-8").read()
    if marker in s:
        print("skip (already has labels):", t)
        continue
    idx = s.rfind("</svg>")
    if idx < 0:
        print("NO </svg> in", t)
        continue
    s2 = s[:idx] + marker + snippet + "</svg>" + s[idx + len("</svg>"):]
    open(t, "w", encoding="utf-8").write(s2)
    print("added labels to", t)
