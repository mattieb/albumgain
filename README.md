`albumgain`
===========

`albumgain` is a Python script that processes directories of MP3s
or Ogg Vorbis files and sets their [ReplayGain][1] as an album.

It was specifically developed to work with my now-lost [Sansa
Fuze][2], and is thus specifically tuned to that player's requirements.

Flags for the `albumgain` script are:

 - `-t`: Required; specifies the type of music file to process—`mp3`
   or `ogg`.

 - `-d`: Dry run.  Shows you what commands would be executed instead
   of actually executing them.

Arguments are one or more directories to process.  `albumgain` can
group certain kinds of related directories (e.g. `Album (disc 1)`
and `Album (disc 2)`) and apply the same ReplayGain value to both
as one album.

[1]: http://en.wikipedia.org/wiki/ReplayGain
[2]: http://en.wikipedia.org/wiki/Sansa_Fuze

