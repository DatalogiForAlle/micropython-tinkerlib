DEVICE_PORT=/dev/tty.usbserial*


deploy: remove
	ampy --port $(DEVICE_PORT) put tinkerlib/

# Remove ignores errors if not existing
# (initial - in the recipe does this)
remove:
	-ampy --port $(DEVICE_PORT) rmdir tinkerlib/ --missing-okay

