# gaia-hacks
Playing with Gaia data

Server: `ly-alpha.mit.edu` (login with your `space` account). This server is pretty crappy, only 4 1GHz cores and 1GB memory. I recommend using other servers to do work.

Data stored at `/ly-alpha/data/alexji` (add `/nfs` to start if accessing from another space network computer).
I have also put an anaconda installation there and installed Jo Bovy's `gaia_tools` and `apogee` package (though not tested extensively): https://github.com/jobovy/gaia_tools

If you are only interested in the TGAS catalog (2M stars with astrometry), that is only 662M and you can download it to your own computer: http://cdn.gea.esac.esa.int/Gaia/tgas_source/ (can also use `gaia_tools`)

If you want the full point source catalog (343G), `/ly-alpha/data/alexji/Gaia/Gaia/gaia_source/fits/*`

The unwise (http://unwise.me/) catalog has been downloaded to `/ly-alpha/data/alexji/SDSS/dr10`. This matches WISE photometry to every SDSS photometric object in the `pobj` catalog.
The (much smaller) spectroscopic catalog in unwise is `specmatch-dr10.fits`

There are also catalogs matched to SDSS DR8, WISE, 2MASS, and APASS withhttp://cdsxmatch.u-strasbg.fr/xmatch



There are some important caveats in the Gaia data.
You should definitely read these to see if your science depends on this: http://www.cosmos.esa.int/web/gaia/dr1
