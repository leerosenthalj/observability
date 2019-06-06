import ephem
import numpy as np
from scipy import ndimage
import pylab as py
import matplotlib.dates as mdates
import pdb

'''Outline:
makeplot
    Put together all of the functions listed below.
drawplot
    Takes dates/times/visibility-map, returns a figure.
observable
    Make map of observability.
numeric
    Test whether input is numeric.
target
    set up target location in proper units.
observatory
    Set up PyEphem 'observer object'. Hardcode a bunch of options.
hms
    Convert between hour/minute/second and decimal degree.
dms
    Convert between degree/minute/second and decimal degree.
'''
Class Observability(object):
    """Class to make observability plot for a given target and observatory.

    Args:
        obs (str): name of hard-coded observatory. 'lick' or 'keck' or 'lapalma'
            or 'mtgraham' or 'mtbigelow' or 'andersonmesa' or 'kpno' or 'ctio'
            or 'cerropachon' or 'palomar' or 'cerroparanal' or 'lasilla' or
            'calaralto' or 'lascampanas'.
        ra  (float): Declination of target, in decimal degrees.
        dec (float): Right Ascension of target, in decimal degrees.
        minEl (float): Minimum visible elevation angle; '30' implies airmass=2.
        twilight (float): Minimum acceptable angular distance of sun below
            horizon, in degrees.
        oversamp (float): Factor by which to oversample observability in time.
        dt (float): Timezone offset from UTC. Positive for east, neg. for west.
        dt (float): Fontsize

    """
    def init(obs, ra, dec, minElev=30, twilight=12, oversamp=16, dt=0, fs=16):
        self.obs = obs
        self.ra = ra
        self.dec = dec
        self.minElev = minElev
        self.twilight = twilight
        self.oversamp=oversamp
        self.dt = dt
        self.fs = fs

    def observable(self, dates, object):
        """Return Boolean map of object visibility at given observatory & time.

        """
        sun = ephem.Sun()

        if not isinstance(dates, np.ndarray):
            dates = np.array(dates)
            if dates.size == 0:
                dates = np.array([dates])

        dateshape = dates.shape
        dates = dates.ravel()
        ndates = dates.size

        alts = np.zeros(ndates, dtype=float)
        sunalts = np.zeros(ndates, dtype=float)

        for i in xrange(ndates):
            obs.date = str(dates[i])
            sun.compute(obs)
            object.compute(obs)
            sunalts[i] = sun.alt
            alts[i] = target.alt

        if self.oversampe != 1:
            alts = ndimage.zoom(alts.reshape(dateshape), oversamp)
            sunalts = ndimage.zoom(sunalts.reshape(dateshape), oversamp)
            dateshape = alts.shape #Reset shape of date array with oversampling.

        #Make visibility boolean map.
        vis = ((-sunalts >= (self.twilight*np.pi/180.)) *
               (alts >= (self.minElev*np.pi/180.))).reshape(dateshape)
               
        return vis

    def drawplot(self, dates, hrs, observability):
        """Generate the observability figure.

        """
        if self.dt==0:
            ylabel='UTC Time'
        else:
            ylabel = 'UTC +{}'.format(self.dt)

        observer = ephem.Observer()
        ddates = []
        for d in dates:
            observer.date = str(d)
            ddates.append(observer.date.datetime())

        fig = py.figure()
        axpos = [.1, .12, .77, .76]
        ax = py.subplot(111, position=axpos)
        py.contourf(ddates, hrs, observability, cmap=py.cm.Greens)
        py.clim(0, 1.5)
        months = mdates.MonthLocator()  # every month
        ax.xaxis.set_major_locator(months)
        hfmt = ddates.DateFormatter('%b ')
        ax.xaxis.set_major_formatter(hfmt)
        yt = np.array([0, 4, 8, 12, 16, 20, 24])

        title = '%s: RA = %s, DEC = %s\nalt > %1.1f, sun < -%1.1f' % \
            (self.obs, str(self.ra), str(self.dec), self.minElev, self.twilight)
        ax.set_title(title, fontsize=self.fs*1.2)
        ax.set_yticks(yt)
        ax.yaxis.set_ticks(range(25), minor=True)
        ax.set_yticklabels(yt % 24 )
        ax.set_ylabel(ylabel, fontsize=self.fs)
        ax.grid(axis='x')

        ax2 = py.twinx()
        ax2.set_position(axpos)
        yt2 = np.arange(-24, 24, 3)
        yt2 = yt2[(yt2>=dt) * (yt2<=(24+dt))]
        ax2.set_ylim(dt, 24+dt)
        ax2.set_yticks(yt2)
        ax2.set_ylabel('Local Time: UTC %+1.1f' % dt, fontsize=fs)
        ax2.grid(axis='y')

        tlabs = yt2 % 12
        tlabs = []
        for yt in yt2:
            if (yt%24)==12:
                lab = 'noon'
            elif (yt%24)==0:
                lab = 'mdnt'
            elif (yt % 24) >= 12:
                lab = '%i pm' % (yt % 12)
            else:
                lab = '%i am' % (yt % 12)
            tlabs.append(lab)
        ax2.set_yticklabels(tlabs)
        ax2.yaxis.set_ticks(range(dt, dt+25), minor=True)

        self.fig = fig

    def makeplot(self):
        """Put everything together and produce an obervability map and plot.

        """
        observatory = self.setup_observatory()
        object = self.setup_object()
        today = observatory.date.datetime()
        if today.month<=5:
            yr_init = today.year
        else:
            yr_init = today.year + 1
        self.dates = yr_init + np.round(np.linspace(0, 1, 366.)*365.)/365.
        ndates = self.dates.size
        hrs = np.linspace(0, 24, 49) #Hardcode spacing of time within each day.
        datetimes = self.dates + hrs.reshape(hrs.size, 1)/(365*24.)

        observability = self.observable(datetimes, object)
        self.drawplot()
