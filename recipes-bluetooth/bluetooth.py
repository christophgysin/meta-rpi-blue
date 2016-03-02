#!/usr/bin/python

from __future__ import print_function

import dbus
import dbus.mainloop.glib
try:
    from gi.repository import GObject
except ImportError:
    import gobject as GObject

from twisted.internet import gireactor
gireactor.install()
from twisted.internet import reactor
from twisted.web import server, resource


_ADAPTERS = {}
_DEVICES = {}
_TRUSTED = ['F8:A9:D0:A8:2C:FA']

_template_css = '''\
      body {
          font-family: monospace;
      }
      table {
        border-collapse: collapse;
      }
      table, th, td {
        border: 1px solid #ddd;
      }
      td {
        padding: 5px;
      }'''

_template = '''\
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html>
  <head>
    <meta charset="UTF-8">
    <meta http-equiv="refresh" content="3">
    <title>audio</title>
    <style>
{css}
    </style>
  </head>
  <body>
    <form method="POST">
      <h1>Adapters</h1>
      <table>
        <tr>
          <td>adapter</td>
          <td>address</td>
          <td></td>
        </tr>
{adapters}
      </table>
      <h1>Trusted</h1>
      <table>
        <tr>
          <td>name</td>
          <td>address</td>
          <td>RSSI</td>
          <td></td>
        </tr>
{trusted}
      </table>
      <h1>Devices</h1>
      <table>
        <tr>
          <td>name</td>
          <td>address</td>
          <td>RSSI</td>
          <td></td>
        </tr>
{devices}
      </table>
    </form>
  </body>
</html>'''

_template_adapter = '''\
        <tr>
          <td>{name}</td>
          <td>{address}</td>
          <td>
            <button name="discover" value="{path}" type="submit">discover</button>
          </td>
        </tr>'''

_template_device = '''\
        <tr>
          <td>{name}</td>
          <td>{address}</td>
          <td>{rssi}</td>
          <td>
            <button name="{action}" value="{address}" type="submit">{action}</button>
          </td>
        </tr>'''


class Site(resource.Resource):
    isLeaf = True
    def render_GET(self, request):
        adapters = []
        for path, adapter in _ADAPTERS.items():
            _, name = path.rsplit('/', 1)
            adapter_item = _template_adapter.format(name=name,
                                                    path=path,
                                                    address=adapter['address'])
            adapters.append(adapter_item)

        trusted = []
        devices = []
        for address, device in _DEVICES.items():
            if address in _TRUSTED:
                trusted.append(_template_device.format(address=address,
                                                       name=device['name'],
                                                       rssi=device['RSSI'],
                                                       action='remove'))
            else:
                devices.append(_template_device.format(address=address,
                                                       name=device['name'],
                                                       rssi=device['RSSI'],
                                                       action='trust'))

        response = _template.format(css=_template_css,
                                    adapters='\n'.join(adapters),
                                    trusted='\n'.join(trusted),
                                    devices='\n'.join(devices))
        return response.encode('utf-8')

    def render_POST(self, request):
        if b'trust' in request.args:
            for arg in request.args[b'trust']:
                address = arg.decode('utf-8')
                _TRUSTED.append(address)
        if b'remove' in request.args:
            for arg in request.args[b'remove']:
                address = arg.decode('utf-8')
                _TRUSTED.remove(address)
        if b'discover' in request.args:
            for arg in request.args[b'discover']:
                path = arg.decode('utf-8')
                start_discovery(path)
        return self.render_GET(request)


def init_webserver():
    site = server.Site(Site())
    reactor.listenTCP(8080, site)


def dbus2py(obj):
    if isinstance(obj, dbus.Array):
        return [dbus2py(e) for e in obj]
    if isinstance(obj, dbus.Dictionary):
        return {(k, dbus2py(v)) for k, v in obj.items()}
    if isinstance(obj, dbus.String):
        return str(obj)
    if isinstance(obj, dbus.ObjectPath):
        return str(obj)
    if isinstance(obj, dbus.Boolean):
        return bool(obj)
    if isinstance(obj, dbus.Int16):
        return int(obj)
    if isinstance(obj, dbus.Int32):
        return int(obj)
    if isinstance(obj, dbus.Int64):
        return int(obj)
    return obj


def split_device_path(path):
    adapter, device = path.rsplit('/', 1)
    address = ':'.join(device.split('_')[1:])
    return adapter, address


def device_changed(iface, changed, invalidated, path=None):
    adapter, address = split_device_path(path)
    print('device: ' + address, end='')
    for name, value in changed.items():
        name = dbus2py(name)
        value = dbus2py(value)
        _DEVICES[address][name] = value
        print(" {}: {}".format(name, value), end='')
    print()


def device_added(path):
    obj = bus.get_object('org.bluez', path)
    props_iface = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
    props_iface.connect_to_signal('PropertiesChanged', device_changed, path_keyword='path')

    props = props_iface.GetAll('org.bluez.Device1')

    adapter = dbus2py(props['Adapter'])
    address = dbus2py(props['Address'])
    name = dbus2py(props.get('Name', ''))
    rssi = dbus2py(props.get('RSSI', ''))

    print('device: {} {} {} {}'.format(adapter, address, name, rssi))

    _DEVICES[address] = {'name': name,
                         'adapter': adapter,
                         'RSSI': rssi}

    if address in _TRUSTED:
        device = dbus.Interface(obj, 'org.bluez.Device1')
        props_iface.Set('org.bluez.Device1', 'Trusted', dbus.Boolean(True))


def iface_added(path, objects):
    if 'org.bluez.Adapter1' in objects:
        adapter_added(path)
    if 'org.bluez.Device1' in objects:
        device_added(path)


def adapter_added(path):
    obj = bus.get_object('org.bluez', path)
    props_iface = dbus.Interface(obj, 'org.freedesktop.DBus.Properties')
    props = props_iface.GetAll('org.bluez.Adapter1')

    address = dbus2py(props['Address'])
    name = dbus2py(props.get('Name', ''))

    print('adapter: {} {} {}'.format(path, address, name))
    _ADAPTERS[path] = {'name': name, 'address': address}

    props_iface.Set('org.bluez.Adapter1', 'Discoverable', dbus.Boolean(True))


def start_discovery(path):
    adapter = dbus.Interface(bus.get_object('org.bluez', path), 'org.bluez.Adapter1')
    try:
        adapter.StartDiscovery()
    except dbus.exceptions.DBusException:
        pass


def connect_to_bluez():
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



if __name__ == '__main__':
    dbus.mainloop.glib.DBusGMainLoop(set_as_default=True)
    bus = dbus.SystemBus()

    connect_to_bluez()
    init_webserver()

    mainloop = GObject.MainLoop()
    mainloop.run()
