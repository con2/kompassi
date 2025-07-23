import ko from "knockout";

ko.subscribable.fn.fmap = function (fn) {
  return ko.pureComputed(() => fn(this()));
};
