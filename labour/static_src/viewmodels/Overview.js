import ko from 'knockout';

import {getJobCategories} from '../services/RosterService';


export default class Overview {
  constructor() {
    this.jobCategories = ko.observable([]);
    getJobCategories().then(this.jobCategories);
  }
}
