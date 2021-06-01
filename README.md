# ALTAR DRAFT 6-1-21
![Image](resources/ALTAR%20new%20logo.jpg)
## About
Altar is a musical piece for 1+ laptop performers.
Inspired by card games, indie video games, and electronic music.  Built with Pygame and PYO.
Performers take turns moving cards around a game board that reacts musically to these actions. 
## Setup

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
pip install requirements.txt
```

## Single Player Launch
Altar can be performed or practiced in a single player mode, or in a multiplayer mode of any number of performers.
For single player, simply enter:
```
python client_gui.py --local
```

and the piece will begin.

##Multiplayer Launch

In multiplayer mode, one performer should be designated as the ADMIN by adding the `--admin` flag.  This player will be
given special START and QUIT controls to start the piece after all performers have joined, and to end the program for all
performers.

Performers can chose whether they want their machine to run the audio engine by adding the
`--audio` flag.
In a performance with all performers in the same location, one performer should hook up their machine to speakers and 
use the AUDIO flag, while all others can leave out this flag.

The optional NAME flag `-name YOUR-USERNAME-HERE` can inform other players of each other's names during turn rotations.
If this is left out, the performer will be provided with a username of a random string of digits.

EXAMPLE:

Tristan, Isolde, Brangane and Marke want to perform ALTAR aboard Tristan's ship.

Tristan acts as the ADMIN:
```
python client_gui.py --admin -name tristan
```

Isolde's hooks her laptop up to the ship's soundsystem for all to hear:
```
python client_gui.py --audio -name isolde
```
Brangane plays as well:
```
python client_gui.py -name brangane
```
Marke participates remotely from his castle, and must use the audio callback to hear the piece:
```
python client_gui.py --audio -name marke
```

## Inside the game
On their turn players can click on any card to move it elsewhere.
Shown here is the full board:

![Image](resources/full_board.jpg)

The draw pile. Click on a card to pick it up and drag it to your hand or a musical zone:

![Image](resources/draw_pile.jpg)

Your hand, of cards only you can see or use.  Putting cards here will (usually) not affect the audio engine.
Click one to pick it up and move it elsewhere: 

![Image](resources/hand.jpg)

One of three musical zones.  Dropping cards in here will modify its sound.  A zone with no cards will (usually) stop 
playing.  Click on a card to move it:

![Image](resources/zone.jpg)


The discard area.  Putting a card here deletes it.  Cards can also be deleted by dropping them on top of each other.

![Image](resources/discard.jpg)

Text appearing only in multiplayer mode annoucing whose turn is up:

![Image](resources/debug_txt.jpg)

## Coming soon:
- A nice UI for configuring the piece

- Visuals designed specifically for audience viewing

- Animations that respond to the musical content of the zones

- Many more cards

## !!SPOILERS!!

- Cards can be applied multiple times on the same zone by removing them and putting them back
- Not all zones have to be active simultaneously.  Sometimes the engine will make noise with completely empty zones!
- Colored cards affect all zones