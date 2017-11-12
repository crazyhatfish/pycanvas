import ctypes, time, cairo, re

class X11Window:
	def __init__(self, width, height, window_name=""):
		self.width = width
		self.height = height

		self.x11 = ctypes.cdll.LoadLibrary("libX11.so")
		self.x11.XOpenDisplay.restype = ctypes.c_void_p
		self.x11.XDefaultScreenOfDisplay.restype = ctypes.c_void_p
		self.x11.XRootWindowOfScreen.restype = ctypes.c_void_p
		self.x11.XCreateGC.restype = ctypes.c_void_p
		self.x11.XDefaultVisualOfScreen.restype = ctypes.c_void_p
		self.x11.XCreateImage.restype = ctypes.c_void_p
		self.x11.XCreateImage.argtypes = [ctypes.c_void_p, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, 
								ctypes.c_int, ctypes.c_void_p, ctypes.c_int, ctypes.c_int, ctypes.c_int, ctypes.c_int]

		self.display = self.x11.XOpenDisplay(0)
		self.screen = self.x11.XDefaultScreenOfDisplay(self.display)
		self.root_window = self.x11.XRootWindowOfScreen(self.screen)
		self.window = self.x11.XCreateSimpleWindow(self.display, self.root_window, 0, 0, width, height, 1, 0, 0xFFFFFF)
		self.x11.XSetStandardProperties(self.display, self.window, window_name, "HELLO", None, None, 0, None)
		self.gc = self.x11.XCreateGC(self.display, self.window, 0, 0)
		self.vis = self.x11.XDefaultVisualOfScreen(self.screen)
		self.x11.XMapWindow(self.display, self.window)
		self.x11.XFlush(self.display)

		self.surface = cairo.ImageSurface(cairo.Format.RGB24, width, height)
		self.context = cairo.Context(self.surface)

		self.context.set_source_rgb(0, 0, 0)
		self.context.rectangle(0, 0, width, height)
		self.context.fill()
		self.surface.flush()

		addr = ctypes.addressof(ctypes.c_char.from_buffer(self.surface.get_data()))

		ZPixmap = 2
		self.img = self.x11.XCreateImage(self.display, self.vis, 24, ZPixmap, 0,
								addr, self.width, self.height, 8, 0)

		assert self.x11.XDefaultDepth(self.display, 0)

	def flush(self):
		self.surface.flush()
		self.x11.XPutImage(self.display, self.window, self.gc, self.img, 0, 0, 0, 0, self.width, self.height)
		self.x11.XSync(self.display, False)

	def handle_events(self):
		event_buffer = (ctypes.c_char * 100)()
		self.x11.XNextEvent(self.display, ctypes.byref(event_buffer))
		type = ctypes.c_int.from_buffer(event_buffer)
		print type

window = X11Window(400, 400)

for x in range(400):
	for y in range(400):
		context = window.context
		context.set_source_rgb(1.0, 0.0, 1.0)
		context.rectangle(0, 0, 400, 400)
		context.fill()
		context.set_source_rgb(1.0, 1.0, 1.0)
		context.curve_to(0, 0, 330, 110, x, y)
		context.stroke()

		time.sleep(0.01)

		window.flush()
