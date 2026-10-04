---
name: explain
description: Pick the lowest rung of a format ladder (prose to narrated video) that carries an explanation, and climb one rung when it did not land. Use when the user wants a system, structure or process explained and names no format, says an explanation did not land, or asks for a visual explanation.
---

# explain

A **ladder** of output formats for understanding. Each rung costs more to make and carries more.
Start on the **lowest rung that carries the idea**; climb only when the reader needs what the next
rung adds.

## Steps

1. **Name the shape** of what must be understood:
   - a fact, definition, or decision → rung 1
   - **structure**: parts and how they connect, a flow, a sequence of calls → rung 2
   - **a space to explore**: many states, parameters, data, "what if I change X" → rung 3
   - **change over time** that intuition needs to *see* move, worth a few minutes of the viewer → rung 4

   If the user already rejected an explanation, start one rung above it. Done when you can say which
   rung and why in one line.

2. **Make it** on that rung:

   | Rung | Form | How |
   |---|---|---|
   | 1 | **Controlled prose** (ASD-STE100 style) | One idea per sentence, at most 20 words. Active voice; name who does what. One term per thing, every time. The plainest exact word. Short vertical lists for anything with three or more parts. |
   | 2 | **Diagram** | Use a diagram skill if one is available (e.g. `oh-my-claudecode:diagram`). Otherwise a Mermaid block where markdown renders, or an ASCII box-and-arrow sketch in a terminal. Label every arrow with what flows along it. |
   | 3 | **Interactive HTML page** | One self-contained `.html` file: inline CSS/JS, controls that change the picture live. Publish it with the Artifact tool when that tool exists; otherwise write the file and give its path. |
   | 4 | **Narrated explainer video** | Invoke `explainer:explainer-video`. **Ask first**: it may install packages and takes minutes to render. |

   Done when the explanation meets every rule in its row.

3. **Close** with one line naming the rung and the next one up, so the user can ask to climb
   ("This is a diagram; say the word for an interactive page"). On rung 4, name the rung only. Done
   when that line is in the reply.
