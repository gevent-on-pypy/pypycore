from __future__ import absolute_import
import sys, os, traceback, signal as signalmodule

__all__ = ['get_version',
           'get_header_version',
           'supported_backends',
           'recommended_backends',
           'embeddable_backends',
           'time',
           'loop']

def st_nlink_type():
    if sys.platform == "darwin":
        return "short"
    return "long long"


from cffi import FFI
ffi = FFI()
ffi.cdef("""

#define EV_MINPRI ...
#define EV_MAXPRI ...

#define EV_VERSION_MAJOR ...
#define EV_VERSION_MINOR ...


#define EV_UNDEF ...
#define EV_NONE ...
#define EV_READ ...
#define EV_WRITE ...
#define EV__IOFDSET ...
#define EV_TIMER ...
#define EV_PERIODIC ...
#define EV_SIGNAL ...
#define EV_CHILD ...
#define EV_STAT ...
#define EV_IDLE ...
#define EV_PREPARE ...
#define EV_CHECK ...
#define EV_EMBED ...
#define EV_FORK ...
#define EV_CLEANUP ...
#define EV_ASYNC ...
#define EV_CUSTOM ...
#define EV_ERROR ...

#define EVFLAG_AUTO ...
#define EVFLAG_NOENV ...
#define EVFLAG_FORKCHECK ...
#define EVFLAG_NOINOTIFY ...
#define EVFLAG_SIGNALFD ...
#define EVFLAG_NOSIGMASK ...

#define EVBACKEND_SELECT ...
#define EVBACKEND_POLL ...
#define EVBACKEND_EPOLL ...
#define EVBACKEND_KQUEUE ...
#define EVBACKEND_DEVPOLL ...
#define EVBACKEND_PORT ...
/* #define EVBACKEND_IOCP ... */

#define EVBACKEND_ALL ...
#define EVBACKEND_MASK ...

#define EVRUN_NOWAIT ...
#define EVRUN_ONCE ...

#define EVBREAK_CANCEL ...
#define EVBREAK_ONE ...
#define EVBREAK_ALL ...

struct ev_loop {    
    int backend_fd;
    ...;
};

struct ev_io {
    int fd;
    int events;
    ...;
};

struct ev_timer {
    double at;
    ...;
};

struct ev_signal {...;};

struct ev_idle  {...;};


struct ev_prepare {...;};

struct ev_fork  {...;};


struct ev_async  {...;};

struct ev_child {
    int pid;
    int rpid;
    int rstatus;
    ...;
};

struct stat {
    """ + st_nlink_type() + """ st_nlink;
    ...;
};

struct ev_stat {
    struct stat attr;
    struct stat prev;
    double interval;
    ...;
};



typedef double ev_tstamp;



int ev_version_major();
int ev_version_minor();

unsigned int ev_supported_backends (void);
unsigned int ev_recommended_backends (void);
unsigned int ev_embeddable_backends (void);

ev_tstamp ev_time (void);
void ev_set_syserr_cb(void *);

int ev_priority(void*);
void ev_set_priority(void*, int);

int ev_is_pending(void*);
int ev_is_active(void*);
void ev_io_init(struct ev_io*, void* callback, int fd, int events);
void ev_io_start(struct ev_loop*, struct ev_io*);
void ev_io_stop(struct ev_loop*, struct ev_io*);
void ev_feed_event(struct ev_loop*, void*, int);

void ev_timer_init(struct ev_timer*, void (*callback)(struct ev_loop *_loop, struct ev_timer *w, int revents), double, double);
void ev_timer_start(struct ev_loop*, struct ev_timer*);
void ev_timer_stop(struct ev_loop*, struct ev_timer*);
void ev_timer_again(struct ev_loop*, struct ev_timer*);

void ev_signal_init(struct ev_signal*, void* callback, int);
void ev_signal_start(struct ev_loop*, struct ev_signal*);
void ev_signal_stop(struct ev_loop*, struct ev_signal*);

void ev_idle_init(struct ev_idle*, void* callback);
void ev_idle_start(struct ev_loop*, struct ev_idle*);
void ev_idle_stop(struct ev_loop*, struct ev_idle*);

void ev_prepare_init(struct ev_prepare*, void* callback);
void ev_prepare_start(struct ev_loop*, struct ev_prepare*);
void ev_prepare_stop(struct ev_loop*, struct ev_prepare*);

void ev_fork_init(struct ev_fork*, void* callback);
void ev_fork_start(struct ev_loop*, struct ev_fork*);
void ev_fork_stop(struct ev_loop*, struct ev_fork*);

void ev_async_init(struct ev_async*, void* callback);
void ev_async_start(struct ev_loop*, struct ev_async*);
void ev_async_stop(struct ev_loop*, struct ev_async*);
void ev_async_send(struct ev_loop*, struct ev_async*);
int ev_async_pending(struct ev_async*);

void ev_child_init(struct ev_child*, void* callback, int, int);
void ev_child_start(struct ev_loop*, struct ev_child*);
void ev_child_stop(struct ev_loop*, struct ev_child*);

void ev_stat_init(struct ev_stat*, void* callback, char*, double);
void ev_stat_start(struct ev_loop*, struct ev_stat*);
void ev_stat_stop(struct ev_loop*, struct ev_stat*);

struct ev_loop *ev_default_loop (unsigned int flags);
struct ev_loop* ev_loop_new(unsigned int flags);
void ev_loop_destroy(struct ev_loop*);
void ev_loop_fork(struct ev_loop*);
int ev_is_default_loop (struct ev_loop *);
unsigned int ev_iteration(struct ev_loop*);
unsigned int ev_depth(struct ev_loop*);
unsigned int ev_backend(struct ev_loop*);
void ev_verify(struct ev_loop*);
void ev_run(struct ev_loop*, int flags);


ev_tstamp ev_now (struct ev_loop *);
void ev_now_update (struct ev_loop *); /* update event loop time */

void ev_ref(struct ev_loop*);
void ev_unref(struct ev_loop*);
void ev_break(struct ev_loop*, int);
unsigned int ev_pending_count(struct ev_loop*);

struct ev_loop* gevent_ev_default_loop(unsigned int flags);
void gevent_install_sigchld_handler();

void (*gevent_noop)(struct ev_loop *_loop, struct ev_timer *w, int revents);
void ev_sleep (ev_tstamp delay); /* sleep for a while */
""")


include_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'gevent')
libev = C = ffi.verify("""   // passed to the real C compiler
#include <ev.h>
#include "libev.h"

// Taken from 'libev.pxd'
struct ev_loop{
    int activecnt;
    int sig_pending;
    int backend_fd;
    int sigfd;
    unsigned int origflags;
};

static void
_gevent_noop(struct ev_loop *_loop, struct ev_timer *w, int revents) { }

void (*gevent_noop)(struct ev_loop *, struct ev_timer *, int) = &_gevent_noop;
""", include_dirs=[include_dir], libraries=["ev"])
del include_dir

libev.vfd_open = libev.vfd_get = lambda fd: fd
libev.vfd_free = lambda fd: None


READWRITE = libev.EV_READ | libev.EV_WRITE

MINPRI = libev.EV_MINPRI
MAXPRI = libev.EV_MAXPRI

BACKEND_PORT = libev.EVBACKEND_PORT
BACKEND_KQUEUE = libev.EVBACKEND_KQUEUE
BACKEND_EPOLL = libev.EVBACKEND_EPOLL
BACKEND_POLL = libev.EVBACKEND_POLL
BACKEND_SELECT = libev.EVBACKEND_SELECT
FORKCHECK = libev.EVFLAG_FORKCHECK
NOINOTIFY = libev.EVFLAG_NOINOTIFY
SIGNALFD = libev.EVFLAG_SIGNALFD
NOSIGMASK = libev.EVFLAG_NOSIGMASK


class _EVENTSType(object):
    def __repr__(self):
        return 'gevent.core.EVENTS'

EVENTS = GEVENT_CORE_EVENTS = _EVENTSType()


def get_version():
    return 'libev-%d.%02d' % (C.ev_version_major(), C.ev_version_minor())


def get_header_version():
    return 'libev-%d.%02d' % (C.EV_VERSION_MAJOR, C.EV_VERSION_MINOR)

_flags = [(C.EVBACKEND_PORT, 'port'),
          (C.EVBACKEND_KQUEUE, 'kqueue'),
          (C.EVBACKEND_EPOLL, 'epoll'),
          (C.EVBACKEND_POLL, 'poll'),
          (C.EVBACKEND_SELECT, 'select'),
          (C.EVFLAG_NOENV, 'noenv'),
          (C.EVFLAG_FORKCHECK, 'forkcheck'),
          (C.EVFLAG_SIGNALFD, 'signalfd'),
          (C.EVFLAG_NOSIGMASK, 'nosigmask')]

_flags_str2int = dict((string, flag) for (flag, string) in _flags)

_events = [(libev.EV_READ,     'READ'),
           (libev.EV_WRITE,    'WRITE'),
           (libev.EV__IOFDSET, '_IOFDSET'),
           (libev.EV_PERIODIC, 'PERIODIC'),
           (libev.EV_SIGNAL,   'SIGNAL'),
           (libev.EV_CHILD,    'CHILD'),
           (libev.EV_STAT,     'STAT'),
           (libev.EV_IDLE,     'IDLE'),
           (libev.EV_PREPARE,  'PREPARE'),
           (libev.EV_CHECK,    'CHECK'),
           (libev.EV_EMBED,    'EMBED'),
           (libev.EV_FORK,     'FORK'),
           (libev.EV_CLEANUP,  'CLEANUP'),
           (libev.EV_ASYNC,    'ASYNC'),
           (libev.EV_CUSTOM,   'CUSTOM'),
           (libev.EV_ERROR,    'ERROR')]


def _flags_to_list(flags):
    result = []
    for code, value in _flags:
        if flags & code:
            result.append(value)
        flags &= ~code
        if not flags:
            break
    if flags:
        result.append(flags)
    return result

if sys.version_info[0] >= 3:
    basestring = (bytes, str)
else:
    from __builtin__ import basestring


def _flags_to_int(flags):
    # Note, that order does not matter, libev has its own predefined order
    if not flags:
        return 0
    if isinstance(flags, (int, long)):
        return flags
    result = 0
    try:
        if isinstance(flags, basestring):
            flags = flags.split(',')
        for value in flags:
            value = value.strip().lower()
            if value:
                result |= _flags_str2int[value]
    except KeyError, ex:
        raise ValueError('Invalid backend or flag: %s\nPossible values: %s' % (ex, ', '.join(sorted(_flags_str2int.keys()))))
    return result


def _str_hex(flag):
    if isinstance(flag, (int, long)):
        return hex(flag)
    return str(flag)


def _check_flags(flags):
    as_list = []
    flags &= libev.EVBACKEND_MASK
    if not flags:
        return
    if not (flags & libev.EVBACKEND_ALL):
        raise ValueError('Invalid value for backend: 0x%x' % flags)
    if not (flags & libev.ev_supported_backends()):
        as_list = [_str_hex(x) for x in _flags_to_list(flags)]
        raise ValueError('Unsupported backend: %s' % '|'.join(as_list))


def _events_to_str(events):
    result = []
    for (flag, string) in _events:
        c_flag = flag
        if events & c_flag:
            result.append(string)
            events = events & (~c_flag)
        if not events:
            break
    if events:
        result.append(hex(events))
    return '|'.join(result)


def supported_backends():
    return _flags_to_list(libev.ev_supported_backends())


def recommended_backends():
    return _flags_to_list(libev.ev_recommended_backends())


def embeddable_backends():
    return _flags_to_list(libev.ev_embeddable_backends())


def time():
    return C.ev_time()

_default_loop_destroyed = False


def before_block(evloop, _, revents):
    pass  # XXX: how do I check for signals from pure python??


class loop(object):
    error_handler = None
    def _prepare_callback(self, evloop, _, revents):
        self._run_callbacks()

    def _run_callbacks(self):
        count = 1000
        libev.ev_timer_stop(self._ptr, self._timer0)
        while self._callbacks and count > 0:
            callbacks = self._callbacks
            self._callbacks = []
            for cb in callbacks:
                self.unref()
                callback = cb.callback
                args = cb.args
                if callback is None or args is None:
                    continue

                cb.callback = None

                try:
                    callback(*args)
                except:
                    self.handle_error(cb, *sys.exc_info())
                cb.args = None

                # cb.callback(*(cb.args if cb.args is not None else ()))
                # gevent_call(self, cb)
                count -= 1
        if self._callbacks:
            libev.ev_timer_start(self._ptr, self._timer0)

    def __init__(self, flags=None, default=None, ptr=0):
        sys.stderr.write("*** using ev loop\n")
        self._callbacks = []
        self._signal_checker = ffi.new("struct ev_prepare *")
        self._signal_checker_cb = ffi.callback("void(*)(struct ev_loop *, struct evprepare *, int)", before_block)
        libev.ev_prepare_init(self._signal_checker, self._signal_checker_cb)

        self._prepare = ffi.new("struct ev_prepare *")
        self._prepare_cb = ffi.callback("void(*)(struct ev_loop *, struct evprepare *, int)", self._prepare_callback)
        libev.ev_prepare_init(self._prepare, self._prepare_cb)

# #ifdef _WIN32
#         libev.ev_timer_init(&self._periodic_signal_checker, <void*>gevent_periodic_signal_check, 0.3, 0.3)
# #endif
        self._timer0 = ffi.new("struct ev_timer *")
        libev.ev_timer_init(self._timer0, libev.gevent_noop, 0.0, 0.0)

        if ptr:
            assert ffi.typeof(ptr) is ffi.typeof("struct ev_loop *")
            self._ptr = ptr
        else:
            c_flags = _flags_to_int(flags)
            _check_flags(c_flags)
            c_flags |= libev.EVFLAG_NOENV
            if default is None:
                default = True
                if _default_loop_destroyed:
                    default = False
            if default:
                self._ptr = libev.gevent_ev_default_loop(c_flags)
                if not self._ptr:
                    raise SystemError("ev_default_loop(%s) failed" % (c_flags, ))

                # if sys.platform == "win32":
                #     libev.ev_timer_start(self._ptr, &self._periodic_signal_checker)
                #     self.unref()

            else:
                self._ptr = libev.ev_loop_new(c_flags)
                if not self._ptr:
                    raise SystemError("ev_loop_new(%s) failed" % (c_flags, ))
            if default or globals()["__SYSERR_CALLBACK"] is None:
                set_syserr_cb(self._handle_syserr)
            libev.ev_prepare_start(self._ptr, self._prepare)
            self.unref()

    def _stop_signal_checker(self):
        if libev.ev_is_active(self._signal_checker):
            self.ref()
            libev.ev_prepare_stop(self._ptr, self._signal_checker)
# #ifdef _WIN32
#         if libev.ev_is_active(&self._periodic_signal_checker):
#             libev.ev_ref(self._ptr)
#             libev.ev_timer_stop(self._ptr, &self._periodic_signal_checker)
# #endif

    def destroy(self):
        global _default_loop_destroyed
        if self._ptr:
            self._stop_signal_checker()
            if globals()["__SYSERR_CALLBACK"] == self._handle_syserr:
                set_syserr_cb(None)
            if libev.ev_is_default_loop(self._ptr):
                _default_loop_destroyed = True
            libev.ev_loop_destroy(self._ptr)
            self._ptr = ffi.NULL

    @property
    def ptr(self):
        return self._ptr

    @property
    def WatcherType(self):
        return watcher

    @property
    def MAXPRI(self):
        return libev.EV_MAXPRI

    @property
    def MINPRI(self):
        return libev.EV_MINPRI

    def _handle_syserr(self, message, errno):
        self.handle_error(None, SystemError, SystemError(message + ': ' + os.strerror(errno)), None)

    def handle_error(self, context, type, value, tb):
        handle_error = None
        error_handler = self.error_handler
        if error_handler is not None:
            # we do want to do getattr every time so that setting Hub.handle_error property just works
            handle_error = getattr(error_handler, 'handle_error', error_handler)
            handle_error(context, type, value, tb)
        else:
            self._default_handle_error(context, type, value, tb)

    def _default_handle_error(self, context, type, value, tb):
        # note: Hub sets its own error handler so this is not used by gevent
        # this is here to make core.loop usable without the rest of gevent
        traceback.print_exception(type, value, tb)
        libev.ev_break(self._ptr, libev.EVBREAK_ONE)

    def run(self, nowait=False, once=False):
        flags = 0
        if nowait:
            flags |= libev.EVRUN_NOWAIT
        if once:
            flags |= libev.EVRUN_ONCE

        libev.ev_run(self._ptr, flags)

    def reinit(self):
        libev.ev_loop_fork(self._ptr)

    def ref(self):
        libev.ev_ref(self._ptr)

    def unref(self):
        libev.ev_unref(self._ptr)

    def break_(self, how=libev.EVBREAK_ONE):
        libev.ev_break(self._ptr, how)

    def verify(self):
        libev.ev_verify(self._ptr)

    def now(self):
        return libev.ev_now(self._ptr)

    def update(self):
        libev.ev_now_update(self._ptr)

    def XXX__repr__(self):
        return '<%s at 0x%x %s>' % (self.__class__.__name__, id(self), self._format())

    @property
    def default(self):
        return True if libev.ev_is_default_loop(self._ptr) else False

    @property
    def iteration(self):
        return libev.ev_iteration(self._ptr)

    @property
    def depth(self):
        return libev.ev_depth(self._ptr)

    @property
    def backend_int(self):
        return libev.ev_backend(self._ptr)

    @property
    def backend(self):
        backend = libev.ev_backend(self._ptr)
        for key, value in _flags:
            if key == backend:
                return value
        return backend

    @property
    def pendingcnt(self):
        return libev.ev_pending_count(self._ptr)

    def io(self, fd, events, ref=True, priority=None):
        return io(self, fd, events, ref, priority)

    def timer(self, after, repeat=0.0, ref=True, priority=None):
        return timer(self, after, repeat, ref, priority)

    def signal(self, signum, ref=True, priority=None):
        return signal(self, signum, ref, priority)

    def idle(self, ref=True, priority=None):
        return idle(self, ref, priority)

    def prepare(self, ref=True, priority=None):
        return prepare(self, ref, priority)

    def fork(self, ref=True, priority=None):
        return fork(self, ref, priority)

    def async(self, ref=True, priority=None):
        return async(self, ref, priority)

    if sys.platform != "win32":
        def child(self, pid, trace=0, ref=True):
            return child(self, pid, trace, ref)

        def install_sigchld(self):
            libev.gevent_install_sigchld_handler()

# #endif

#     def stat(self, bytes path, float interval=0.0, ref=True, priority=None):
#         return stat(self, path, interval, ref, priority)

    def callback(self, priority=None):
        return callback(self, priority)

    def run_callback(self, func, *args):
        cb = callback(func, args)
        self._callbacks.append(cb)
        self.ref()
        return cb

    def _format(self):
        msg = self.backend
        if self.default:
            msg += ' default'
        msg += ' pending=%s' % self.pendingcnt
# #ifdef LIBEV_EMBED
#         msg += self._format_details()
# #endif
        return msg

    def fileno(self):
        fd = self._ptr.backend_fd
        if fd >= 0:
            return fd

#     LOOP_PROPERTY(activecnt)

# #if EV_USE_SIGNALFD
#     LOOP_PROPERTY(sigfd)
# #endif

#     property origflags:

#         def __get__(self):
#             return _flags_to_list(self._ptr.origflags)

#     property origflags_int:

#         def __get__(self):
#             return self._ptr.origflags

# #endif

_refcount = {}

class watcher(object):
    libev_start_this_watcher = None
    libev_stop_this_watcher = None
    _callback = None
    loop = None
    args = None
    _flags = 0

    def __init__(self, _loop, ref=True, priority=None):
        assert isinstance(_loop, loop)
        assert self.libev_stop_this_watcher is not None
        self.loop = _loop
        if ref:
            self._flags = 0
        else:
            self._flags = 4
        if priority is not None:
            libev.ev_set_priority(self._watcher, priority)

    def _run_callback(self, loop, c_watcher, revents):
        try:
            self.callback(*self.args)
        except:
            try:
                self.loop.handle_error(self, *sys.exc_info())
            finally:
                if revents & (libev.EV_READ|libev.EV_WRITE):
                    # /* io watcher: not stopping it may cause the failing callback to be called repeatedly */
                    try:
                        self.stop()
                    except:
                        self.loop.handle_error(self, *sys.exc_info())
                    return

        # callbacks' self.active differs from ev_is_active(...) at
        # this point. don't use it!
        if not libev.ev_is_active(c_watcher):
            self.stop()

    def _libev_unref(self):
        if self._flags & 6 == 4:
            self.loop.unref()
            self._flags |= 2

    def _python_incref(self):
        if not self._flags & 1:
            try:
                _refcount[self] += 1
            except KeyError:
                _refcount[self] = 1
            # Py_INCREF(<PyObjectPtr>self)
            self._flags |= 1

    def _python_decref(self):
        try:
            if _refcount[self] <= 1:
                del _refcount[self]
            else:
                _refcount[self] -= 1
        except KeyError:
            pass


    def _get_ref(self):
        return False if self._flags & 4 else True

    def _set_ref(self, value):
        if value:
            if not self._flags & 4:
                return  # ref is already True
            if self._flags & 2:  # ev_unref was called, undo
                self.loop.ref()
            self._flags &= ~6  # do not want unref, no outstanding unref
        else:
            if self._flags & 4:
                return  # ref is already False
            self._flags |= 4
            if not self._flags & 2 and libev.ev_is_active(self._watcher):
                self.loop.unref()
                self._flags |= 2

    ref = property(_get_ref, _set_ref)

    def _get_callback(self):
        return self._callback

    def _set_callback(self, callback):
        assert callable(callback)
        self._callback = callback
    callback = property(_get_callback, _set_callback)

    def start(self, callback, *args):
        self.callback = callback
        self.args = args
        self._libev_unref()
        self.libev_start_this_watcher(self.loop._ptr, self._watcher)
        self._python_incref()

    def stop(self):
        if self._flags & 2:
            self.loop.ref()
            self._flags &= ~2
        self.libev_stop_this_watcher(self.loop._ptr, self._watcher)
        self._callback = None
        self.args = None
        if self._flags & 1:
            self._python_decref()
            # Py_DECREF(<PyObjectPtr>self)
            self._flags &= ~1

    def _get_priority(self):
        return libev.ev_priority(self._watcher)

    def _set_priority(self, priority):
        if libev.ev_is_active(self._watcher):
            raise AttributeError("Cannot set priority of an active watcher")
        libev.ev_set_priority(self._watcher, priority)

    priority = property(_get_priority, _set_priority)

    def feed(self, revents, callback, *args):
        self.callback = callback
        self.args = args
        if self._flags & 6 == 4:
            self.loop.unref()
            self._flags |= 2
        libev.ev_feed_event(self.loop._ptr, self._watcher, revents)
        if not self._flags & 1:
            # Py_INCREF(<PyObjectPtr>self)
            self._flags |= 1

    @property
    def active(self):
        return True if libev.ev_is_active(self._watcher) else False

    @property
    def pending(self):
        return True if libev.ev_is_pending(self._watcher) else False


class io(watcher):
    libev_start_this_watcher = libev.ev_io_start
    libev_stop_this_watcher = libev.ev_io_stop

    def __init__(self, loop, fd, events, ref=True, priority=None):
        if fd < 0:
            raise ValueError('fd must be non-negative: %r' % fd)
        if events & ~(libev.EV__IOFDSET | libev.EV_READ | libev.EV_WRITE):
            raise ValueError('illegal event mask: %r' % events)

        self._watcher = ffi.new("struct ev_io *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_io *, int)", self._run_callback)

        libev.ev_io_init(self._watcher, self._cb, fd, events)
        watcher.__init__(self, loop, ref=ref, priority=priority)

    def _get_fd(self):
        return libev.vfd_get(self._watcher.fd)

    def _set_fd(self, fd):
        if libev.ev_is_active(self._watcher):
            raise AttributeError("'io' watcher attribute 'fd' is read-only while watcher is active")
        vfd = libev.vfd_open(fd)
        libev.vfd_free(self._watcher.fd)
        libev.ev_io_init(self._watcher, self._cb, vfd, self._watcher.events)

    fd = property(_get_fd, _set_fd)

    def _get_events(self):
        return libev.vfd_get(self._watcher.fd)

    def _set_events(self, events):
        if libev.ev_is_active(self._watcher):
            raise AttributeError("'io' watcher attribute 'events' is read-only while watcher is active")
        libev.ev_io_init(self._watcher, self._cb, self._watcher.fd, events)

    events = property(_get_events, _set_events)

    @property
    def events_str(self):
        return _events_to_str(self._watcher.events)

    def _format(self):
        return ' fd=%s events=%s' % (self.fd, self.events_str)


class timer(watcher):
    libev_start_this_watcher = libev.ev_timer_start
    libev_stop_this_watcher = libev.ev_timer_stop

    def __init__(self, loop, after=0.0, repeat=0.0, ref=True, priority=None):
        if repeat < 0.0:
            raise ValueError("repeat must be positive or zero: %r" % repeat)

        self._watcher = ffi.new("struct ev_timer *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_timer *, int)", self._run_callback)

        libev.ev_timer_init(self._watcher, self._cb, after, repeat)
        watcher.__init__(self, loop, ref=ref, priority=priority)

    def start(self, callback, *args, **kw):
        update = kw.get("update", True)
        self.callback = callback
        self.args = args

        self._libev_unref()  # LIBEV_UNREF

        if update:
            libev.ev_now_update(self.loop._ptr)
        libev.ev_timer_start(self.loop._ptr, self._watcher)

        self._python_incref()  # PYTHON_INCREF

    @property
    def at(self):
        return self._watcher.at

    def again(self, callback, *args, **kw):
        update = kw.get("update", True)
        self.callback = callback
        self.args = args
        self._libev_unref()
        if update:
            libev.ev_now_update(self.loop._ptr)
        libev.ev_timer_again(self.loop._ptr, self._watcher)
        self._python_incref()


class signal(watcher):
    libev_start_this_watcher = libev.ev_signal_start
    libev_stop_this_watcher = libev.ev_signal_stop

    def __init__(self, loop, signalnum, ref=True, priority=None):
        if signalnum < 1 or signalnum >= signalmodule.NSIG:
            raise ValueError('illegal signal number: %r' % signalnum)
        # still possible to crash on one of libev's asserts:
        # 1) "libev: ev_signal_start called with illegal signal number"
        #    EV_NSIG might be different from signal.NSIG on some platforms
        # 2) "libev: a signal must not be attached to two different loops"
        #    we probably could check that in LIBEV_EMBED mode, but not in general

        self._watcher = ffi.new("struct ev_signal *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_signal *, int)", self._run_callback)

        libev.ev_signal_init(self._watcher, self._cb, signalnum)
        watcher.__init__(self, loop, ref=ref, priority=priority)


class idle(watcher):
    libev_start_this_watcher = libev.ev_idle_start
    libev_stop_this_watcher = libev.ev_idle_stop

    def __init__(self, loop, ref=True, priority=None):
        self._watcher = ffi.new("struct ev_idle *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_idle *, int)", self._run_callback)
        libev.ev_idle_init(self._watcher, self._cb)
        watcher.__init__(self, loop, ref=ref, priority=priority)


class prepare(watcher):
    libev_start_this_watcher = libev.ev_prepare_start
    libev_stop_this_watcher = libev.ev_prepare_stop

    def __init__(self, loop, ref=True, priority=None):
        self._watcher = ffi.new("struct ev_prepare *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_prepare *, int)", self._run_callback)
        libev.ev_prepare_init(self._watcher, self._cb)
        watcher.__init__(self, loop, ref=ref, priority=priority)


class fork(watcher):
    libev_start_this_watcher = libev.ev_fork_start
    libev_stop_this_watcher = libev.ev_fork_stop

    def __init__(self, loop, ref=True, priority=None):
        self._watcher = ffi.new("struct ev_fork *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_fork *, int)", self._run_callback)
        libev.ev_fork_init(self._watcher, self._cb)
        watcher.__init__(self, loop, ref=ref, priority=priority)


class async(watcher):
    libev_start_this_watcher = libev.ev_async_start
    libev_stop_this_watcher = libev.ev_async_stop

    def __init__(self, loop, ref=True, priority=None):
        self._watcher = ffi.new("struct ev_async *")
        self._cb = ffi.callback("void(*)(struct ev_loop *, struct ev_async *, int)", self._run_callback)
        libev.ev_async_init(self._watcher, self._cb)
        watcher.__init__(self, loop, ref=ref, priority=priority)

    def send(self):
        libev.ev_async_send(self.loop._ptr, self._watcher)

    @property
    def pending(self):
        return True if libev.ev_async_pending(self._watcher) else False

class child(watcher):
    libev_start_this_watcher = libev.ev_child_start
    libev_stop_this_watcher = libev.ev_child_stop

    def __init__(self, loop, pid, trace=0, ref=True):
        if not loop.default:
            raise TypeError('child watchers are only available on the default loop')

        self._watcher = ffi.new("struct ev_child *")
        self._cb = ffi.callback("void(*)(struct ev_loop*, struct ev_child *, int)", self._run_callback)
        loop.install_sigchld()
        libev.ev_child_init(self._watcher, self._cb, pid, trace)
        watcher.__init__(self, loop, ref)

    def _format(self):
        return ' pid=%r rstatus=%r' % (self.pid, self.rstatus)

    @property
    def pid(self):
        return self._watcher.pid

    @property
    def rpid(self, ):
        return self._watcher.rpid

    @rpid.setter
    def rpid(self, value):
        self._watcher.rpid = value

    @property
    def rstatus(self):
        return self._watcher.rstatus

    @rstatus.setter
    def rstatus(self, value):
        self._watcher.rstatus = value

class callback(object):
    def __init__(self, callback, args):
        self.callback = callback
        self.args = args

    def stop(self):
        self.callback = None
        self.args = None

    # Note, that __nonzero__ and pending are different
    # nonzero is used in contexts where we need to know whether to schedule another callback,
    # so it's true if it's pending or currently running
    # 'pending' has the same meaning as libev watchers: it is cleared before entering callback

    def __nonzero__(self):
        # it's nonzero if it's pending or currently executing
        return self.args is not None

    @property
    def pending(self):
        return self.callback is not None

    def _format(self):
        return ''

def _syserr_cb(msg):
    try:
        __SYSERR_CALLBACK(msg, ffi.errno)
    except:
        set_syserr_cb(None)
        print_exc = getattr(traceback, 'print_exc', None)
        if print_exc is not None:
            print_exc()

_syserr_cb._cb = ffi.callback("void(*)(char *msg)", _syserr_cb)

def set_syserr_cb(callback):
    global __SYSERR_CALLBACK
    if callback is None:
        libev.ev_set_syserr_cb(ffi.NULL)
        __SYSERR_CALLBACK = None
    elif callable(callback):
        libev.ev_set_syserr_cb(_syserr_cb._cb)
        __SYSERR_CALLBACK = callback
    else:
        raise TypeError('Expected callable or None, got %r' % (callback, ))

__SYSERR_CALLBACK = None
