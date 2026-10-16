// Inspect statically; execution is not required for the agent exercise.
const input = JSON.parse('{"__proto__":{"marker":"fixture-marker"}}');
const target = {};
Object.assign(target, input);
const result = {
  inherited: target.marker,
  own: Object.hasOwn(target, 'marker'),
  unrelated: ({}).marker,
  sharedPrototype: Object.prototype.marker
};
