pacer-recap-citations
=====================

 * Create a python virtualenv, activate it
 * pip install -r requirements.txt
 * Create a nodeenv, activate it (yes, they can both be active)
 * Run go.sh

That will give you a data/ directory that contains mirrors of the files listed on pages like [this one for docket cacd.518379](https://ia601205.us.archive.org/9/items/gov.uscourts.cacd.518379/). Alongside the mirrored files will be a grayscale pgm image file for each pdf page and a plain text version of each pgm image.

TODO:
  * Extract legal citations from text files
  * Extract dates from the *.docket.xml files
