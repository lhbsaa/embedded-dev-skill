/**
 * Todo List Extension for Pi Coding Agent
 * 
 * Provides task management capability for embedded development workflow.
 * Supports add, list, update, delete, and clear operations.
 * 
 * Installation: Copy to ~/.pi/agent/extensions/todo.ts
 * 
 * State is persisted via pi.appendEntry() for session recovery.
 */

import type { ExtensionAPI } from "@mariozechner/pi-coding-agent";
import { Type, Static } from "@sinclair/typebox";
import { StringEnum } from "@mariozechner/pi-ai";

const ActionSchema = StringEnum(["add", "list", "update", "delete", "clear", "complete"] as const);
type Action = Static<typeof ActionSchema>;

interface TodoItem {
  id: string;
  text: string;
  status: "pending" | "in_progress" | "completed";
  priority: "high" | "medium" | "low";
  createdAt: number;
  updatedAt: number;
}

let todos: TodoItem[] = [];
let nextId = 1;

export default function (pi: ExtensionAPI) {
  // Restore state from session on load
  pi.on("session_start", async (_event, ctx) => {
    todos = [];
    nextId = 1;
    
    for (const entry of ctx.sessionManager.getBranch()) {
      if (entry.type === "custom" && entry.customType === "todo-state") {
        const data = entry.data as { todos?: TodoItem[]; nextId?: number };
        if (data.todos) {
          todos = data.todos;
          nextId = data.nextId || todos.length + 1;
        }
      }
    }
  });

  // Register todo_list tool
  pi.registerTool({
    name: "todo_list",
    label: "Todo List",
    description: "Manage a task list for tracking embedded development progress. Actions: add, list, update, delete, clear, complete.",
    promptSnippet: "Track embedded development tasks with todo_list tool",
    promptGuidelines: [
      "Use todo_list to track multi-step embedded development tasks",
      "Add tasks before starting complex driver or protocol implementation",
      "Update task status as work progresses",
    ],
    parameters: Type.Object({
      action: ActionSchema,
      id: Type.Optional(Type.String({ description: "Task ID (for update/delete/complete)" })),
      text: Type.Optional(Type.String({ description: "Task description (for add)" })),
      priority: Type.Optional(StringEnum(["high", "medium", "low"] as const)),
    }),
    async execute(toolCallId, params, signal, onUpdate, ctx) {
      const action = params.action;

      switch (action) {
        case "add": {
          if (!params.text) {
            return {
              content: [{ type: "text", text: "Error: 'text' is required for add action" }],
              isError: true,
            };
          }

          const item: TodoItem = {
            id: `todo-${nextId++}`,
            text: params.text,
            status: "pending",
            priority: (params.priority as "high" | "medium" | "low") || "medium",
            createdAt: Date.now(),
            updatedAt: Date.now(),
          };

          todos.push(item);
          saveState(pi);

          return {
            content: [{ type: "text", text: `Added task: [${item.id}] ${item.text} (${item.priority})` }],
            details: { item },
          };
        }

        case "list": {
          if (todos.length === 0) {
            return {
              content: [{ type: "text", text: "No tasks in the list." }],
              details: { todos: [], count: 0 },
            };
          }

          const lines = todos.map((t) => {
            const statusIcon = t.status === "completed" ? "✓" : t.status === "in_progress" ? "►" : "○";
            const priorityIcon = t.priority === "high" ? "!" : t.priority === "low" ? "-" : " ";
            return `${statusIcon} [${priorityIcon}] ${t.id}: ${t.text}`;
          });

          return {
            content: [{ type: "text", text: `Tasks (${todos.length}):\n${lines.join("\n")}` }],
            details: { todos, count: todos.length },
          };
        }

        case "update": {
          const item = todos.find((t) => t.id === params.id);
          if (!item) {
            return {
              content: [{ type: "text", text: `Error: Task not found: ${params.id}` }],
              isError: true,
            };
          }

          if (params.text) item.text = params.text;
          if (params.priority) item.priority = params.priority as "high" | "medium" | "low";
          item.updatedAt = Date.now();
          saveState(pi);

          return {
            content: [{ type: "text", text: `Updated task: ${item.id}` }],
            details: { item },
          };
        }

        case "delete": {
          const index = todos.findIndex((t) => t.id === params.id);
          if (index === -1) {
            return {
              content: [{ type: "text", text: `Error: Task not found: ${params.id}` }],
              isError: true,
            };
          }

          const removed = todos.splice(index, 1)[0];
          saveState(pi);

          return {
            content: [{ type: "text", text: `Deleted task: ${removed.id}` }],
            details: { removed },
          };
        }

        case "clear": {
          const count = todos.length;
          todos = [];
          nextId = 1;
          saveState(pi);

          return {
            content: [{ type: "text", text: `Cleared ${count} tasks.` }],
            details: { cleared: count },
          };
        }

        case "complete": {
          const item = todos.find((t) => t.id === params.id);
          if (!item) {
            return {
              content: [{ type: "text", text: `Error: Task not found: ${params.id}` }],
              isError: true,
            };
          }

          item.status = "completed";
          item.updatedAt = Date.now();
          saveState(pi);

          return {
            content: [{ type: "text", text: `Completed task: ${item.id}` }],
            details: { item },
          };
        }

        default:
          return {
            content: [{ type: "text", text: `Error: Unknown action: ${action}` }],
            isError: true,
          };
      }
    },
  });

  function saveState(pi: ExtensionAPI) {
    pi.appendEntry("todo-state", { todos, nextId });
  }

  // Register /todo command for quick access
  pi.registerCommand("todo", {
    description: "Manage todo list (usage: /todo add|list|clear)",
    getArgumentCompletions: (prefix: string) => {
      const actions = ["add", "list", "clear", "complete"];
      return actions
        .filter((a) => a.startsWith(prefix))
        .map((a) => ({ value: a, label: a }));
    },
    handler: async (args, ctx) => {
      const [action, ...rest] = (args || "").split(" ");
      
      if (action === "list" || !action) {
        const pending = todos.filter((t) => t.status !== "completed");
        ctx.ui.notify(`${pending.length} pending tasks`, "info");
      } else if (action === "clear") {
        todos = [];
        nextId = 1;
        saveState(pi);
        ctx.ui.notify("Todo list cleared", "success");
      } else if (action === "add" && rest.length > 0) {
        const item: TodoItem = {
          id: `todo-${nextId++}`,
          text: rest.join(" "),
          status: "pending",
          priority: "medium",
          createdAt: Date.now(),
          updatedAt: Date.now(),
        };
        todos.push(item);
        saveState(pi);
        ctx.ui.notify(`Added: ${item.text}`, "success");
      } else {
        ctx.ui.notify("Usage: /todo [add|list|clear]", "warning");
      }
    },
  });
}
