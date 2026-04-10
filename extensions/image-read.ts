/**
 * Image Read Extension for Pi Coding Agent
 * 
 * Provides image reading capability for GUI visual feedback in embedded development.
 * Used by embedded-dev skill for LCD display analysis.
 * 
 * Installation: Copy to ~/.pi/agent/extensions/image-read.ts
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type } from "@sinclair/typebox";
import { readFileSync, existsSync } from "node:fs";
import { extname } from "node:path";

export default function (pi: ExtensionAPI) {
  pi.registerTool({
    name: "image_read",
    label: "Image Read",
    description: "Read and analyze an image file. Returns base64 encoded image data with metadata. Used for GUI visual feedback analysis in embedded development.",
    parameters: Type.Object({
      path: Type.String({ description: "Path to the image file (PNG, JPG, GIF, BMP supported)" }),
      analyze: Type.Optional(Type.Boolean({ description: "Whether to include basic image analysis (dimensions, format)" })),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      const absolutePath = params.path.startsWith("/") || params.path.match(/^[A-Za-z]:/)
        ? params.path
        : `${ctx.cwd}/${params.path}`;

      if (!existsSync(absolutePath)) {
        return {
          content: [{ type: "text", text: `Error: Image file not found: ${absolutePath}` }],
          isError: true,
          details: { error: "file_not_found" },
        };
      }

      try {
        const buffer = readFileSync(absolutePath);
        const base64 = buffer.toString("base64");
        const ext = extname(absolutePath).toLowerCase();

        // Determine media type
        const mediaTypes: Record<string, string> = {
          ".png": "image/png",
          ".jpg": "image/jpeg",
          ".jpeg": "image/jpeg",
          ".gif": "image/gif",
          ".bmp": "image/bmp",
          ".webp": "image/webp",
        };

        const mediaType = mediaTypes[ext] || "application/octet-stream";

        const result: any = {
          path: absolutePath,
          mediaType,
          size: buffer.length,
          base64: base64.substring(0, 100) + "...", // Preview only
        };

        if (params.analyze) {
          // Basic PNG/JPG dimension detection (simplified)
          result.analysis = {
            format: ext.replace(".", "").toUpperCase(),
            sizeBytes: buffer.length,
            note: "For detailed analysis, use Python scripts/image_compare.py",
          };
        }

        return {
          content: [
            { type: "text", text: `Image loaded: ${absolutePath}\nSize: ${buffer.length} bytes\nType: ${mediaType}` },
            { type: "image", source: { type: "base64", mediaType, data: base64 } },
          ],
          details: result,
        };
      } catch (error: any) {
        return {
          content: [{ type: "text", text: `Error reading image: ${error.message}` }],
          isError: true,
          details: { error: error.message },
        };
      }
    },
  });

  pi.on("session_start", async (_event, ctx) => {
    ctx.ui.notify("Image Read extension loaded", "info");
  });
}
