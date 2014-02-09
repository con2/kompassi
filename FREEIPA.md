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

## Setting up your environment for FreeIPA integration development

If you need to do development on the FreeIPA integration, follow this short HOWTO for setting up your development environment on a (Ubuntu) Linux machine that is not integrated into the `TRACON.FI` Kerberos realm.

### Install Kerberos libraries and utilities

    sudo apt-get install krb5-user libkrb5-dev python-dev build-essential
    pip install -r requirements-kerberos.txt

### Get the FreeIPA CA certificate

Visit https://moukari.tracon.fi/ipa/config/ca.crt in your browser. Save the certificate file in eg. `/etc/ipa/ca.crt`.

### Set up SSH tunnels

You need to do this every time it gets disconnected.

    ssh -L 64088:localhost:88 -L 64749:localhost:749 -fN moukari.tracon.fi

### Set up `/etc/krb5.conf`

    [realms]
        TRACON.FI = {
            kdc = localhost:64088
            master_kdc = localhost:64088
            admin_server = localhost:64749
            default_domain = tracon.fi
        }

    [domain_realm]
        tracon.fi = TRACON.FI
        .tracon.fi = TRACON.FI

### Check that everything works

    kinit yourname@TRACON.FI
    klist

You should see something like this:

    Ticket cache: FILE:/tmp/krb5cc_1000
    Default principal: yourname@TRACON.FI

    Valid starting    Expires           Service principal
    09/02/2014 13:48  10/02/2014 13:47  krbtgt/TRACON.FI@TRACON.FI

You should also be able to authenticate an SSH session to Moukari with Kerberos:

    unset SSH_AUTH_SOCK
    ssh -Kv moukari.tracon.fi

Look for

    debug1: Authentication succeeded (gssapi-with-mic).
