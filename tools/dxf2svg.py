"""Convert DXF files (produced from DWG via ODA File Converter) to clean SVG.

For each DXF in <indir>, writes:
  <outdir>/<name>.svg      native ezdxf SVG backend, white bg + black lines
  <outdir>/<name>.png      matplotlib preview (for visual inspection)

Usage:
    python tools/dxf2svg.py <indir> <outdir>
"""
import sys
import os
import glob
import ezdxf
from ezdxf.addons.drawing import Frontend, RenderContext, layout, svg
from ezdxf.addons.drawing import matplotlib as ezmpl
from ezdxf.addons.drawing import config as dcfg


def _config() -> "dcfg.Configuration":
    base = dcfg.Configuration()
    changes = {}
    if hasattr(dcfg, "BackgroundPolicy"):
        changes["background_policy"] = dcfg.BackgroundPolicy.WHITE
    if hasattr(dcfg, "ColorPolicy"):
        changes["color_policy"] = dcfg.ColorPolicy.BLACK
    try:
        return base.with_changes(**changes)
    except Exception:
        return base


def convert(dxf_path: str, svg_path: str, png_path: str) -> None:
    doc = ezdxf.readfile(dxf_path)
    msp = doc.modelspace()
    cfg = _config()
    # native SVG
    backend = svg.SVGBackend()
    Frontend(RenderContext(doc), backend, config=cfg).draw_layout(msp)
    page = layout.Page(0, 0)  # 0,0 => size from content
    with open(svg_path, "w", encoding="utf-8") as f:
        f.write(backend.get_string(page))
    # PNG preview
    try:
        ezmpl.qsave(msp, png_path, bg="#ffffff", config=cfg)
    except Exception as e:
        print("  (png preview failed:", repr(e), ")")


def main() -> None:
    indir, outdir = sys.argv[1], sys.argv[2]
    os.makedirs(outdir, exist_ok=True)
    for dxf in sorted(glob.glob(os.path.join(indir, "*.dxf"))):
        name = os.path.splitext(os.path.basename(dxf))[0]
        svg_path = os.path.join(outdir, name + ".svg")
        png_path = os.path.join(outdir, name + ".png")
        try:
            convert(dxf, svg_path, png_path)
            print("OK", name, "svg=", os.path.getsize(svg_path))
        except Exception as e:
            print("FAIL", name, repr(e))


if __name__ == "__main__":
    main()
