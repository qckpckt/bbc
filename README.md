```
BBBBBBBBBBBBBBBBBBBB    BBBBBBBBBBBBBBBBBBBB    CCCCCCCCCCCCCCCÇCCCC
BBBB       °ºBBBBBBB    BBBB       °ºBBBBBBB    CCCCCº°       °ºCCCC
BBBB  BBBo   ºBBBBBB    BBBB  BBBo   ºBBBBBB    CCCC   .cCCCCc. CCCC
BBBB  BBBBB  .BBBBBB    BBBB  BBBBB  .BBBBBB    CCC   CCCCCCCCCCCCCC
BBBB  BBBº .oBBBBBBB    BBBB  BBBº .oBBBBBBB    CC   CCCCCCCCCCCCCCC
BBBB         °ºBBBBB    BBBB         °ºBBBBB    CC   CCCCCCCCCCCCCCC
BBBB  BBBBBo.  ºBBBB    BBBB  BBBBBo.  ºBBBB    CC   CCCCCCCCCCCCCCC
BBBB  BBBBBBB   BBBB    BBBB  BBBBBBB   BBBB    CCC   CCCCCCCCCCCCCC
BBBB  BBBBBº   BBBBB    BBBB  BBBBBº   BBBBB    CCCc   °ºCCCCº° CCCC
BBBB        .o0BBBBB    BBBB        .o0BBBBB    CCCCCc.      .cCCCCC
BBBBBBBBBBBBBBBBBBBB    BBBBBBBBBBBBBBBBBBBB    CCCCCCCCCCCCCCCCCCCC
```
BetterBetterCloud is a Python script that generates personalized email signatures
from an HTML template. It pulls user information from Bamboo HR using an API call
then publishes it to employee email accounts using Google Apps Manager.

### Dependencies

`Gam-3.7` (included in /lib, but you will need to authorize before it will work: https://github.com/jay0lee/GAM/wiki/CreatingClientSecretsFile).

Before you start, add an empty text file called `nobrowser.txt` into the src folder. This will allow you to authorize the scopes in a seperate browser window.

When prompted to enter a command using GAM, please note that the docker container does not have gam aliased. The path is `/lib/GAM-3.71/src/gam.py`.


`Bamboo API key` https://www.bamboohr.com/api/documentation/ follow instructions here under 'Authorization'. Create a .env file in the top level directory. The Docker instance will import the environment variable for you. `signature.py` expects an environment variable called `BAMBOO_API_KEY`.


### Build

`docker build -t bbc .`

### Run

```
docker run -it -p 8000:8000 -v `pwd`:/app --env-file .env bbc_new:latest
```
Note - the port arguments are to allow you to check the generated signatures. They are not needed for normal operations and can be omitted.

In the container:

`cd /app`
`python3 {name of script}`
