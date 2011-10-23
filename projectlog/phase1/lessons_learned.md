# Lessons learned

In no particular order

## 1. Make it right the first time

Time wasted re-doing and re-checking wiring etc was a major problem, make sure to only
use people who already know what they are doing (train them separately if you have the time) and stress
to them the importance of doing things properly rather than quickly, any time saved going to quick-and-dirty
way is lost three times over when it inevitably fails

## 2. Have simulated hardware

We destroyed a bunch of servos since middleware was sending a lot of weird and off-spec drive commands to them, plan an
API and then first implement the simulated hardware (basically draw simple switch and servo analogs that can be clicked 
resulting in DBUS messages and then support the methods to move the servo arms via DBUS calls).

Same applies regardless of messaging API used.

## 3. Finish one thing at a time

Should have started by finishing the reactor console (with the switches, lights and servos) before moving on to the reactor lid
and other consoles, having a huge bunch of stuff 80-90% done is no good.

## 4. Make sure your messaging API is fully supported by the languages you plan to use

We had to rewrite the simulation in one night since Javas DBUS support wasn't up to spec and the actual
simulation engine was written in Scala. Do not trust the fact that there are packages/libraries, verify this
yourself as the very first thing before starting writing any real code.

## 5. Working on things on the stand is a good thing

We got a bunch of feedback telling us how nice it was that we were actually doing things (like soldering stuff etc)
on the stand, of course this was because there was still a ton of stuff to do before we could have functional consoles
but still. 

So make your main thing ready, but have small things you can work on and that are not time critical so you can take the
time to tell the audience what you're working on.

## 6. Getting composite video output from a computer seems to be hard these days

Basically we ended up having a laptop with S-Video output, but that didn't work with an adapter cable
we had to borrow a full-featured scan-converter box (that we ended up not actually using due to time constraints and still
spent lots of hours trying to get this working, see point number 3)

## 7. Have stackable boxes to store everything in

Various bags are a recipe for disaster.

## 8. Have lot's and lot's of small organizer bins with lids

Keeping things in neat order can't be done if you have a big box and lot's of small items.

## 9. Keep your work area tidy

Especially when working at a stand, immediately after use return any items you take back to their
proper bin (see 8), wasting time looking for things is not something you want to do. Especially when
you're tired you just about immediately forget where you put down that screwdriver.

## 10. USB-Serial is unreliable

Having 4 arduinos on a hub all talking back and forth with the PC is starting to strain the bus, also there are the
cable lenght limits and those active cables might work for one thing but not another.

Alternative communication methods should be investigated (ethernet would be good for many reasons but gets
a bit expensive if you have a ton of I/O boards).

## 11. Make proper circuit boards out of everything

First prototype on solderless breadboard is ok but trying to use that for "production" use will fail. Either
use breadboard or etched, or if you have time and need to do many boards (like shift-register breakouts) order them 
custom made from china.

Making boards takes time but debugging issues rising from funky mess of wires that might come loose at any time takes even more.

## 12. Use proper connectors

Sticking individual female jumper cables to pin-headers (where wires have just directly been soldered) has
many problems (and soldering those wires correctly without causing shorts or melting [and thus distorting] 
the headers takes skill [see 1]).

I guess flat cables would be ok, or RJ connectors, or Molex, or UMNL. Pay the price, it will save headache.

## 13. Servos don't make good indicator dials

They're very easy to control (because they have smarts built in for that) but they break easily and make a lot
of noise. Galvanometers (analog volt/ammeter) are also easy to drive (PWM, though HW PWM pins are usually in short
supply but software PWM should be good enough) but suffer from the same lack of movement range as servos.

Steppers might be considered but have other issues (like needing endstop sensors and rotary encoders for any sort of accurate drive-to-position
-type of control, also you need pins and software on the Arduino for all that or a separate driver-board with the intelligence)

## 14. Keep a journal

We took a bunch of photos (that still need to be categorized and stored somewhere for future reference) but having public journals
would have been good. And no doubt we'll miss those journals even more two months from now when things are no longer in fresh memory.

