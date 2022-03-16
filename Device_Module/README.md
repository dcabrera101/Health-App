
### Phase 2:
*og_app.py*: the original application I made for the device module. It defines the patient database and the api to perform operations on it.

*test.py*: the script that tests *og_app.py* by making several calls to the corresponding api.

You must first run *og_app.py* and then make calls to the api (like *test.py* does)

The rest of the files is my attempt at separating the database and api from the application that hosts them:
- *models.py* : defines the patientModel for the database
- *database.db* : the database itself
- APIS/ : directory containing current API

### Phase 1:
The work for phase 1 is included under phase1 directory; it is largely irrelevant becuase my phase2 implementation does not use it.



