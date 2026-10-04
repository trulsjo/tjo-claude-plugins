---
name: explain
description: Pick the clearest format to explain something - plain prose, a diagram, an interactive HTML page, or a narrated video - and climb one rung when an explanation did not land. Use when the user wants to understand something complex and the format is open, says they still don't get an explanation, or asks to explain it visually or better.
---

# explain

Karpathy's **ladder** of output formats for understanding (https://x.com/karpathy/status/2105819303471976479).
Each rung costs more to make and carries more. Start on the **lowest rung that carries the idea**;
climb only when it fails.

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
   | 1 | **Controlled prose** - "80% of the way to ASD-STE100" | One idea per sentence, at most 20 words. Active voice; name who does what. One term per thing, every time. The plainest exact word. Short vertical lists for anything with three or more parts. |
   | 2 | **Diagram** | Use a diagram skill if one is available (e.g. `oh-my-claudecode:diagram`). Otherwise a Mermaid block where markdown renders, or an ASCII box-and-arrow sketch in a terminal. Label every arrow with what flows along it. |
   | 3 | **Interactive HTML page** | One self-contained `.html` file: inline CSS/JS, controls that change the picture live. Publish it with the Artifact tool when that tool exists; otherwise write the file and give its path. |
   | 4 | **Narrated explainer video** | Invoke `explainer:explainer-video`. **Ask first**: it may install packages and takes minutes to render. |

   Done when the explanation exists in that form.

3. **Close** with one line naming the rung and the next one up, so the user can ask to climb
   ("This is a diagram; say the word for an interactive page"). Done when that line is in the reply.

## The ladder in one rule

Climb for the **reader's** need, never for effect: a diagram that restates two sentences, or a
video for a one-line fact, costs the reader more than it gives.
