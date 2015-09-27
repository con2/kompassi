import ko from 'knockout';
import page from 'page';

import {getJobCategories} from '../services/RosterService';


export default class Overview {
  constructor(app) {
    this.app = app;
    this.jobCategories = ko.observable([]);
    this.setupRoutes();
  }

  setupRoutes() {
    this.actions = {
      selectJobCategories: (ctx, next) => { getJobCategories().then(this.jobCategories).then(next); },
      activate: (ctx) => { this.app.activeView('Overview'); },
    }

    page('/',
      this.actions.selectJobCategories,
      this.actions.activate
    );
  }
}
