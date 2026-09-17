import type { Locator, Page } from "playwright-core";

/**
 * A control the docs point at, named the way a reader names it: by role and
 * visible text. A restyled control keeps its callout; a renamed one fails the run.
 */
export type Target =
  | { role: "button" | "tab" | "link" | "textbox" | "combobox" | "switch"; name: string | RegExp }
  | { text: string | RegExp }
  | { css: string };

export interface Focus {
  target: Target;
  /** Printed in the badge. Step N of the page's <Steps> list is badge N. */
  step: number;
  /** Which top corner holds the badge. Right keeps it off a label sitting above the control. */
  corner?: "left" | "right";
}

interface Box {
  x: number;
  y: number;
  width: number;
  height: number;
  step: number;
  corner: "left" | "right";
}

const outline = "#d9480f";

export function locate(page: Page, target: Target): Locator {
  if ("css" in target) return page.locator(target.css);
  if ("text" in target) return page.getByText(target.text);
  return page.getByRole(target.role, { name: target.name });
}

/** Measures each target and paints the outlines and badges into the live page. */
export async function drawFocus(page: Page, focuses: Focus[]): Promise<void> {
  const boxes: Box[] = [];
  for (const focus of focuses) {
    const locator = locate(page, focus.target).first();
    await locator.waitFor({ state: "visible" });
    const box = await locator.boundingBox();
    if (box === null) {
      throw new Error(`nothing to annotate for step ${focus.step}: ${JSON.stringify(focus.target)}`);
    }
    boxes.push({ ...box, step: focus.step, corner: focus.corner ?? "left" });
  }
  await page.evaluate(paint, { boxes, outline });
}

/** Runs in the browser. Boxes arrive in viewport pixels and are placed in document pixels, so a fullPage shot keeps them. */
function paint(input: { boxes: Box[]; outline: string }): void {
  const layer = document.createElement("div");
  layer.style.cssText = "position:absolute;left:0;top:0;width:0;height:0;overflow:visible;z-index:2147483647;pointer-events:none";
  const pad = 5;
  const dx = window.scrollX;
  const dy = window.scrollY;

  for (const box of input.boxes) {
    const x = box.x + dx;
    const y = box.y + dy;
    const frame = document.createElement("div");
    frame.style.cssText = [
      "position:absolute",
      `left:${x - pad}px`,
      `top:${y - pad}px`,
      `width:${box.width + pad * 2}px`,
      `height:${box.height + pad * 2}px`,
      `border:2.5px solid ${input.outline}`,
      "border-radius:9px",
      "box-shadow:0 0 0 2px rgba(255,255,255,.9)",
    ].join(";");
    layer.appendChild(frame);

    const badge = document.createElement("div");
    badge.textContent = String(box.step);
    badge.style.cssText = [
      "position:absolute",
      `left:${box.corner === "right" ? x + box.width + pad - 12 : x - pad - 12}px`,
      `top:${y - pad - 12}px`,
      "width:24px",
      "height:24px",
      "border-radius:999px",
      `background:${input.outline}`,
      "color:#fff",
      "font:700 13px/24px ui-sans-serif,system-ui,sans-serif",
      "text-align:center",
      "box-shadow:0 0 0 2px #fff",
    ].join(";");
    layer.appendChild(badge);
  }
  document.documentElement.appendChild(layer);
}
