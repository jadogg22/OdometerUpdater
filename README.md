# Omni api

This script is for Sharp transportation to automatically update the odometer readings in Dossier from Omnitracks.

## Getting setup

1. First things first you're going to need to make sure that you have all of the things setup before we can start. one of the first things that you will need is the api access token and a username for dossier and omnitracks. (contact IT) Once you have the required access you will need to create a .env file in the base directory with those encluded values.

```
subscribersId=
omniUsername=
omniPassword=

dossUsername=
dossPassword=
client_secret=

```

2. In our case we have some Odometers that we do not want to track that I have to manually add and when that changes we will go ahead and have to change it as that changes forturnalty it doesnt change much. Change / add any name in the list to not include it in the updated odometers. 

```python
ownerOperated = ["Do", "not", "Include"]

```

3. Finally just make sure to have all of the dependencys included inorder to run the python scripts. This can be done with the following command

```bash
pip install -r production/requirements.txt
```

## Running

finally we can start running the script by running the following command

```bash
./script.sh
```