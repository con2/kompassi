import ko from 'knockout';
// import $ from 'jquery';
// import 'bootstrap';

import moment from 'moment';


export default class ShiftModal {
  constructor(app) {
    this.app = app;
    this.job = ko.observable(null);

    this.$el = $('#roster-shift-modal');
    this.startTime = ko.observable('');
    this.hours = ko.observable(1);
    this.person = ko.observable(null);

    this.people = ko.observable([{id: "foo", text: "Foo Bar"}, {id: "bar", text: "Bar Foo"}]);

    this.resolve = null;
  }

  prompt(shiftCell) {
    this.job(shiftCell.lane.job);
    this.startTime(shiftCell.startTime);
    this.hours(1);
    this.person(null);

    this.$el.modal('show');
    return new Promise((resolve, reject) => {
      this.resolve = resolve;
    });
  }

  cancel() {
    this.$el.modal('hide');
    this.resolve({result: 'cancelled'});
  }

  ok() {
    this.$el.modal('hide');
    this.resolve({
      result: 'ok',
      request: {
        startTime: this.startTime(),
        hours: parseInt(this.hours()),
        required: parseInt(this.required()),
      },
    });
  }
}
