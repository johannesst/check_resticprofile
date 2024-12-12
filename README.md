# check_resticprofile
A nagios/icinga2 plugin for monitoring resticprofile statusfiles
Hacked together by Johannes Starosta December 2024

## Usage


````
os plugin for checking resticprofile status files

options:
  -h, --help            show this help message and exit
  -w HOURS, --warning HOURS
                        return warning if last successfull ACTION is older
                        than HOURS
  -c HOURS, --critical HOURS
                        return critical if last successfull ACTION is older
                        than HOURS
  -a ACTION, --action ACTION
                        ACTION to check for, Default: backup
  -p PROFILE, --profile PROFILE
                        resticprofile to use, Default: default
  -f FILE, --file FILE  Path to resticprofile status file
````

## Testfiles

The directory testdata contains two testfiles produced with resticprofile. You can use them to test the plugin:
````
./check_resticprofile.py -f testdata/status-error.json   --profile local -a check
CRITICAL: Last check failed | Last check 9 hours ago + 'Last check'=35956s;86400;172800;;
Duration of check: 1 sec | 'Duration': 1s;;;


Fatal: repository does not exist: unable to open config file: stat sftp://server.local/resticrepo/config: no such file
or directory

Is there a repository at the following location?

sftp://server.local/resticrepo

 ./check_resticprofile.py -f testdata/status-success.json   --profile local -a check
 WARNING: Last check 24 hours ago + 'Last check'=89579s;86400;172800;;
 Duration of check: 70 sec | 'Duration': 70s;;;
````
## Caveats

This is a quick hack and more sysadmin python3 than anything else. This is not ideal for the reasons Kristian Köhntopp
pointed out in [Using Python to bash](https://blog.koehntopp.info/2021/01/05/using-python-to-bash.html).
You should consider to implement a proper plugin with the [nagiosplugin-API](https://nagiosplugin.readthedocs.io/en/stable/). 
If I ever have  the time I would to this but I can't promise anything right now.
