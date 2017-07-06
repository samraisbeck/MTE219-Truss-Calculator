# MTE219 Truss Calulator
Program to calculate the modes of failure for a crane truss.

## General Info
By Sam Raisbeck - Updated July 5, 2017

This program is meant for calculating the failure modes and corresponding
loads for a crane design (MTE 219 @ UW). Currently, you must enter in the values
in `main.py` for member length, width, etc. The GUI is not functional right now
for adding custom values for members.

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

Right now, the load feature does not do anything...this is for when I implement
an actual GUI. When it's ready, it will basically allow you to load an existing crane
configuration that had already been saved. So when you first start off, you'll have to
begin creating and saving designs. Then if you would like to return to a previous
design to, say, modify it in a slightly different way, you will be able to.

The current version saves crane designs as text files into the `designs` folder.
They come in the format of failure results at the top, and member/joint specs at the
bottom. The load function is coded to follow the format of how it's saved, so it can only
load previously saved files, or ones that have been typed up to resemble it.

This is a very specific project as it is for a class project but it can
be modified for similar projects (i.e a bridge rather than a crane).
If by any means you would like to use this for something, feel free, but
*please* reference the repository and my name.

So far, there is no optimization features, as this would require the actual
geometry of the structure.

## Comments
If you think a feature would be useful, leave a comment, or implement it
yourself and send a pull request.
