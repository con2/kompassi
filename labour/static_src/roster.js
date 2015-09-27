'use strict';


import ko from 'knockout';

import moment from 'moment';
import 'moment/locale/fi'; // XXX I18N hardcoded fi only

import Roster from './viewmodels/Roster';
import config from './services/ConfigService';


moment.locale(config.lang);
ko.applyBindings(new Roster(), document.getElementById('labour-admin-roster-view'));
