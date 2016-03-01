#!/usr/bin/python

from __future__ import print_function

import dbus
import dbus.mainloop.glib
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject


def dbus2py(obj):
    if isinstance(obj, dbus.Array):
        return list(obj)
    if isinstance(obj, dbus.Dictionary):
        return dict(obj)
    if isinstance(obj, dbus.String):
        return str(obj)
    if isinstance(obj, dbus.Boolean):
        return bool(obj)
    if isinstance(obj, dbus.Int16):
        return int(obj)
    if isinstance(obj, dbus.Int32):
        return int(obj)
    if isinstance(obj, dbus.Inti64):
        return int(obj)


def device_changed(iface, changed, invalidated, path=None):
    print('device: ' + path, end='')
    for name, value in changed.items():
        print(" {}: {}".format(name, dbus2py(value)), end='')
    print()


def device_added(path):
    obj = bus.get_object('org.bluez', path)
    props_iface = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
    props_iface.connect_to_signal('PropertiesChanged', device_changed, path_keyword='path')

    props = props_iface.GetAll('org.bluez.Device1')
    print('device: {} {}{}'.format(
        props['Adapter'],
        props['Address'],
        ' ' + props['Name'] if 'Name' in props else ''))

    device = dbus.Interface(obj, 'org.bluez.Device1')


def iface_added(path, objects):
    if 'org.bluez.Adapter1' in objects:
        adapter_added(path)
    if 'org.bluez.Device1' in objects:
        device_added(path)


def adapter_added(path):
    obj = bus.get_object('org.bluez', path)
    props_iface = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
    props = props_iface.GetAll('org.bluez.Adapter1')
    print('adapter: {} {}{}'.format(
        path,
        props['Address'],
        ' ' + props['Name'] if 'Name' in props else ''))

    props_iface.Set('org.bluez.Adapter1', 'Discoverable', dbus.Boolean(True))

    #adapter = dbus.Interface(bus.get_object('org.bluez', path), 'org.bluez.Adapter1')
    #adapter.StartDiscovery()


if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)

    bus = dbus.SystemBus()
    root = bus.get_object('org.bluez', '/')
    objmanager = dbus.Interface(root, 'org.freedesktop.DBus.ObjectManager')
    objects = objmanager.GetManagedObjects()

    objmanager.connect_to_signal('InterfacesAdded', iface_added)

    adapters = []
    for path, interfaces in objects.items():
        if 'org.bluez.Adapter1' in interfaces:
            adapter_added(path)
        if 'org.bluez.Device1' in interfaces:
            device_added(path)

    mainloop = GObject.MainLoop()
    mainloop.run()
