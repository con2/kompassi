# FreeIPA integration in ConDB

ConDB supports optional integration with FreeIPA via LDAP, Kerberos and JSON-RPC.

## Configuration

In `condb/settings.py`:

* `CONDB_INSTALLATION_NAME`: Used as a prefix in many things such as FreeIPA groups.

## FreeIPA groups

### Labour

* `<installation name>-<event slug>-labour-accepted` (eg. `turskadev-tracon9-labour-accepted`) - Accepted volunteers for an event
* `<installation name>-<event slug>-labour-admins` - Volunteer workforce admins for an event
* `<installation name>-<event slug>-labour-readonly` - People with read-only access to volunteer data of an event
* `<installation name>-<event slug>-labour-cat-<job category slug>` (eg. `turskadev-tracon9-labour-jobcategory-info`)