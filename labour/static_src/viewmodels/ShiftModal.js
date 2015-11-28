import ko from 'knockout';
import _ from 'lodash';
// import $ from 'jquery';
// import 'bootstrap';

import moment from 'moment';

import '../helpers/KoHelper'; // fmap


export default class ShiftModal {
  constructor(app) {
    this.app = app;
    this.job = ko.observable(null);

    this.$el = $('#roster-shift-modal');
    this.startTime = ko.observable('');
    this.hours = ko.observable(1);
    this.person = ko.observable(null);

    this.shiftWishes = this.person.fmap(person => {
      if (person) {
        return person.shiftWishes || '';
      } else {
        return 'Henkilön työvuorotoiveet näkyvät tässä valittuasi henkilön...';
      }
    });

    this.people = ko.observable([]);

    this.resolve = null;
  }

  prompt(shiftCell) {
    this.job(shiftCell.lane.job);

    this.people(shiftCell.lane.job.jobCategory.people);
    this.startTime(shiftCell.startTime);
    this.hours(shiftCell.hours);
    this.person(shiftCell.person);

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
