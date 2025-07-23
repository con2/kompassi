"use strict";

// polyfills
import "whatwg-fetch";

import ko from "knockout";
import page from "page";
import moment from "moment";
import "moment/locale/fi"; // XXX I18N hardcoded fi only

import Roster from "./viewmodels/Roster";
import config from "./services/ConfigService";

ko.applyBindings(
  (window.kompassiLabourRoster = new Roster()),
  document.getElementById("labour-admin-roster-view"),
);
page();
