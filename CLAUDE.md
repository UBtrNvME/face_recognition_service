# CLAUDE.md
## Reatom v1000 — Explanatory Guide + Rules for Cursor Agents

This file is generated directly from the official Reatom v1000 handbook.
Its purpose is to teach AI coding agents (Cursor / Claude) the *mental model*, *rules*, and *correct patterns* required to work with Reatom v1000 safely.

This document combines **explanations + strict rules**. If a rule is violated, generated code is considered incorrect.

---

## 1. What Reatom Is

Reatom v1000 is a **reactive graph engine** with an **implicit execution context**.
Atoms are graph nodes, reads create dependencies, writes trigger invalidation, and actions represent events and side effects.

Reatom is **not Redux**, **not MobX**, **not Zustand**, and **not React-driven**.
React is only a renderer.

---

## 2. Implicit Execution Context (async-context.md)

Reatom operates using a hidden execution stack (context).
Every atom read/write happens relative to the currently active context.

Async operations *break* this context unless explicitly restored.

### Rules
- NEVER use `ctx` or `Ctx`
- NEVER pass context manually
- NEVER store context
- Async boundaries MUST be wrapped using `wrap()`

---

## 3. Async Rules (async-context.md, async.md)

Async logic must live inside actions and must preserve context.

### Correct Pattern
```ts
action(() => wrap(async () => {
  const data = await fetch('/api')
  atom.set(data)
}))
```

### Forbidden Patterns
- `action(async () => {})`
- `await` outside `wrap()`
- async inside components
- async inside derived atoms

---

## 4. Atoms & Atomization (atomization.md)

Atoms are the fundamental graph nodes.

### State Atoms
Hold mutable state and can be updated via `.set()`.

### Derived Atoms
- Lazy
- Pure
- Read-only
- No async
- No side effects

Atoms must be small, domain-focused, and defined outside components.

---

## 5. Events & Actions (events.md)

Actions represent **events**, not state.

They:
- Batch mutations
- Host side effects
- Define async lifetimes

Do NOT store events in atoms.

---

## 6. Extension System (extensions.md)

Reatom supports a powerful Extension System via `.extend()`.

Extensions are reusable capability units that add behavior or derived state.

### Two Extension Types
1. Assigner extensions — return an object merged into the target
2. Middleware extensions — intercept execution via `withMiddleware`

### Rules
- Extension factories are named `withX`
- Extension interfaces use `NameExt`
- Use `Ext<Target, Result>` typing
- Use `target.name` for naming derived actions/atoms
- Middleware must use `withMiddleware`

### Middleware Order
Extensions are applied inside-out.
The last extension passed to `.extend()` executes first.

---

## 7. Forms as Reactive State Machines (forms/*)

Forms in Reatom are first-class reactive graphs, not UI abstractions.

`reatomForm` models:
- fields
- validation
- submit lifecycle

### Rules
- Forms are not components
- `onSubmit` must be synchronous
- Async submit logic must delegate to actions

---

## 8. React Integration

React is a consumer of Reatom state.

### Supported Patterns
- `useAtom(atom)` — explicit, hook-based
- `reatomComponent(({ atom }) => ...)` — implicit, signal-like

Both are equivalent at the graph level.

### Forbidden in React
- side effects
- async logic
- subscriptions
- atom creation

---

## 9. File Organization

```
src/
├─ atoms/        # state + derived atoms
├─ actions/      # async / side effects
├─ forms/        # reatomForm definitions
├─ components/   # React UI only
```

---

## 10. Decision Guide for AI Agents

1. Is this state? → atom
2. Is this derived computation? → derived atom
3. Is this an event or side effect? → action + wrap
4. Is this UI? → React component
5. Is this form logic? → reatomForm

If a rule is violated, STOP and refactor.

---

## Source Files Used

- handbook/async-context.md
- handbook/async.md
- handbook/atomization.md
- handbook/events.md
- handbook/extensions.md
- handbook/forms.md
- handbook/forms/comparison.md
- handbook/forms/concepts/field-array.md
- handbook/forms/concepts/field-atom.md
- handbook/forms/concepts/fieldset.md
- handbook/forms/concepts/form.md
- handbook/forms/concepts/reactive-validation.md
- handbook/forms/introduction.md
- handbook/forms/migration/react-hook-form.md
- handbook/forms/recipes/abstract-components.md
- handbook/forms/recipes/async-default-values.md
- handbook/forms/recipes/async-validation-debounce.md
- handbook/forms/recipes/auto-submit.md
- handbook/forms/recipes/compound-fields.md
- handbook/forms/recipes/dependent-validation.md
- handbook/forms/recipes/errors-ux.md
- handbook/forms/recipes/fields-factory.md
- handbook/forms/recipes/focus-management.md
- handbook/forms/recipes/persistence.md
- handbook/forms/recipes/wizard-forms.md
- handbook/history.md
- handbook/lifecycle.md
- handbook/persist.md
- handbook/routing.md
- handbook/sampling.md
- handbook/suspense.md
