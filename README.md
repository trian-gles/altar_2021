# ALTAR DRAFT 6-29-21
![Image](resources/ALTAR%20new%20logo.jpg)
## About
Altar is a musical piece for 1+ laptop performers.
Inspired by card games, indie video games, and electronic music.  Built with Pygame and PYO.
Performers take turns moving cards around a game board that reacts musically to these actions. 
## Easy Setup
A pre-compiled executable for windows can be found at this link:
https://drive.google.com/drive/folders/1KMxm2jdU8EbsCabT9OrbMU2_6555GGu5?usp=sharing

OSX build coming very soon!

## Running from source
Requires python 3.8+

The latest version of python can be installed here:
https://www.python.org/downloads/


Next, download the code hosted at this Github repo.

If you have git installed at the command line, you can use:

```
git clone https://github.com/trian-gles/altar_2021
```
OR

Use this button on the top right of this github page:

![Image](resources/code_download.jpg)

Once the code is downloaded, from the root altar directory install the required python packages:

```
pip install -r requirements.txt
```

Finally, run the client script:
```
python client_gui.py
```

For additionally command line options, use `-h`

## Single Player Launch
Altar can be performed or practiced in a single player mode, or in a multiplayer mode of any number of performers.
For single player check the "local" option in the start menu and the piece will begin.

## Multiplayer Launch

Leaving out the "local" field will connect to an already configured external server (please contact me if it doesn't work!).

In this mode, one performer should be designated as the ADMIN by selecting the "admin" option.  This player will be
given special START and QUIT controls to start the piece after all performers have joined, and to end the program for all
performers.

Performers can chose whether they want their machine to run the audio engine by adding the
selecting the "audio" option.
In a performance with all performers in the same location, one performer should hook up their machine to speakers and 
use the "audio" option, while all others can leave this out.

The optional "username" field can inform other players of each other's names during turn rotations.
If this is left out, the performer will be provided with a username of a random string of digits.

A machine can be used to run a projector for the audience to view by checking the "Projector view" option.
This view cannot move cards, and shows no draw/discard piles or hand.

## Inside the game
On their turn players can click on any card to move it elsewhere.
Shown here is the full board:

![Image](resources/full_board.jpg)

The draw pile. Click on a card to pick it up and move it to your hand or a musical zone:

![Image](resources/draw_pile.jpg)

Your hand, of cards only you can see or use.  Putting cards here will not affect the audio engine.
Click one to pick it up and move it elsewhere: 

![Image](resources/hand.jpg)

One of three musical zones.  Dropping cards in here will modify its sound.  
Alternatively, you can right click a card on your turn to reactivate its effects.  
A zone with no cards will (usually) stop 
playing.

![Image](resources/zone.jpg)


The discard area.  Putting a card here deletes it.  Cards can also be deleted by dropping them on top of each other.

![Image](resources/discard.jpg)

Text appearing only in multiplayer mode annoucing whose turn is up.  The suggested turn order is not enforced, and if
players 

![Image](resources/debug_txt.jpg)

## Coming soon:
- More cards
- More mysteries

## !!SPOILERS!!
- Not all zones have to be active simultaneously.  Sometimes the engine will make noise with completely empty zones!
- Colored cards affect all zones
- Some cards will only have their effects the moment they are dropped in a new zone.  Others will continue to effect whatever zone they 
are dropped in.
- Repeatedly reapplying(right click) certain cards can have crazy results