/**
 * The app's state container: one object, replaced by patches, with listeners
 * notified after each change. Views render from a snapshot and never write to
 * it; only main.ts's loaders do.
 */
export class Store<S extends object> {
  private listeners = new Set<(state: S) => void>();

  constructor(private state: S) {}

  get(): S {
    return this.state;
  }

  set(patch: Partial<S>): void {
    this.state = { ...this.state, ...patch };
    for (const listener of this.listeners) listener(this.state);
  }

  subscribe(listener: (state: S) => void): () => void {
    this.listeners.add(listener);
    return () => this.listeners.delete(listener);
  }
}
