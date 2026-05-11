#!/usr/bin/env python3
"""Generate a readable .excalidraw learning-aid scene from a small JSON spec.

This script is a fallback for environments without a live Excalidraw MCP/API. It
favors large typography, whitespace, lanes, labels, and callouts over compact
Mermaid-style layouts.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import random
import textwrap
from collections import defaultdict
from pathlib import Path
from typing import Any

CANVAS_MARGIN_X = 120
TITLE_Y = 50
LANE_START_Y = 190
LANE_GAP_Y = 230
COLUMN_GAP_X = 390
NODE_MIN_W = 280
NODE_MAX_W = 380
NODE_MIN_H = 120
NODE_PAD = 22
DETAIL_FONT = 18
LABEL_FONT = 26
ANCHOR_FONT = 15

KIND_STYLE = {
    "external": {"backgroundColor": "#f1f3f5", "strokeColor": "#495057"},
    "interface": {"backgroundColor": "#e7f5ff", "strokeColor": "#1971c2"},
    "api": {"backgroundColor": "#e7f5ff", "strokeColor": "#1971c2"},
    "component": {"backgroundColor": "#edf2ff", "strokeColor": "#4263eb"},
    "domain": {"backgroundColor": "#ebfbee", "strokeColor": "#2b8a3e"},
    "process": {"backgroundColor": "#ebfbee", "strokeColor": "#2b8a3e"},
    "worker": {"backgroundColor": "#f3f0ff", "strokeColor": "#7048e8"},
    "queue": {"backgroundColor": "#f3f0ff", "strokeColor": "#7048e8"},
    "data": {"backgroundColor": "#fff3bf", "strokeColor": "#e67700"},
    "store": {"backgroundColor": "#fff3bf", "strokeColor": "#e67700"},
    "decision": {"backgroundColor": "#fff9db", "strokeColor": "#f08c00"},
    "danger": {"backgroundColor": "#ffe3e3", "strokeColor": "#c92a2a"},
    "default": {"backgroundColor": "#ffffff", "strokeColor": "#1e1e1e"},
}

EDGE_STYLE = {
    "sync": {"strokeColor": "#1864ab", "strokeStyle": "solid"},
    "async": {"strokeColor": "#7048e8", "strokeStyle": "dashed"},
    "data": {"strokeColor": "#e67700", "strokeStyle": "solid"},
    "control": {"strokeColor": "#2b8a3e", "strokeStyle": "solid"},
    "error": {"strokeColor": "#c92a2a", "strokeStyle": "dashed"},
    "default": {"strokeColor": "#1e1e1e", "strokeStyle": "solid"},
}


def stable_int(*parts: Any, modulo: int = 2_000_000_000) -> int:
    h = hashlib.sha1("|".join(str(p) for p in parts).encode("utf-8")).hexdigest()
    return int(h[:12], 16) % modulo


class SceneBuilder:
    def __init__(self) -> None:
        self.elements: list[dict[str, Any]] = []
        self.counter = 0

    def eid(self, prefix: str) -> str:
        self.counter += 1
        return f"{prefix}_{self.counter}_{stable_int(prefix, self.counter):x}"[:32]

    def add(self, element: dict[str, Any]) -> str:
        element["index"] = f"a{len(self.elements):04d}"
        self.elements.append(element)
        return element["id"]

    def base(
        self,
        element_type: str,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        stroke_color: str = "#1e1e1e",
        background_color: str = "transparent",
        fill_style: str = "hachure",
        stroke_width: int = 2,
        stroke_style: str = "solid",
        roughness: int = 1,
        group_ids: list[str] | None = None,
    ) -> dict[str, Any]:
        element_id = self.eid(element_type)
        element: dict[str, Any] = {
            "id": element_id,
            "type": element_type,
            "x": round(float(x), 2),
            "y": round(float(y), 2),
            "width": round(float(width), 2),
            "height": round(float(height), 2),
            "angle": 0,
            "strokeColor": stroke_color,
            "backgroundColor": background_color,
            "fillStyle": fill_style,
            "strokeWidth": stroke_width,
            "strokeStyle": stroke_style,
            "roughness": roughness,
            "opacity": 100,
            "groupIds": group_ids or [],
            "frameId": None,
            "seed": stable_int(element_id, "seed"),
            "version": 1,
            "versionNonce": stable_int(element_id, "nonce"),
            "isDeleted": False,
            "boundElements": None,
            "updated": 1,
            "link": None,
            "locked": False,
        }
        if element_type in {"rectangle", "diamond"}:
            element["roundness"] = {"type": 3}
        return element

    def rectangle(
        self,
        x: float,
        y: float,
        width: float,
        height: float,
        *,
        stroke_color: str = "#1e1e1e",
        background_color: str = "transparent",
        fill_style: str = "hachure",
        stroke_width: int = 2,
        stroke_style: str = "solid",
        group_ids: list[str] | None = None,
        roughness: int = 1,
    ) -> str:
        return self.add(
            self.base(
                "rectangle",
                x,
                y,
                width,
                height,
                stroke_color=stroke_color,
                background_color=background_color,
                fill_style=fill_style,
                stroke_width=stroke_width,
                stroke_style=stroke_style,
                roughness=roughness,
                group_ids=group_ids,
            )
        )

    def text(
        self,
        x: float,
        y: float,
        text: str,
        *,
        font_size: int = 24,
        width: float | None = None,
        stroke_color: str = "#1e1e1e",
        text_align: str = "left",
        group_ids: list[str] | None = None,
    ) -> str:
        lines = text.splitlines() or [""]
        estimated_w = max(len(line) for line in lines) * font_size * 0.58 + 10
        element_width = width or estimated_w
        element_height = max(font_size * 1.25 * len(lines), font_size * 1.25)
        element = self.base(
            "text",
            x,
            y,
            element_width,
            element_height,
            stroke_color=stroke_color,
            background_color="transparent",
            fill_style="solid",
            stroke_width=1,
            group_ids=group_ids,
        )
        element.update(
            {
                "text": text,
                "fontSize": font_size,
                "fontFamily": 1,
                "textAlign": text_align,
                "verticalAlign": "top",
                "containerId": None,
                "originalText": text,
                "autoResize": False,
                "lineHeight": 1.25,
            }
        )
        return self.add(element)

    def arrow(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        *,
        stroke_color: str = "#1e1e1e",
        stroke_style: str = "solid",
        stroke_width: int = 3,
    ) -> str:
        element = self.base(
            "arrow",
            x1,
            y1,
            x2 - x1,
            y2 - y1,
            stroke_color=stroke_color,
            background_color="transparent",
            fill_style="hachure",
            stroke_width=stroke_width,
            stroke_style=stroke_style,
        )
        element.update(
            {
                "points": [[0, 0], [round(x2 - x1, 2), round(y2 - y1, 2)]],
                "lastCommittedPoint": None,
                "startBinding": None,
                "endBinding": None,
                "startArrowhead": None,
                "endArrowhead": "arrow",
                "elbowed": False,
            }
        )
        return self.add(element)


def wrap(text: str, max_chars: int) -> str:
    if not text:
        return ""
    paragraphs = str(text).split("\n")
    wrapped: list[str] = []
    for paragraph in paragraphs:
        if not paragraph.strip():
            wrapped.append("")
        else:
            wrapped.extend(textwrap.wrap(paragraph, width=max_chars, break_long_words=False) or [paragraph])
    return "\n".join(wrapped)


def node_size(node: dict[str, Any]) -> tuple[int, int, str, str, str]:
    label = str(node.get("label") or node.get("id") or "node")
    detail = str(node.get("detail") or "")
    source = str(node.get("source") or "")
    width = int(node.get("width") or min(NODE_MAX_W, max(NODE_MIN_W, len(label) * 16 + 80)))
    label_wrapped = wrap(label, max(14, int(width / 15)))
    detail_wrapped = wrap(detail, max(22, int(width / 10)))
    source_wrapped = wrap(source, max(25, int(width / 9)))
    line_count = len(label_wrapped.splitlines()) + len(detail_wrapped.splitlines()) + len(source_wrapped.splitlines())
    height = int(node.get("height") or max(NODE_MIN_H, NODE_PAD * 2 + 34 + max(0, line_count - 1) * 24))
    return width, height, label_wrapped, detail_wrapped, source_wrapped


def auto_layout(nodes: list[dict[str, Any]]) -> dict[str, dict[str, float]]:
    by_lane: dict[str, list[dict[str, Any]]] = defaultdict(list)
    lane_order: list[str] = []
    for node in nodes:
        lane = str(node.get("lane") or "main")
        if lane not in by_lane:
            lane_order.append(lane)
        by_lane[lane].append(node)

    positions: dict[str, dict[str, float]] = {}
    for lane_index, lane in enumerate(lane_order):
        ranked: dict[int, list[dict[str, Any]]] = defaultdict(list)
        for index, node in enumerate(by_lane[lane]):
            rank = int(node.get("rank", index))
            ranked[rank].append(node)
        for rank in sorted(ranked):
            stack = ranked[rank]
            for stack_index, node in enumerate(stack):
                x = float(node.get("x", CANVAS_MARGIN_X + rank * COLUMN_GAP_X))
                y = float(node.get("y", LANE_START_Y + lane_index * LANE_GAP_Y + stack_index * 170))
                positions[str(node["id"])] = {"x": x, "y": y, "lane": lane, "rank": rank}
    return positions


def add_lanes(builder: SceneBuilder, nodes: list[dict[str, Any]], positions: dict[str, dict[str, float]]) -> None:
    lanes: dict[str, list[str]] = defaultdict(list)
    for node in nodes:
        node_id = str(node["id"])
        lanes[str(positions[node_id]["lane"])].append(node_id)
    for lane, ids in lanes.items():
        xs = [positions[i]["x"] for i in ids]
        ys = [positions[i]["y"] for i in ids]
        min_x, max_x = min(xs) - 40, max(xs) + NODE_MAX_W + 50
        min_y, max_y = min(ys) - 52, max(ys) + NODE_MIN_H + 60
        builder.rectangle(min_x, min_y, max_x - min_x, max_y - min_y, stroke_color="#ced4da", background_color="transparent", stroke_style="dashed", stroke_width=1, roughness=0)
        builder.text(min_x + 16, min_y + 12, lane.upper(), font_size=20, stroke_color="#495057")


def add_groups(builder: SceneBuilder, groups: list[dict[str, Any]], node_boxes: dict[str, dict[str, float]]) -> None:
    for group in groups:
        ids = [str(i) for i in group.get("node_ids", []) if str(i) in node_boxes]
        if not ids:
            continue
        min_x = min(node_boxes[i]["x"] for i in ids) - 36
        min_y = min(node_boxes[i]["y"] for i in ids) - 52
        max_x = max(node_boxes[i]["x"] + node_boxes[i]["w"] for i in ids) + 36
        max_y = max(node_boxes[i]["y"] + node_boxes[i]["h"] for i in ids) + 36
        builder.rectangle(min_x, min_y, max_x - min_x, max_y - min_y, stroke_color=str(group.get("strokeColor", "#868e96")), background_color="transparent", stroke_style="dashed", stroke_width=2)
        builder.text(min_x + 18, min_y + 12, str(group.get("label", group.get("id", "group"))), font_size=20, stroke_color=str(group.get("strokeColor", "#495057")))


def add_node(builder: SceneBuilder, node: dict[str, Any], x: float, y: float) -> dict[str, float]:
    kind = str(node.get("kind", "default")).lower()
    style = KIND_STYLE.get(kind, KIND_STYLE["default"])
    width, height, label, detail, source = node_size(node)
    group_id = f"grp_{stable_int(node.get('id'), 'group'):x}"
    builder.rectangle(
        x,
        y,
        width,
        height,
        stroke_color=str(node.get("strokeColor", style["strokeColor"])),
        background_color=str(node.get("backgroundColor", style["backgroundColor"])),
        fill_style=str(node.get("fillStyle", "hachure")),
        stroke_width=int(node.get("strokeWidth", 2)),
        group_ids=[group_id],
    )
    builder.text(x + NODE_PAD, y + 18, label, font_size=int(node.get("labelFontSize", LABEL_FONT)), width=width - NODE_PAD * 2, stroke_color=str(node.get("textColor", "#1e1e1e")), group_ids=[group_id])
    current_y = y + 56 + 28 * max(0, len(label.splitlines()) - 1)
    if detail:
        builder.text(x + NODE_PAD, current_y, detail, font_size=int(node.get("detailFontSize", DETAIL_FONT)), width=width - NODE_PAD * 2, stroke_color="#343a40", group_ids=[group_id])
        current_y += 28 * len(detail.splitlines()) + 4
    if source:
        builder.text(x + NODE_PAD, current_y, source, font_size=ANCHOR_FONT, width=width - NODE_PAD * 2, stroke_color="#495057", group_ids=[group_id])
    return {"x": x, "y": y, "w": width, "h": height}


def connection_points(start: dict[str, float], end: dict[str, float]) -> tuple[float, float, float, float]:
    sx, sy = start["x"] + start["w"] / 2, start["y"] + start["h"] / 2
    ex, ey = end["x"] + end["w"] / 2, end["y"] + end["h"] / 2
    dx, dy = ex - sx, ey - sy
    if abs(dx) >= abs(dy):
        x1 = start["x"] + (start["w"] if dx >= 0 else 0)
        y1 = sy
        x2 = end["x"] if dx >= 0 else end["x"] + end["w"]
        y2 = ey
    else:
        x1 = sx
        y1 = start["y"] + (start["h"] if dy >= 0 else 0)
        x2 = ex
        y2 = end["y"] if dy >= 0 else end["y"] + end["h"]
    return x1, y1, x2, y2


def add_edges(builder: SceneBuilder, edges: list[dict[str, Any]], node_boxes: dict[str, dict[str, float]]) -> None:
    for edge in edges:
        start_id = str(edge.get("from"))
        end_id = str(edge.get("to"))
        if start_id not in node_boxes or end_id not in node_boxes:
            continue
        style = EDGE_STYLE.get(str(edge.get("kind", "default")).lower(), EDGE_STYLE["default"])
        x1, y1, x2, y2 = connection_points(node_boxes[start_id], node_boxes[end_id])
        builder.arrow(x1, y1, x2, y2, stroke_color=str(edge.get("strokeColor", style["strokeColor"])), stroke_style=str(edge.get("strokeStyle", style["strokeStyle"])), stroke_width=int(edge.get("strokeWidth", 3)))
        label = str(edge.get("label", "")).strip()
        if label:
            mid_x = (x1 + x2) / 2
            mid_y = (y1 + y2) / 2
            label_text = wrap(label, 24)
            builder.rectangle(mid_x - 90, mid_y - 24, 180, 48, stroke_color="transparent", background_color="#ffffff", fill_style="solid", stroke_width=1, roughness=0)
            builder.text(mid_x - 82, mid_y - 17, label_text, font_size=int(edge.get("fontSize", 16)), width=164, stroke_color=str(edge.get("textColor", "#343a40")))


def add_callouts(builder: SceneBuilder, callouts: list[dict[str, Any]], node_boxes: dict[str, dict[str, float]]) -> None:
    placement_counts: dict[str, int] = defaultdict(int)
    for index, callout in enumerate(callouts):
        target = str(callout.get("target", ""))
        width = int(callout.get("width", 300))
        text = wrap(str(callout.get("text", "")), max(24, int(width / 10)))
        height = int(callout.get("height", max(90, 34 + 24 * len(text.splitlines()))))
        if target and target in node_boxes:
            box = node_boxes[target]
            offset = placement_counts[target]
            placement_counts[target] += 1
            x = float(callout.get("x", box["x"] + box["w"] + 52))
            y = float(callout.get("y", box["y"] + offset * (height + 18)))
        else:
            x = float(callout.get("x", CANVAS_MARGIN_X + (index % 2) * 360))
            y = float(callout.get("y", LANE_START_Y + 520 + (index // 2) * 130))
        builder.rectangle(x, y, width, height, stroke_color=str(callout.get("strokeColor", "#c92a2a")), background_color=str(callout.get("backgroundColor", "#fff5f5")), fill_style="hachure", stroke_width=2)
        heading = str(callout.get("title", "note"))
        if heading:
            builder.text(x + 18, y + 12, heading.upper(), font_size=16, width=width - 36, stroke_color=str(callout.get("strokeColor", "#c92a2a")))
            builder.text(x + 18, y + 38, text, font_size=int(callout.get("fontSize", 17)), width=width - 36, stroke_color="#343a40")
        else:
            builder.text(x + 18, y + 18, text, font_size=int(callout.get("fontSize", 17)), width=width - 36, stroke_color="#343a40")


def add_legend(builder: SceneBuilder, spec: dict[str, Any], node_boxes: dict[str, dict[str, float]]) -> None:
    legend = spec.get("legend")
    if legend is None:
        used_kinds = []
        for node in spec.get("nodes", []):
            kind = str(node.get("kind", "default")).lower()
            if kind not in used_kinds:
                used_kinds.append(kind)
        labels = {
            "external": "external actor/system",
            "interface": "interface or ui",
            "api": "api/network boundary",
            "component": "component/module",
            "domain": "domain logic",
            "process": "process/transformation",
            "worker": "worker/async processing",
            "queue": "queue/event bus",
            "data": "state/data store",
            "store": "state/data store",
            "decision": "decision point",
            "danger": "risk/failure path",
            "default": "other",
        }
        legend = [{"kind": kind, "label": labels.get(kind, kind)} for kind in used_kinds[:8]]
    if not legend:
        return
    max_bottom = max((box["y"] + box["h"] for box in node_boxes.values()), default=LANE_START_Y)
    x = float(spec.get("legendX", CANVAS_MARGIN_X))
    y = float(spec.get("legendY", max_bottom + 120))
    builder.text(x, y, "Legend", font_size=24, stroke_color="#343a40")
    cursor_x = x
    cursor_y = y + 44
    for item in legend:
        kind = str(item.get("kind", "default")).lower()
        style = KIND_STYLE.get(kind, KIND_STYLE["default"])
        builder.rectangle(cursor_x, cursor_y, 34, 24, stroke_color=style["strokeColor"], background_color=style["backgroundColor"], stroke_width=2)
        builder.text(cursor_x + 48, cursor_y - 2, str(item.get("label", kind)), font_size=16, width=210, stroke_color="#343a40")
        cursor_x += 280
        if cursor_x > x + 900:
            cursor_x = x
            cursor_y += 42


def build_scene(spec: dict[str, Any]) -> dict[str, Any]:
    if "nodes" not in spec or not isinstance(spec["nodes"], list):
        raise ValueError("spec must include a nodes array")
    for node in spec["nodes"]:
        if "id" not in node:
            raise ValueError("every node must include an id")

    random.seed(int(spec.get("seed", 7)))
    builder = SceneBuilder()

    title = str(spec.get("title", "Untitled learning aid"))
    subtitle = str(spec.get("subtitle", ""))
    builder.text(CANVAS_MARGIN_X, TITLE_Y, wrap(title, 42), font_size=int(spec.get("titleFontSize", 42)), width=1200, stroke_color="#1e1e1e")
    if subtitle:
        builder.text(CANVAS_MARGIN_X, TITLE_Y + 62, wrap(subtitle, 88), font_size=int(spec.get("subtitleFontSize", 22)), width=1200, stroke_color="#495057")

    nodes = spec["nodes"]
    positions = auto_layout(nodes)
    if spec.get("showLanes", True):
        add_lanes(builder, nodes, positions)

    node_boxes: dict[str, dict[str, float]] = {}
    for node in nodes:
        node_id = str(node["id"])
        pos = positions[node_id]
        node_boxes[node_id] = add_node(builder, node, pos["x"], pos["y"])

    add_groups(builder, spec.get("groups", []), node_boxes)
    add_edges(builder, spec.get("edges", []), node_boxes)
    add_callouts(builder, spec.get("callouts", []), node_boxes)
    add_legend(builder, spec, node_boxes)

    return {
        "type": "excalidraw",
        "version": 2,
        "source": "excalidraw-learning-aids",
        "elements": builder.elements,
        "appState": {
            "gridSize": None,
            "viewBackgroundColor": str(spec.get("background", "#ffffff")),
            "theme": "light",
            "name": title[:80],
        },
        "files": {},
    }


EXAMPLE_SPEC = {
    "title": "How a request becomes a saved project",
    "subtitle": "A newcomer-friendly map of the repo mechanism: route -> validation -> domain service -> database -> event.",
    "nodes": [
        {"id": "client", "label": "User action", "detail": "Clicks Save Project", "lane": "external", "kind": "external", "rank": 0, "source": "web/src/pages/project.tsx"},
        {"id": "route", "label": "API route", "detail": "Accepts POST /projects and checks auth", "lane": "api boundary", "kind": "api", "rank": 1, "source": "api/routes/projects.ts"},
        {"id": "validate", "label": "Validate payload", "detail": "Normalizes user input and rejects invalid config", "lane": "domain", "kind": "process", "rank": 2, "source": "packages/core/project/schema.ts"},
        {"id": "service", "label": "ProjectService.save()", "detail": "Applies defaults, computes derived fields", "lane": "domain", "kind": "domain", "rank": 3, "source": "packages/core/project/service.ts"},
        {"id": "db", "label": "Projects table", "detail": "Persists project row and metadata", "lane": "storage", "kind": "data", "rank": 4, "source": "db/schema.sql"},
        {"id": "event", "label": "project.saved event", "detail": "Invalidates cache and notifies workers", "lane": "async", "kind": "queue", "rank": 5, "source": "packages/events/project-events.ts"},
    ],
    "edges": [
        {"from": "client", "to": "route", "label": "POST /projects", "kind": "sync"},
        {"from": "route", "to": "validate", "label": "payload + user", "kind": "control"},
        {"from": "validate", "to": "service", "label": "validated command", "kind": "data"},
        {"from": "service", "to": "db", "label": "transaction", "kind": "data"},
        {"from": "service", "to": "event", "label": "emit after commit", "kind": "async"},
    ],
    "callouts": [
        {"target": "validate", "title": "teaching point", "text": "Validation is part of the mechanism, not just a guardrail: it creates the normalized command used downstream."},
        {"target": "event", "title": "watch for", "text": "Async side effects happen after the database commit, so diagram them separately from the request response."},
    ],
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate a readable .excalidraw scene from a JSON spec.")
    parser.add_argument("spec", nargs="?", help="Input JSON spec")
    parser.add_argument("output", nargs="?", help="Output .excalidraw path")
    parser.add_argument("--example", action="store_true", help="Print an example spec and exit")
    parser.add_argument("--validate-only", action="store_true", help="Validate/build but do not write output")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.example:
        print(json.dumps(EXAMPLE_SPEC, indent=2))
        return 0
    if not args.spec:
        raise SystemExit("missing spec path; use --example to see the format")
    spec_path = Path(args.spec).expanduser().resolve()
    spec = json.loads(spec_path.read_text(encoding="utf-8"))
    scene = build_scene(spec)
    if args.validate_only:
        print(f"valid spec: {len(scene['elements'])} elements")
        return 0
    if not args.output:
        raise SystemExit("missing output .excalidraw path")
    output_path = Path(args.output).expanduser().resolve()
    output_path.write_text(json.dumps(scene, indent=2), encoding="utf-8")
    print(f"wrote {output_path} with {len(scene['elements'])} elements")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
