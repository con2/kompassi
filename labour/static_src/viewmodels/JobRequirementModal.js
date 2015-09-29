import ko from 'knockout';
// import $ from 'jquery';
// import 'bootstrap';

import moment from 'moment';


export default class JobRequirementModal {
  constructor(app) {
    this.app = app;
    this.job = {
      slug: 'tapahtumavastaava',
      title: 'Tapahtumavastaava',
      jobCategory: {
        slug: 'conitea',
        title: 'Conitea'
      }
    }

    this.$el = $('#roster-job-requirement-modal');
    this.startTime = ko.observable(moment());
    this.hours = ko.observable(1);
    this.numPeople = ko.observable(0);

    this.resolve = this.reject = null;
  }

  // XXX temporary, for UI devt
  show() { $('#roster-job-requirement-modal').modal('show'); }
  hide() { $('#roster-job-requirement-modal').modal('hide'); }

  // XXX wip
  run(jobRequirementCell) {
    this.job(jobRequirement.job);
    this.startTime(jobRequirement.startTime);
    this.hours(1);
    this.numPeople(jobRequirement.numPeople);

    this.show();
    return new Promise((resolve, reject) => {
      this.resolve = resolve;
      this.reject = reject;
    });
  }

  cancel() {
    this.reject();
  }

  ok() {
    this.resolve({
      startTime: this.startTime(),
      hours: this.hours(),
      numPeople: this.numPeople(),
    });
  }
}
