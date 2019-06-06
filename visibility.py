import ephem
import numpy as np
from scipy import ndimage
import pylab as py
import matplotlib.dates as mdates
import pdb

import observability.utils as utils

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
Class Visibility(object):
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

    def setup_observatory(self):
        #If an ephem.Observer object has been passed, use that.
        if isinstance(self.obs, ephem.Observer):
            observer = obs
        #If it is an observatory name, set up the appropriate Observer object.
        else:
            observer = ephem.Observer()
            if obs == 'keck':
                observer.long, observer.lat = '-155:28.7','19:49.7'
                observer.elevation = 4160
            elif obs == 'lick':
                observer.long, observer.lat = '-121:38.2','37:20.6'
                observer.elevation = 1290
            elif obs=='palomar':
                observer.long, observer.lat = '-116:51:50', '33:21:21'
                observer.elevation = 1712
            elif obs == 'flwo':
                observer.long, observer.lat = '-110:52.7', '31:40.8'
                observer.elevation = 2606
            elif obs == 'lapalma':
                observer.long, observer.lat = '-17:53.6','28:45.5'
                observer.elevation = 2396
            elif obs == 'ctio':
                observer.long, observer.lat = '-70:48:54','-30:9.92'
                observer.elevation = 2215
            elif obs == 'dct' or obs == 'happyjack':
                observer.long, observer.lat = '-111:25:20', '34:44:40'
                observer.elevation = 2360
            elif obs == 'andersonmesa':
                observer.long, observer.lat = '-111:32:09', '30:05:49'
                observer.elevation = 2163
            elif obs == 'mtbigelow' or obs == 'catalina':
                observer.long, observer.lat = '-110:44:04.3', '32:24:59.3'
                observer.elevation = 2518
            elif obs == 'mtgraham':
                observer.long, observer.lat = '-109:53:23', '32:42:05'
                observer.elevation = 3221
            elif obs == 'kpno':
                observer.long, observer.lat = '-111:25:48', '31:57:30'
                observer.elevation = 2096
            elif obs == 'cerropachon':
                observer.long, observer.lat = '-70:44:11.7', '-30:14:26.6'
                observer.elevation = 2722
            elif obs == 'lasilla':
                observer.long, observer.lat = '-70:43:53', '-29:15:40'
                observer.elevation = 2400
            elif obs == 'cerroparanal':
                observer.long, observer.lat = '-70:24:15', '-24:37:38'
                observer.elevation = 2635
            elif obs == 'calaralto':
                observer.long, observer.lat = '-02:32:46', '+37:13:25'
                observer.elevation = 2168
            elif obs == 'lascampanas':
                observer.long, observer.lat = '-70:41:33', '-29:00:53'
                observer.elevation = 2380
            elif obs == 'saao':
                observer.long, observer.lat = '-32:22:42', '+20:48:38'
                observer.elevation = 1798
            elif obs == 'sidingspring':
                observer.long, observer.lat = '-31:16:24', '+149:04:16'
                observer.elevation = 1116

        self.observer = observer

    def setup_object(self):


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
