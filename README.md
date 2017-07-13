# MTE219 Truss Calulator
Program to calculate the modes of failure for a crane truss.

## General Info
By Sam Raisbeck - Updated July 13, 2017

This program is meant for calculating the failure modes and corresponding
loads for a crane design (MTE 219 @ UW). To look see how to use the GUI, run
the program and go to About->Help or hit Ctrl+H.

## To run the program
You need to have Python 2.7. The only external package is PySide. I used Enthought Canopy package manager
to download PySide, but I think `pip install pyside` would also work. I haven't tried that though.

Go to the command line, and do: `cd ...\...\MTE219-Truss-Calculator` then `python main.py [designName]`
The program will open with the design previously saved as 'designName' if this argument is provided.
Note that you do not need to include the extension (.txt) but it won't cause an error if you do.

#### Utilizing the Software

This is a very specific project as it is for a class project but it can
be modified for similar projects (i.e a bridge rather than a crane).
If by any means you would like to use this for something, feel free, but
*please* reference the repository and my name.

#### Extra help

It's easy to create members, just add in the correct values. To create joints,
the members must be added to the joints such that they are in order of
appearance when viewing the structure from the side. It does not matter which
side it is viewed from, just stay consistent. This is so that pin-shear
calculations can be done easily.
**I will add a picture describing this soon**

Currently there is no feature implemented to do a pin-shear for more than 3-
member joints. This is because you would need to know the geometry with angles.
It can be done, it just would add more attributes to the members, and also would
require consistency with reference angles and stuff like that.

The current version saves crane designs as text files into the `designs` folder after the program GUI closes.
They come in the format of failure results at the top, and member/joint specs at the
bottom. The load function is coded to follow the format of how it's saved, so it can only
load previously saved files, or ones that have been typed up to resemble it.

So far, there is no optimization features, as this would require the actual
geometry of the structure.

## Comments
If you think a feature would be useful, leave a comment, or implement it
yourself and send a pull request.
